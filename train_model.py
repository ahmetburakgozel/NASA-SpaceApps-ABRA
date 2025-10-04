import requests
import pandas as pd
import numpy as np
from io import StringIO
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib


# --- 1. VERİ ÇEKME ---
def fetch_continuous_data(lat, lon, start_year, end_year):
    print(f"{start_year}-{end_year} arası tüm veriler çekiliyor...")
    # --- DEĞİŞİKLİK: T2M yerine T2M_MAX istiyoruz ---
    parameters = "T2M_MAX,RH2M,PRECTOTCORR,WS10M"
    start_date_str = f"{start_year}0101"
    end_date_str = f"{end_year}1231"
    api_url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?start={start_date_str}&end={end_date_str}"
        f"&latitude={lat}&longitude={lon}"
        f"&community=RE&parameters={parameters}&format=CSV"
    )
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("NASA API'den veri alınamadı.")

    csv_text = response.text
    data_start_index = csv_text.find("YEAR,MO,DY")
    data_csv = csv_text[data_start_index:]
    df = pd.read_csv(StringIO(data_csv))

    # --- DEĞİŞİKLİK: Yeni sütun ismini ekle ---
    df.columns = ['YEAR', 'MO', 'DY', 'T2M_MAX', 'RH2M', 'PRECTOTCORR', 'WS10M']

    df['DATE'] = pd.to_datetime({'year': df['YEAR'], 'month': df['MO'], 'day': df['DY']})
    df = df.set_index('DATE')

    # --- DEĞİŞİKLİK: Sütun listesini güncelle ---
    df = df[['T2M_MAX', 'RH2M', 'PRECTOTCORR', 'WS10M']]
    df.replace(-999, np.nan, inplace=True)
    df.fillna(method='ffill', inplace=True)
    return df


# --- 2. VERİ ÖN İŞLEME ---
def prepare_data_for_lstm(df, look_back=7):
    print("Veri LSTM modeli için hazırlanıyor...")
    data = df.values

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X, Y = [], []
    for i in range(len(scaled_data) - look_back):
        X.append(scaled_data[i:(i + look_back), :])
        # --- DEĞİŞİKLİK: Hedefimiz hala ilk sütun, ama artık o T2M_MAX ---
        Y.append(scaled_data[i + look_back, 0])

    X, Y = np.array(X), np.array(Y)

    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    Y_train, Y_test = Y[:train_size], Y[train_size:]

    return X_train, Y_train, X_test, Y_test, scaler


# build_and_train_model fonksiyonu aynı kalıyor...
def build_and_train_model(X_train, Y_train):
    print("LSTM modeli oluşturuluyor ve eğitiliyor...")
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
        LSTM(units=50),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, Y_train, epochs=20, batch_size=32, verbose=1)
    return model


# --- ANA ÇALIŞTIRMA BLOĞU ---
if __name__ == '__main__':
    LATITUDE = 37.5753
    LONGITUDE = 36.9228
    data_df = fetch_continuous_data(LATITUDE, LONGITUDE, 1990, 2023)
    LOOK_BACK_DAYS = 7
    X_train, Y_train, X_test, Y_test, scaler = prepare_data_for_lstm(data_df, look_back=LOOK_BACK_DAYS)
    weather_model = build_and_train_model(X_train, Y_train)

    print("Model 'weather_model.h5' olarak kaydediliyor.")
    weather_model.save('weather_model.h5')
    print("Scaler 'data_scaler.gz' olarak kaydediliyor.")
    joblib.dump(scaler, 'data_scaler.gz')
    print("\nEğitim tamamlandı!")