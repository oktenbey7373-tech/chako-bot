import requests
import time

TOKEN = "8732581183:AAgKyg2vS07HaGqTWcVHX0zkr50KePf600"
CHAT_ID = "975223951"  # Senin Telegram ID'n

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

def check_market():
    url = "https://api.btcturk.com/api/v2/ticker"
    try:
        response = requests.get(url)
        data = response.json()
        if "data" in data:
            tickers = data["data"]
            for ticker in tickers:
                pair = ticker.get("pair")
                if pair == "BTC_TRY":
                    last_price = ticker.get("last")
                    daily_percent = ticker.get("dailyPercent")
                    msg = f"🚨 *CHAKO AI Sinyal Güncellemesi*\n\n🪙 Coin: `{pair}`\n💰 Fiyat: `{last_price:,.2f} TL`\n📈 Değişim: ` %{daily_percent}`"
                    send_telegram_message(msg)
                    print(f"Gönderildi: {pair} - {last_price} TL")
    except Exception as e:
        print(f"API bağlantı hatası: {e}")

if __name__ == "__main__":
    print("CHAKO AI Trade Asistanı ve Telegram Botu Başlatılıyor...")
    while True:
        check_market()
        print("Veriler kontrol edildi, 60 saniye bekleniyor...\n")
        time.sleep(60)
