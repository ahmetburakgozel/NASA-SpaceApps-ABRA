import sqlite3

# Veritabanı bağlantısını kur (dosya yoksa oluşturur)
connection = sqlite3.connect('turizm.db')
cursor = connection.cursor()

# --- Tabloları Oluşturma ---
# Etkinlikler Tablosu (Dağ Tırmanışı, Plaj Keyfi vb.)
cursor.execute('''
               CREATE TABLE IF NOT EXISTS activities
               (
                   id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   name
                   TEXT
                   NOT
                   NULL
                   UNIQUE
               )
               ''')

# Lokasyonlar Tablosu (Ağrı Dağı, Kaputaş Plajı vb.)
cursor.execute('''
               CREATE TABLE IF NOT EXISTS locations
               (
                   id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   name
                   TEXT
                   NOT
                   NULL,
                   city
                   TEXT
                   NOT
                   NULL,
                   activity_id
                   INTEGER,
                   description
                   TEXT,
                   FOREIGN
                   KEY
               (
                   activity_id
               ) REFERENCES activities
               (
                   id
               )
                   )
               ''')

# Yorumlar Tablosu
cursor.execute('''
               CREATE TABLE IF NOT EXISTS comments
               (
                   id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   location_id
                   INTEGER,
                   username
                   TEXT
                   NOT
                   NULL,
                   comment_text
                   TEXT
                   NOT
                   NULL,
                   rating
                   INTEGER,
                   created_at
                   TIMESTAMP
                   DEFAULT
                   CURRENT_TIMESTAMP,
                   FOREIGN
                   KEY
               (
                   location_id
               ) REFERENCES locations
               (
                   id
               )
                   )
               ''')

# --- Örnek Verileri Ekleme ---
try:
    # Örnek Etkinlikler
    cursor.execute("INSERT INTO activities (name) VALUES ('Dağ Tırmanışı')")
    cursor.execute("INSERT INTO activities (name) VALUES ('Plaj Keyfi')")
    cursor.execute("INSERT INTO activities (name) VALUES ('Tarihi Gezi')")

    # Örnek Lokasyonlar
    cursor.execute("INSERT INTO locations (name, city, activity_id, description) VALUES (?, ?, ?, ?)",
                   ('Ağrı Dağı', 'Ağrı', 1, 'Türkiye''nin en yüksek dağı, profesyonel tırmanış için ideal.'))
    cursor.execute("INSERT INTO locations (name, city, activity_id, description) VALUES (?, ?, ?, ?)",
                   ('Kaçkar Dağları', 'Rize', 1, 'Yeşillikler içinde zorlu ve keyifli tırmanış rotaları sunar.'))
    cursor.execute("INSERT INTO locations (name, city, activity_id, description) VALUES (?, ?, ?, ?)",
                   ('Kaputaş Plajı', 'Antalya', 2, 'Turkuaz suları ve etkileyici manzarasıyla ünlüdür.'))
    cursor.execute("INSERT INTO locations (name, city, activity_id, description) VALUES (?, ?, ?, ?)",
                   ('Efes Antik Kenti', 'İzmir', 3,
                    'Tarihin en büyük medeniyetlerinden birine ev sahipliği yapmış antik bir harika.'))

    # Örnek Yorum
    cursor.execute("INSERT INTO comments (location_id, username, comment_text, rating) VALUES (?, ?, ?, ?)",
                   (1, 'Dağcı_Ali', 'Zirveye tırmanış harikaydı, ama hava çok değişkendi. Mutlaka hazırlıklı gidin!',
                    5))

except sqlite3.IntegrityError:
    print("Örnek veriler zaten eklenmiş.")

# Değişiklikleri kaydet ve bağlantıyı kapat
connection.commit()
connection.close()

print("Veritabanı 'turizm.db' başarıyla oluşturuldu ve örnek veriler eklendi.")