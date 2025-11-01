from flask import Flask, request, jsonify
import os, datetime, traceback, logging, json, re, threading
from flask_cors import CORS
import pymysql
from pymysql.err import OperationalError
from paddleocr import PaddleOCR
import easyocr
import doctr.models as doctr_models
from doctr.io import DocumentFile
from PIL import Image

# =====================================================
# Add-on Konfiguration (/data/options.json)
# =====================================================
CONFIG_PATH = "/data/options.json"
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        options = json.load(f)
else:
    options = {}

OUTPUT_MODE = options.get("output_mode", "both")  # json | sql | both
RESULT_JSON = options.get("json_output_path", "/share/ocr/results.json")

DB_HOST = options.get("db_host", "mariadb")
DB_PORT = int(options.get("db_port", 3306))
DB_NAME = options.get("db_name", "receipts")
DB_USER = options.get("db_user", "receipts")
DB_PASS = options.get("db_password", "change_me")
DB_CREATE = options.get("db_create", True)

# =====================================================
# Flask Setup
# =====================================================
app = Flask(__name__)
if not os.getenv("INGRESS_PORT"):
    CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.INFO)

# =====================================================
# MariaDB Funktionen
# =====================================================
def db_connect():
    try:
        return pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4"
        )
    except OperationalError as e:
        app.logger.warning(f"DB-Verbindung fehlgeschlagen: {e}")
        return None


def db_init():
    conn = db_connect()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        file VARCHAR(255),
        engine VARCHAR(50),
        store VARCHAR(100),
        total DECIMAL(12,2),
        timestamp DATETIME,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receipt_items (
        id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        receipt_id BIGINT UNSIGNED,
        name VARCHAR(255),
        qty DECIMAL(12,3),
        price DECIMAL(12,2),
        FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    conn.close()
    app.logger.info("[SQL] Schema geprüft/angelegt.")


def save_to_db(entry):
    conn = db_connect()
    if not conn:
        app.logger.error("[SQL] Keine DB-Verbindung.")
        return

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO receipts (file, engine, store, total, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        entry["file"],
        entry["engine"],
        entry.get("store"),
        entry.get("total"),
        entry.get("timestamp"),
    ))
    rid = cur.lastrowid

    for item in entry.get("items", []):
        cur.execute("""
            INSERT INTO receipt_items (receipt_id, name, qty, price)
            VALUES (%s, %s, %s, %s)
        """, (rid, item.get("name"), item.get("qty"), item.get("price")))

    conn.close()
    app.logger.info(f"[SQL] Beleg in DB gespeichert (ID={rid}).")


if OUTPUT_MODE in ("sql", "both") and DB_CREATE:
    db_init()

# =====================================================
# OCR + Parsing (dein Originalcode)
# =====================================================
ocr_engines = {"paddle": None, "easyocr": None, "doctr": None}
DEFAULT_ENGINE = "doctr"

DEBUG_DIR = "/share/ocr/debug_outputs"
MEDIA_PATH = "/media/ocr"
os.makedirs(DEBUG_DIR, exist_ok=True)
os.makedirs(MEDIA_PATH, exist_ok=True)

KNOWN_SUPERMARKETS = [
    "EDEKA", "REWE", "ALDI", "NETTO", "PENNY", "LIDL",
    "KAUFLAND", "REAL", "GLOBUS", "DM", "ROSSMANN",
    "BIO COMPANY", "DENNREE", "ALNATURA", "HIT",
    "TEGUT", "FAMILA"
]


