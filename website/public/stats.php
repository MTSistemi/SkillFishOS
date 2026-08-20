<?php
// SkillFishOS — private analytics dashboard. Password set on first visit.
require __DIR__ . '/_sfstats.php';
session_start();
header('Cache-Control: no-store, private');
header('X-Robots-Tag: noindex, nofollow');
header('Referrer-Policy: no-referrer');

$DIR       = sfstats_dir();
$PWD_FILE  = $DIR . '/admin.php';      // stores password_hash (as PHP, never served raw)
$FAIL_FILE = $DIR . '/fails.json';

function pwd_hash_get($f) { return is_file($f) ? (include $f) : ''; }
function pwd_hash_set($f, $hash) { @file_put_contents($f, "<?php return " . var_export($hash, true) . ";\n"); }

$HASH = pwd_hash_get($PWD_FILE);
$err  = '';
$now  = time();

// ---- rate limiting (per-process file) ----
function fails_load($f) { return is_file($f) ? (json_decode(file_get_contents($f), true) ?: array()) : array(); }
function fails_save($f, $a) { @file_put_contents($f, json_encode($a)); }
$fails = fails_load($FAIL_FILE);
$fails = array_values(array_filter($fails, function ($t) use ($now) { return $t > $now - 900; })); // 15 min window
$locked = count($fails) >= 8;

// ---- actions ----
$action = $_POST['action'] ?? '';

if ($action === 'logout') {
    $_SESSION = array(); session_destroy();
    header('Location: stats.php'); exit;
}

// First-run: create the password.
if (!$HASH && $action === 'setup') {
    $p1 = (string)($_POST['p1'] ?? ''); $p2 = (string)($_POST['p2'] ?? '');
    if (strlen($p1) < 8) $err = 'La password deve avere almeno 8 caratteri.';
    elseif ($p1 !== $p2) $err = 'Le due password non coincidono.';
    else {
        pwd_hash_set($PWD_FILE, password_hash($p1, PASSWORD_DEFAULT));
        $_SESSION['sf_ok'] = 1;
        header('Location: stats.php'); exit;
    }
    $HASH = pwd_hash_get($PWD_FILE);
}

// Login.
if ($HASH && $action === 'login') {
    if ($locked) {
        $err = 'Troppi tentativi. Riprova tra qualche minuto.';
    } elseif (password_verify((string)($_POST['pwd'] ?? ''), $HASH)) {
        $_SESSION['sf_ok'] = 1;
        fails_save($FAIL_FILE, array());
        header('Location: stats.php'); exit;
    } else {
        $fails[] = $now; fails_save($FAIL_FILE, $fails);
        $err = 'Password errata.';
    }
}

$authed = !empty($_SESSION['sf_ok']);

// ----------------------------------------------------------------------------
// Render helpers
function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function page_head($title) {
    echo '<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">';
    echo '<meta name="viewport" content="width=device-width,initial-scale=1">';
    echo '<meta name="robots" content="noindex,nofollow"><title>' . h($title) . '</title>';
    // La stessa favicon del sito. Va qui dentro e non nelle due pagine, perche'
    // page_head() le serve entrambe: la schermata di accesso e il cruscotto.
    // Metterla in una sola avrebbe lasciato l'icona vuota proprio sulla pagina
    // che si tiene aperta in una scheda per ore.
    echo '<link rel="icon" href="/img/badge.png" type="image/png">';
    echo '<style>'
       . ':root{--bg:#0c0a06;--panel:#1a140b;--panel2:#211a0f;--gold:#d8a849;--gold-lt:#e8c878;'
       . '--copper:#b9722f;--cream:#efe6d3;--muted:#a9967a;--line:rgba(216,168,73,.18)}'
       . '*{margin:0;padding:0;box-sizing:border-box}'
       . 'body{font-family:Inter,system-ui,Segoe UI,sans-serif;background:var(--bg);color:var(--cream);min-height:100vh}'
       . 'a{color:var(--gold-lt)}.wrap{max-width:1100px;margin:0 auto;padding:20px}'
       . '.mid{min-height:100vh;display:grid;place-items:center;padding:20px}'
       . '.card{background:linear-gradient(160deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:16px;padding:22px}'
       . '.lbox{width:min(380px,92vw);text-align:center}'
       . '.brand{font-weight:800;font-size:1.4rem;margin-bottom:4px}'
       . '.brand .g{background:linear-gradient(100deg,#f3dca0,#d8a849 50%,#b9722f);-webkit-background-clip:text;background-clip:text;color:transparent}'
       . '.sub{color:var(--muted);font-size:.9rem;margin-bottom:18px}'
       . 'input{width:100%;background:#0d0b06;border:1px solid var(--line);border-radius:10px;color:var(--cream);padding:11px 14px;margin:7px 0;font-size:1rem}'
       . 'input:focus{outline:none;border-color:var(--gold)}'
       . '.btn{width:100%;margin-top:12px;padding:12px;border:none;border-radius:10px;cursor:pointer;font-weight:700;background:linear-gradient(135deg,#e8c878,#d8a849 55%,#b9722f);color:#1a130a}'
       . '.btn:hover{filter:brightness(1.06)}.err{color:#e07b5a;font-size:.88rem;min-height:1.2em;margin-top:8px}'
       . 'header{display:flex;align-items:center;gap:12px;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:18px}'
       . 'header .sp{flex:1}.ghost{background:rgba(216,168,73,.08);border:1px solid var(--line);color:var(--gold-lt);border-radius:9px;padding:7px 12px;cursor:pointer;font-weight:600}'
       . '.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:18px}'
       . '.kpi{background:linear-gradient(160deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:14px;padding:14px 16px}'
       . '.kpi .n{font-size:1.7rem;font-weight:800;color:var(--gold-lt)}.kpi .l{color:var(--muted);font-size:.82rem;margin-top:2px}'
       . '.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:760px){.grid2{grid-template-columns:1fr}}'
       . '.panel{background:linear-gradient(160deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:16px}'
       . '.panel h3{font-size:1rem;color:var(--gold-lt);margin-bottom:12px}'
       . 'table{width:100%;border-collapse:collapse;font-size:.9rem}'
       . 'td,th{text-align:left;padding:6px 4px;border-bottom:1px solid rgba(216,168,73,.08)}'
       . 'th{color:var(--muted);font-weight:600;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em}'
       . 'td.r,th.r{text-align:right}.bar{height:8px;background:linear-gradient(90deg,#b9722f,#e8c878);border-radius:4px}'
       . '.muted{color:var(--muted)}.foot{color:var(--muted);font-size:.8rem;text-align:center;margin-top:18px}'
       . '</style></head><body>';
}

