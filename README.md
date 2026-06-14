# 🦑 KRAKEN - Subdomain Discovery Engine

**Professional Bug Bounty Tool • Zero False Positive • Live Verification**

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/Kraken-000/kraken-subdomain-engine)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Termux](https://img.shields.io/badge/Termux-Compatible-orange.svg)](https://termux.com)

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

Linux

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

Enter target domain:

```
[?] Enter target domain: hackerone.com
```

---

Output

File Description
output/domain_live.txt List of live subdomains
output/domain_report.json Complete metadata

---

Requirements

· Python 3.8+
· requests library
· Internet connection

---

Disclaimer

⚠️ This tool is for educational and authorized testing only.

---

Contact

· GitHub: @Kraken-000
· Email: jtralala090@gmail.com

---

License

MIT License

---

Made with 🦑 for the bug bounty community
