#!/bin/bash

echo "[+] Installing dependencies..."
pip3 install -r requirements.txt

echo "[+] Making tool executable..."
chmod +x ipinfo.py

echo "[+] Copying tool to /usr/local/bin..."
sudo cp ipinfo.py /usr/local/bin/ipinfo

echo "[✓] Installed successfully. Run the tool using: ipinfo -i 1.1.1.1"
