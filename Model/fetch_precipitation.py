import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

# Visual Crossing Weather API
API_KEY = "A42RC6C6K4VQYHDQ3DJFSVGSE"
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Klasör yolları
SOURCE_FOLDER = os.path.join(os.path.dirname(__file__), 'sehirler')
PRECIP_FOLDER = os.path.join(os.path.dirname(__file__), 'sehirler-with-precip')

# Yağış verisi klasörü yoksa oluştur
if not os.path.exists(PRECIP_FOLDER):
    os.makedirs(PRECIP_FOLDER)

def fetch_precipitation_data(city, start_date, end_date):
    """
    Belirtilen şehir ve tarih aralığı için günlük yağış verilerini çeker
    Yağış verileri mm cinsindendir
    """
    # URL'yi düzelt - şehir adını tekrarlama
    url = f"{BASE_URL}/{city}"
    params = {
        'unitGroup': 'metric',
        'key': API_KEY,
        'startDateTime': start_date,
        'endDateTime': end_date,
        'include': 'days',
        'elements': 'datetime,precip',
        'contentType': 'json'
    }

    try:
        print(f"API çağrısı yapılıyor: {start_date} - {end_date}")
        response = requests.get(url, params=params)

        if response.status_code == 429:  # Rate limit aşıldı
            print("Rate limit aşıldı. 60 saniye bekleniyor...")
            time.sleep(60)
            return fetch_precipitation_data(city, start_date, end_date)

        if response.status_code != 200:
            print(f"API Hatası ({response.status_code}): {response.text}")
            return None

        data = response.json()

        daily_data = []
        for day in data.get('days', []):
            daily_data.append({
                'time': day['datetime'],
                'precip': day.get('precip', 0)  # Yağış yoksa 0 kabul et
            })

        return pd.DataFrame(daily_data)

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return None

def split_date_range(start_date, end_date, chunk_days=365):
    """Tarih aralığını küçük parçalara böler"""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    current = start
    while current < end:
        chunk_end = min(current + timedelta(days=chunk_days), end)
        yield current.strftime('%Y-%m-%d'), chunk_end.strftime('%Y-%m-%d')
        current = chunk_end + timedelta(days=1)

def main():
    print(f"Kaynak veri klasörü: {SOURCE_FOLDER}")
    print(f"Yağış verisi klasörü: {PRECIP_FOLDER}")

    # Türkiye şehirleri
    cities = {
        'eskisehir': 'Eskisehir,Turkey',
        'istanbul': 'Istanbul,Turkey',
        'van': 'Van,Turkey',
        'antalya': 'Antalya,Turkey',
        'mersin': 'Mersin,Turkey',
        'canakkale': 'Canakkale,Turkey',
        'maras': 'Kahramanmaras,Turkey',
        'erzurum': 'Erzurum,Turkey',
        'mugla': 'Mugla,Turkey',
        'bursa': 'Bursa,Turkey',
        'izmir': 'Izmir,Turkey',
        'kapadokya': 'Nevsehir,Turkey',
        'sakarya': 'Sakarya,Turkey',
        'bolu': 'Bolu,Turkey'
    }

    for city_file, city_name in cities.items():
        print(f"\nİşleniyor: {city_file}")

        try:
            # Kaynak CSV dosyasını oku
            source_path = os.path.join(SOURCE_FOLDER, f"{city_file}.csv")
            if not os.path.exists(source_path):
                print(f"Kaynak dosya bulunamadı: {source_path}")
                continue

            # Hedef dosya yolu
            target_path = os.path.join(PRECIP_FOLDER, f"{city_file}.csv")

            df = pd.read_csv(source_path)
            df['time'] = pd.to_datetime(df['time'])

            # Tarih aralığını belirle
            start_date = df['time'].min()
            end_date = df['time'].max()

            # Tüm yağış verilerini topla
            all_precip_data = []

            # Tarih aralığını parçala ve her parça için veri çek
            for chunk_start, chunk_end in split_date_range(start_date, end_date):
                precip_df = fetch_precipitation_data(city_name, chunk_start, chunk_end)
                if precip_df is not None:
                    all_precip_data.append(precip_df)
                time.sleep(2)  # API rate limit için bekle

            if all_precip_data:
                # Tüm yağış verilerini birleştir
                precip_df = pd.concat(all_precip_data, ignore_index=True)
                precip_df['time'] = pd.to_datetime(precip_df['time'])

                # Tekrar eden tarihleri temizle
                precip_df = precip_df.drop_duplicates(subset=['time'])

                # Mevcut verilerle birleştir
                df = df.merge(precip_df, on='time', how='left')

                # Yeni dosyaya kaydet
                df.to_csv(target_path, index=False)
                print(f"Yağış verileri eklendi ve yeni dosyaya kaydedildi: {target_path}")

        except Exception as e:
            print(f"Hata oluştu ({city_file}): {str(e)}")
            continue

if __name__ == "__main__":
    main()
