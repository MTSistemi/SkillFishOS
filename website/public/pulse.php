<?php
// SkillFishOS — visit collector. Called by a tiny beacon on every page.
// Records an anonymous, cookieless hit and returns 204 No Content.
require __DIR__ . '/_sfstats.php';

header('Content-Type: text/plain');
header('Cache-Control: no-store');
// CORS: only our own origins may post here.
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (preg_match('#^https?://([a-z0-9-]+\.)?skillfishos\.com$#i', $origin)) {
    header('Access-Control-Allow-Origin: ' . $origin);
}

$ua   = substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 300);
$path = substr((string)($_POST['p'] ?? $_GET['p'] ?? '/'), 0, 300);
$ref  = substr((string)($_POST['r'] ?? $_GET['r'] ?? ''), 0, 300);

// Keep only the path part of whatever was sent; drop query strings.
$path = parse_url($path, PHP_URL_PATH) ?: '/';
// Referrer: keep the host (for aggregation) and, for EXTERNAL referrers, the
// full URL too. Self-referrals are ignored.
$ref_host = '';
$ref_full = '';
if ($ref) {
    $h = parse_url($ref, PHP_URL_HOST) ?: '';
    $scheme = strtolower((string)(parse_url($ref, PHP_URL_SCHEME) ?: ''));
    if ($h && !preg_match('/skillfishos\.com$/i', $h)) {
        $ref_host = strtolower($h);
        if ($scheme === 'http' || $scheme === 'https') $ref_full = $ref; // already capped to 300
    }
}

list($country, $cname) = sfstats_country();

try {
    $db = sfstats_db();
    $st = $db->prepare('INSERT INTO hits(ts,day,path,ref,vis,bot,browser,os,country,cname,ref_full)
                        VALUES(:ts,:day,:path,:ref,:vis,:bot,:br,:os,:cc,:cn,:rf)');
    $st->execute(array(
        ':ts'   => time(),
        ':day'  => gmdate('Y-m-d'),
        ':path' => $path,
        ':ref'  => $ref_host,
        ':vis'  => sfstats_visitor($ua),
        ':bot'  => sfstats_is_bot($ua),
        ':br'   => sfstats_browser($ua),
        ':os'   => sfstats_os($ua),
        ':cc'   => $country,
        ':cn'   => $cname,
        ':rf'   => $ref_full,
    ));
} catch (Throwable $e) {
    // never break a page load because of analytics
}

http_response_code(204);