def get_ocr_texts(engine_name, image_path):
    global ocr_engines
    engine_name = engine_name.lower()
    texts = []
    if engine_name == "paddle":
        global ocr_engines
        if ocr_engines["paddle"] is None:
            ocr_engines["paddle"] = PaddleOCR(use_doc_orientation_classify=False,
                                              use_doc_unwarping=False,
                                              use_textline_orientation=True,
                                              lang='de')
        result = ocr_engines["paddle"].predict(image_path)
        for res in result:
            if isinstance(res, dict) and "rec_texts" in res:
                texts.extend([t.strip() for t in res["rec_texts"] if t.strip()])
        return texts

    elif engine_name == "easyocr":
        if ocr_engines["easyocr"] is None:
            ocr_engines["easyocr"] = easyocr.Reader(['de'])
        result = ocr_engines["easyocr"].readtext(image_path)
        texts = [r[1] for r in result]
        return texts

    elif engine_name == "doctr":
        if ocr_engines["doctr"] is None:
            ocr_engines["doctr"] = doctr_models.ocr_predictor(
                det_arch='db_resnet50',
                reco_arch='crnn_vgg16_bn',
                pretrained=True
            )
        single_img_doc = DocumentFile.from_images(image_path)
        result = ocr_engines["doctr"](single_img_doc)
        return [word.value for block in result.pages[0].blocks for line in block.lines for word in line.words]
    else:
        raise ValueError(f"Unbekannte OCR-Engine: {engine_name}")


