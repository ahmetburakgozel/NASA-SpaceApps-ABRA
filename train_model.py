import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

INPUT_FILE = "turkey_weather_dataset.csv"
LOOK_BACK_DAYS = 10


def prepare_data(df, look_back=10):
    df['DATE'] = pd.to_datetime(df[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
    df = df.set_index('DATE')

    # Modelin kullanacağı sütunlar (lat/lon dahil)
    features = ['T2M', 'PRECTOTCORR', 'WS10M', 'RH2M', 'PS', 'latitude', 'longitude']
    target_features = ['T2M', 'PRECTOTCORR', 'WS10M']

    df = df[features]

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)

    scaled_df = pd.DataFrame(scaled_data, index=df.index, columns=features)

    X, Y = [], []
    # Şehirler arası veri geçişini önlemek için gruplama
    for city_group in scaled_df.groupby(df['latitude']):
        city_data = city_group[1].values
        for i in range(len(city_data) - look_back):
            X.append(city_data[i:(i + look_back), :])
            Y.append(city_data[i + look_back, 0:len(target_features)])

    return np.array(X), np.array(Y), scaler


def build_and_train_model(X, Y):
    model = Sequential([
        LSTM(units=70, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        LSTM(units=50),
        Dense(units=3)  # T2M, PRECTOTCORR, WS10M
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, Y, epochs=20, batch_size=128, verbose=1, validation_split=0.1)
    return model


if __name__ == "__main__":
    print(f"'{INPUT_FILE}' okunuyor...")
    dataset = pd.read_csv(INPUT_FILE)

    print("Veri, model için hazırlanıyor...")
    X_data, Y_data, scaler = prepare_data(dataset, look_back=LOOK_BACK_DAYS)

    print(f"Eğitim için {len(X_data)} adet veri dizisi oluşturuldu. Model eğitiliyor...")
    model = build_and_train_model(X_data, Y_data)

    model.save('weather_model.h5')
    joblib.dump(scaler, 'weather_scaler.gz')
    print("\nBAŞARILI! Türkiye geneli için eğitilmiş model ve scaler kaydedildi.")