from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import requests
from io import StringIO
import joblib
from datetime import datetime, timedelta, date

app = Flask(__name__)
# ... TURKISH_CITIES sözlüğünü buraya ekleyin ...
TURKISH_CITIES = {
    "Adana": {"lat": 37.0, "lon": 35.3213}, "Adıyaman": {"lat": 37.7648, "lon": 38.2763},
    "Afyonkarahisar": {"lat": 38.7568, "lon": 30.5387}, "Ağrı": {"lat": 39.7191, "lon": 43.0506},
    "Amasya": {"lat": 40.65, "lon": 35.8333}, "Ankara": {"lat": 39.9208, "lon": 32.8541},
    "Antalya": {"lat": 36.8969, "lon": 30.7133}, "Artvin": {"lat": 41.1828, "lon": 41.8194},
    "Aydın": {"lat": 37.838, "lon": 27.8456}, "Balıkesir": {"lat": 39.6534, "lon": 27.8903},
    "Bilecik": {"lat": 40.1428, "lon": 29.9792}, "Bingöl": {"lat": 38.8853, "lon": 40.4983},
    "Bitlis": {"lat": 38.4005, "lon": 42.1095}, "Bolu": {"lat": 40.7348, "lon": 31.6095},
    "Burdur": {"lat": 37.7203, "lon": 30.2908}, "Bursa": {"lat": 40.1933, "lon": 29.0742},
    "Çanakkale": {"lat": 40.1467, "lon": 26.4086}, "Çankırı": {"lat": 40.6013, "lon": 33.6136},
    "Çorum": {"lat": 40.5499, "lon": 34.9535}, "Denizli": {"lat": 37.7833, "lon": 29.0944},
    "Diyarbakır": {"lat": 37.9144, "lon": 40.2306}, "Edirne": {"lat": 41.6771, "lon": 26.5557},
    "Elazığ": {"lat": 38.6749, "lon": 39.2225}, "Erzincan": {"lat": 39.7431, "lon": 39.4904},
    "Erzurum": {"lat": 39.9059, "lon": 41.2769}, "Eskişehir": {"lat": 39.7667, "lon": 30.5256},
    "Gaziantep": {"lat": 37.0662, "lon": 37.3833}, "Giresun": {"lat": 40.9128, "lon": 38.3895},
    "Gümüşhane": {"lat": 40.4601, "lon": 39.4816}, "Hakkari": {"lat": 37.5744, "lon": 43.7408},
    "Hatay": {"lat": 36.2023, "lon": 36.1603}, "Isparta": {"lat": 37.7648, "lon": 30.5517},
    "Mersin": {"lat": 36.8121, "lon": 34.6415}, "İstanbul": {"lat": 41.0082, "lon": 28.9784},
    "İzmir": {"lat": 38.4237, "lon": 27.1428}, "Kars": {"lat": 40.6013, "lon": 43.0975},
    "Kastamonu": {"lat": 41.3887, "lon": 33.7827}, "Kayseri": {"lat": 38.7205, "lon": 35.4826},
    "Kırklareli": {"lat": 41.7352, "lon": 27.225}, "Kırşehir": {"lat": 39.1466, "lon": 34.1593},
    "Kocaeli": {"lat": 40.8533, "lon": 29.8815}, "Konya": {"lat": 37.8746, "lon": 32.4932},
    "Kütahya": {"lat": 39.4213, "lon": 29.9833}, "Malatya": {"lat": 38.3552, "lon": 38.3095},
    "Manisa": {"lat": 38.6191, "lon": 27.4289}, "Kahramanmaraş": {"lat": 37.5753, "lon": 36.9228},
    "Mardin": {"lat": 37.3129, "lon": 40.7339}, "Muğla": {"lat": 37.2153, "lon": 28.3636},
    "Muş": {"lat": 38.7461, "lon": 41.4817}, "Nevşehir": {"lat": 38.6251, "lon": 34.7142},
    "Niğde": {"lat": 37.9667, "lon": 34.6792}, "Ordu": {"lat": 40.9833, "lon": 37.8833},
    "Rize": {"lat": 41.0201, "lon": 40.5234}, "Sakarya": {"lat": 40.7731, "lon": 30.3948},
    "Samsun": {"lat": 41.2833, "lon": 36.3333}, "Siirt": {"lat": 37.9333, "lon": 41.95},
    "Sinop": {"lat": 42.0286, "lon": 35.155}, "Sivas": {"lat": 39.7477, "lon": 37.0179},
    "Tekirdağ": {"lat": 40.9781, "lon": 27.5117}, "Tokat": {"lat": 40.3235, "lon": 36.5522},
    "Trabzon": {"lat": 41.0027, "lon": 39.7169}, "Tunceli": {"lat": 39.1061, "lon": 39.5483},
    "Şanlıurfa": {"lat": 37.1674, "lon": 38.7957}, "Uşak": {"lat": 38.6823, "lon": 29.4019},
    "Van": {"lat": 38.5019, "lon": 43.373}, "Yozgat": {"lat": 39.8203, "lon": 34.8087},
    "Zonguldak": {"lat": 41.4564, "lon": 31.7987}, "Aksaray": {"lat": 38.3686, "lon": 34.037},
    "Bayburt": {"lat": 40.2551, "lon": 40.2246}, "Karaman": {"lat": 37.1811, "lon": 33.2222},
    "Kırıkkale": {"lat": 39.8468, "lon": 33.5153}, "Batman": {"lat": 37.8812, "lon": 41.1351},
    "Şırnak": {"lat": 37.5165, "lon": 42.4556}, "Bartın": {"lat": 41.6339, "lon": 32.3374},
    "Ardahan": {"lat": 41.1105, "lon": 42.7022}, "Iğdır": {"lat": 39.9204, "lon": 44.045},
    "Yalova": {"lat": 40.6556, "lon": 29.2769}, "Karabük": {"lat": 41.1982, "lon": 32.6281},
    "Kilis": {"lat": 36.7184, "lon": 37.1141}, "Osmaniye": {"lat": 37.0746, "lon": 36.2464},
    "Düzce": {"lat": 40.8438, "lon": 31.1565}
}
MODEL = load_model('weather_model.h5')
SCALER = joblib.load('weather_scaler.gz')
LOOK_BACK_DAYS = 10
NUM_FEATURES = 7  # T2M, PRECTOTCORR, WS10M, RH2M, PS, latitude, longitude
ALL_HISTORICAL_DATA = pd.read_csv("turkey_weather_dataset.csv")


