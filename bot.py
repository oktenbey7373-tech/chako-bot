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

# BtcTurk API Ayarları
API_KEY = os.getenv("BTCTURK_PUBLIC_KEY")
SECRET_KEY = os.getenv("BTCTURK_PRIVATE_KEY")

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
        return jsonify({"status": "completed", "btcturk_response": response.json(), "status_code": response.status_code})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "message": "CHAKO AI Trade Bot API calisiyor."})

@app.route('/signal', methods=['POST'])
def receive_signal():
    try:
        data = request.json or {}
        symbol = data.get('symbol', 'BTC_TRY')
        action = data.get('action', 'HOLD')
        price = data.get('price', 0)

        print(f"Sinyal alindi -> Sembol: {symbol}, Islem: {action}, Fiyat: {price}")

        return jsonify({
            "status": "success",
            "message": f"Sinyal basariyla alindi: {symbol} - {action}"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Arka planda periyodik calisan test dongusu (Ornek: Her 5 dakikada bir piyasa kontrolu)
def background_market_checker():
    while True:
        try:
            print("Arka planda piyasa verileri kontrol ediliyor...")
            # Burada BtcTurk public fiyat endpoint'inden anlik fiyat cekip strateji uygulayacagiz
            response = requests.get("https://api.btcturk.com/api/v2/ticker?pairSymbol=BTC_TRY")
            if response.status_code == 200:
                data = response.json()
                # Ornek veri okuma
                last_price = data['data'][0]['last']
                print(f"Guncel BTC/TRY Fiyati: {last_price}")
        except Exception as e:
            print(f"Arka plan hata: {e}")
        
        # 5 dakikada bir kontrol et (300 saniye)
        time.sleep(300)

if __name__ == '__main__':
    # Arka plan is parcacigini baslat
    t = Thread(target=background_market_checker)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
