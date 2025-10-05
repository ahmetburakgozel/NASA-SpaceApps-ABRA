<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    //http_response_code(405);
    echo json_encode(['error' => 'Method not, allowed']);
echo $_SERVER['REQUEST_METHOD'];
    //exit;
}

$input = json_decode(file_get_contents('php://input'), true);

if (!$input || !isset($input['city']) || !isset($input['date'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required parameters']);
    exit;
}

$city = $input['city'];
$date = $input['date'];

// Tarih kontrolü
$requestDate = new DateTime($date);
$today = new DateTime();
$diff = $requestDate->diff($today);

if ($diff->days > 365) {
    http_response_code(400);
    echo json_encode(['error' => 'Maksimum 365 gün sonrasına kadar tahmin yapılabilir']);
    exit;
}

// Mock hava durumu verisi
$weatherConditions = [
    'Güneşli', 'Açık', 'Bulutlu', 'Parçalı Bulutlu', 'Çok Bulutlu', 
    'Yağmurlu', 'Hafif Yağmur', 'Şiddetli Yağmur', 'Karlı', 'Hafif Kar', 
    'Sisli', 'Fırtınalı', 'Gök Gürültülü'
];

$descriptions = [
    'Güneşli' => 'Açık ve güneşli hava',
    'Açık' => 'Temiz ve açık gökyüzü',
    'Bulutlu' => 'Çoğunlukla bulutlu',
    'Parçalı Bulutlu' => 'Parçalı bulutlu hava',
    'Çok Bulutlu' => 'Çok bulutlu ve kapalı',
    'Yağmurlu' => 'Yağmur yağışı bekleniyor',
    'Hafif Yağmur' => 'Hafif yağmur yağışı',
    'Şiddetli Yağmur' => 'Şiddetli yağmur yağışı',
    'Karlı' => 'Kar yağışı bekleniyor',
    'Hafif Kar' => 'Hafif kar yağışı',
    'Sisli' => 'Sisli ve puslu hava',
    'Fırtınalı' => 'Fırtınalı hava koşulları',
    'Gök Gürültülü' => 'Gök gürültülü sağanak'
];

// Şehre göre temel sıcaklık ayarlaması
$cityTempBase = [
    'İstanbul' => 15, 'Ankara' => 12, 'İzmir' => 18, 'Bursa' => 16, 'Antalya' => 20,
    'Adana' => 19, 'Konya' => 13, 'Gaziantep' => 17, 'Mersin' => 19, 'Diyarbakır' => 16,
    'Kayseri' => 11, 'Eskişehir' => 14, 'Urfa' => 18, 'Malatya' => 15, 'Erzurum' => 5,
    'Van' => 8, 'Batman' => 16, 'Elazığ' => 13, 'İzmit' => 15, 'Manisa' => 17,
    'Sivas' => 10, 'Gebze' => 15, 'Balıkesir' => 16, 'Kahramanmaraş' => 17, 'Denizli' => 16,
    'Sakarya' => 15, 'Uşak' => 15, 'Düzce' => 15, 'Muğla' => 18, 'Trabzon' => 14,
    'Ordu' => 15, 'Çanakkale' => 16, 'Aydın' => 17, 'Tekirdağ' => 15, 'Muş' => 9,
    'Kars' => 4, 'Ağrı' => 6, 'Bolu' => 10, 'Erzincan' => 11, 'Kapadokya' => 12,
    'Bodrum' => 19, 'Marmaris' => 19, 'Fethiye' => 18, 'Çeşme' => 18, 'Kuşadası' => 18,
    'Alanya' => 20, 'Side' => 20, 'Kaş' => 19, 'Kemer' => 20, 'Belek' => 20
];

$baseTemp = $cityTempBase[$city] ?? 15;

// Tarihe göre sıcaklık ayarlaması
$month = (int)$requestDate->format('n');
$dayOfYear = (int)$requestDate->format('z');

// Mevsimsel değişiklikler (basit sinüs dalgası)
$seasonalAdjustment = 8 * sin(($dayOfYear / 365) * 2 * M_PI - M_PI/2);
$temperature = round($baseTemp + $seasonalAdjustment + rand(-3, 3));

// Hava durumu koşulunu seç
$condition = $weatherConditions[array_rand($weatherConditions)];

// Sıcaklığa göre hava durumunu ayarla
if ($temperature < 0) {
    $condition = in_array($condition, ['Karlı', 'Hafif Kar', 'Sisli']) ? $condition : 'Karlı';
} elseif ($temperature < 10) {
    $condition = in_array($condition, ['Bulutlu', 'Sisli', 'Hafif Yağmur']) ? $condition : 'Bulutlu';
} elseif ($temperature > 25) {
    $condition = in_array($condition, ['Güneşli', 'Açık', 'Parçalı Bulutlu']) ? $condition : 'Güneşli';
}

// Hissedilen sıcaklık (rüzgar ve nem etkisi)
$windSpeed = rand(5, 25);
$humidity = rand(30, 90);
$feelsLike = $temperature;

// Rüzgar soğutma etkisi
if ($windSpeed > 15) {
    $feelsLike -= 2;
}

// Nem etkisi
if ($humidity > 70) {
    $feelsLike += 1;
} elseif ($humidity < 40) {
    $feelsLike -= 1;
}

// Günlük tahmin oluştur
$forecast = [];
$forecastDays = ['Bugün', 'Yarın', 'Sonraki Gün', '4. Gün', '5. Gün'];
$forecastConditions = ['Güneşli', 'Bulutlu', 'Parçalı Bulutlu', 'Yağmurlu', 'Hafif Yağmur'];

for ($i = 0; $i < 5; $i++) {
    $forecastCondition = $forecastConditions[array_rand($forecastConditions)];
    $forecastTemp = $temperature + rand(-5, 5);
    
    $forecast[] = [
        'day' => $forecastDays[$i],
        'condition' => $forecastCondition,
        'maxTemp' => $forecastTemp + rand(2, 5),
        'minTemp' => $forecastTemp - rand(2, 5),
        'precipitation' => rand(0, 60)
    ];
}

// Gün doğumu ve batımı hesapla (basit mock)
$sunrise = sprintf('%02d:%02d', rand(5, 7), rand(0, 59));
$sunset = sprintf('%02d:%02d', rand(17, 19), rand(0, 59));

// Rüzgar yönü
$windDirections = ['Kuzey', 'Kuzeydoğu', 'Doğu', 'Güneydoğu', 'Güney', 'Güneybatı', 'Batı', 'Kuzeybatı'];
$windDirection = $windDirections[array_rand($windDirections)];

$result = [
    'city' => $city,
    'date' => $requestDate->format('d.m.Y'),
    'temperature' => $temperature,
    'feelsLike' => round($feelsLike),
    'condition' => $condition,
    'description' => $descriptions[$condition],
    'humidity' => $humidity,
    'windSpeed' => $windSpeed,
    'windDirection' => rand(0, 360),
    'visibility' => rand(5, 15),
    'precipitation' => rand(0, 80),
    'pressure' => rand(1000, 1030),
    'sunrise' => $sunrise,
    'sunset' => $sunset,
    'forecast' => $forecast
];

echo json_encode($result);
?>
