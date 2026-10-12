#!/usr/bin/env bash
set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Crear directorio bin y descargar Shaka Packager para Linux
mkdir -p bin
curl -L https://github.com/shaka-project/shaka-packager/releases/download/v3.2.0/packager-linux-x64 -o bin/packager-linux-x64
chmod +x bin/packager-linux-x64
