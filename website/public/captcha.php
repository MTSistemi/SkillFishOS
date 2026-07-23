<?php
// Serves a simple math captcha challenge. The answer is stored server-side in
// the PHP session and validated by contact.php — never exposed to the client.
session_start();
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, no-cache, must-revalidate');

$a = random_int(1, 9);
$b = random_int(1, 9);
$_SESSION['captcha_answer'] = $a + $b;

echo json_encode(['q' => "$a + $b"]);
