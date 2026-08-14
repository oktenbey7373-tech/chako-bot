import requests
import time

def get_btcturk_tickers():
    url = "https://api.btcturk.com/api/v2/ticker"
    try:
        response = requests.get(url)
        data = response.json()
        if "data" in data:
            tickers = data["data"]
            print("--- CHAKO AI Trade: BtcTurk Canlı Veriler ---")
            for ticker in tickers:
                pair = ticker.get("pair")
                last_price = ticker.get("last")
                daily_percent = ticker.get("dailyPercent")
                if pair and last_price:
                    print(f"Coin: {pair} | Fiyat: {last_price} TL | Değişim: %{daily_percent}")
        else:
            print("Veri alınamadı.")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    print("CHAKO AI Trade Asistanı Başlatılıyor...")
    while True:
        get_btcturk_tickers()
        print("\nVeriler güncelleniyor (30 saniye bekleniyor)...\n")
        time.sleep(30)