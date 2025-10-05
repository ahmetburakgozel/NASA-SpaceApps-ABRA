⚙️ Model Oluşturma Süreci

Bu klasör, ABRA Weather projesinin kalbi olan yapay zeka modelini oluşturmak için gerekli olan Python script'lerini içerir. Buradaki süreç iki ana adımdan oluşur:

    Veri Toplama: Türkiye'deki 81 ilin tamamı için 40 yılı aşkın (1981-2024) geçmiş hava durumu verilerinin NASA POWER API'sinden çekilmesi.

    Model Eğitimi: Toplanan bu dev veri seti kullanılarak, geleceğe yönelik öngörülerde bulunacak olan LSTM (Long Short-Term Memory) modelinin eğitilmesi.

Bu klasördeki script'ler, projenin ana dizininde bulunan app.py web uygulamasının ihtiyaç duyduğu weather_model.h5 ve weather_scaler.gz dosyalarını üretir.

📁 Dosyalar

    create_dataset.py: 81 ilin koordinatlarını kullanarak NASA POWER API'sine bağlanır. Her il için belirtilen tarih aralığındaki tüm günlük hava durumu verilerini çeker. Son olarak, tüm bu verileri birleştirir, temizler ve turkey_weather_dataset.csv adında tek bir büyük CSV dosyasına kaydeder.

    train_model.py: create_dataset.py tarafından oluşturulan turkey_weather_dataset.csv dosyasını okur. Veriyi, LSTM modelinin anlayacağı sıralı diziler (sequences) haline getirir. Modeli bu veriyle eğitir ve eğitimin sonunda, projenin ana uygulamasında kullanılacak olan weather_model.h5 (eğitilmiş model) ve weather_scaler.gz (veri ölçekleyici) dosyalarını oluşturur.

🚀 Kullanım

Bu model oluşturma sürecini kendi makinenizde çalıştırmak için aşağıdaki adımları sırasıyla izleyin.

1. Gereksinimler

Öncelikle, gerekli Python kütüphanelerinin yüklü olduğundan emin olun. Terminalde aşağıdaki komutu çalıştırabilirsiniz:
Bash

pip install tensorflow pandas numpy requests scikit-learn joblib

2. Adım: Veri Setini Oluşturma

Terminalde, projenin ana klasöründeyken create_dataset.py script'ini çalıştırın.
Bash

python3 create_dataset.py

⚠️ Uyarı: Bu script, 81 il için 40 yılı aşkın veriyi NASA sunucularından indirdiği için çalışması oldukça uzun sürecektir (İnternet hızınıza bağlı olarak 15-30 dakika veya daha fazla). Lütfen sabırla işlemin tamamlanmasını ve turkey_weather_dataset.csv dosyasının oluşmasını bekleyin.

3. Adım: Modeli Eğitme

Veri seti oluşturulduktan sonra, train_model.py script'ini çalıştırarak modeli eğitin.
Bash

python3 train_model.py

⚠️ Uyarı: Bu script de büyük veri seti üzerinde çalıştığı ve bir derin öğrenme modeli eğittiği için tamamlanması zaman alacaktır (Bilgisayarınızın işlemci gücüne bağlı olarak 5-15 dakika veya daha fazla).

İşlem bittiğinde, projenin ana klasöründe weather_model.h5 ve weather_scaler.gz dosyaları oluşmuş olacaktır. Artık projenin ana app.py uygulamasını çalıştırmaya hazırsınız.
