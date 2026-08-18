import os
import time
import hmac
import hashlib
import base64
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from threading import Thread

load_dotenv()
app = Flask(__name__)

# BtcTurk ve Telegram Ayarları
API_KEY = os.getenv("BTCTURK_PUBLIC_KEY")
SECRET_KEY = os.getenv("BTCTURK_PRIVATE_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """Telegram üzerinden anlık bildirim gönderir"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram token veya chat ID eksik!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    try:
        data = request.json or {}
        pair = data.get("pair", "BTC_TRY")
        order_type = data.get("order_type", 0)  # 0: Alış (Buy), 1: Satış (Sell)

        url = "https://api.btcturk.com/api/v2/order"
        nonce = str(int(time.time() * 1000))

        message = (API_KEY + nonce).encode('utf-8')
        decoded_secret = base64.b64decode(SECRET_KEY)
        signature = hmac.new(decoded_secret, message, hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature).decode('utf-8')

        headers = {
            'X-API-KEY': API_KEY,
            'X-Nonce': nonce,
            'X-Signature': signature_b64,
            'Content-Type': 'application/json'
        }

        payload = {
            "pair": pair,
            "orderType": "buy" if order_type == 0 else "sell",
            "orderMethod": "market",
            "quantity": 0.001
        }

        response = requests.post(url, headers=headers, json=payload)
        
        # İşlem sonucunu Telegram'a bildir
        res_data = response.json()
        if response.status_code == 200:
            send_telegram_message(f"🚨 *BtcTurk İşlem Başarılı!*\nİşlem: {'Alış' if order_type==0 else 'Satış'}\nParite: {pair}")
        else:
            send_telegram_message(f"⚠️ *İşlem Hatası!* \nKod: {response.status_code}\nDetay: {res_data}")

        return jsonify({"status": "completed", "btcturk_response": res_data, "status_code": response.status_code})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "message": "CHAKO AI Trade Bot API calisiyor."})

# Arka planda periyodik çalışan piyasa analiz ve test döngüsü
def background_market_checker():
    # Test başlangıç bildirimi
    send_telegram_message("🟢 *CHAKO AI Bot* 3 Aylık Test Süreci Başlatıldı ve Aktif!")
    
    while True:
        try:
            response = requests.get("https://api.btcturk.com/api/v2/ticker?pairSymbol=BTC_TRY")
            if response.status_code == 200:
                data = response.json()
                last_price = data['data'][0]['last']
                print(f"Güncel BTC/TRY Fiyatı: {last_price}")
                
                # Buraya kendi test strateji koşullarını ekleyebiliriz (Örn: Belirli fiyat altı/üstü alım sinyali)
                
        except Exception as e:
            print(f"Arka plan hata: {e}")
        
        # Her 5 dakikada bir kontrol (300 saniye)
        time.sleep(300)

if __name__ == '__main__':
    t = Thread(target=background_market_checker)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