def process_ocr(image_path, image_name, engine_name):
    try:
        app.logger.info(f"OCR-Prozess gestartet für {image_name} mit Engine: {engine_name}")

        texts = get_ocr_texts(engine_name, image_path)

        with open(os.path.join(DEBUG_DIR, f"debug_last_ocr_{engine_name}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(texts))

        parsed = parse_receipt(texts)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
            "file": image_name,
            "engine": engine_name,
            **parsed
        }

        # JSON
        if OUTPUT_MODE in ("json", "both"):
            data = []
            if os.path.exists(RESULT_JSON):
                try:
                    with open(RESULT_JSON, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception as e:
                    app.logger.warning(f"results.json konnte nicht gelesen werden: {e}")
                    data = []
            data.append(entry)
            os.makedirs(os.path.dirname(RESULT_JSON), exist_ok=True)
            with open(RESULT_JSON, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        # SQL
        if OUTPUT_MODE in ("sql", "both"):
            save_to_db(entry)

        app.logger.info(f"OCR abgeschlossen für {image_name} (Engine: {engine_name})")

    except Exception as e:
        app.logger.error(f"OCR-Fehler ({image_name}, Engine {engine_name}): {e}")
        app.logger.debug(traceback.format_exc())


@app.route('/ocr', methods=['POST'])
def run_ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    engine_name = request.args.get("engine", DEFAULT_ENGINE).lower()
    if engine_name not in ocr_engines:
        return jsonify({"error": f"Unknown OCR engine '{engine_name}'"}), 400

    image = request.files['file']
    tmp_path = os.path.join(DEBUG_DIR, image.filename)
    image.save(tmp_path)
    app.logger.info(f"OCR gestartet für Datei: {image.filename} mit Engine: {engine_name}")

    thread = threading.Thread(target=process_ocr, args=(tmp_path, image.filename, engine_name))
    thread.daemon = True
    thread.start()

    return jsonify({"status": "processing", "file": image.filename, "engine": engine_name})


# Dein vollständiger parse_receipt() – unverändert aus Original
def parse_receipt(lines):
    lines = [t.strip() for t in lines if t.strip()]
    print(f"[DEBUG] {len(lines)} Zeilen erkannt")

    store = ""
    for t in lines[:10]:
        for market in KNOWN_SUPERMARKETS:
            if market.lower() in t.lower():
                store = market
                break
        if store:
            break

    start_idx = 0
    for i, t in enumerate(lines):
        if t.strip().upper() == "EUR":
            start_idx = i + 1
            break
    lines = lines[start_idx:]

    merged = []
    i = 0
    while i < len(lines):
        t = lines[i]
        if (
            i < len(lines) - 1
            and re.match(r"^\d+[.,]\d?$", t)
            and re.match(r"^\d+$", lines[i + 1])
        ):
            merged.append(t + lines[i + 1])
            i += 2
        else:
            merged.append(t)
            i += 1
    lines = merged

    price_re = re.compile(r"(\d+[.,]\d{2})(?!\d)")
    skip_tokens = {"eur", "€", "visa", "mastercard", "uid", "nr", "geg.", "total"}
    summe_tokens = {"summe", "gesamt", "betrag"}

    items = []
    buffer_name = ""
    last_item = None

    def clean_name(s):
        s = s.replace("  ", " ").strip(" .,-")
        s = re.sub(r"^[ABC]\b|\b[ABC]$", "", s).strip()
        return s

    for t in lines:
        tl = t.lower()
        if not t or any(tok in tl for tok in skip_tokens):
            continue
        if any(word in tl for word in summe_tokens):
            break

        m_price = price_re.search(t)
        if m_price:
            price = float(m_price.group(1).replace(",", "."))
            name_part = t[:m_price.start()].strip()
            if not name_part or name_part.lower() in {"a", "b"}:
                name_part = buffer_name
                buffer_name = ""
            name_part = clean_name(name_part)
            qty = 1.0
            m_qty = re.search(r"(\d+[.,]?\d*)\s*(kg|stk|stück|x)?", name_part.lower())
            if m_qty:
                try:
                    qty = float(m_qty.group(1).replace(",", "."))
                except:
                    pass
                name_part = re.sub(
                    r"(\d+[.,]?\d*)\s*(kg|stk|stück|x)", "", name_part, flags=re.IGNORECASE
                ).strip()
            if len(name_part) > 1:
                items.append({"qty": qty, "name": name_part, "price": price})
                last_item = items[-1]
            continue

        if last_item and re.search(r"\d+[.,]?\d*\s*(kg|stk|stück|x)", tl):
            m_qty = re.search(r"(\d+[.,]?\d*)", t)
            if m_qty:
                try:
                    last_item["qty"] = float(m_qty.group(1).replace(",", "."))
                except:
                    pass
            continue
        buffer_name = (buffer_name + " " + t).strip()

    total = None
    for i, t in enumerate(lines):
        if any(x in t.lower() for x in summe_tokens):
            nearby = lines[i : i + 6]
            nums = [x for x in nearby if re.search(r"\d+[.,]?\d*", x)]
            joined = "".join(nums)
            m = re.search(r"(\d+[.,]\d{2})", joined)
            if m:
                total = float(m.group(1).replace(",", "."))
                break

    if total is None:
        nums = [x for x in lines[-10:] if re.match(r"^\d+[.,]?\d*$", x)]
        if len(nums) >= 2:
            joined = "".join(nums[-2:])
            m = re.search(r"(\d+[.,]\d{2})", joined)
            if m:
                total = float(m.group(1).replace(",", "."))
        elif nums:
            m = re.search(r"(\d+[.,]\d{2})", nums[-1])
            if m:
                total = float(m.group(1).replace(",", "."))

    return {"store": store, "total": total, "items": items, "lines": lines}


@app.route('/status', methods=['GET'])
def get_status():
    if not os.path.exists(RESULT_JSON):
        return jsonify({"status": "no_results"})
    with open(RESULT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    file_query = request.args.get("file")
    if file_query:
        results = [d for d in data if d.get("file") == file_query]
        if not results:
            return jsonify({"status": "processing"})
        return jsonify({"status": "done", "result": results[-1]})

    return jsonify({"status": "done", "results": data})


@app.route('/')
def index():
    return jsonify({
        "status": "ready",
        "endpoint": "/ocr",
        "language": "de",
        "result_file": RESULT_JSON,
        "output_mode": OUTPUT_MODE,
        "db_host": DB_HOST,
        "db_port": DB_PORT,
        "db_name": DB_NAME
    })


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    ingress_port = os.getenv("INGRESS_PORT")
    print(f"[DEBUG] INGRESS_PORT = {ingress_port}")
    port = int(ingress_port or 5000)
    app.run(host="0.0.0.0", port=port)