// ----------------------------------------------------------------------------
// Not authenticated → setup or login screen
if (!$authed) {
page_head('SkillFishOS · Statistiche');
    echo '<div class="mid"><div class="card lbox">';
    echo '<div class="brand">SkillFish<span class="g">OS</span> · Statistiche</div>';
    if (!$HASH) {
        echo '<div class="sub">Primo accesso — imposta la password (solo tua).</div>';
        echo '<form method="post"><input type="hidden" name="action" value="setup">';
        echo '<input type="password" name="p1" placeholder="Nuova password (min 8)" autocomplete="new-password" autofocus>';
        echo '<input type="password" name="p2" placeholder="Ripeti password" autocomplete="new-password">';
        echo '<button class="btn" type="submit">Crea password</button>';
        echo '<div class="err">' . h($err) . '</div></form>';
    } else {
        echo '<div class="sub">Area privata — accedi.</div>';
        echo '<form method="post"><input type="hidden" name="action" value="login">';
        echo '<input type="password" name="pwd" placeholder="Password" autocomplete="current-password" autofocus>';
        echo '<button class="btn" type="submit">Entra</button>';
        echo '<div class="err">' . h($err) . '</div></form>';
    }
    echo '</div></div></body></html>';
    exit;
}

// ----------------------------------------------------------------------------
// Authenticated → dashboard
$db = sfstats_db();
$incl_bots = isset($_GET['bots']);
$botw = $incl_bots ? '' : ' AND bot=0';

function one($db, $sql) { $s = $db->query($sql); $r = $s->fetch(PDO::FETCH_NUM); return $r ? (int)$r[0] : 0; }

$today = gmdate('Y-m-d');
$d7    = gmdate('Y-m-d', time() - 6 * 86400);
$d30   = gmdate('Y-m-d', time() - 29 * 86400);

$views_total = one($db, "SELECT COUNT(*) FROM hits WHERE 1=1$botw");
$views_today = one($db, "SELECT COUNT(*) FROM hits WHERE day='$today'$botw");
$views_7     = one($db, "SELECT COUNT(*) FROM hits WHERE day>='$d7'$botw");
$views_30    = one($db, "SELECT COUNT(*) FROM hits WHERE day>='$d30'$botw");
$uniq_today  = one($db, "SELECT COUNT(DISTINCT vis) FROM hits WHERE day='$today'$botw");
$uniq_7      = one($db, "SELECT COUNT(DISTINCT vis) FROM hits WHERE day>='$d7'$botw");
$uniq_30     = one($db, "SELECT COUNT(DISTINCT vis) FROM hits WHERE day>='$d30'$botw");

