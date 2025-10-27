from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import yaml, os, datetime

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='de')

RESULT_PATH = "/share/ocr/result.yaml"
os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)

@app.route('/ocr', methods=['POST'])
def run_ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    image = request.files['file']
    tmp_path = "/tmp/input.jpg"
    image.save(tmp_path)

    result = ocr.ocr(tmp_path, cls=True)
    text_lines = [line[1][0] for line in result[0]]
    joined_text = "\n".join(text_lines)

    entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'text': joined_text
    }

    # Ergebnis zu YAML-Datei anhängen
    data = []
    if os.path.exists(RESULT_PATH):
        with open(RESULT_PATH, 'r') as f:
            try:
                data = yaml.safe_load(f) or []
            except yaml.YAMLError:
                data = []

    data.append(entry)
    with open(RESULT_PATH, 'w') as f:
        yaml.safe_dump(data, f, allow_unicode=True)

    return jsonify(entry)

@app.route('/')
def index():
    return jsonify({"status": "ready", "endpoint": "/ocr"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
