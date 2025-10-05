import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os
from datetime import datetime, timedelta

# Mutlak yolları ayarla
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'sehirler-manip')
PREDICTIONS_FOLDER = os.path.join(BASE_DIR, 'predictions')

def create_sequences(data, seq_length):
    sequences = []
    targets = []
    for i in range(len(data) - seq_length):
        seq = data[i:i + seq_length]
        target = data[i + seq_length]
        sequences.append(seq)
        targets.append(target)
    return np.array(sequences), np.array(targets)

def create_lstm_model(input_shape, output_shape):
    model = Sequential([
        LSTM(100, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(output_shape)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def prepare_data(df):
    # Tarihi datetime'a çevir
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time')

    # Kullanılacak özellikler - CSV'deki gerçek sütun isimleri
    features = ['tavg', 'tmin', 'tmax', 'wspd', 'pres', 'yagis']
    available_features = [f for f in features if f in df.columns]

    # Verileri normalize et
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[available_features])

    return scaled_data, scaler, available_features

def predict_future(model, last_sequence, scaler, n_days, seq_length):
    predictions = []
    current_seq = last_sequence.copy()

    for _ in range(n_days):
        current_pred = model.predict(current_seq.reshape(1, seq_length, -1), verbose=0)
        predictions.append(current_pred[0])

        current_seq = np.roll(current_seq, -1, axis=0)
        current_seq[-1] = current_pred[0]

    predictions = np.array(predictions)
    predictions = scaler.inverse_transform(predictions)

    return predictions

def main():
    print(f"Veri klasörü: {DATA_FOLDER}")

    # Tahmin klasörü oluştur
    if not os.path.exists(PREDICTIONS_FOLDER):
        os.makedirs(PREDICTIONS_FOLDER)
        print(f"Tahmin klasörü oluşturuldu: {PREDICTIONS_FOLDER}")

    # Model parametreleri
    seq_length = 30  # 30 günlük veri kullanarak tahmin yap
    n_days = 365  # 1 yıllık tahmin

    if not os.path.exists(DATA_FOLDER):
        print(f"Hata: Veri klasörü bulunamadı: {DATA_FOLDER}")
        return

    # Her şehir için işlem yap
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith('.csv'):
            city_name = filename.replace('.csv', '')
            print(f"\nİşleniyor: {city_name}")

            try:
                # Veriyi yükle
                file_path = os.path.join(DATA_FOLDER, filename)
                df = pd.read_csv(file_path)
                print(f"Veri yüklendi: {len(df)} satır")

                # Veriyi hazırla
                scaled_data, scaler, features = prepare_data(df)
                print(f"Kullanılan özellikler: {features}")

                # Sequence'leri oluştur
                X, y = create_sequences(scaled_data, seq_length)
                print(f"Eğitim verileri hazırlandı: {len(X)} sequence")

                # Modeli oluştur ve eğit
                model = create_lstm_model((seq_length, len(features)), len(features))
                print("Model eğitiliyor...")
                model.fit(X, y, epochs=50, batch_size=32, verbose=0)

                # Son sequence'i al
                last_sequence = scaled_data[-seq_length:]

                # Gelecek tahminleri yap
                predictions = predict_future(model, last_sequence, scaler, n_days, seq_length)

                # Tahminleri DataFrame'e dönüştür
                last_date = df['time'].iloc[-1]
                future_dates = [pd.to_datetime(last_date) + timedelta(days=i+1) for i in range(n_days)]
                pred_df = pd.DataFrame(predictions, columns=features)
                pred_df['time'] = future_dates

                # Tahminleri kaydet
                output_file = os.path.join(PREDICTIONS_FOLDER, f"{city_name}_predictions.csv")
                pred_df.to_csv(output_file, index=False)
                print(f"Tahminler kaydedildi: {output_file}")

            except Exception as e:
                print(f"Hata oluştu ({city_name}): {str(e)}")
                continue

if __name__ == "__main__":
    main()
