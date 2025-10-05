<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);

if (!$input || !isset($input['country']) || !isset($input['activities']) || !isset($input['startDate']) || !isset($input['endDate'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required parameters']);
    exit;
}

$country = $input['country'];
$activities = $input['activities'];
$startDate = $input['startDate'];
$endDate = $input['endDate'];

// Etkinlik-şehir eşleştirmeleri
$activityCities = [
    'winter-sports' => ['Erzurum', 'Maraş', 'Bolu', 'Kars', 'Ağrı'],
    'beach-sea' => ['Antalya', 'Muğla', 'Çanakkale', 'İzmir', 'Mersin'],
    'water-sports' => ['Van', 'Sakarya', 'Muğla', 'Bodrum', 'Antalya'],
    'camping' => ['Sakarya', 'Bolu', 'Antalya', 'Erzincan'],
    'photography' => ['Kapadokya', 'Eskişehir', 'Ağrı', 'İstanbul'],
    'paragliding' => ['Sakarya', 'Maraş', 'Ordu', 'Bursa', 'Antalya']
];

// Seçilen etkinliklere göre şehirleri bul
$selectedCities = [];
foreach ($activities as $activity) {
    if (isset($activityCities[$activity])) {
        if (empty($selectedCities)) {
            $selectedCities = $activityCities[$activity];
        } else {
            $selectedCities = array_intersect($selectedCities, $activityCities[$activity]);
        }
    }
}

// Eğer hiç kesişen şehir yoksa, tüm etkinliklerin şehirlerini birleştir
if (empty($selectedCities)) {
    foreach ($activities as $activity) {
        if (isset($activityCities[$activity])) {
            $selectedCities = array_merge($selectedCities, $activityCities[$activity]);
        }
    }
    $selectedCities = array_unique($selectedCities);
}

// Mock veri oluştur
$results = [];
$weatherConditions = ['Güneşli', 'Bulutlu', 'Parçalı Bulutlu', 'Yağmurlu', 'Karlı', 'Sisli'];
$specificLocations = [
    'Erzurum' => ['Palandöken Kayak Merkezi', 'Tortum Şelalesi', 'Çifte Minareli Medrese'],
    'Maraş' => ['Ahır Dağı Kayak Merkezi', 'Maraş Kalesi', 'Döngel Mağaraları'],
    'Bolu' => ['Kartalkaya Kayak Merkezi', 'Abant Gölü', 'Yedigöller Milli Parkı'],
    'Kars' => ['Sarıkamış Kayak Merkezi', 'Ani Harabeleri', 'Çıldır Gölü'],
    'Ağrı' => ['Ağrı Dağı', 'İshak Paşa Sarayı', 'Doğubayazıt'],
    'Antalya' => ['Konyaaltı Plajı', 'Lara Plajı', 'Kaş', 'Side'],
    'Muğla' => ['Bodrum', 'Marmaris', 'Fethiye', 'Çeşme'],
    'Çanakkale' => ['Gelibolu Yarımadası', 'Truva Antik Kenti', 'Assos'],
    'İzmir' => ['Çeşme', 'Kuşadası', 'Foça', 'Alaçatı'],
    'Mersin' => ['Silifke', 'Anamur', 'Tarsus', 'Mersin Marina'],
    'Van' => ['Van Gölü', 'Akdamar Adası', 'Hoşap Kalesi'],
    'Sakarya' => ['Sapanca Gölü', 'Kartepe', 'Sakarya Nehri'],
    'Bodrum' => ['Bodrum Kalesi', 'Bodrum Marina', 'Gümüşlük'],
    'Erzincan' => ['Erzincan Ovası', 'Kemah Kalesi', 'Refahiye'],
    'Kapadokya' => ['Göreme', 'Ürgüp', 'Avanos', 'Derinkuyu'],
    'Eskişehir' => ['Odunpazarı', 'Sazova Parkı', 'Porsuk Çayı'],
    'İstanbul' => ['Sultanahmet', 'Galata Kulesi', 'Boğaz', 'Adalar'],
    'Ordu' => ['Ordu Teleferik', 'Boztepe', 'Çambaşı Yaylası'],
    'Bursa' => ['Uludağ', 'Bursa Kalesi', 'Cumalıkızık']
];

foreach ($selectedCities as $city) {
    $specificLocation = $specificLocations[$city][array_rand($specificLocations[$city])];
    $weatherCondition = $weatherConditions[array_rand($weatherConditions)];
    
    // Tarihe göre sıcaklık hesapla (basit mock)
    $startMonth = (int)date('n', strtotime($startDate));
    $baseTemp = 20; // Ortalama sıcaklık
    
    // Mevsimsel değişiklikler
    if (in_array($startMonth, [12, 1, 2])) {
        $baseTemp = 5; // Kış
    } elseif (in_array($startMonth, [3, 4, 5])) {
        $baseTemp = 15; // İlkbahar
    } elseif (in_array($startMonth, [6, 7, 8])) {
        $baseTemp = 25; // Yaz
    } else {
        $baseTemp = 18; // Sonbahar
    }
    
    // Şehre göre sıcaklık ayarlaması
    $cityTempAdjustments = [
        'Erzurum' => -10, 'Maraş' => -5, 'Bolu' => -3, 'Kars' => -8, 'Ağrı' => -6,
        'Antalya' => 5, 'Muğla' => 3, 'Çanakkale' => 0, 'İzmir' => 2, 'Mersin' => 4,
        'Van' => -2, 'Sakarya' => 0, 'Bodrum' => 3, 'Erzincan' => -4,
        'Kapadokya' => -1, 'Eskişehir' => 0, 'İstanbul' => 1, 'Ordu' => 0, 'Bursa' => 0
    ];
    
    $temperature = $baseTemp + ($cityTempAdjustments[$city] ?? 0) + rand(-5, 5);
    
    $results[] = [
        'id' => uniqid(),
        'city' => $city,
        'specificLocation' => $specificLocation,
        'temperature' => $temperature,
        'weatherCondition' => $weatherCondition,
        'humidity' => rand(30, 90),
        'windSpeed' => rand(5, 25),
        'visibility' => rand(5, 15),
        'precipitation' => rand(0, 80),
        'seaTemperature' => in_array($city, ['Antalya', 'Muğla', 'Çanakkale', 'İzmir', 'Mersin', 'Bodrum']) ? rand(15, 25) : null,
        'airQuality' => ['İyi', 'Orta', 'Kötü'][rand(0, 2)],
        'sunrise' => sprintf('%02d:%02d', rand(5, 7), rand(0, 59)),
        'sunset' => sprintf('%02d:%02d', rand(17, 19), rand(0, 59)),
        'rating' => rand(3, 5)
    ];
}

// Sonuçları karıştır
shuffle($results);

echo json_encode($results);
?>
