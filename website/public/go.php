<?php
// SkillFishOS — passaggio per i download.
//
// I file stanno su SourceForge, quindi un clic sul pulsante lascia il nostro
// sito e noi non ne sapremmo niente. Questo script registra il clic e poi
// rimanda dove deve, senza chiedere niente all'utente e senza cookie: la
// stessa privacy del resto delle statistiche.
//
// L'elenco delle destinazioni e' chiuso apposta: se il bersaglio arrivasse
// dall'indirizzo, chiunque potrebbe usare il nostro dominio per rimandare a un
// sito qualsiasi, e ci ritroveremmo a fare da trampolino a chi manda spam.
require __DIR__ . '/_sfstats.php';

$SF = 'https://sourceforge.net/projects/skillfishos/files/26.06.3-Aetherium/';

// Internet Archive: dall'Europa va circa dieci volte piu' veloce di SourceForge,
// che serve tutto da San Diego. Stesso file, stesso checksum.
$IA = 'https://archive.org/download/skillfishos-26.06.3-aetherium/';

$DEST = array(
    'ia-bc250'   => $IA . 'SkillFishOS-26.06.3-Aetherium-BC250-amd64.iso',
    'ia-generic' => $IA . 'SkillFishOS-26.06.3-Aetherium-Generic-amd64.iso',
    'bc250'      => $SF . 'SkillFishOS-26.06.3-Aetherium-BC250-amd64.iso/download',
    'generic'    => $SF . 'SkillFishOS-26.06.3-Aetherium-Generic-amd64.iso/download',
    'sha-bc250'  => $SF . 'SkillFishOS-26.06.3-Aetherium-BC250-amd64.iso.sha256/download',
    'sha-generic'=> $SF . 'SkillFishOS-26.06.3-Aetherium-Generic-amd64.iso.sha256/download',
    'note'       => $SF . 'RELEASE-NOTES-26.06.3.md/download',
    'tutti'      => $SF,
    // i .torrent li serviamo noi: 25 KB, e cosi' partono anche se SourceForge
    // e' lento. Restano qui per essere contati come gli altri.
    'tor-bc250'  => '/torrent/SkillFishOS-26.06.3-Aetherium-BC250-amd64.iso.torrent',
    'tor-generic'=> '/torrent/SkillFishOS-26.06.3-Aetherium-Generic-amd64.iso.torrent',
);

// I magnet non passano di qui: il clic li consegna direttamente al programma
// torrent, senza nessuna richiesta al nostro sito. Per contarli la pagina manda
// una segnalazione (go.php?f=...&b=1) e noi rispondiamo senza rimandare da
// nessuna parte. Restano in un elenco a parte proprio perche' per loro non
// esiste una destinazione: se qualcuno li chiedesse senza b=1 e' un errore.
$SEGNALI = array('magnet-bc250', 'magnet-generic');

$f = (string)($_GET['f'] ?? '');
$segnale = isset($_GET['b']) && $_GET['b'] === '1';

$valido = $segnale ? in_array($f, $SEGNALI, true) : isset($DEST[$f]);
if (!$valido) {
    http_response_code(404);
    header('Content-Type: text/plain; charset=utf-8');
    echo "file sconosciuto\n";
    exit;
}

// --- registra ---------------------------------------------------------------
$ua = substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 300);
try {
    $db = sfstats_db();
    $db->exec('CREATE TABLE IF NOT EXISTS dl(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER NOT NULL, day TEXT NOT NULL,
        file TEXT NOT NULL, kind TEXT NOT NULL DEFAULT "iso",
        vis TEXT NOT NULL, bot INTEGER NOT NULL DEFAULT 0,
        country TEXT NOT NULL DEFAULT "", cname TEXT NOT NULL DEFAULT "",
        lang TEXT NOT NULL DEFAULT "")');
    $db->exec('CREATE INDEX IF NOT EXISTS idx_dl_day ON dl(day)');
    $db->exec('CREATE INDEX IF NOT EXISTS idx_dl_file ON dl(file)');

    // da che pagina arrivava: ci dice in che lingua naviga chi scarica
    $lang = '';
    $ref = (string)($_SERVER['HTTP_REFERER'] ?? '');
    if (preg_match('#skillfishos\.com/(en|pl|uk)/#i', $ref, $m)) $lang = strtolower($m[1]);
    elseif (strpos($ref, 'skillfishos.com') !== false) $lang = 'it';

    $kind = (strpos($f, 'magnet-') === 0) ? 'magnet'
          : ((strpos($f, 'tor-') === 0) ? 'torrent'
          : ((strpos($f, 'ia-') === 0) ? 'archive'
          : ((strpos($f, 'sha') === 0) ? 'sha' : (($f === 'note' || $f === 'tutti') ? 'altro' : 'iso'))));

    list($cc, $cn) = sfstats_country();
    $st = $db->prepare('INSERT INTO dl(ts,day,file,kind,vis,bot,country,cname,lang)
                        VALUES(:ts,:day,:f,:k,:v,:b,:cc,:cn,:l)');
    $st->execute(array(
        ':ts' => time(), ':day' => gmdate('Y-m-d'),
        ':f' => $f, ':k' => $kind,
        ':v' => sfstats_visitor($ua), ':b' => sfstats_is_bot($ua),
        ':cc' => $cc, ':cn' => $cn, ':l' => $lang,
    ));
} catch (Throwable $e) {
    // un problema con le statistiche non deve mai impedire un download
}

// --- rispondi ---------------------------------------------------------------
header('Cache-Control: no-store');
if ($segnale) {
    // al magnet ci pensa gia' il browser: qui non c'e' niente da consegnare
    http_response_code(204);
    exit;
}
header('Location: ' . $DEST[$f], true, 302);
exit;
