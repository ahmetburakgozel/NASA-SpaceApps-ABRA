// Hava durumu sayfası JavaScript dosyası
document.addEventListener('DOMContentLoaded', function() {
    // Tema değiştirme (ana sayfadan kopyalandı)
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
    
    // Şehir autocomplete
    const cityInput = document.getElementById('cityInput');
    const citySuggestions = document.getElementById('citySuggestions');
    
    const cities = [
        'İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Konya', 'Gaziantep',
        'Mersin', 'Diyarbakır', 'Kayseri', 'Eskişehir', 'Urfa', 'Malatya', 'Erzurum',
        'Van', 'Batman', 'Elazığ', 'İzmit', 'Manisa', 'Sivas', 'Gebze', 'Balıkesir',
        'Kahramanmaraş', 'Denizli', 'Sakarya', 'Uşak', 'Düzce', 'Eskişehir', 'Muğla',
        'Trabzon', 'Ordu', 'Çanakkale', 'Aydın', 'Tekirdağ', 'Muş', 'Kars', 'Ağrı',
        'Bolu', 'Erzincan', 'Kapadokya', 'Bodrum', 'Marmaris', 'Fethiye', 'Çeşme',
        'Kuşadası', 'Alanya', 'Side', 'Kaş', 'Kemer', 'Belek', 'Çıralı', 'Patara'
    ];
    
    cityInput.addEventListener('input', function() {
        const value = this.value.toLowerCase();
        if (value.length < 2) {
            citySuggestions.style.display = 'none';
            return;
        }
        
        const filteredCities = cities.filter(city => 
            city.toLowerCase().includes(value)
        );
        
        if (filteredCities.length === 0) {
            citySuggestions.style.display = 'none';
            return;
        }
        
        citySuggestions.innerHTML = filteredCities.map(city => 
            `<div class="suggestion-item" onclick="selectCity('${city}')">${city}</div>`
        ).join('');
        citySuggestions.style.display = 'block';
    });
    
    // Şehir seçimi
    window.selectCity = function(city) {
        cityInput.value = city;
        citySuggestions.style.display = 'none';
    };
    
    // Dışarı tıklama ile suggestions'ı kapat
    document.addEventListener('click', function(e) {
        if (!cityInput.contains(e.target) && !citySuggestions.contains(e.target)) {
            citySuggestions.style.display = 'none';
        }
    });
    
    // Hava durumu formu
    const weatherForm = document.getElementById('weatherForm');
    const weatherResultsSection = document.getElementById('weatherResultsSection');
    const weatherCard = document.getElementById('weatherCard');
    
    weatherForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(weatherForm);
        const city = formData.get('city');
        const date = formData.get('date');
        
        if (!city || !date) {
            alert('Lütfen şehir ve tarih bilgilerini girin.');
            return;
        }
        
        // Loading animasyonu
        const submitBtn = weatherForm.querySelector('.weather-search-btn');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sorgulanıyor...';
        submitBtn.disabled = true;
        
        // Backend'e istek gönder
        fetch('api/weather.php', {
            method: 'POST',
            body: JSON.stringify({
                city: city,
                date: date
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            displayWeatherData(data);
            weatherResultsSection.style.display = 'block';
            weatherResultsSection.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Bir hata oluştu. Lütfen tekrar deneyin.');
        })
        .finally(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    });
    
    function displayWeatherData(data) {
        const weatherIcon = getWeatherIcon(data.condition);
        const windDirection = getWindDirection(data.windDirection);
        
        weatherCard.innerHTML = `
            <div class="weather-header">
                <div class="weather-location">
                    <h2>${data.city}</h2>
                    <p>${data.date}</p>
                </div>
                <div class="weather-icon">
                    <i class="${weatherIcon}"></i>
                </div>
            </div>
            
            <div class="weather-main">
                <div class="temperature-large">${data.temperature}°C</div>
                <div class="weather-condition-large">${data.condition}</div>
                <div class="weather-description">${data.description}</div>
            </div>
            
            <div class="weather-details">
                <div class="detail-grid">
                    <div class="detail-item">
                        <i class="fas fa-thermometer-half"></i>
                        <div class="detail-content">
                            <span class="detail-label">Hissedilen</span>
                            <span class="detail-value">${data.feelsLike}°C</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-tint"></i>
                        <div class="detail-content">
                            <span class="detail-label">Nem</span>
                            <span class="detail-value">${data.humidity}%</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-wind"></i>
                        <div class="detail-content">
                            <span class="detail-label">Rüzgar</span>
                            <span class="detail-value">${data.windSpeed} km/h ${windDirection}</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-eye"></i>
                        <div class="detail-content">
                            <span class="detail-label">Görüş</span>
                            <span class="detail-value">${data.visibility} km</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-cloud-rain"></i>
                        <div class="detail-content">
                            <span class="detail-label">Yağış Olasılığı</span>
                            <span class="detail-value">${data.precipitation}%</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-compress-arrows-alt"></i>
                        <div class="detail-content">
                            <span class="detail-label">Basınç</span>
                            <span class="detail-value">${data.pressure} hPa</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-sun"></i>
                        <div class="detail-content">
                            <span class="detail-label">Gün Doğumu</span>
                            <span class="detail-value">${data.sunrise}</span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <i class="fas fa-moon"></i>
                        <div class="detail-content">
                            <span class="detail-label">Gün Batımı</span>
                            <span class="detail-value">${data.sunset}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="weather-forecast">
                <h3>Günlük Tahmin</h3>
                <div class="forecast-items">
                    ${data.forecast.map(day => `
                        <div class="forecast-item">
                            <div class="forecast-day">${day.day}</div>
                            <div class="forecast-icon">
                                <i class="${getWeatherIcon(day.condition)}"></i>
                            </div>
                            <div class="forecast-temp">
                                <span class="temp-high">${day.maxTemp}°</span>
                                <span class="temp-low">${day.minTemp}°</span>
                            </div>
                            <div class="forecast-precipitation">${day.precipitation}%</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    function getWeatherIcon(condition) {
        const icons = {
            'Güneşli': 'fas fa-sun',
            'Açık': 'fas fa-sun',
            'Bulutlu': 'fas fa-cloud',
            'Parçalı Bulutlu': 'fas fa-cloud-sun',
            'Çok Bulutlu': 'fas fa-cloud',
            'Yağmurlu': 'fas fa-cloud-rain',
            'Hafif Yağmur': 'fas fa-cloud-drizzle',
            'Şiddetli Yağmur': 'fas fa-cloud-rain',
            'Karlı': 'fas fa-snowflake',
            'Hafif Kar': 'fas fa-snowflake',
            'Sisli': 'fas fa-smog',
            'Fırtınalı': 'fas fa-bolt',
            'Gök Gürültülü': 'fas fa-bolt'
        };
        return icons[condition] || 'fas fa-cloud-sun';
    }
    
    function getWindDirection(degrees) {
        const directions = ['K', 'KKD', 'KD', 'DKD', 'D', 'DGD', 'GD', 'GGD', 'G', 'GGB', 'GB', 'BGB', 'B', 'BKB', 'KB', 'KKB'];
        const index = Math.round(degrees / 22.5) % 16;
        return directions[index];
    }
    
    // Tarih validasyonu
    const weatherDateInput = document.getElementById('weatherDate');
    const today = new Date().toISOString().split('T')[0];
    weatherDateInput.min = today;
    
    // Maksimum 365 gün sonrasına kadar tahmin
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + 365);
    weatherDateInput.max = maxDate.toISOString().split('T')[0];
});
