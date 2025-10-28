from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import yaml, os, datetime, traceback, logging, json, re, threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
logging.basicConfig(level=logging.INFO)

app.logger.info("Initialisiere PaddleOCR (de)...")
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang='de',
    text_det_box_thresh=0.3,      # empfindlicher für kleine Boxen
    text_det_db_thresh=0.2,       # zusätzliche Schwelle
    text_det_unclip_ratio=2.0,    # größere Boxen
    show_log=True
)
app.logger.info("PaddleOCR bereit.")

RESULT_JSON = "/share/ocr/results.json"
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


def process_ocr(image_path, image_name):
    try:
        result = ocr.predict(image_path)
        for idx, res in enumerate(result):
            base_name = os.path.splitext(image_name)[0]
            json_out = os.path.join(MEDIA_PATH, f"{base_name}_res")
            img_out = os.path.join(MEDIA_PATH, f"{base_name}_res")

            if hasattr(res, "save_to_json"):
                res.save_to_json(json_out)
            elif isinstance(res, dict):
                with open(json_out, "w", encoding="utf-8") as f:
                    json.dump(res, f, ensure_ascii=False, indent=2)
            if hasattr(res, "save_to_img"):
                res.save_to_img(img_out)

        texts = []
        for res in result:
            if isinstance(res, dict) and "rec_texts" in res:
                texts.extend([t.strip() for t in res["rec_texts"] if t.strip()])

        with open(os.path.join(DEBUG_DIR, "debug_last_ocr.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(texts))

        parsed = parse_receipt(texts)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
            "file": image_name,
            **parsed
        }

        data = []
        if os.path.exists(RESULT_JSON):
            try:
                with open(RESULT_JSON, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                app.logger.warning(f"results.json konnte nicht gelesen werden: {e}")
                data = []

        data.append(entry)
        with open(RESULT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        app.logger.info(f"OCR abgeschlossen für {image_name}")

    except Exception as e:
        app.logger.error(f"OCR-Fehler ({image_name}): {e}")
        app.logger.debug(traceback.format_exc())


@app.route('/ocr', methods=['POST'])
def run_ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image = request.files['file']
    tmp_path = os.path.join(DEBUG_DIR, image.filename)
    image.save(tmp_path)
    app.logger.info(f"OCR gestartet für Datei: {image.filename}")

    thread = threading.Thread(target=process_ocr, args=(tmp_path, image.filename))
    thread.daemon = True
    thread.start()

    return jsonify({"status": "processing", "file": image.filename})


def parse_receipt(lines):
    lines = [t.strip() for t in lines if t.strip()]
    app.logger.info(f"[DEBUG] parse_receipt(): {len(lines)} Zeilen")

    store = ""
    for i, t in enumerate(lines[:10]):
        for market in KNOWN_SUPERMARKETS:
            if market.lower() in t.lower():
                store = " ".join(lines[i:i + 5])
                break
        if store:
            break

    price_re = re.compile(r"(\d+[.,]\d{2})\s?(?:€|[A-Z]{1,3})?$")
    qty_re = re.compile(
        r"(?:(\d+[.,]?\d*)\s*(?:x|stk|stück|kg)\b)|(?:x\s?(\d+[.,]?\d*))",
        re.IGNORECASE
    )

    skip_words = {"eur", "€", "summe", "visa", "mastercard",
                  "gesamt", "betrag", "posten", "theke"}
    items = []
    last_item = None
    last_name = None

    for t in lines:
        t_clean = t.lower()
        m = price_re.search(t)
        if m:
            price = float(m.group(1).replace(",", "."))
            name_part = t[:m.start()].strip(" .-")
            if any(w in name_part.lower() for w in skip_words):
                continue
            if not name_part and last_name and \
                    not any(w in last_name.lower() for w in skip_words):
                name_part = last_name

            qty = 1.0
            qmatch = qty_re.search(name_part)
            if qmatch:
                q_val = qmatch.group(1) or qmatch.group(2)
                if q_val:
                    try:
                        qty = float(q_val.replace(",", "."))
                    except ValueError:
                        pass
                name_part = qty_re.sub("", name_part).strip(" .-")

            item = {"qty": qty, "name": name_part, "price": price}
            items.append(item)
            last_item = item
            last_name = None
        else:
            if last_item and ("x" in t or "stk" in t or "kg" in t):
                q_val = None
                qmatch = qty_re.search(t)
                if qmatch:
                    q_val = qmatch.group(1) or qmatch.group(2)
                if q_val:
                    try:
                        last_item["qty"] = float(q_val.replace(",", "."))
                    except ValueError:
                        pass
                m2 = price_re.search(t)
                if m2:
                    last_item["price"] = float(m2.group(1).replace(",", "."))
                continue
            last_name = t

    total = None
    for t in lines:
        if any(x in t.lower() for x in ["summe", "gesamt", "total"]):
            m = price_re.search(t)
            if m:
                total = float(m.group(1).replace(",", "."))
                break
    if total is None:
        for t in reversed(lines):
            m = price_re.search(t)
            if m:
                total = float(m.group(1).replace(",", "."))
                break

    items = [it for it in items if not any(
        kw in it["name"].lower() for kw in skip_words)]

    return {"store": store, "total": total, "items": items}


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
        "debug_dir": DEBUG_DIR
    })


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
