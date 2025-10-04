import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

# --- AYARLAR: Buradaki değerleri değiştirerek farklı veriler çekebilirsiniz ---

# İncelenecek Konum (Varsayılan: Kahramanmaraş)
LATITUDE = 37.5753
LONGITUDE = 36.9228

# İncelenecek Tarih Aralığı (Modelin kullandığı son 10 günü çekmek için ayarlandı)
# Örneğin, son 12 günün verisini çekip -999 olup olmadığını kontrol edelim.
END_DATE = datetime.now() - timedelta(days=2)
START_DATE = END_DATE - timedelta(days=11)

# Çekilecek Parametreler (Modelin kullandığı tüm girdiler)
PARAMETERS = "T2M,PRECTOTCORR,WS10M,RH2M,PS"

# Sonucun kaydedileceği dosya adı
OUTPUT_FILENAME = "nasa_veri_çıktısı.csv"


# --------------------------------------------------------------------------

def fetch_and_save_data(lat, lon, start_date, end_date, params, filename):
    """
    Belirtilen konum ve tarih aralığı için NASA'dan veri çeker,
    temizler ve bir CSV dosyasına kaydeder.
    """
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')

    print(f"NASA POWER API'den veri çekiliyor...")
    print(f"Konum: Lat={lat}, Lon={lon}")
    print(f"Tarih Aralığı: {start_str} - {end_str}")

    api_url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?start={start_str}&end={end_str}"
        f"&latitude={lat}&longitude={lon}"
        f"&community=RE&parameters={params}"
        f"&format=CSV"
    )

    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"HATA: API'den veri alınamadı. Status Kodu: {response.status_code}")
        print(f"Sunucu Yanıtı: {response.text}")
        return

    csv_text = response.text
    data_start_index = csv_text.find("YEAR,MO,DY")
    if data_start_index == -1:
        print("HATA: Gelen veride beklenen format bulunamadı.")
        return

    data_csv = csv_text[data_start_index:]
    df = pd.read_csv(StringIO(data_csv))

    print("\n--- HAM VERİ (İlk 5 Satır) ---")
    print(df.head())

    # Veriyi Temizleme
    df.replace(-999, pd.NA, inplace=True)
    # Bu script'te boş veriyi doldurmuyoruz ki nerede olduğunu görebilelim

    # Tarih sütunu oluşturma
    df['DATE'] = pd.to_datetime(df[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
    df = df.set_index('DATE')

    try:
        df.to_csv(filename)
        print(f"\nBAŞARILI: Veriler temizlendi ve '{filename}' dosyasına kaydedildi.")
        print("Bu dosyayı Excel veya başka bir programla açıp inceleyebilirsiniz.")
    except Exception as e:
        print(f"\nHATA: Dosya kaydedilirken bir sorun oluştu: {e}")


if __name__ == '__main__':
    fetch_and_save_data(LATITUDE, LONGITUDE, START_DATE, END_DATE, PARAMETERS, OUTPUT_FILENAME)