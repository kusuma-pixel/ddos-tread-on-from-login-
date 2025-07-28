# ddos-tread-on-from-login-
# 🔐 Python Web Flooder with Proxy, Tor, and CAPTCHA Bypass

Project ini adalah program **simulasi pengujian ketahanan web login** menggunakan metode rotasi IP dengan **Tor**, **proxy publik**, dan bypass CAPTCHA via **OCR Tesseract** atau **2Captcha**.

> ⚠️ **Peringatan**: Script ini **hanya untuk tujuan edukasi dan pengujian pada sistem milik sendiri.** Menggunakan script ini pada website tanpa izin dapat melanggar hukum di banyak negara.

---

## 📦 Fitur Utama

- 🚀 Multithread (hingga ratusan koneksi paralel)
- 🌍 Rotasi IP via:
  - Tor (`socks5h://127.0.0.1:9050`)
  - Daftar proxy publik (HTTP/S)
- 🧠 CAPTCHA bypass:
  - OCR lokal (Tesseract)
  - 2Captcha API (jika diaktifkan)
- 🎭 Fake user-agent random untuk setiap request
- 👁️ Bypass referer dengan Google search palsu

---

## 🧰 Instalasi

### 1. Install dependency sistem:
```bash
sudo apt update
sudo apt install tor tesseract-ocr
