from datetime import datetime
from meteostat import Point, Daily
import pandas as pd

# --- AYARLAR ---
CITY_NAME = "Kahramanmaraş"
LATITUDE = 37.5753
LONGITUDE = 36.9228
START_YEAR = 2000
END_YEAR = 2024
OUTPUT_FILE = "kahramanmaras_dataset.csv"


# ---------------

def create_meteostat_dataset():
    """Belirtilen konum için Meteostat'tan tarihsel veri çeker ve CSV olarak kaydeder."""

    print(f"{CITY_NAME} için hava istasyonu verileri aranıyor...")
    start = datetime(START_YEAR, 1, 1)
    end = datetime(END_YEAR, 12, 31)

    # Veri çekme
    data = Daily(Point(LATITUDE, LONGITUDE), start, end)
    data = data.fetch()

    if data.empty:
        print("HATA: Bu konum ve tarih aralığı için veri bulunamadı.")
        return

    print(f"{len(data)} günlük veri başarıyla çekildi.")

    # Gerekli sütunları seçme ve isimlendirme (projemizin standartına uygun)
    # tavg: Ort. Sıcaklık, prcp: Yağış, wspd: Rüzgar Hızı, pres: Basınç
    df = data[['tavg', 'prcp', 'wspd', 'pres']]
    df.rename(columns={
        'tavg': 'T2M',
        'prcp': 'PRECTOTCORR',
        'wspd': 'WS10M',
        'pres': 'PS'
    }, inplace=True)

    # Meteostat nem verisini günlük olarak sunmuyor, bu yüzden onu şimdilik dışarıda bırakıyoruz.
    # Modelimizin öğrenmesi için yeterli veri var.
    df['RH2M'] = 60.0  # Ortalama bir nem değeriyle dolduralım
    df = df[['T2M', 'PRECTOTCORR', 'WS10M', 'RH2M', 'PS']]  # Standart sıralamamıza getir

    # Eksik verileri doldurma
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)  # Baştaki boşluklar için

    df.to_csv(OUTPUT_FILE)

    print(f"\nBAŞARILI! Veri seti '{OUTPUT_FILE}' dosyasına kaydedildi.")


if __name__ == "__main__":
    create_meteostat_dataset()