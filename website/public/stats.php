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

page_head('SkillFishOS · Statistiche');
echo '<div class="wrap">';
echo '<header><div class="brand">SkillFish<span class="g">OS</span> · Statistiche</div><div class="sp"></div>';
echo '<a class="ghost" href="?' . ($incl_bots ? '' : 'bots=1') . '">' . ($incl_bots ? 'Escludi bot' : 'Includi bot') . '</a>';
echo '<form method="post" style="display:inline"><input type="hidden" name="action" value="logout"><button class="ghost" type="submit">Esci</button></form>';
echo '</header>';

// KPIs
$kpi = function ($n, $l) { echo '<div class="kpi"><div class="n">' . number_format($n, 0, ',', '.') . '</div><div class="l">' . h($l) . '</div></div>'; };
echo '<div class="kpis">';
$kpi($views_today, 'Visite oggi'); $kpi($uniq_today, 'Visitatori oggi');
$kpi($views_7, 'Visite 7 giorni'); $kpi($uniq_7, 'Visitatori 7 giorni');
$kpi($views_30, 'Visite 30 giorni'); $kpi($views_total, 'Visite totali');
echo '</div>';

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

echo '<div class="foot">Dati anonimi (cookieless, IP non memorizzato) · solo sul tuo hosting · SkillFishOS</div>';
echo '</div></body></html>';
