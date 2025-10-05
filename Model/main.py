import requests
import pandas as pd
from io import StringIO

# 1. PARAMETRELERİ AYARLAMA
# Kahramanmaraş'ın yaklaşık koordinatları
latitude = 37.5753
longitude = 36.9228

# İlgilendiğimiz tarih aralığı
# API genellikle bir önceki yılı tamamlanmış olarak sunar, bu yüzden 2023 yerine 2022'ye kadar istiyoruz.
start_year = 1990
end_year = 2022

# İlgilendiğimiz parametreler
# T2M_MAX: Maksimum Hava Sıcaklığı (Celcius)
# PRECTOTCORR: Toplam Yağış Miktarı (mm/gün)
parameters = "T2M_MAX,PRECTOTCORR"

# NASA POWER API URL'ini oluşturma
# Sadece belirli bir gün (5 Ekim) için veri çekecek şekilde formatlanmıştır.
# YYYYMMDD formatı gereklidir.
start_date = f"{start_year}1005"
end_date = f"{end_year}1005"
api_url = (
    f"https://power.larc.nasa.gov/api/temporal/daily/point"
    f"?start={start_date}&end={end_date}"  # YYYYMMDD formatında 5 Ekim
    f"&latitude={latitude}&longitude={longitude}"
    f"&community=RE&parameters={parameters}&format=CSV"
)

# 2. API'YE İSTEK GÖNDERME VE VERİYİ ALMA
print("NASA POWER API'sinden veri çekiliyor...")
response = requests.get(api_url)

# İstek başarılı mı kontrol etme
if response.status_code == 200:
    print("Veri başarıyla çekildi!")

    # API'den dönen CSV metnini okuma
    # NASA POWER API'si veriden önce birkaç satır başlık bilgisi gönderir, bunları atlamamız gerekiyor.
    csv_text = response.text

    # Verinin başladığı satırı bulma
    data_start_index = csv_text.find("YEAR,MO,DY")

    # Sadece veri kısmını alıp bir DataFrame'e dönüştürme
    data_csv = csv_text[data_start_index:]
    df = pd.read_csv(StringIO(data_csv))

    # Sadece 5 Ekim günlerini filtrele
    df_5ekim = df[(df['MO'] == 10) & (df['DY'] == 5)]

    # Filtrelenen verileri CSV dosyasına kaydet
    df_5ekim.to_csv("5ekim_verileri.csv", index=False)
    print("5 Ekim verileri '5ekim_verileri.csv' dosyasına kaydedildi.")

    # 3. VERİYİ GÖRÜNTÜLEME
    print("\n--- 5 Ekim Günü İçin Tarihsel Veriler ---")
    print(df_5ekim.head())  # İlk 5 satırı göster

    # 4. BASİT BİR OLASILIK HESAPLAMASI
    # Eşik değerlerimizi belirleyelim
    sicaklik_esigi = 20.0  # 20°C'den sıcak günler "çok sıcak" sayılsın
    yagis_esigi = 5.0  # 5mm'den fazla yağış olan günler "çok yağışlı" sayılsın

    # Eşiği geçen gün sayısını bulma
    cok_sicak_gun_sayisi = df_5ekim[df_5ekim['T2M_MAX'] > sicaklik_esigi].shape[0]
    cok_yagisli_gun_sayisi = df_5ekim[df_5ekim['PRECTOTCORR'] > yagis_esigi].shape[0]

    # Toplam 5 Ekim günü sayısını bulma
    toplam_5ekim_sayisi = df_5ekim.shape[0]

    # Olasılıkları hesaplama
    sicaklik_olasiligi = (cok_sicak_gun_sayisi / toplam_5ekim_sayisi) * 100 if toplam_5ekim_sayisi > 0 else 0
    yagis_olasiligi = (cok_yagisli_gun_sayisi / toplam_5ekim_sayisi) * 100 if toplam_5ekim_sayisi > 0 else 0

    print("\n--- Olasılık Hesaplamaları ---")
    print(f"Veri aralığı: {start_year}-{end_year} ({toplam_5ekim_sayisi} adet 5 Ekim günü)")
    print(f"5 Ekim'de havanın {sicaklik_esigi}°C'den sıcak olma olasılığı: {sicaklik_olasiligi:.2f}%")
    print(f"5 Ekim'de yağışın {yagis_esigi}mm'den fazla olma olasılığı: {yagis_olasiligi:.2f}%")

else:
    print(f"API'den veri çekilemedi. Hata Kodu: {response.status_code}")
    print(response.text)