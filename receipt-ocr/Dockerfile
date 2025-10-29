FROM python:3.12-slim

# System libraries for PaddleOCR + PyMuPDF build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential make gcc g++ swig \
    libgl1 libglib2.0-0 libjpeg-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install -U pip setuptools wheel


RUN pip install paddleocr paddlepaddle \
    opencv-python-headless pillow pyyaml flask flask-cors \
    easyocr doctr[torch] torch torchvision torchaudio \
    transformers keras-ocr
    

WORKDIR /app
COPY app /app

EXPOSE 5000
CMD ["python", "server.py"]
