<?php
// SkillFishOS contact form handler.
// The recipient address lives ONLY here (server-side) — it is never exposed in
// the public HTML/JS, to avoid email harvesting / spam.
session_start();

const RECIPIENT = 'info@skillfishos.com';
const FROM      = 'SkillFishOS <noreply@skillfishos.com>';

// --- resolve a safe local return path (prevents open redirects) ---
$ret = $_POST['ret'] ?? '/contact';
if (!preg_match('#^/[A-Za-z0-9/_-]*$#', $ret)) {
    $ret = '/contact';
}
function back(string $query): void {
    global $ret;
    header('Location: ' . $ret . '?' . $query);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    back('error=generic');
}

// --- honeypot: real users never fill this hidden field ---
if (!empty($_POST['company'])) {
    back('sent=1'); // silently pretend success to the bot
}

// --- captcha (validated against the session answer set by captcha.php) ---
$captcha = trim($_POST['captcha'] ?? '');
if (!isset($_SESSION['captcha_answer']) || $captcha === ''
    || (string) $_SESSION['captcha_answer'] !== $captcha) {
    back('error=captcha');
}
unset($_SESSION['captcha_answer']); // one-shot

// --- fields ---
$name    = trim($_POST['name'] ?? '');
$email   = trim($_POST['email'] ?? '');
$type    = $_POST['type'] ?? 'info';
$message = trim($_POST['message'] ?? '');

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    back('error=fields');
}

// length caps
$name    = mb_substr($name, 0, 80);
$message = mb_substr($message, 0, 4000);

$types  = ['support' => 'Assistenza', 'info' => 'Informazioni', 'other' => 'Altro'];
$tlabel = $types[$type] ?? 'Richiesta';

// strip CR/LF from header-bound values (email header injection protection)
$safeName  = str_replace(["\r", "\n"], ' ', $name);
$safeEmail = str_replace(["\r", "\n"], '', $email);

$subject = "[SkillFishOS] $tlabel - $safeName";
$body  = "Tipo richiesta: $tlabel\n";
$body .= "Nome: $safeName\n";
$body .= "Email: $safeEmail\n";
$body .= "Lingua pagina: " . ($_POST['lang'] ?? '?') . "\n";
$body .= "----------------------------------------\n\n";
$body .= $message . "\n";

$headers  = 'From: ' . FROM . "\r\n";
$headers .= 'Reply-To: ' . $safeName . ' <' . $safeEmail . ">\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "MIME-Version: 1.0\r\n";

$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$ok = @mail(RECIPIENT, $encodedSubject, $body, $headers);

back($ok ? 'sent=1' : 'error=send');