// daily series (last 30 days)
$series = array();
$rows = $db->query("SELECT day, COUNT(*) v, COUNT(DISTINCT vis) u FROM hits
                    WHERE day>='$d30'$botw GROUP BY day")->fetchAll(PDO::FETCH_ASSOC);
$map = array(); foreach ($rows as $r) $map[$r['day']] = $r;
for ($i = 29; $i >= 0; $i--) {
    $d = gmdate('Y-m-d', time() - $i * 86400);
    $series[] = array('day' => $d, 'v' => (int)($map[$d]['v'] ?? 0), 'u' => (int)($map[$d]['u'] ?? 0));
}
$maxv = 1; foreach ($series as $s) $maxv = max($maxv, $s['v']);

function toprows($db, $col, $where, $limit = 8) {
    $out = $db->query("SELECT $col k, COUNT(*) c FROM hits WHERE 1=1 $where
                       GROUP BY $col ORDER BY c DESC LIMIT $limit")->fetchAll(PDO::FETCH_ASSOC);
    return $out;
}
$top_pages = toprows($db, 'path', "$botw AND day>='$d30'");
$top_refs  = toprows($db, 'ref',  "$botw AND day>='$d30' AND ref<>''");
$browsers  = toprows($db, 'browser', "$botw AND day>='$d30'", 6);
$oses      = toprows($db, 'os', "$botw AND day>='$d30'", 6);
$countries = $db->query("SELECT country, MAX(cname) cname, COUNT(*) c FROM hits
                         WHERE 1=1 $botw AND day>='$d30' AND country<>''
                         GROUP BY country ORDER BY c DESC LIMIT 15")->fetchAll(PDO::FETCH_ASSOC);
$top_links = $db->query("SELECT ref_full k, COUNT(*) c FROM hits
                         WHERE 1=1 $botw AND day>='$d30' AND ref_full<>''
                         GROUP BY ref_full ORDER BY c DESC LIMIT 12")->fetchAll(PDO::FETCH_ASSOC);
$recent    = $db->query("SELECT ts,path,ref,ref_full,browser,os,bot,country,cname
                         FROM hits ORDER BY id DESC LIMIT 20")->fetchAll(PDO::FETCH_ASSOC);

// ⚠️ QUESTO BLOCCO VA DOPO `$db = sfstats_db()` E PRIMA DEI RIQUADRI.
// `page_head('SkillFishOS · Statistiche')` compare DUE VOLTE nel file: una per
// la schermata di accesso e una per il cruscotto. Mettendolo prima della prima
// occorrenza finiva nella schermata di accesso, dove il database non e' ancora
// aperto: la pagina rispondeva 500 a chiunque provasse a entrare. Non lo
// avrebbe detto nessun controllo di sintassi — si e' visto solo eseguendola.

// --- i totali, calcolati PRIMA dei riquadri ---------------------------------
// Questo blocco stava a meta' pagina, sotto le tabelle dei download. I numeri
// che riassumono tutto - quanti download in tutto, quanti visitatori da quando
// il sito esiste - servono in ALTO, dove si guarda per primo, non in fondo dopo
// aver scorso otto tabelle. Il calcolo e' lo stesso; e' cambiato solo il punto
// in cui viene fatto, perche' i riquadri stanno sopra e in PHP una variabile
// non esiste finche' non la si e' riempita.

// --- i numeri veri, presi da SourceForge -------------------------------------
// Si interroga ogni mezz'ora e si tiene in cache: l'API e' pubblica ma non va
// martellata, e questa pagina si ricarica spesso. Mezz'ora e' la stessa cadenza
// del raccoglitore sul container, cosi' i due numeri non si contraddicono.
define('SF_CACHE', 1800);
$sf = null; $sf_err = '';
try {
    $cache = sfstats_dir() . '/sf-downloads.json';
    if (is_file($cache) && (time() - filemtime($cache) < SF_CACHE)) {
        $sf = json_decode((string)file_get_contents($cache), true);
    } else {
        $url = 'https://sourceforge.net/projects/skillfishos/files/stats/json'
             . '?start_date=' . gmdate('Y-m-d', time() - 30 * 86400)
             . '&end_date=' . gmdate('Y-m-d');
        $ctx = stream_context_create(array('http' => array(
            'timeout' => 8, 'header' => "User-Agent: SkillFishOS-stats\r\n")));
        $raw = @file_get_contents($url, false, $ctx);
        if ($raw) { @file_put_contents($cache, $raw); $sf = json_decode($raw, true); }
        else $sf_err = 'SourceForge non ha risposto';
    }
} catch (Throwable $e) { $sf_err = 'errore nella lettura'; }

// --- il totale da sempre -----------------------------------------------------
// L'API accetta qualunque data d'inizio e taglia da sola al primo caricamento,
// quindi partiamo da prima che il progetto esistesse e lasciamo fare a lei.
// Anche questo ogni mezz'ora: prima erano sei ore, e nei giorni in cui i
// download si muovono davvero - un video, un articolo - sei ore di ritardo
// vogliono dire guardare una pagina che dice il falso.
$sf_tot = null; $sf_dal = '';
try {
    $cache_tot = sfstats_dir() . '/sf-downloads-sempre.json';
    $d = null;
    if (is_file($cache_tot) && (time() - filemtime($cache_tot) < SF_CACHE)) {
        $d = json_decode((string)file_get_contents($cache_tot), true);
    } else {
        $url = 'https://sourceforge.net/projects/skillfishos/files/stats/json'
             . '?start_date=2026-01-01&end_date=' . gmdate('Y-m-d');
        $ctx = stream_context_create(array('http' => array(
            'timeout' => 12, 'header' => "User-Agent: SkillFishOS-stats\r\n")));
        $raw = @file_get_contents($url, false, $ctx);
        if ($raw) { @file_put_contents($cache_tot, $raw); $d = json_decode($raw, true); }
        elseif (is_file($cache_tot)) {
            // se SourceForge non risponde meglio un numero vecchio che nessun numero
            $d = json_decode((string)file_get_contents($cache_tot), true);
        }
    }
    if (is_array($d) && isset($d['total'])) {
        $sf_tot = (int)$d['total'];
        foreach ((array)($d['downloads'] ?? array()) as $g) {
            if (is_array($g) && (int)$g[1] > 0) { $sf_dal = substr((string)$g[0], 0, 10); break; }
        }
    }
} catch (Throwable $e) { }

// --- il dettaglio file per file ----------------------------------------------
// Lo raccoglie il container una volta al giorno (skillfish-stat-sourceforge):
// sono quasi trenta file e ognuno vuole una richiesta all'API, farlo mentre la
// pagina si carica vorrebbe dire mezzo minuto di attesa a ogni apertura.
$det = null;
$f_det = sfstats_dir() . '/sf-dettaglio.json';
if (is_file($f_det)) {
    $d2 = json_decode((string)file_get_contents($f_det), true);
    if (is_array($d2) && isset($d2['totale'])) {
        $det = $d2;
        $sf_tot = (int)$d2['totale'];              // piu' attendibile: e' la stessa fonte
        if (!empty($d2['dal'])) $sf_dal = (string)$d2['dal'];
    }
}

// I clic sui nostri pulsanti, in totale. Non sono i download veri: dicono
// quanti li hanno AVVIATI dal sito. Il numero di SourceForge e' sempre piu'
// alto, perche' comprende anche chi arriva li' senza passare da noi.
$dl_clic = 0; $dl_persone = 0;
try {
    $dl_clic    = one($db, 'SELECT COUNT(*) FROM dl WHERE bot=0');
    $dl_persone = one($db, 'SELECT COUNT(DISTINCT vis) FROM dl WHERE bot=0');
} catch (Throwable $e) { /* la tabella arriva col primo clic */ }

// ⚠️ Da quando esiste il sito: il PRIMO giorno che risulta nel database, non
// una data scritta a mano che poi resta indietro.
$dal_giorno = '';
try {
    $s = $db->query('SELECT MIN(day) FROM hits');
    $r = $s->fetch(PDO::FETCH_NUM);
    if ($r && $r[0]) $dal_giorno = (string)$r[0];
} catch (Throwable $e) { }

// ⚠️ VISITATORI TOTALI, e va detto cosa sono davvero. L'identificativo del
// visitatore contiene il GIORNO (e' cosi' che restiamo senza cookie e senza
// poter risalire alla persona), quindi chi torna domani conta come qualcuno di
// nuovo. Questo numero e' la somma dei visitatori giornalieri: e' il massimo
// che si puo' dire senza tracciare le persone, e chiamarlo "persone diverse"
// sarebbe falso.
$uniq_total = one($db, "SELECT COUNT(DISTINCT vis) FROM hits WHERE 1=1$botw");

page_head('SkillFishOS · Statistiche');
echo '<div class="wrap">';
echo '<header><div class="brand">SkillFish<span class="g">OS</span> · Statistiche</div><div class="sp"></div>';
echo '<a class="ghost" href="?' . ($incl_bots ? '' : 'bots=1') . '">' . ($incl_bots ? 'Escludi bot' : 'Includi bot') . '</a>';
echo '<form method="post" style="display:inline"><input type="hidden" name="action" value="logout"><button class="ghost" type="submit">Esci</button></form>';
echo '</header>';

// KPIs
$kpi = function ($n, $l) { echo '<div class="kpi"><div class="n">' . number_format($n, 0, ',', '.') . '</div><div class="l">' . h($l) . '</div></div>'; };

// Prima fila: il movimento recente.
echo '<div class="kpis">';
$kpi($views_today, 'Visite oggi'); $kpi($uniq_today, 'Visitatori oggi');
$kpi($views_7, 'Visite 7 giorni'); $kpi($uniq_7, 'Visitatori 7 giorni');
$kpi($views_30, 'Visite 30 giorni'); $kpi($uniq_30, 'Visitatori 30 giorni');
echo '</div>';

// Seconda fila: i totali da quando il sito esiste, download compresi. Stavano
// sparsi in fondo alla pagina, sotto le tabelle; sono i numeri che si vogliono
// vedere per primi, quindi stanno accanto alle visite.
// ⚠️ Ogni totale porta la SUA data d'inizio, non una comune. Il sito conta le
// visite dal 15/06; SourceForge contava i download da prima che il sito
// esistesse. Una data sola in cima al gruppo le avrebbe attribuite entrambe al
// giorno sbagliato.
$da_sito = $dal_giorno ? ' · dal ' . date('d/m/Y', strtotime($dal_giorno)) : '';
$da_sf   = $sf_dal ? ' · dal ' . date('d/m/Y', strtotime($sf_dal)) : '';
echo '<h3 style="margin:26px 0 10px">Da sempre</h3>';
echo '<div class="kpis">';
$kpi($views_total, 'Visite totali' . $da_sito);
$kpi($uniq_total, 'Visitatori totali' . $da_sito);
if ($sf_tot !== null) $kpi($sf_tot, 'Download completati' . $da_sf);
if ($sf && isset($sf['total'])) $kpi((int)$sf['total'], 'Download 30 giorni');
$kpi($dl_clic, 'Download avviati dal sito');
$kpi($dl_persone, 'Chi li ha avviati');
echo '</div>';
// ⚠️ Gli accenti si scrivono accentati. La prima stesura usava l'apostrofo
// (perche', meta') per non litigare con le virgolette del PHP, e sulla pagina
// si leggeva cosi': in mezzo a un testo che per il resto ha gli accenti giusti.
// Con le virgolette doppie il problema non esiste.
echo '<div class="muted" style="font-size:.78rem;margin:8px 2px 0">'
   . "<strong>Download completati</strong>: i numeri veri di SourceForge, compreso chi ci arriva senza passare dal sito. "
   . "<strong>Avviati dal sito</strong>: i clic sui nostri pulsanti — sempre di meno, perché chi cambia idea a metà non conta. "
   . "<strong>Visitatori totali</strong>: la somma dei visitatori giornalieri. Restiamo senza cookie, quindi chi torna un altro giorno non lo possiamo riconoscere e conta due volte."
   . '</div>';

// chart
echo '<div class="panel"><h3>Andamento ultimi 30 giorni</h3>';
$W = 1000; $H = 180; $pad = 24; $bw = ($W - $pad * 2) / 30;
echo '<svg viewBox="0 0 ' . $W . ' ' . $H . '" style="width:100%;height:auto" preserveAspectRatio="none">';
foreach ($series as $i => $s) {
    $bh = ($H - $pad * 2) * $s['v'] / $maxv;
    $x = $pad + $i * $bw; $y = $H - $pad - $bh;
    echo '<rect x="' . round($x + 1, 1) . '" y="' . round($y, 1) . '" width="' . round($bw - 2, 1) . '" height="' . round($bh, 1) . '" rx="2" fill="url(#g)"><title>' . h($s['day']) . ': ' . $s['v'] . ' visite, ' . $s['u'] . ' visitatori</title></rect>';
}
echo '<defs><linearGradient id="g" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#b9722f"/><stop offset="1" stop-color="#e8c878"/></linearGradient></defs>';
echo '<line x1="' . $pad . '" y1="' . ($H - $pad) . '" x2="' . ($W - $pad) . '" y2="' . ($H - $pad) . '" stroke="rgba(216,168,73,.25)"/>';
echo '</svg>';
echo '<div class="muted" style="font-size:.78rem;margin-top:6px">' . h($series[0]['day']) . ' → ' . h($series[29]['day']) . ' · max ' . $maxv . ' visite/giorno</div>';
echo '</div>';

// tables
function tbl($title, $rows, $klabel, $linkpath = false) {
    echo '<div class="panel"><h3>' . h($title) . '</h3><table><tr><th>' . h($klabel) . '</th><th class="r">Visite</th></tr>';
    if (!$rows) echo '<tr><td class="muted" colspan="2">Nessun dato ancora.</td></tr>';
    $max = 1; foreach ($rows as $r) $max = max($max, (int)$r['c']);
    foreach ($rows as $r) {
        $k = $r['k'] === '' ? '(diretto)' : $r['k'];
        $disp = $linkpath ? '<span class="muted">' . h($k) . '</span>' : h($k);
        $pct = round(100 * $r['c'] / $max);
        echo '<tr><td>' . $disp . '<div class="bar" style="width:' . $pct . '%;margin-top:4px"></div></td><td class="r">' . (int)$r['c'] . '</td></tr>';
    }
    echo '</table></div>';
}
// countries
echo '<div class="panel"><h3>Paesi di origine (30g)</h3><table><tr><th>Paese</th><th class="r">Visite</th></tr>';
if (!$countries) echo '<tr><td class="muted" colspan="2">Nessun dato ancora.</td></tr>';
$cmax = 1; foreach ($countries as $r) $cmax = max($cmax, (int)$r['c']);
foreach ($countries as $r) {
    $label = sfstats_flag($r['country']) . ' ' . h($r['cname'] ?: $r['country']);
    $pct = round(100 * $r['c'] / $cmax);
    echo '<tr><td>' . $label . '<div class="bar" style="width:' . $pct . '%;margin-top:4px"></div></td><td class="r">' . (int)$r['c'] . '</td></tr>';
}
echo '</table></div>';

echo '<div class="grid2"><div>';
tbl('Pagine più viste (30g)', $top_pages, 'Pagina', true);
tbl('Provenienza (domini, 30g)', $top_refs, 'Sito');
echo '</div><div>';
tbl('Browser (30g)', $browsers, 'Browser');
tbl('Sistema operativo (30g)', $oses, 'OS');
echo '</div></div>';

// full referrer links
echo '<div class="panel"><h3>Link di provenienza completi (30g)</h3><table><tr><th>URL referrer</th><th class="r">Visite</th></tr>';
if (!$top_links) echo '<tr><td class="muted" colspan="2">Nessun link esterno registrato.</td></tr>';
$lmax = 1; foreach ($top_links as $r) $lmax = max($lmax, (int)$r['c']);
foreach ($top_links as $r) {
    $u = $r['k'];
    $pct = round(100 * $r['c'] / $lmax);
    echo '<tr><td><a href="' . h($u) . '" target="_blank" rel="noreferrer noopener nofollow">' . h($u) . '</a>'
       . '<div class="bar" style="width:' . $pct . '%;margin-top:4px"></div></td><td class="r">' . (int)$r['c'] . '</td></tr>';
}
echo '</table></div>';

// recent
echo '<div class="panel"><h3>Ultime visite</h3><table><tr><th>Quando (UTC)</th><th>Paese</th><th>Pagina</th><th>Da</th><th>Client</th></tr>';
if (!$recent) echo '<tr><td class="muted" colspan="5">Nessuna visita registrata.</td></tr>';
foreach ($recent as $r) {
    $cc = $r['country'] ?? '';
    $country = $cc ? sfstats_flag($cc) . ' ' . h($cc) : '<span class="muted">—</span>';
    if (!empty($r['ref_full'])) {
        $da = '<a href="' . h($r['ref_full']) . '" target="_blank" rel="noreferrer noopener nofollow">' . h($r['ref'] ?: $r['ref_full']) . '</a>';
    } else {
        $da = '<span class="muted">' . h($r['ref'] ?: '—') . '</span>';
    }
    echo '<tr><td class="muted">' . h(gmdate('d/m H:i', (int)$r['ts'])) . ($r['bot'] ? ' 🤖' : '') . '</td>'
       . '<td>' . $country . '</td>'
       . '<td>' . h($r['path']) . '</td>'
       . '<td>' . $da . '</td>'
       . '<td class="muted">' . h($r['browser'] . ' / ' . $r['os']) . '</td></tr>';
}
echo '</table></div>';

// ---------------------------------------------------------------- download ---
// Due fonti, e vanno lette insieme:
//   - i nostri clic sui pulsanti (go.php): dicono chi ha AVVIATO un download e
//     da che paese e lingua arrivava;
//   - i numeri di SourceForge: dicono quanti download sono andati a buon fine
//     davvero, compresi quelli di chi arriva da fuori dal nostro sito.
// Il primo numero e' sempre piu' basso: chi cambia idea a meta' non conta.
$dl_tot = array(); $dl_day = array(); $dl_paese = array(); $dl_lingua = array();
$dl_ver = array();
try {
    $db->exec('CREATE TABLE IF NOT EXISTS dl(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER NOT NULL, day TEXT NOT NULL,
        file TEXT NOT NULL, kind TEXT NOT NULL DEFAULT "iso",
        vis TEXT NOT NULL, bot INTEGER NOT NULL DEFAULT 0,
        country TEXT NOT NULL DEFAULT "", cname TEXT NOT NULL DEFAULT "",
        lang TEXT NOT NULL DEFAULT "")');
    $dl_tot = $db->query('SELECT file, kind, COUNT(*) c, COUNT(DISTINCT vis) u
                          FROM dl WHERE bot=0 GROUP BY file ORDER BY c DESC')->fetchAll();
    $dl_day = $db->query('SELECT day, COUNT(*) c FROM dl WHERE bot=0
                          GROUP BY day ORDER BY day DESC LIMIT 14')->fetchAll();
    $dl_paese = $db->query('SELECT country, cname, COUNT(*) c FROM dl
                            WHERE bot=0 AND country<>"" GROUP BY country
                            ORDER BY c DESC LIMIT 8')->fetchAll();
    $dl_lingua = $db->query('SELECT lang, COUNT(*) c FROM dl WHERE bot=0 AND lang<>""
                             GROUP BY lang ORDER BY c DESC')->fetchAll();
    // Per versione. La colonna e' arrivata il 17/08/2026: i clic precedenti
    // hanno ver="" e restano contati a parte, dichiarati per quello che sono,
    // invece di essere attribuiti alla versione sbagliata.
    $dl_ver = $db->query('SELECT ver, kind, COUNT(*) c, COUNT(DISTINCT vis) u
                          FROM dl WHERE bot=0 GROUP BY ver, kind
                          ORDER BY ver DESC, c DESC')->fetchAll();
} catch (Throwable $e) { }

$etichetta = array(
    'bc250' => 'ISO BC-250', 'generic' => 'ISO Generic',
    'tor-bc250' => 'torrent BC-250', 'tor-generic' => 'torrent Generic',
    'magnet-bc250' => 'magnet BC-250', 'magnet-generic' => 'magnet Generic',
    'sha-bc250' => 'sha256 BC-250', 'sha-generic' => 'sha256 Generic',
    'note' => 'note di rilascio', 'tutti' => 'elenco file',
);

echo '<div class="panel"><h3>Download avviati dal sito</h3>';
echo '<table><tr><th>File</th><th class="r">Clic</th><th class="r">Persone</th></tr>';
if (!$dl_tot) echo '<tr><td class="muted" colspan="3">Nessun download ancora registrato.</td></tr>';
$dl_max = 0; foreach ($dl_tot as $r) $dl_max = max($dl_max, (int)$r['c']);
foreach ($dl_tot as $r) {
    $nome = $etichetta[$r['file']] ?? $r['file'];
    $pct = $dl_max ? round(100 * $r['c'] / $dl_max) : 0;
    echo '<tr><td>' . h($nome)
       . '<div class="bar" style="width:' . $pct . '%;margin-top:4px"></div></td>'
       . '<td class="r">' . (int)$r['c'] . '</td><td class="r">' . (int)$r['u'] . '</td></tr>';
}
echo '</table>';

if ($dl_day) {
    echo '<h3 style="margin-top:18px">Ultimi giorni</h3><table><tr><th>Giorno</th><th class="r">Download</th></tr>';
    $m = 0; foreach ($dl_day as $r) $m = max($m, (int)$r['c']);
    foreach ($dl_day as $r) {
        $pct = $m ? round(100 * $r['c'] / $m) : 0;
        echo '<tr><td>' . h($r['day']) . '<div class="bar" style="width:' . $pct . '%;margin-top:4px"></div></td>'
           . '<td class="r">' . (int)$r['c'] . '</td></tr>';
    }
    echo '</table>';
}

// --- per versione ------------------------------------------------------------
// Quale versione sta scaricando la gente adesso. Serve per capire quanto in
// fretta una nuova immagine sostituisce la precedente, e - quando ne ritiriamo
// una - se qualcuno la sta ancora prendendo da una pagina in cache o da un
// segnalibro.
if ($dl_ver) {
    $per_ver = array();
    foreach ($dl_ver as $r) {
        $v = $r['ver'] !== '' ? $r['ver'] : '?';
        if (!isset($per_ver[$v])) $per_ver[$v] = array('c' => 0, 'u' => 0, 'k' => array());
        $per_ver[$v]['c'] += (int)$r['c'];
        $per_ver[$v]['u'] += (int)$r['u'];
        $per_ver[$v]['k'][$r['kind']] = (int)$r['c'];
    }
    krsort($per_ver);
    $vmax = 0; foreach ($per_ver as $d) $vmax = max($vmax, $d['c']);
    echo '<h3 style="margin-top:18px">Per versione di SkillFishOS '
       . '<span class="muted" style="font-weight:400">· clic sui nostri pulsanti</span></h3>';
    echo '<table><tr><th>Versione</th><th>Cosa</th><th class="r">Clic</th><th class="r">Persone</th></tr>';
    foreach ($per_ver as $v => $d) {
        arsort($d['k']);
        $pezzi = array();
        foreach ($d['k'] as $k => $n) $pezzi[] = h($k) . ' ' . $n;
        $eti = $v === '?'
            ? '<span class="muted">prima del 17/08</span>'
            : h($v);
        echo '<tr><td>' . $eti
           . '<div class="bar" style="width:' . ($vmax ? round(100 * $d['c'] / $vmax) : 0) . '%;margin-top:4px"></div></td>'
           . '<td class="muted" style="font-size:.82rem">' . implode(' · ', $pezzi) . '</td>'
           . '<td class="r">' . $d['c'] . '</td>'
           . '<td class="r muted">' . $d['u'] . '</td></tr>';
    }
    echo '</table>';
    if (isset($per_ver['?']))
        echo '<p class="muted" style="font-size:.8rem;margin-top:8px">'
           . 'I clic segnati "prima del 17/08" sono stati registrati quando ancora non '
           . 'annotavamo la versione: non si possono attribuire a posteriori senza tirare a indovinare.</p>';
}

if ($dl_paese || $dl_lingua) {
    echo '<h3 style="margin-top:18px">Da dove, e in che lingua</h3><table><tr><th>Paese</th><th class="r">Download</th></tr>';
    foreach ($dl_paese as $r)
        echo '<tr><td>' . sfstats_flag($r['country']) . ' ' . h($r['cname'] ?: $r['country'])
           . '</td><td class="r">' . (int)$r['c'] . '</td></tr>';
    foreach ($dl_lingua as $r)
        echo '<tr><td class="muted">pagina in ' . h(strtoupper($r['lang']))
           . '</td><td class="r">' . (int)$r['c'] . '</td></tr>';
    echo '</table>';
}
echo '</div>';

echo '<div class="panel"><h3>Download completati su SourceForge</h3>';
// ⚠️ Il totale da sempre e quello a 30 giorni sono saliti in cima alla pagina.
// Ripeterli qui non aggiungeva niente e faceva sembrare che fossero due
// misure diverse. Resta il numero che in alto non c'e': quanti di quei
// download sono immagini ISO e non firme, note o elenchi.
if ($sf_tot !== null && $det && !empty($det['per_tipo'])) {
    $iso = 0;
    foreach ($det['per_tipo'] as $tp => $n) if (strpos($tp, 'ISO') === 0) $iso += (int)$n;
    echo '<div class="kpis">';
    echo '<div class="kpi"><div class="n">' . number_format($iso, 0, ',', '.') . '</div>'
       . '<div class="l">di cui immagini ISO</div></div>';
    echo '<div class="kpi"><div class="n">' . ($sf_tot ? round(100 * $iso / $sf_tot) : 0) . '%</div>'
       . '<div class="l">del totale</div></div>';
    echo '</div>';
}

if ($det) {
    // Per tipo: dice cosa scarica davvero la gente. Le firme sha256 quasi a zero
    // rispetto alle ISO significano che quasi nessuno verifica il file.
    if (!empty($det['per_tipo'])) {
        $tp = $det['per_tipo']; arsort($tp);
        $max = max(array_map('intval', $tp)) ?: 1;
        echo '<h3 style="margin-top:4px">Per tipo di file <span class="muted" style="font-weight:400">· da sempre</span></h3>';
        echo '<table><tr><th>Tipo</th><th class="r">Download</th><th class="r">%</th></tr>';
        foreach ($tp as $nome => $n) {
            $pct = $sf_tot ? round(100 * $n / $sf_tot) : 0;
            echo '<tr><td>' . h($nome)
               . '<div class="bar" style="width:' . round(100 * $n / $max) . '%;margin-top:4px"></div></td>'
               . '<td class="r">' . number_format((int)$n, 0, ',', '.') . '</td>'
               . '<td class="r muted">' . $pct . '%</td></tr>';
        }
        echo '</table>';
    }

    if (!empty($det['per_rilascio'])) {
        $rl = $det['per_rilascio']; krsort($rl);
        echo '<h3 style="margin-top:18px">Per versione <span class="muted" style="font-weight:400">· da sempre</span></h3>';
        echo '<table><tr><th>Rilascio</th><th class="r">Download</th></tr>';
        foreach ($rl as $nome => $n)
            echo '<tr><td>' . h($nome) . '</td><td class="r">' . number_format((int)$n, 0, ',', '.') . '</td></tr>';
        echo '</table>';
    }

    if (!empty($det['file'])) {
        echo '<h3 style="margin-top:18px">File per file <span class="muted" style="font-weight:400">· da sempre</span></h3>';
        echo '<table><tr><th>File</th><th class="r">Download</th></tr>';
        foreach ($det['file'] as $v) {
            if ((int)$v['totale'] <= 0) continue;   // i file mai scaricati non dicono niente
            echo '<tr><td>' . h($v['nome'])
               . ' <span class="muted" style="font-size:.8rem">' . h($v['tipo']) . '</span></td>'
               . '<td class="r">' . number_format((int)$v['totale'], 0, ',', '.') . '</td></tr>';
        }
        echo '</table>';
        $zero = 0;
        foreach ($det['file'] as $v) if ((int)$v['totale'] <= 0) $zero++;
        if ($zero) echo '<p class="muted" style="font-size:.82rem;margin-top:8px">'
                      . $zero . ' file non ancora scaricati da nessuno.</p>';
    }
    $eta = time() - (int)$det['aggiornato'];
    echo '<p class="muted" style="font-size:.8rem;margin-top:10px">Dettaglio aggiornato il '
       . h(date('d/m/Y \a\l\l\e H:i', (int)$det['aggiornato'])) . ', ogni 30 minuti'
       . ($eta > 7200 ? ' <strong>(fermo da ' . round($eta / 3600) . ' ore: il raccoglitore '
                      . 'sul container non sta girando)</strong>' : '')
       . '.</p>';
}

echo '<h3 style="margin-top:18px">Ultimi 30 giorni <span class="muted" style="font-weight:400">· da dove arrivano</span></h3>';
if ($sf && isset($sf['total'])) {
    echo '<table><tr><th>Voce</th><th class="r">Download</th></tr>';
    echo '<tr><td><strong>Totale</strong></td><td class="r"><strong>' . (int)$sf['total'] . '</strong></td></tr>';
    if (!empty($sf['countries'])) {
        $obc = $sf['oses_by_country'] ?? array();
        foreach (sfstats_paesi($sf['countries'], 10) as $p) {
            $bandiera = $p['iso'] ? sfstats_flag($p['iso']) . ' ' : '';
            $nome = $p['nome'] === 'Unknown' ? '<span class="muted">paese sconosciuto</span>' : h($p['nome']);
            $sp = sfstats_paesi_os($obc, $p['nome']);
            $nota = '';
            if ($sp !== null && $p['n'] > 0) {
                $q = round(100 * $sp['auto'] / $p['n']);
                $nota = ' <span class="muted" style="font-size:.8rem">· ' . $sp['browser'] . ' da browser'
                      . ($q >= 40 ? ', ' . $q . '% automatici' : '') . '</span>';
            }
            echo '<tr><td>' . $bandiera . $nome . $nota . '</td>'
               . '<td class="r">' . $p['n'] . '</td></tr>';
        }
        echo '<tr><td colspan="2" class="muted" style="font-size:.78rem;padding-top:8px">'
           . 'Il totale di SourceForge conta anche i client torrent, che tirano dai nostri '
           . 'web seed senza dichiarare un browser: dove gli "automatici" sono tanti, il numero '
           . 'di persone sta più vicino alla cifra «da browser».</td></tr>';
    }
    echo '</table>';
} else {
    echo '<p class="muted">' . h($sf_err ?: 'nessun dato disponibile') . '. I numeri completi restano su '
       . '<a href="https://sourceforge.net/projects/skillfishos/files/stats/timeline" target="_blank" rel="noopener">SourceForge</a>.</p>';
}
echo '</div>';

echo '<div class="foot">Dati anonimi (cookieless, IP non memorizzato) · solo sul tuo hosting · SkillFishOS</div>';
echo '</div></body></html>';
