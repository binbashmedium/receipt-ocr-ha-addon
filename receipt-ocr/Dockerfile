# =====================================================
# STAGE 1: Build environment (Doctr + Torch CPU)
# =====================================================
FROM python:3.12-slim-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# -----------------------------------------------------
# Systembibliotheken – minimal, nur was Doctr braucht
# -----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    libgl1 libglib2.0-0 libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -U pip setuptools wheel

# -----------------------------------------------------
# Installiere PyTorch (CPU), Doctr, Flask etc.
# -----------------------------------------------------
RUN pip install --no-cache-dir \
    torch==2.3.1+cpu torchvision==0.18.1+cpu torchaudio==2.3.1+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html && \
    pip install --no-cache-dir \
    python-doctr[torch] \
    pillow pyyaml flask flask-cors \
    PyMySQL paho-mqtt

WORKDIR /app
COPY app /app


# =====================================================
# STAGE 2: Runtime
# =====================================================
FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# Runtime-Libs (kein Build-Zeug)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libjpeg62-turbo zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Kopiere installierte Python-Pakete + App
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

WORKDIR /app

# Aufräumen
RUN rm -rf /root/.cache /tmp/*

# Start
CMD ["python", "server.py"]
