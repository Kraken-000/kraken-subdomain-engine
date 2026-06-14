Ada sedikit masalah dengan penulisan heredoc dan beberapa bagian yang tidak rapi. Mari kita perbaiki dengan cara yang lebih sederhana.

---

🔧 Langkah 1: Hapus README yang bermasalah

```bash
cd ~/dev/kraken

# Hapus README yang error
rm -f README.md
```

---

📝 Langkah 2: Buat README.md dengan Cara yang Lebih Sederhana

Kita akan buat file menggunakan nano (lebih mudah dan tidak error):

```bash
nano README.md
```

---

📋 Copy dan Paste Isi Berikut ke Nano

Cara copy: Tekan dan tahan teks di bawah, pilih "Copy", atau gunakan keyboard untuk memilih teks.

Isi README.md (copy semua dari baris # 🦑 KRAKEN sampai for the bug bounty community):

```
# 🦑 KRAKEN - Subdomain Discovery Engine

**Professional Bug Bounty Tool • Zero False Positive • Live Verification**

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/Kraken-000/kraken-subdomain-engine)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Termux](https://img.shields.io/badge/Termux-Compatible-orange.svg)](https://termux.com)

---

## Screenshot

```

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║      ██╗  ██╗██████╗  █████╗ ██╗  ██╗███████╗███╗   ██╗                     ║
║      ██║ ██╔╝██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║                     ║
║      █████╔╝ ██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║                     ║
║      ██╔═██╗ ██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║                     ║
║      ██║  ██╗██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║                     ║
║      ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝                     ║
║                                                                              ║
║         KRAKEN - Subdomain Discovery Engine                                 ║
║         Unleash the Beast • 0% False Positive                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

```

---

## Features

| Feature | Description |
|---------|-------------|
| 🎯 Zero False Positive | Every reported subdomain is 100% live and verified |
| 🌐 Live Verification | HTTP/HTTPS check with status code & title extraction |
| 🏆 Priority Scoring | Automated ranking of high-value targets |
| 📊 Rich Output | TXT + JSON reports with full metadata |
| ⚡ Multi-threaded | Fast scanning with configurable workers |
| 🎨 Professional CLI | Beautiful interface like sqlmap |

---

## Installation

### Termux (Android)
```bash
git clone https://github.com/Kraken-000/kraken-subdomain-engine.git
cd kraken-subdomain-engine
python -m pip install requests
python main.py
```

Linux (Ubuntu/Debian)

```bash
git clone https://github.com/Kraken-000/kraken-subdomain-engine.git
cd kraken-subdomain-engine
pip3 install requests
python3 main.py
```

---

Usage

```bash
python main.py
```

Then enter your target domain:

```
[?] Enter target domain: hackerone.com
```

---

Output

File Description
output/domain_live.txt List of live subdomains
output/domain_report.json Complete metadata (status, titles, priorities)

Example Output

```json
[
  {
    "subdomain": "www.hackerone.com",
    "status_code": 200,
    "title": "HackerOne",
    "priority": 70,
    "live": true
  }
]
```

---

Priority Scoring

Score Label Description
70-100 CRITICAL Admin panels, dashboards, internal systems
40-69 HIGH APIs, login portals, config interfaces
0-39 MEDIUM Standard web applications

---

Requirements

· Python 3.8+
· requests library
· Internet connection
· Termux (Android) or Linux

---

Disclaimer

⚠️ This tool is for educational purposes and authorized testing only. Use only on targets you own or have explicit permission to test.

---

Contact

· GitHub: @Kraken-000
· Email: jtralala090@gmail.com

---

License

MIT License

---

Made with 🦑 for the bug bounty community

```

---
