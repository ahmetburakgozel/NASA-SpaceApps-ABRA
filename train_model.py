import requests
import pandas as pd
import numpy as np
from io import StringIO
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib


# train_model.py içindeki fetch_continuous_data fonksiyonu

# train_model.py içindeki fetch_continuous_data fonksiyonu

def fetch_continuous_data(lat, lon, start_year, end_year):
    print(f"{start_year}-{end_year} arası tüm veriler çekiliyor...")
    # --- DEĞİŞİKLİK: T2M_MIN kaldırıldı ---
    parameters = "T2M_MAX,RH2M,PRECTOTCORR,WS10M,PS,SLP,GWETTOP"

    start_date_str = f"{start_year}0101"
    end_date_str = f"{end_year}1231"
    api_url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?start={start_date_str}&end={end_date_str}&latitude={lat}&longitude={lon}&community=RE&parameters={parameters}&format=CSV")
    response = requests.get(api_url)
    if response.status_code != 200: raise Exception("NASA API'den veri alınamadı.")

    csv_text = response.text
    data_start_index = csv_text.find("YEAR,MO,DY")
    data_csv = csv_text[data_start_index:]
    df = pd.read_csv(StringIO(data_csv))

    # --- DEĞİŞİKLİK: Yeni sütun listesi ---
    df.columns = ['YEAR', 'MO', 'DY', 'T2M_MAX', 'RH2M', 'PRECTOTCORR', 'WS10M', 'PS', 'SLP', 'GWETTOP']
    df['DATE'] = pd.to_datetime({'year': df['YEAR'], 'month': df['MO'], 'day': df['DY']})
    df = df.set_index('DATE')

    # --- DEĞİŞİKLİK: Yeni özellik listesi ---
    df = df[['T2M_MAX', 'PRECTOTCORR', 'RH2M', 'WS10M', 'PS', 'SLP', 'GWETTOP']]
    df.replace(-999, np.nan, inplace=True)
    df.fillna(method='ffill', inplace=True)
    return df


def prepare_data_for_lstm(df, look_back=7):
    print("Veri LSTM modeli için hazırlanıyor...")
    data = df.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X, Y = [], []
    for i in range(len(scaled_data) - look_back):
        X.append(scaled_data[i:(i + look_back), :])
        # --- DEĞİŞİKLİK: Artık 2 değeri tahmin ediyoruz: T2M_MAX (0. sütun) ve PRECTOTCORR (1. sütun) ---
        Y.append(scaled_data[i + look_back, 0:2])

    X, Y = np.array(X), np.array(Y)
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    Y_train, Y_test = Y[:train_size], Y[train_size:]
    return X_train, Y_train, X_test, Y_test, scaler


def build_and_train_model(X_train, Y_train):
    print("Çoklu-çıktı LSTM modeli oluşturuluyor ve eğitiliyor...")
    model = Sequential([
        LSTM(units=70, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
        LSTM(units=50),
        # --- DEĞİŞİKLİK: Çıkış katmanında artık 2 nöron var (Sıcaklık ve Yağış için) ---
        Dense(units=2)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, Y_train, epochs=25, batch_size=32, verbose=1)  # Epoch sayısını biraz artırdık
    return model


if __name__ == '__main__':
    LATITUDE = 37.5753
    LONGITUDE = 36.9228
    data_df = fetch_continuous_data(LATITUDE, LONGITUDE, 1990, 2023)
    LOOK_BACK_DAYS = 7
    X_train, Y_train, X_test, Y_test, scaler = prepare_data_for_lstm(data_df, look_back=LOOK_BACK_DAYS)
    weather_model = build_and_train_model(X_train, Y_train)

    weather_model.save('weather_model.h5')
    joblib.dump(scaler, 'data_scaler.gz')
    print("\nEğitim tamamlandı! Yeni çoklu-çıktı modeliniz hazır.")