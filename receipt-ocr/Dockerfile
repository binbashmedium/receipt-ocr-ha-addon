FROM python:3.12-slim

# ------------------------------------------------------
# System Libraries – nur das, was Doctr + MySQL braucht
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
# Install only what's really needed
# ------------------------------------------------------
RUN pip install --no-cache-dir \
    flask flask-cors pillow pyyaml \
    python-doctr[torch] \
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
