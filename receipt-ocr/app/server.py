from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import yaml, os, datetime, traceback, logging

# --- Flask Setup ---
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# --- OCR Initialisierung ---
# Hinweis: use_angle_cls=True ist korrekt ab PaddleOCR 2.7.x
app.logger.info("Initialisiere PaddleOCR (de)...")
ocr = PaddleOCR(use_angle_cls=True, lang='de')
app.logger.info("PaddleOCR bereit.")

# --- Pfade ---
RESULT_PATH = "/share/ocr/result.yaml"
os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)

# --- OCR Endpoint ---
@app.route('/ocr', methods=['POST'])
def run_ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image = request.files['file']
    tmp_path = "/tmp/input.jpg"
    image.save(tmp_path)

    app.logger.info(f"OCR gestartet für Datei: {image.filename}")

    try:
        result = ocr.ocr(tmp_path)
        if not result or not result[0]:
            app.logger.warning("Keine Textzeilen erkannt.")
            joined_text = ""
        else:
            text_lines = [line[1][0] for line in result[0]]
            joined_text = "\n".join(text_lines)

        entry = {
            'timestamp': datetime.datetime.now().isoformat(timespec='seconds'),
            'file': image.filename,
            'text': joined_text
        }

        # Bestehende YAML laden (wenn vorhanden)
        data = []
        if os.path.exists(RESULT_PATH):
            with open(RESULT_PATH, 'r', encoding='utf-8') as f:
                try:
                    data = yaml.safe_load(f) or []
                except yaml.YAMLError:
                    app.logger.warning("Konnte bestehende YAML nicht lesen – wird überschrieben.")
                    data = []

        # Neues Ergebnis anhängen
        data.append(entry)
        with open(RESULT_PATH, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True)

        app.logger.info(f"OCR erfolgreich abgeschlossen für {image.filename}")
        return jsonify(entry)

    except Exception as e:
        app.logger.error("Fehler bei OCR-Verarbeitung: %s", e)
        app.logger.debug(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# --- Status Endpoint ---
@app.route('/')
def index():
    return jsonify({
        "status": "ready",
        "endpoint": "/ocr",
        "language": "de",
        "result_file": RESULT_PATH
    })


if __name__ == '__main__':
    # Home Assistant-kompatibler Start
    app.run(host='0.0.0.0', port=5000)
