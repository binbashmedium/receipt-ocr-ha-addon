from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import yaml, os, datetime, traceback, logging, json, re
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
logging.basicConfig(level=logging.INFO)

# --- OCR Initialisierung ---
app.logger.info("Initialisiere PaddleOCR (de)...")
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang='de'
)
app.logger.info("PaddleOCR bereit.")

RESULT_JSON = "/share/ocr/results.json"
DEBUG_DIR = "/share/ocr/debug_outputs"
os.makedirs(DEBUG_DIR, exist_ok=True)

# Liste bekannter Supermärkte in Deutschland
KNOWN_SUPERMARKETS = [
    "EDEKA", "REWE", "ALDI", "NETTO", "PENNY", "LIDL",
    "KAUFLAND", "REAL", "GLOBUS", "DM", "ROSSMANN",
    "BIO COMPANY", "DENNREE", "ALNATURA", "HIT",
    "TEGUT", "FAMILA"
]


# ---------------- OCR Verarbeitung ---------------- #
@app.route('/ocr', methods=['POST'])
def run_ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image = request.files['file']
    tmp_path = os.path.join(DEBUG_DIR, image.filename)
    image.save(tmp_path)

    app.logger.info(f"OCR gestartet für Datei: {image.filename}")

    try:
        # --- OCR Prediction ---
        result = ocr.predict(tmp_path)

        # --- Debug speichern ---
        for idx, res in enumerate(result):
            base_name = os.path.splitext(image.filename)[0]
            json_out = os.path.join(DEBUG_DIR, f"{base_name}_res_{idx}.json")
            img_out = os.path.join(DEBUG_DIR, f"{base_name}_res_{idx}.jpg")

            if hasattr(res, "save_to_json"):
                res.save_to_json(json_out)
            elif isinstance(res, dict):
                with open(json_out, "w", encoding="utf-8") as f:
                    json.dump(res, f, ensure_ascii=False, indent=2)
            if hasattr(res, "save_to_img"):
                res.save_to_img(img_out)

        # --- Texte extrahieren ---
        texts = []
        for res in result:
            if isinstance(res, dict) and "rec_texts" in res:
                texts.extend([t.strip() for t in res["rec_texts"] if t.strip()])

        with open(os.path.join(DEBUG_DIR, "debug_last_ocr.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(texts))

        parsed = parse_receipt(texts)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
            "file": image.filename,
            **parsed
        }

        # --- Ergebnisse speichern ---
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

        app.logger.info(f"OCR erfolgreich abgeschlossen für {image.filename}")
        return jsonify(entry)

    except Exception as e:
        app.logger.error("Fehler bei OCR-Verarbeitung: %s", e)
        app.logger.debug(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# ---------------- Parsing ---------------- #
def parse_receipt(lines):
    """Extrahiere Store, Total und Items aus erkannter Textliste."""
    lines = [t.strip() for t in lines if t.strip()]
    app.logger.info(f"[DEBUG] parse_receipt(): {len(lines)} Zeilen")

    # --- Store erkennen ---
    store = ""
    for i, t in enumerate(lines[:10]):
        for market in KNOWN_SUPERMARKETS:
            if market.lower() in t.lower():
                store = " ".join(lines[i:i + 5])
                break
        if store:
            break

    # --- Items extrahieren ---
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

        # Preiszeile?
        m = price_re.search(t)
        if m:
            price = float(m.group(1).replace(",", "."))
            name_part = t[:m.start()].strip(" .-")

            # "EUR" oder Summen ignorieren
            if any(w in name_part.lower() for w in skip_words):
                continue

            # vorherige Zeile als Name verwenden, wenn leer
            if not name_part and last_name and \
                    not any(w in last_name.lower() for w in skip_words):
                name_part = last_name

            qty = 1.0
            # Mengen in derselben Zeile (z. B. „x 2“ oder „1,5 kg“)
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
            # Zeilen mit "x" + Preis (z. B. "2 Stk x 0,90") gehören zum letzten Artikel
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
                # Preis aus dieser Zeile ggf. aktualisieren (z. B. "1,50 €/kg")
                m2 = price_re.search(t)
                if m2:
                    last_item["price"] = float(m2.group(1).replace(",", "."))
                continue

            # sonst ist es evtl. ein Name
            last_name = t

    # --- Total finden ---
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

    # Filter: Summen-/Kartenzahlungen aus items entfernen
    items = [it for it in items if not any(
        kw in it["name"].lower() for kw in skip_words)]

    return {"store": store, "total": total, "items": items}




# ---------------- Status ---------------- #
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
