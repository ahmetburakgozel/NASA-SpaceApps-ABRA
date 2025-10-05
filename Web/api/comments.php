<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$locationId = $_GET['id'] ?? '';

if (empty($locationId)) {
    http_response_code(400);
    echo json_encode(['error' => 'Location ID is required']);
    exit;
}

// Mock yorum verisi
$comments = [
    [
        'author' => 'Ahmet Y.',
        'date' => '15.12.2024',
        'rating' => 5,
        'text' => 'Harika bir yer! Hava durumu mükemmeldi ve etkinlikler çok eğlenceliydi. Kesinlikle tekrar gelmek istiyorum.'
    ],
    [
        'author' => 'Fatma K.',
        'date' => '12.12.2024',
        'rating' => 4,
        'text' => 'Güzel bir deneyimdi. Sadece biraz kalabalıktı ama genel olarak memnun kaldım. Özellikle manzara muhteşemdi.'
    ],
    [
        'author' => 'Mehmet S.',
        'date' => '10.12.2024',
        'rating' => 5,
        'text' => 'Ailemle birlikte geldik ve çok eğlendik. Çocuklarım da çok mutlu oldu. Hava durumu da güzeldi.'
    ],
    [
        'author' => 'Ayşe M.',
        'date' => '08.12.2024',
        'rating' => 3,
        'text' => 'Orta düzeyde bir deneyim. Hava biraz soğuktu ama yine de güzel vakit geçirdik. Fiyatlar biraz yüksekti.'
    ],
    [
        'author' => 'Can T.',
        'date' => '05.12.2024',
        'rating' => 4,
        'text' => 'Güzel bir yer ama biraz daha organize olabilirdi. Yine de tavsiye ederim. Hava durumu da uygundu.'
    ],
    [
        'author' => 'Zeynep A.',
        'date' => '03.12.2024',
        'rating' => 5,
        'text' => 'Mükemmel bir tatil geçirdik! Hava durumu harikaydı ve etkinlikler çok çeşitliydi. Kesinlikle tekrar geleceğiz.'
    ],
    [
        'author' => 'Emre D.',
        'date' => '01.12.2024',
        'rating' => 4,
        'text' => 'Güzel bir deneyimdi. Sadece ulaşım biraz zordu ama değdi. Hava durumu da güzeldi.'
    ],
    [
        'author' => 'Selin R.',
        'date' => '28.11.2024',
        'rating' => 5,
        'text' => 'Harika bir yer! Doğa çok güzel ve hava durumu mükemmeldi. Etkinlikler de çok eğlenceliydi.'
    ]
];

// Rastgele yorumları seç (3-6 arası)
$randomCount = rand(3, 6);
$selectedComments = array_slice($comments, 0, $randomCount);

echo json_encode($selectedComments);
?>
