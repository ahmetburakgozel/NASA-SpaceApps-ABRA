#!/usr/bin/env python3
#   pip install meteostat pandas

import sys
from datetime import datetime
import pandas as pd
from meteostat import Point, Daily

def main():
    # Komut satırı argümanlarını kontrol et
    if len(sys.argv) < 4:
        print("Kullanım: python3 hava_verisi.py <enlem> <boylam> <output.csv>")
        print("Örnek : python3 hava_verisi.py 37.59002 36.90548 onikisubat.csv")
        sys.exit(1)

    # 1) Parametreleri al
    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    filename = sys.argv[3]

    elevation = None  # istersen metre cinsinden yükseklik verebilirsin (ör. 650)

    # 2) Tarih aralığı: bugünden geriye son 5 yıl
    end = pd.Timestamp.now().normalize()           # bugünün tarihi (saat 00:00)
    start = end - pd.DateOffset(years=5)           # 5 yıl öncesi

    # 3) Nokta nesnesi oluştur
    loc = Point(lat, lon, elevation)

    # 4) Günlük veriyi çek
    data = Daily(loc, start, end)
    df = data.fetch()

    # 5) Kontrol ve çıktı
    if df.empty:
        print(f"No data returned for the period {start.date()} -> {end.date()}.")
        sys.exit(1)

    # 6) CSV olarak kaydet
    df.to_csv(filename, index=True, date_format='%Y-%m-%d')
    print(f"✅ {len(df)} satır '{filename}' dosyasına kaydedildi.")
    print("📅 Tarih aralığı:", start.date(), "→", end.date())
    print("📊 Sütunlar:", list(df.columns))

if __name__ == "__main__":
    main()

