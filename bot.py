import requests
import time
import base64
import hmac
import hashlib
import json

# --- KULLANICI AYARLARI (BURAYI KENDİ BİLGİLERİNLE DOLDUR) ---
TOKEN = "8732581183:AAGkyg2vs07HaOgQTwCVHx0zkr5DKePf600"
CHAT_ID = "975223951"
API_KEY = "5a91cad3-42c8-43f6-b5fa-de1ec872c6a9"
SECRET_KEY = "c0w1PL/gp6C2t59JAGZ1XQ9Aq5Yfc"

def send_telegram_message(message, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    if reply_markup: payload["reply_markup"] = reply_markup
    requests.post(url, json=payload)

def btc_turk_trade(pair, order_type, price):
    # order_type: 0 (Alım/Buy), 1 (Satış/Sell)
    url = "https://api.btcturk.com/api/v2/order"
    nonce = str(int(time.time() * 1000))
    message = f"{API_KEY}{nonce}".encode('utf-8')
    decoded_secret = base64.b64decode(SECRET_KEY)
    signature = hmac.new(decoded_secret, message, hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    
    headers = {
        'X-PCK': API_KEY, 'X-Nonce': nonce, 'X-Signature': signature_b64, 'Content-Type': 'application/json'
    }
    
    # 0.001 miktarını test amaçlı sabit tuttum, ihtiyacına göre artırabilirsin
    payload = {
        "pair": pair, 
        "orderType": "buy" if order_type == 0 else "sell", 
        "orderMethod": "market", 
        "quantity": 0.001 
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print("CHAKO AI Otonom Ticaret Motoru Aktif...")
    last_update_id = 0
    
    while True:
        # 1. Piyasayı tara (Burayı senin kendi analiz fonksiyonunla değiştirebilirsin)
        # Örnek sinyal üretimi:
        pair = "BTC_TRY"
        price = 3000000 
        signal_type = "ALIM" # Sinyal mantığına göre değişecek
        order_code = 0 
        
        # 2. Telegram'a butonlu onay mesajı gönder
        msg = f"🔔 *YENİ İŞLEM FIRSATI*\nParite: {pair}\nKarar: {signal_type}\nFiyat: {price}\n\nOnaylıyor musun?"
        keyboard = {"inline_keyboard": [[{"text": f"✅ {signal_type} ONAYLA", "callback_data": f"trade_{pair}_{order_code}"}]]}
        send_telegram_message(msg, reply_markup=keyboard)
        
        # 3. Onay beklerken buton tıklamasını dinle
        start_wait = time.time()
        while time.time() - start_wait < 300: # 5 dakika boyunca dinle
            time.sleep(2)
            updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}").json()
            
            if updates.get("result"):
                for update in updates["result"]:
                    last_update_id = update["update_id"]
                    if "callback_query" in update:
                        data = update["callback_query"]["data"]
                        if "trade" in data:
                            # İşlemi tetikle
                            _, pair_val, code = data.split("_")
                            result = btc_turk_trade(pair_val, int(code), 0)
                            send_telegram_message(f"🚀 *İŞLEM SONUCU:*\n{json.dumps(result, indent=2)}")
                            return # İşlem sonrası döngü başa döner

if __name__ == "__main__":
    main()
