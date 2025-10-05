<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hava Durumu Tahmini - Abraouter</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    
    <?php
        include "header.php";
    ?>


    <main class="main">
        <section class="weather-hero">
            <div class="container">
                <div class="weather-content">
                    <h1 class="weather-title">Hava Durumu Tahmini</h1>
                    <p class="weather-subtitle">Şehir ve tarih seçerek gelecekteki hava durumunu öğrenin</p>
                </div>
            </div>
        </section>

        <section class="weather-search-section">
            <div class="container">
                <div class="weather-search-card">
                    <h2>Hava Durumu Sorgula</h2>
                    <form id="weatherForm" class="weather-form">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="cityInput">Şehir</label>
                                <div class="autocomplete-container">
                                    <input type="text" id="cityInput" name="city" placeholder="Şehir adı yazın..." required>
                                    <div class="autocomplete-suggestions" id="citySuggestions"></div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="weatherDate">Tarih</label>
                                <input type="date" id="weatherDate" name="date" required>
                            </div>
                        </div>
                        <button type="submit" class="weather-search-btn">
                            <i class="fas fa-search"></i>
                            Hava Durumunu Sorgula
                        </button>
                    </form>
                </div>
            </div>
        </section>

        <section class="weather-results-section" id="weatherResultsSection" style="display: none;">
            <div class="container">
                <div class="weather-card" id="weatherCard">
                    <!-- Hava durumu kartı buraya gelecek -->
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Abraouter. Tüm hakları saklıdır.</p>
        </div>
    </footer>

    <script src="weather.js"></script>
</body>
</html>
