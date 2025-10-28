FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Modern pip
RUN python -m pip install -U pip setuptools wheel

# PaddleOCR minimal
RUN pip install paddleocr==2.7.0.3 paddlepaddle==2.6.0 opencv-python-headless pillow pyyaml flask

WORKDIR /app
COPY app /app

EXPOSE 5000
CMD ["python", "server.py"]
