ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM ${BUILD_FROM}

# Labels
LABEL maintainer="yourname@example.com"
LABEL description="PaddleOCR Add-on for Home Assistant"

# Systempakete
RUN apk add --no-cache python3 py3-pip py3-yaml py3-opencv

# Python-Dependencies
RUN pip install --no-cache-dir paddleocr==2.7.0.3 flask==3.0.3 Pillow

# App kopieren
WORKDIR /app
COPY app /app

# Port & Start
EXPOSE 5000
CMD ["python3", "server.py"]
