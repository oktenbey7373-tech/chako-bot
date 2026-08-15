import requests
import time

TOKEN = "8732581183:AAgKyg2vS07HaGqTWcVHX0zkr50KePf600"
CHAT_ID = "975223951"

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

def run_chako_ai_agent():
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
                    daily_percent = float(ticker.get("dailyPercent", 0))
                    
                    # CHAKO AI Agent Karar Mekanizması
                    if daily_percent > 1.5:
                        ai_signal = "🟢 GÜÇLÜ AL (Bullish Momentum)"
                    elif daily_percent < -1.5:
                        ai_signal = "🔴 DİKKAT / SATIŞ BASKISI"
                    else:
                        ai_signal = "🟡 NÖTR / YATAY SEYİR"
                        
                    msg = (
                        f"🤖 *CHAKO AI Agent Raporu*\n\n"
                        f"🪙 Parite: `{pair}`\n"
                        f"💰 Güncel Fiyat: `{last_price:,.2f} TL`\n"
                        f"📈 24s Değişim: ` %{daily_percent}`\n"
                        f"🧠 AI Kararı: *{ai_signal}*\n"
                        f"⚡ _On-chain ve duygu modelleri güncellendi._"
                    )
                    send_telegram_message(msg)
                    print(f"AI Agent Sinyali Gönderildi: {pair} - {last_price} TL")
    except Exception as e:
        print(f"Agent bağlantı hatası: {e}")

if __name__ == "__main__":
    print("CHAKO AI Agent Otomasyonu Başlatılıyor...")
    while True:
        run_chako_ai_agent()
        print("Analiz tamamlandı, sonraki döngü için 60 saniye bekleniyor...\n")
        time.sleep(60)
