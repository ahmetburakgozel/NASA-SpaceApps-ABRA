// Ana sayfa JavaScript dosyası
document.addEventListener('DOMContentLoaded', function() {
    // Tema değiştirme
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Tema durumunu kontrol et
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
    
    // Etkinlik ekleme/çıkarma
    const addActivityBtn = document.getElementById('addActivity');
    const activitiesContainer = document.querySelector('.activities-container');
    
    addActivityBtn.addEventListener('click', function() {
        addActivityInput();
    });
    
    function addActivityInput() {
        const activityGroup = document.createElement('div');
        activityGroup.className = 'activity-input-group';
        activityGroup.innerHTML = `
            <select class="activity-select" name="activities[]" required>
                <option value="">Etkinlik Seçin</option>
                <option value="winter-sports">Kış Sporları</option>
                <option value="beach-sea">Plaj ve Deniz</option>
                <option value="water-sports">Su Sporları</option>
                <option value="camping">Kamp</option>
                <option value="photography">Fotoğrafçılık</option>
                <option value="paragliding">Yamaç Paraşütü</option>
            </select>
            <button type="button" class="remove-activity-btn" onclick="removeActivity(this)">
                <i class="fas fa-times"></i>
            </button>
        `;
        activitiesContainer.appendChild(activityGroup);
    }
    
    // Global fonksiyon olarak tanımla
    window.removeActivity = function(button) {
        button.parentElement.remove();
    };
    
    // Form gönderimi
    const searchForm = document.getElementById('searchForm');
    const resultsSection = document.getElementById('resultsSection');
    const resultsGrid = document.getElementById('resultsGrid');
    
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(searchForm);
        const activities = Array.from(document.querySelectorAll('select[name="activities[]"]'))
            .map(select => select.value)
            .filter(value => value !== '');
        
        if (activities.length === 0) {
            alert('Lütfen en az bir etkinlik seçin.');
            return;
        }
        
        // Loading animasyonu
        const submitBtn = searchForm.querySelector('.search-btn');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Aranıyor...';
        submitBtn.disabled = true;
        
        // Backend'e istek gönder
        fetch('api/search.php', {
            method: 'POST',
            body: JSON.stringify({
                country: formData.get('country'),
                startDate: formData.get('startDate'),
                endDate: formData.get('endDate'),
                activities: activities
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
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
    
    function displayResults(data) {
        resultsGrid.innerHTML = '';
        
        if (data.length === 0) {
            resultsGrid.innerHTML = '<p style="text-align: center; color: var(--text-muted); grid-column: 1 / -1;">Seçilen kriterlere uygun şehir bulunamadı.</p>';
            return;
        }
        
        data.forEach(location => {
            const card = createLocationCard(location);
            resultsGrid.appendChild(card);
        });
    }
    
    function createLocationCard(location) {
        const card = document.createElement('div');
        card.className = 'location-card';
        
        const weatherIcon = getWeatherIcon(location.weatherCondition);
        const ratingStars = generateRatingStars(location.rating);
        
        card.innerHTML = `
            <div class="location-header">
                <div>
                    <h3 class="location-name">${location.city}</h3>
                    <p class="location-specific">${location.specificLocation}</p>
                </div>
                <div class="rating">
                    ${ratingStars}
                </div>
            </div>
            
            <div class="weather-condition">
                <i class="${weatherIcon}"></i>
                <p>${location.weatherCondition}</p>
            </div>
            
            <div class="temperature">${location.temperature}°C</div>
            
            <div class="weather-info">
                <div class="weather-item">
                    <i class="fas fa-tint"></i>
                    <span>Nem: <span class="value">${location.humidity}%</span></span>
                </div>
                <div class="weather-item">
                    <i class="fas fa-wind"></i>
                    <span>Rüzgar: <span class="value">${location.windSpeed} km/h</span></span>
                </div>
                <div class="weather-item">
                    <i class="fas fa-eye"></i>
                    <span>Görüş: <span class="value">${location.visibility} km</span></span>
                </div>
                <div class="weather-item">
                    <i class="fas fa-cloud-rain"></i>
                    <span>Yağış: <span class="value">${location.precipitation}%</span></span>
                </div>
                ${location.seaTemperature ? `
                <div class="weather-item">
                    <i class="fas fa-thermometer-half"></i>
                    <span>Deniz: <span class="value">${location.seaTemperature}°C</span></span>
                </div>
                ` : ''}
                <div class="weather-item">
                    <i class="fas fa-sun"></i>
                    <span>Gün Doğumu: <span class="value">${location.sunrise}</span></span>
                </div>
                <div class="weather-item">
                    <i class="fas fa-moon"></i>
                    <span>Gün Batımı: <span class="value">${location.sunset}</span></span>
                </div>
                <div class="weather-item">
                    <i class="fas fa-smog"></i>
                    <span>Hava Kalitesi: <span class="value">${location.airQuality}</span></span>
                </div>
            </div>
            
            <div class="location-actions">
                <button class="btn btn-primary" onclick="openLocationModal('${location.id}')">
                    <i class="fas fa-comments"></i>
                    Yorumlar
                </button>
                <a href="location-detail.html?id=${location.id}" class="btn btn-secondary" target="_blank">
                    <i class="fas fa-external-link-alt"></i>
                    Detaylar
                </a>
            </div>
        `;
        
        return card;
    }
    
    function getWeatherIcon(condition) {
        const icons = {
            'Güneşli': 'fas fa-sun',
            'Bulutlu': 'fas fa-cloud',
            'Yağmurlu': 'fas fa-cloud-rain',
            'Karlı': 'fas fa-snowflake',
            'Sisli': 'fas fa-smog',
            'Fırtınalı': 'fas fa-bolt'
        };
        return icons[condition] || 'fas fa-cloud-sun';
    }
    
    function generateRatingStars(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            stars += `<i class="fas fa-star star ${i <= rating ? '' : 'empty'}"></i>`;
        }
        return stars;
    }
    
    // Modal işlevleri
    window.openLocationModal = function(locationId) {
        const modal = document.getElementById('locationModal');
        const modalContent = document.getElementById('modalContent');
        
        // Yorumları yükle
        fetch(`api/comments.php?id=${locationId}`)
            .then(response => response.json())
            .then(comments => {
                modalContent.innerHTML = `
                    <h3>Yorumlar</h3>
                    <div class="comments-container">
                        ${comments.map(comment => `
                            <div class="comment">
                                <div class="comment-header">
                                    <strong>${comment.author}</strong>
                                    <span class="comment-date">${comment.date}</span>
                                </div>
                                <p>${comment.text}</p>
                                <div class="comment-rating">
                                    ${generateRatingStars(comment.rating)}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
                modal.style.display = 'block';
            })
            .catch(error => {
                console.error('Error loading comments:', error);
                modalContent.innerHTML = '<p>Yorumlar yüklenirken bir hata oluştu.</p>';
                modal.style.display = 'block';
            });
    };
    
    // Modal kapatma
    const modal = document.getElementById('locationModal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Tarih validasyonu
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    
    startDateInput.addEventListener('change', function() {
        const startDate = new Date(this.value);
        const minEndDate = new Date(startDate);
        minEndDate.setDate(minEndDate.getDate() + 1);
        endDateInput.min = minEndDate.toISOString().split('T')[0];
    });
    
    endDateInput.addEventListener('change', function() {
        const endDate = new Date(this.value);
        const maxStartDate = new Date(endDate);
        maxStartDate.setDate(maxStartDate.getDate() - 1);
        startDateInput.max = maxStartDate.toISOString().split('T')[0];
    });
    
    // Bugünün tarihini minimum tarih olarak ayarla
    const today = new Date().toISOString().split('T')[0];
    startDateInput.min = today;
    endDateInput.min = today;
});
