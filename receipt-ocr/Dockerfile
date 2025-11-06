# =====================================================
# STAGE 1: Build environment (Doctr + Torch CPU)
# =====================================================
FROM python:3.12-slim-bookworm AS builder

# Keine interaktiven apt-Dialoge
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# -----------------------------------------------------
# Systembibliotheken – nur das, was Doctr + Pillow braucht
# -----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    libgl1 libglib2.0-0 libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------
# Python Setup
# -----------------------------------------------------
RUN python -m pip install -U pip setuptools wheel

# -----------------------------------------------------
# Installiere OCR + Flask + SQL + MQTT (CPU only)
# -----------------------------------------------------
RUN pip install --no-cache-dir \
    torch==2.4.0+cpu torchvision==0.19.0+cpu torchaudio==2.4.0+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html \
 && pip install --no-cache-dir \
    python-doctr[torch] \
    pillow pyyaml flask flask-cors \
    PyMySQL paho-mqtt

# App Code kopieren
WORKDIR /app
COPY app /app


# =====================================================
# STAGE 2: Runtime (klein & sauber)
# =====================================================
FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# -----------------------------------------------------
# Minimale Systemlibs, die Doctr & Pillow zur Laufzeit brauchen
# -----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Abhängigkeiten & App übernehmen
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

WORKDIR /app

# -----------------------------------------------------
# Aufräumen (spart nochmal ~200 MB)
# -----------------------------------------------------
RUN rm -rf /root/.cache /tmp/*

# -----------------------------------------------------
# Startbefehl
# -----------------------------------------------------
CMD ["python", "server.py"]
