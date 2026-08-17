from flask import Flask, request, jsonify
import time, base64, hmac, hashlib, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# BtcTurk API Ayarları
API_KEY = os.getenv("BTCTURK_PUBLIC_KEY")
SECRET_KEY = os.getenv("BTCTURK_PRIVATE_KEY")

# Bu fonksiyon Lovable'dan gelen istekle tetiklenecek
@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    data = request.json
    pair = data.get("pair", "BTC_TRY")
    order_type = data.get("order_type", 0) # 0: Alış, 1: Satış
    
    # BtcTurk işlem mantığı (İmzalama ve İstek)
    # ... (Buraya daha önce yazdığımız imzalama kodunu ekleyeceğiz) ...
    
    return jsonify({"status": "success", "message": f"{pair} için işlem yapıldı"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
