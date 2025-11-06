FROM python:3.12-slim

# ------------------------------------------------------
# System Libraries – nur das, was Doctr + PyMuPDF + MariaDB braucht
# ------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    libgl1 libglib2.0-0 libjpeg-dev zlib1g-dev \
    
    default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------
# Python setup
# ------------------------------------------------------
RUN python -m pip install -U pip setuptools wheel

# ------------------------------------------------------
# Python dependencies – nur das, was du wirklich brauchst
# ------------------------------------------------------
RUN pip install \
    pillow pyyaml flask flask-cors \
    python-doctr torch torchvision torchaudio tensorflow \
    transformers \
    PyMySQL paho-mqtt

# ------------------------------------------------------
# App setup
# ------------------------------------------------------
WORKDIR /app
COPY app /app

# ------------------------------------------------------
# Start command
# ------------------------------------------------------
CMD ["python", "server.py"]
