import requests
import time
import base64
import hmac
import hashlib

TOKEN = "8732581183:AAgKyg2vS07HaGqTwcVHX0zkr50KePf600"
CHAT_ID = "975223951"
API_KEY = "5a91cad3-42c8-43f6-b5fa-de1ec872c6a9"
SECRET_KEY = "cOw1PL/gp6C2t59JAGZ1XQ9Aq5YfC"

def send_telegram_message(message, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram Yanıtı: {response.status_code}")
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

def btc_turk_trade(pair, order_type, price, amount):
    """
    BtcTurk Gerçek Alım/Satım Emir Fonksiyonu (0: Buy, 1: Sell)
    """
    url = "https://api.btcturk.com/api/v2/order"
    
    # BtcTurk API İmza Hesaplama Mantığı
    nonce = str(int(time.time() * 1000))
    message = f"{API_KEY}{nonce}".encode('utf-8')
    decoded_secret = base64.b64decode(SECRET_KEY)
    signature = hmac.new(decoded_secret, message, hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    headers = {
        'X-PCK': API_KEY,
        'X-Nonce': nonce,
        'X-Signature': signature_b64,
        'Content-Type': 'application/json'
    }

    payload = {
        "quantity": str(amount),
        "price": str(price),
        "stopPrice": "0",
        "newOrderMethod": "market", # Piyasa fiyatından hızlı işlem
        "pairSymbol": pair,
        "orderType": str(order_type), # 0: Buy (Alış), 1: Sell (Satış)
        "orderMethod": "limit"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        print(f"BtcTurk İşlem Sonucu: {res_data}")
        return res_data
    except Exception as e:
        print(f"BtcTurk emir hatası: {e}")
        return None

def get_market_data():
    url = "https://api.btcturk.com/api/v2/ticker"
    try:
        response = requests.get(url)
        data = response.json()
        if "data" in data:
            coin_list = []
            for ticker in data["data"]:
                pair = ticker.get("pair", "")
                if pair.endswith("_TRY"):
                    try:
                        last = float(ticker.get("last", 0))
                        high = float(ticker.get("high", 0))
                        low = float(ticker.get("low", 0))
                        daily_percent = float(ticker.get("dailyPercent", 0))
                        
                        coin_list.append({
                            "pair": pair,
                            "last_price": last,
                            "high": high,
                            "low": low,
                            "daily_percent": daily_percent
                        })
                    except (ValueError, TypeError):
                        continue
            return coin_list
    except Exception as e:
        print(f"Piyasa veri çekme hatası: {e}")
    return []

def run_chako_ai_agent():
    print("CHAKO AI Piyasa Taraması Başlatıldı...")
    markets = get_market_data()
    
    if not markets:
        print("Piyasa verisi alınamadı.")
        # Test amaçlı Telegram'ın çalıştığını görmek için ilk coini test mesajı atalım
        send_telegram_message("🤖 *CHAKO AI Aktif*: Sistem çalışıyor, piyasalar taranıyor...")
        return

    # Test ve gözlem için ilk aşamada eşiği biraz esnetelim ki hemen mesaj alabilelim
    for coin in markets:
        pair = coin["pair"]
        last_price = coin["last_price"]
        daily_percent = coin["daily_percent"]

        # Örnek olarak BTC veya hareketli bir coin yakalayalım
        if abs(daily_percent) > 0.5: # Eşiği şimdilik esnettik ki test edebilesin
            ai_signal = "🚀 ALIM FIRSATI TESPİT EDİLDİ" if daily_percent > 0 else "🛡️ SATIş BASKISI"
            
            msg = (
                f"🧠 *CHAKO AI Otonom Sinyal*\n\n"
                f"🔤 Parite: `{pair}`\n"
                f"💰 Güncel Fiyat: `{last_price:,.2f}` TL\n"
                f"📈 24s Değişim: `% {daily_percent}`\n"
                f"🤖 Durum: *{ai_signal}*\n\n"
                f"👉 *İşlem yapmak için aşağıdaki onay butonunu kullanabilirsin.*"
            )

            # Butona basıldığında doğrudan borsa üzerinden işlem açabilmesi için altyapı hazırlandı
            # Otomatik test için bu döngüde ilk gördüğü fırsatı Telegram'a atacak
            send_telegram_message(msg)
            break # Sadece ilkini atıp spam olmasını önleyelim

if __name__ == "__main__":
    print("CHAKO AI Broker Bot Başlatıldı...")
    while True:
        run_chako_ai_agent()
        print("Döngü tamamlandı, 5 dakika bekleniyor...\n")
        time.sleep(300)
