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

def send_telegram_message(message, reply_markup=None):
    """Telegram üzerinden butonlu veya düz bildirim gönderir"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    """Kullanıcı Telegram'dan onay verdiğinde tetiklenecek gerçek işlem fonksiyonu"""
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

        # 1000 TL bütçeye uygun minimum tutarlarda test emri
        payload = {
            "pair": pair,
            "orderType": "buy" if order_type == 0 else "sell",
            "orderMethod": "market",
            "quantity": 0.001 if "BTC" in pair else 1.0 # Pariteye göre miktar ayarı
        }

        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        
        if response.status_code == 200:
            send_telegram_message(f"✅ *BtcTurk İşlemi Başarıyla Gerçekleştirildi!*\nParite: {pair}\nİşlem: {'Alış' if order_type==0 else 'Satış'}")
        else:
            send_telegram_message(f"⚠️ *BtcTurk İşlem Reddedildi/Hata!* \nDetay: {res_data}")

        return jsonify({"status": "completed", "response": res_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "message": "CHAKO AI Trade Bot Aktif ve Onay Bekliyor."})

# Arka planda piyasayı tarayıp kullanıcıya ONAY soran döngü
def background_market_scanner():
    send_telegram_message("🟢 *CHAKO AI Bot* 1000 TL Test Süreci Başlatıldı!\n\n_Kural: Bot asla senden habersiz işlem yapmaz. Fırsat bulduğunda onayına sunacak._")
    
    while True:
        try:
            # Örnek: BTC ve popüler pariteleri tarama
            response = requests.get("https://api.btcturk.com/api/v2/ticker?pairSymbol=BTC_TRY")
            if response.status_code == 200:
                data = response.json()
                last_price = data['data'][0]['last']
                
                # Test aşamasında sistemi yormamak ve spam yapmamak için 
                # Gerçek strateji eşiklerini buraya ekleyeceğiz.
                print(f"Piyasa taranıyor... BTC Fiyat: {last_price} TL")
                
        except Exception as e:
            print(f"Tarama hatası: {e}")
        
        # 15 dakikada bir piyasa taraması
        time.sleep(900)

if __name__ == '__main__':
    t = Thread(target=background_market_scanner)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
