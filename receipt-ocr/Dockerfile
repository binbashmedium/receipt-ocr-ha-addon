# =====================================================
# STAGE 1: Build environment (Pakete & Python-Abhängigkeiten)
# =====================================================
FROM python:3.12-slim AS builder

# System Libraries, die für Doctr + PyMuPDF + Pillow notwendig sind
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    libgl1 libglib2.0-0 libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------
# Python: Pip modernisieren
# -----------------------------------------------------
RUN python -m pip install -U pip setuptools wheel

# -----------------------------------------------------
# Python dependencies – CPU-only Torch & Doctr
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
# STAGE 2: Runtime Image (schlank, kein Build-Overhead)
# =====================================================
FROM python:3.12-slim

# Minimal benötigte Systempakete
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libjpeg62-turbo zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Abhängigkeiten & App aus Builder übernehmen
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

WORKDIR /app

# -----------------------------------------------------
# Optional: Cache & temporäre Dateien löschen (spart Platz)
# -----------------------------------------------------
RUN rm -rf /root/.cache /tmp/*

# -----------------------------------------------------
# Start Command
# -----------------------------------------------------
CMD ["python", "server.py"]
