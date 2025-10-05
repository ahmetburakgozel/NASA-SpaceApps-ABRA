import requests
import pandas as pd
from datetime import date, timedelta

# --- AYARLAR ---
API_KEY = '96bdf2eec8f34c13bc192004250410'
CITY = 'Kahramanmaras'
START_DATE = '2020-01-01'
END_DATE = '2024-12-31'  # Geçmiş 2 yıllık veri
OUTPUT_FILE = 'egitim_veriseti.csv'


# ---------------

def scrape_historical_data():
    """WeatherAPI'den geçmiş verileri çeker ve bir CSV dosyasına kaydeder."""

    all_data = []
    current_date = date.fromisoformat(START_DATE)
    end_date_obj = date.fromisoformat(END_DATE)

    print(f"{START_DATE} ile {END_DATE} arası veriler WeatherAPI'den çekiliyor...")

    while current_date <= end_date_obj:
        date_str = current_date.isoformat()
        url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={CITY}&dt={date_str}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()['forecast']['forecastday'][0]['day']
                all_data.append({
                    'DATE': date_str,
                    'T2M': data['avgtemp_c'],
                    'PRECTOTCORR': data['totalprecip_mm'],
                    'WS10M': data['maxwind_kph'],
                    'RH2M': data['avghumidity'],
                    'PS': 101.3,  # WeatherAPI bu veriyi doğrudan sunmuyor, standart bir değer kullanalım
                })
                print(f"{date_str} verisi çekildi.")
            else:
                print(f"HATA: {date_str} verisi çekilemedi. Sebep: {response.text}")
        except Exception as e:
            print(f"HATA: {date_str} işlenirken sorun oluştu: {e}")

        current_date += timedelta(days=1)

    if not all_data:
        print("Hiç veri çekilemedi. API anahtarınızı veya tarih aralığını kontrol edin.")
        return

    df = pd.DataFrame(all_data)
    df.set_index('DATE', inplace=True)
    df.to_csv(OUTPUT_FILE)

    print(f"\nBAŞARILI! Toplam {len(df)} günlük veri '{OUTPUT_FILE}' dosyasına kaydedildi.")


if __name__ == '__main__':
    scrape_historical_data()