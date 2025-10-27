ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM ${BUILD_FROM}

LABEL maintainer="you@example.com"

# Systempakete
RUN apk add --no-cache python3 py3-pip py3-yaml py3-opencv py3-virtualenv

WORKDIR /opt

# Virtuelle Umgebung anlegen
RUN python3 -m venv venv

# Abhängigkeiten in venv installieren (um PEP 668 zu umgehen)
RUN /opt/venv/bin/pip install --no-cache-dir paddleocr==2.7.0.3 flask==3.0.3 Pillow pyyaml

# App kopieren
WORKDIR /app
COPY app /app

# Standard python im venv starten
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000

CMD ["python3", "server.py"]
