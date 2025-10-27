ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:latest
FROM $BUILD_FROM

# Arbeitsverzeichnis
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apk update && apk upgrade
RUN apk add python3 py3-pip
RUN apk add git

# LibreTranslate klonen
RUN git clone --depth 1 https://github.com/LibreTranslate/LibreTranslate.git /app

# Virtuelle Umgebung
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


# Pip aktualisieren
RUN pip install --upgrade pip

RUN echo "Contents of /app:" && ls -al /app

#RUN pip install -r requirements.txt


# Übersetzungen kompilieren
#RUN python scripts/compile_locales.py

# Copy root filesystem
COPY rootfs /
