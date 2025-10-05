from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'turizm.db'
WEATHER_API_KEY = '96bdf2eec8f34c13bc192004250410'


def get_db_connection():
    """Veritabanı bağlantısı oluşturur."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Sonuçlara sütun isimleriyle erişim sağlar
    return conn


@app.route('/')
def index():
    """Anasayfayı yükler ve etkinlik listesini gönderir."""
    conn = get_db_connection()
    activities = conn.execute('SELECT * FROM activities').fetchall()
    conn.close()
    return render_template('index.html', activities=activities)


@app.route('/search')
def search():
    """Arama kriterlerine göre lokasyonları, hava durumunu ve yorumları bulur."""
    city = request.args.get('city')
    date_str = request.args.get('date')
    activity_id = request.args.get('activity_id')

    # 1. Hava Durumu Tahminini Al
    weather_data = None
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&dt={date_str}&aqi=no&alerts=no"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()['forecast']['forecastday'][0]['day']
            # İkonu da alalım
            weather_data['icon'] = weather_data['condition']['icon']
    except Exception as e:
        print(f"Hava durumu alınamadı: {e}")

    # 2. Veritabanından Uygun Lokasyonları Bul
    conn = get_db_connection()
    query = "SELECT * FROM locations WHERE activity_id = ? AND city = ?"
    locations = conn.execute(query, (activity_id, city)).fetchall()

    # 3. Her lokasyon için yorumları bul
    results = []
    for loc in locations:
        comments = conn.execute('SELECT * FROM comments WHERE location_id = ? ORDER BY created_at DESC',
                                (loc['id'],)).fetchall()
        results.append({
            'location': dict(loc),
            'comments': [dict(comment) for comment in comments]
        })

    conn.close()

    return render_template('results.html',
                           results=results,
                           weather=weather_data,
                           city=city,
                           date=datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %B %Y'))


# Diğer sayfalar (örneğin yorum ekleme) buraya eklenebilir.

if __name__ == '__main__':
    app.run(debug=True, port=5001)