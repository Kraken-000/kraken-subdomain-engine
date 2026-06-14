#!/bin/bash
# KRAKEN Installer

echo "[+] Installing KRAKEN - Subdomain Discovery Engine"

# Install dependencies
pkg update -y
pkg install python -y
python -m pip install requests

# Setup wordlist
mkdir -p wordlists
cd wordlists
curl -L -o subdomains.txt "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt"

cd ..
mkdir -p output

echo "[✓] Installation complete!"
echo "[✓] Run: python main.py"
