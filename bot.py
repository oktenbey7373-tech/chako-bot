from flask import Flask, request, jsonify
import time
import base64
import hmac
import hashlib
import requests
import os
from dotenv import load_dotenv

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
        return jsonify({"status": "completed", "btcturk_response": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "message": "CHAKO AI Trade Bot API calisiyor."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
