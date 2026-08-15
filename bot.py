import requests
import time

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
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

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
                        volume = float(ticker.get("volume", 0))
                        
                        coin_list.append({
                            "pair": pair,
                            "last_price": last,
                            "high": high,
                            "low": low,
                            "daily_percent": daily_percent,
                            "volume": volume
                        })
                    except (ValueError, TypeError):
                        continue
            return coin_list
    except Exception as e:
        print(f"Piyasa veri çekme hatası: {e}")
    return []

def run_chako_ai_agent():
    print("CHAKO AI Genişletilmiş Kripto Hafızası ile Piyasaları Tıyor...")
    markets = get_market_data()
    
    if not markets:
        print("Piyasa verisi alınamadı.")
        return

    for coin in markets:
        pair = coin["pair"]
        last_price = coin["last_price"]
        high = coin["high"]
        low = coin["low"]
        daily_percent = coin["daily_percent"]
        volume = coin["volume"]

        # Kapsamlı AI Analiz ve Skorlama Mantığı
        # Fiyat aralığı (high - low) ve günlük değişim üzerinden momentum hesaplama
        price_range = high - low if high > low else 1
        position_in_range = (last_price - low) / price_range # 0 ile 1 arası dip/tepe konumu
        
        ai_signal = None
        strategy = ""
        keyboard = None

        # Güçlü Alım Sinyali Koşulları (Yüksek momentum veya dip dönüşü)
        if daily_percent > 4.0 and position_in_range > 0.7:
            ai_signal = "🚨 ACİL: 🚀 GÜÇLÜ MOMENTUM ALIM FIRSATI"
            strategy = "Boğa iştahı yüksek, hacim destekli yukarı kırılım gerçekleşiyor. İşlem değerlendirilebilir."
            keyboard = {"inline_keyboard": [[{"text": f"✅ {pair} ALIM ONAYI VER", "callback_data": f"buy_{pair}"}]]}
        elif daily_percent < -4.0 and position_in_range < 0.2:
            ai_signal = "🚨 ACİL: 🛡️ KRİTİK DESTEK / DİPTE REAKSİYON"
            strategy = "Fiyat dip seviyelerine geriledi, aşırı satım bölgesinden tepki alımı gelebilir."
            keyboard = {"inline_keyboard": [[{"text": f"🎯 {pair} DİPTEKİ ALICIYI ONAYLA", "callback_data": f"buy_dip_{pair}"}]]}
        elif daily_percent > 7.0:
            ai_signal = "⚠️ AŞIRI ISINMA / KAR REALİZASYONU"
            strategy = "Kısa sürede çok sert yükseldi, düzeltme gelebilir dikkatli olunmalı."
            keyboard = {"inline_keyboard": [[{"text": f"📉 {pair} SAT / KÂR AL", "callback_data": f"sell_{pair}"}]]}
        else:
            # Gürültüyü önlemek için normal ve durgun coinleri rapora boğmuyoruz
            continue

        msg = (
            f"🧠 *CHAKO AI Uzman Piyasa Analizi*\n\n"
            f"🔤 Parite: `{pair}`\n"
            f"💰 Güncel Fiyat: `{last_price:,.2f}` TL\n"
            f"📈 24s Değişim: `% {daily_percent}`\n"
            f"📊 24s En Yüksek/Düşük: `{high:,.2f}` / `{low:,.2f}` TL\n"
            f"⚖️ Aralık Konumu: `% {position_in_range * 100:.1f}` (Tepeye yakınlık)\n"
            f"🤖 AI Kararı: *{ai_signal}*\n"
            f"💡 Geniş Hafıza Stratejisi: _{strategy}_\n"
            f"⚡ *Sistem Durumu: Genişletilmiş Tarama Aktif*"
        )

        send_telegram_message(msg, reply_markup=keyboard)
        time.sleep(1.5) # Mesajların çakışmaması için ufak gecikme

if __name__ == "__main__":
    print("CHAKO AI Trade Bot Başlatıldı...")
    while True:
        run_chako_ai_agent()
        print("Tarama döngüsü bitti. 5 dakika sonra tekrar taranacak...\n")
        time.sleep(300) # Tam 5 dakika (300 saniye) bekleme