@app.route('/')
def index():
    return render_template('index.html', cities=TURKISH_CITIES.keys())


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        city_name, date_str = data.get('city'), data.get('date')
        city_coords = TURKISH_CITIES.get(city_name)
        if not city_coords: return jsonify({"error": "Geçersiz şehir."}), 400

        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        days_ahead = (target_date - date.today()).days

        lat, lon = city_coords['lat'], city_coords['lon']

        if days_ahead <= 14:
            # Gerçek son 10 günün verisi için API'ye gidelim
            start_date_param = (datetime.now() - timedelta(days=LOOK_BACK_DAYS + 2)).strftime('%Y%m%d')
            end_date_param = (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')
            params = "T2M,PRECTOTCORR,WS10M,RH2M,PS"
            api_url = (
                f"https://power.larc.nasa.gov/api/temporal/daily/point?start={start_date_param}&end={end_date_param}&latitude={lat}&longitude={lon}&community=RE&parameters={params}&format=CSV")
            response = requests.get(api_url)
            if response.status_code != 200: return jsonify({"error": "Güncel veri alınamadı."}), 500

            csv_text = response.text
            data_start_index = csv_text.find("YEAR,MO,DY")
            df = pd.read_csv(StringIO(csv_text[data_start_index:]))
            df.replace(-999, np.nan, inplace=True)
            df.fillna(method='ffill', inplace=True)
            df = df.tail(LOOK_BACK_DAYS)

            df['latitude'] = lat
            df['longitude'] = lon
            input_sequence = df[['T2M', 'PRECTOTCORR', 'WS10M', 'RH2M', 'PS', 'latitude', 'longitude']].values
        else:
            # Uzak tarih için lokal veri setimizden ortalama alalım
            sequence_end_date = target_date - timedelta(days=1)
            sequence_start_date = sequence_end_date - timedelta(days=LOOK_BACK_DAYS - 1)

            simulated_sequence = []
            current_date_iter = sequence_start_date
            while current_date_iter <= sequence_end_date:
                month, day = current_date_iter.month, current_date_iter.day
                daily_avg = ALL_HISTORICAL_DATA[
                    (ALL_HISTORICAL_DATA['MO'] == month) & (ALL_HISTORICAL_DATA['DY'] == day)].mean(numeric_only=True)
                simulated_sequence.append(daily_avg[['T2M', 'PRECTOTCORR', 'WS10M', 'RH2M', 'PS']])
                current_date_iter += timedelta(days=1)

            df_simulated = pd.DataFrame(simulated_sequence)
            df_simulated['latitude'] = lat
            df_simulated['longitude'] = lon
            input_sequence = df_simulated.values

        scaled_sequence = SCALER.transform(input_sequence)
        prediction_scaled = MODEL.predict(np.array([scaled_sequence]))[0]

        # Geri ölçekleme için dummy array
        dummy_array = np.zeros((1, NUM_FEATURES))
        dummy_array[0, 0:3] = prediction_scaled  # İlk 3 sütun tahmin edildi
        dummy_array[0, 3:] = scaled_sequence[-1, 3:]  # Kalanları son günden al
        prediction_actual = SCALER.inverse_transform(dummy_array)[0]

        # Sonuçları formatla
        temp, precip, wind = prediction_actual[0], prediction_actual[1], prediction_actual[2]

        # Güven aralığı için o günün tarihsel standart sapmasını alalım
        target_month, target_day = target_date.month, target_date.day
        historical_day_data = ALL_HISTORICAL_DATA[
            (ALL_HISTORICAL_DATA['city'] == city_name) & (ALL_HISTORICAL_DATA['MO'] == target_month) & (
                        ALL_HISTORICAL_DATA['DY'] == target_day)]
        temp_std_dev = historical_day_data['T2M'].std()

        icon = '☀️'
        if precip > 0.5: icon = '🌧️'
        if temp < 5:
            icon = '❄️'
        elif temp > 28:
            icon = '🥵'

        result = {
            "city": city_name, "date": target_date.strftime('%d %B %Y'),
            "avg_temp": round(float(temp), 1),
            "precipitation": round(float(precip), 2),
            "wind_speed": round(float(wind), 2),
            "confidence": round(float(temp_std_dev), 1) if pd.notna(temp_std_dev) else 2.5,
            "icon": icon
        }
        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Sunucuda bir hata oluştu: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)