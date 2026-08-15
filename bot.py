import requests
import time

TOKEN = "8732581183:AAgKyg2vS07HaGqTWcVHX0zkr50KePf600"
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
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")
def get_market_data():
    url = "https://api.btcturk.com/api/v2/ticker"
    try:
        response = requests.get(url)
        data = response.json()
        if "data" in data:
            for ticker in data["data"]:
                if ticker.get("pair") == "BTC_TRY":
                    return {
                        "last_price": ticker.get("last"),
                        "daily_percent": float(ticker.get("dailyPercent", 0)),
                        "high": ticker.get("high"),
                        "low": ticker.get("low")
                    }
    except Exception as e:
        print(f"Piyasa veri hatası: {e}")
    return None

def run_chako_ai_agent():
    market = get_market_data()
    if market:
        last_price = market["last_price"]
        daily_percent = market["daily_percent"]
        
        # CHAKO AI Gelişmiş Karar Mekanizması
        # CHAKO AI Gelişmiş Karar Mekanizması
    if daily_percent > 2.0:
        ai_signal = "✅ GÜÇLÜ AL (Yüksek Momentum)"
        strategy = "Boğa sezonu iştahı yüksek, direnç seviyeleri takip edilmeli."
        keyboard = {"inline_keyboard": [[{"text": "🚀 AL ONAYI", "callback_data": "buy"}]]}
    elif daily_percent < -2.0:
        ai_signal = "❌ DİKKAT / SATIŞ BASKISI"
        strategy = "Destek noktaları test ediliyor, kademeli alım bölgesi kullanılabilir."
        keyboard = {"inline_keyboard": [[{"text": "🛡️ SAT ONAYI", "callback_data": "sell"}]]}
    else:
        ai_signal = "⚖️ NÖTR / KONSOLİDASYON"
        strategy = "Piyasa yatay seyirde, balina hareketleri bekleniyor."
        keyboard = None
            
        msg = (
            f"🤖 *CHAKO AI Agent Akıllı Raporu*\n\n"
            f"🪙 Parite: `BTC_TRY`\n"
            f"💰 Güncel Fiyat: `{last_price:,.2f} TL`\n"
            f"📈 24s Değişim: ` %{daily_percent}`\n"
            f"📊 En Yüksek / Düşük: `{market['high']:,.2f} / {market['low']:,.2f}`\n\n"
            f"🧠 AI Kararı: *{ai_signal}*\n"
            f"💡 Strateji Notu: _{strategy}_\n"
            f"⚡ *Sistem Durumu: Aktif (7/24 İzleniyor)*"
        )
        send_telegram_message(msg, reply_markup=keyboard)
        print("AI Agent akıllı analizi Telegram'a gönderildi.")

if __name__ == "__main__":
    print("CHAKO AI Agent Beyin Entegrasyonu Başlatıldı...")
    while True:
        run_chako_ai_agent()
        print("Döngü tamamlandı, sonraki analiz için 60 saniye bekleniyor...\n")
        time.sleep(60)
