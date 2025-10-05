<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Abraouter - Tatil Planlama Uygulaması</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <?php
	include "header.php";
    ?>

    <main class="main">
        <section class="hero">
            <div class="container">
                <div class="hero-content">
                    <h1 class="hero-title">Hayalinizdeki Tatili Planlayın</h1>
                    <p class="hero-subtitle">Etkinliklerinize uygun ideal şehri bulun ve hava durumuna göre plan yapın</p>
                </div>
            </div>
        </section>

        <section class="search-section">
            <div class="container">
                <div class="search-card">
                    <h2>Tatil Planınızı Oluşturun</h2>
                    <form id="searchForm" class="search-form">
                        <div class="form-group">
                            <label for="country">Ülke</label>
                            <select id="country" name="country" required>
                                <option value="turkey">Ülke Seçin</option>
                                <option value="turkey" selected>Türkiye</option>
                            </select>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label for="startDate">Başlangıç Tarihi</label>
                                <input type="date" id="startDate" name="startDate" value="2026-06-10" required>
                            </div>
                            <div class="form-group">
                                <label for="endDate">Bitiş Tarihi</label>
                                <input type="date" id="endDate" name="endDate" value="2026-06-15" required>
                            </div>
                        </div>

                        <div class="form-group">
                            <label>Etkinlikler</label>
                            <div class="activities-container">
                                <div class="activity-input-group">
                                    <select class="activity-select" name="activities[]" required>
                                        <option value="">Etkinlik Seçin</option>
                                        <option value="winter-sports">Kış Sporları</option>
                                        <option value="beach-sea">Plaj ve Deniz</option>
                                        <option value="water-sports">Su Sporları</option>
                                        <option value="camping">Kamp</option>
                                        <option value="photography">Fotoğrafçılık</option>
                                        <option value="paragliding">Yamaç Paraşütü</option>
                                    </select>
                                    <button type="button" class="add-activity-btn" id="addActivity">
                                        <i class="fas fa-plus"></i>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <button type="submit" class="search-btn">
                            <i class="fas fa-search"></i>
                            İdeal Şehirleri Bul
                        </button>
                    </form>
                </div>
            </div>
        </section>

        <section class="results-section" id="resultsSection" style="display: none;">
            <div class="container">
                <h2>Önerilen Şehirler</h2>
                <div class="results-grid" id="resultsGrid">
                    <!-- Sonuçlar buraya gelecek -->
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Abraouter. Tüm hakları saklıdır.</p>
        </div>
    </footer>

    <!-- Modal -->
    <div class="modal" id="locationModal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div id="modalContent">
                <!-- Modal içeriği buraya gelecek -->
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
