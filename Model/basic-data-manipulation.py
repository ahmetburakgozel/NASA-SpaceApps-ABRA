import os
import pandas as pd
from datetime import datetime

# Klasör yolları
current_dir = os.path.dirname(os.path.abspath(__file__))
source_folder = os.path.join(current_dir, 'sehirler-with-precip')
manip_folder = os.path.join(current_dir, 'sehirler-manip')

print(f"Kaynak klasör: {source_folder}")
print(f"Hedef klasör: {manip_folder}")

# Hedef klasörü kontrol et/oluştur
if not os.path.exists(manip_folder):
    os.makedirs(manip_folder)
    print("sehirler-manip klasörü oluşturuldu")

def clean_weather_data(df):
    # İstenmeyen sütunları kaldır
    for col in ["snow", "wdir", "tsun", "wpgt"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Yağış verisini kontrol et ve düzelt
    if 'yagis' not in df.columns:
        df['yagis'] = 0
    else:
        df['yagis'] = pd.to_numeric(df['yagis'], errors='coerce').fillna(0)

    return df

# Ana döngü
for filename in os.listdir(source_folder):
    if filename.endswith('.csv'):
        print(f"\nİşleniyor: {filename}")
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(manip_folder, filename.lower())  # Dosya adını küçük harfe çevir

        try:
            # CSV'yi oku
            df = pd.read_csv(source_path)
            print(f"Okundu: {len(df)} satır")

            # Veriyi temizle
            df = clean_weather_data(df)

            # Manipüle edilmiş veriyi kaydet
            df.to_csv(target_path, index=False)
            print(f"Kaydedildi: {target_path}")

        except Exception as e:
            print(f"HATA ({filename}): {str(e)}")
