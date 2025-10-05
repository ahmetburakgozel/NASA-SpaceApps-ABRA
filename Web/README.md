# Abraouter - Tatil Planlama Uygulaması

Modern bir hava durumu uygulaması ve tatil planlama sistemi. Kullanıcılar etkinliklerine uygun ideal şehirleri bulabilir ve hava durumu tahminlerini görüntüleyebilir.

## Özellikler

### Ana Sayfa
- **Tatil Planlama Formu**: Ülke, tarih aralığı ve etkinlik seçimi
- **Dinamik Etkinlik Ekleme**: Kullanıcılar birden fazla etkinlik ekleyebilir
- **Akıllı Şehir Önerileri**: Seçilen etkinliklere göre kesişen şehirleri bulur
- **Detaylı Hava Durumu Kartları**: Her şehir için kapsamlı hava durumu bilgileri

### Hava Durumu Sayfası
- **Şehir Arama**: Autocomplete özellikli şehir seçimi
- **Tarih Seçimi**: 7 güne kadar hava durumu tahmini
- **Detaylı Hava Durumu**: Sıcaklık, nem, rüzgar, görüş mesafesi vb.
- **Günlük Tahmin**: 5 günlük hava durumu öngörüsü

### Lokasyon Detay Sayfası
- **Otel Rezervasyonları**: Fiyat ve değerlendirme bilgileri
- **Ulaşım Seçenekleri**: Hava yolu, otobüs, tren, araç kiralama
- **Konum Bilgileri**: Detaylı lokasyon ve hava durumu verileri
- **Ek Bilgiler**: En iyi ziyaret zamanı, popüler etkinlikler

## Teknolojiler

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: PHP 7.4+
- **Stil**: Modern CSS Grid/Flexbox, CSS Variables
- **İkonlar**: Font Awesome 6
- **Fontlar**: Google Fonts (Poppins)

## Kurulum

1. Projeyi web sunucunuza kopyalayın
2. PHP 7.4+ sürümünün yüklü olduğundan emin olun
3. Web sunucusunu başlatın
4. `index.html` dosyasını tarayıcıda açın

## Kullanım

### Ana Sayfa
1. Ülke seçin
2. Başlangıç ve bitiş tarihlerini belirleyin
3. Etkinlik(ler) seçin (birden fazla ekleyebilirsiniz)
4. "İdeal Şehirleri Bul" butonuna tıklayın
5. Sonuçları inceleyin ve detayları görüntüleyin

### Hava Durumu
1. Şehir adını yazmaya başlayın (autocomplete devreye girer)
2. Tarih seçin (bugünden 7 gün sonrasına kadar)
3. "Hava Durumunu Sorgula" butonuna tıklayın
4. Detaylı hava durumu bilgilerini görüntüleyin

## Etkinlik-Şehir Eşleştirmeleri

- **Kış Sporları**: Erzurum, Maraş, Bolu, Kars, Ağrı
- **Plaj ve Deniz**: Antalya, Muğla, Çanakkale, İzmir, Mersin
- **Su Sporları**: Van, Sakarya, Muğla, Bodrum, Antalya
- **Kamp**: Sakarya, Bolu, Antalya, Erzincan
- **Fotoğrafçılık**: Kapadokya, Eskişehir, Ağrı, İstanbul
- **Yamaç Paraşütü**: Sakarya, Maraş, Ordu, Bursa, Antalya

## Tema Desteği

- **Açık Tema**: Varsayılan modern tasarım
- **Karanlık Tema**: Göz yormayan koyu renk paleti
- Tema tercihi tarayıcıda saklanır

## Responsive Tasarım

- Masaüstü, tablet ve mobil cihazlarda optimize edilmiş
- Modern CSS Grid ve Flexbox kullanımı
- Touch-friendly arayüz elemanları

## API Endpoints

- `POST /api/search.php`: Tatil planlama araması
- `POST /api/weather.php`: Hava durumu sorgulama
- `GET /api/comments.php`: Lokasyon yorumları

## Mock Veri

Uygulama şu anda mock veri kullanmaktadır. Gerçek API entegrasyonu için:
- Hava durumu API'si (OpenWeatherMap, AccuWeather vb.)
- Otel rezervasyon API'si
- Ulaşım API'si

## Geliştirme Notları

- Tüm veriler dinamik olarak oluşturulur
- Responsive tasarım tüm cihazlarda test edilmiştir
- Modern web standartlarına uygun kod yapısı
- Performans optimizasyonları uygulanmıştır

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
