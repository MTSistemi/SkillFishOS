<?php
// SkillFishOS — self-hosted, cookieless visitor analytics (shared library).
// Privacy: no cookies, raw IP never stored (hashed with a rotating daily salt).
// Storage: SQLite, kept OUTSIDE the web root when possible.

if (!defined('SFSTATS_LIB')) {
    define('SFSTATS_LIB', 1);

    function sfstats_dir() {
        // Prefer a dir ABOVE document root (not web-accessible); fall back to a
        // protected dir inside the site if the parent isn't writable.
        $docroot = $_SERVER['DOCUMENT_ROOT'] ?? __DIR__;
        $candidates = array(dirname($docroot) . '/.sfstats', __DIR__ . '/.sfstats');
        foreach ($candidates as $d) {
            if (is_dir($d) || @mkdir($d, 0700, true)) {
                if (is_writable($d)) {
                    // If it sits inside the web root, lock it down.
                    if (strpos(realpath($d), realpath($docroot)) === 0) {
                        $ht = $d . '/.htaccess';
                        if (!is_file($ht)) @file_put_contents($ht, "Require all denied\nDeny from all\n");
                    }
                    return $d;
                }
            }
        }
        return sys_get_temp_dir() . '/.sfstats';
    }

    function sfstats_db() {
        static $db = null;
        if ($db !== null) return $db;
        $dir = sfstats_dir();
        @mkdir($dir, 0700, true);
        $db = new PDO('sqlite:' . $dir . '/stats.db');
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->exec('PRAGMA journal_mode=WAL');
        $db->exec('CREATE TABLE IF NOT EXISTS hits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER NOT NULL, day TEXT NOT NULL,
            path TEXT NOT NULL, ref TEXT NOT NULL DEFAULT "",
            vis TEXT NOT NULL, bot INTEGER NOT NULL DEFAULT 0,
            browser TEXT NOT NULL DEFAULT "", os TEXT NOT NULL DEFAULT "",
            country TEXT NOT NULL DEFAULT "", cname TEXT NOT NULL DEFAULT "",
            ref_full TEXT NOT NULL DEFAULT "")');
        // migrate older databases that predate the new columns
        foreach (array('country','cname','ref_full') as $col) {
            try { $db->exec('ALTER TABLE hits ADD COLUMN ' . $col . ' TEXT NOT NULL DEFAULT ""'); }
            catch (Throwable $e) { /* column already exists */ }
        }
        $db->exec('CREATE INDEX IF NOT EXISTS idx_day ON hits(day)');
        $db->exec('CREATE INDEX IF NOT EXISTS idx_vis ON hits(vis)');

        // ---- doppioni: si tolgono una volta, e poi non tornano piu' --------
        // Nel database c'erano 29 visite e 5 clic registrati DUE VOLTE: stesso
        // secondo, stessa pagina, stesso visitatore. Non e' una persona che
        // ricarica - quella cade in un altro secondo - e' lo stesso evento
        // scritto due volte. Erano lo 0,4%: poco, ma gonfiano ogni conteggio.
        //
        // ⚠️ NON si toccano le visite ravvicinate ma non identiche. Ne avevamo
        // 299 e sembravano lo stesso guaio: non lo erano. Riguardavano l'1,7%
        // dei visitatori e il 76% veniva da CINQUE persone che macinavano
        // pagine - traffico vero, o al limite un raccoglitore che non abbiamo
        // riconosciuto. Cancellarle avrebbe falsato i numeri al ribasso.
        //
        // L'indice unico e' cio' che impedisce il ritorno: da qui in poi un
        // secondo inserimento identico viene semplicemente ignorato (le
        // scritture usano INSERT OR IGNORE), senza errori e senza doppioni.
        $fatto = $dir . '/.doppioni-tolti';
        if (!is_file($fatto)) {
            try {
                $db->exec('DELETE FROM hits WHERE id NOT IN
                           (SELECT MIN(id) FROM hits GROUP BY ts, path, vis)');
                $db->exec('CREATE TABLE IF NOT EXISTS dl(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts INTEGER NOT NULL, day TEXT NOT NULL,
                    file TEXT NOT NULL, kind TEXT NOT NULL DEFAULT "iso",
                    vis TEXT NOT NULL, bot INTEGER NOT NULL DEFAULT 0,
                    country TEXT NOT NULL DEFAULT "", cname TEXT NOT NULL DEFAULT "",
                    lang TEXT NOT NULL DEFAULT "")');
                $db->exec('DELETE FROM dl WHERE id NOT IN
                           (SELECT MIN(id) FROM dl GROUP BY ts, file, vis)');
                $db->exec('CREATE UNIQUE INDEX IF NOT EXISTS idx_unico ON hits(ts, path, vis)');
                $db->exec('CREATE UNIQUE INDEX IF NOT EXISTS idx_unico_dl ON dl(ts, file, vis)');
                @file_put_contents($fatto, gmdate('c') . "
");
            } catch (Throwable $e) {
                // Se qualcosa va storto si riprova al prossimo giro: meglio
                // ritentare che lasciare il segno e non farlo mai piu'.
            }
        }
        return $db;
    }

    // Persistent random secret used to salt visitor hashes.
    function sfstats_secret() {
        $f = sfstats_dir() . '/secret.php';
        if (is_file($f)) { $s = include $f; if ($s) return $s; }
        $s = bin2hex(random_bytes(16));
        @file_put_contents($f, "<?php return '" . $s . "';\n");
        return $s;
    }

    function sfstats_client_ip() {
        $ip = $_SERVER['REMOTE_ADDR'] ?? '';
        if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $parts = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
            $ip = trim($parts[0]);
        }
        return $ip;
    }

    // Cookieless visitor id: changes daily, cannot be reversed to an IP.
    function sfstats_visitor($ua) {
        $day = gmdate('Ymd');
        return substr(hash('sha256', sfstats_secret() . '|' . $day . '|' .
            sfstats_client_ip() . '|' . $ua), 0, 20);
    }

    function sfstats_is_bot($ua) {
        return preg_match('/bot|crawl|spider|slurp|bing|google|yandex|baidu|duckduck|'
            . 'facebookexternal|preview|monitor|curl|wget|python-requests|headless|'
            . 'lighthouse|pingdom|uptime|semrush|ahrefs|mj12|dotbot/i', $ua) ? 1 : 0;
    }

    function sfstats_browser($ua) {
        if (preg_match('/Edg/i', $ua)) return 'Edge';
        if (preg_match('/OPR|Opera/i', $ua)) return 'Opera';
        if (preg_match('/Firefox/i', $ua)) return 'Firefox';
        if (preg_match('/Chrome|Chromium/i', $ua)) return 'Chrome';
        if (preg_match('/Safari/i', $ua)) return 'Safari';
        return 'Altro';
    }

    // Country from OVH/Apache mod_geoip (server-side, IP never leaves the host).
    function sfstats_country() {
        $code = strtoupper(substr((string)($_SERVER['GEOIP_COUNTRY_CODE'] ?? ''), 0, 2));
        $name = (string)($_SERVER['GEOIP_COUNTRY_NAME'] ?? '');
        if ($code && !$name) $name = $code;
        return array($code, substr($name, 0, 60));
    }

    // Two-letter country code -> flag emoji (regional indicators), with fallback.
    function sfstats_flag($code) {
        $code = strtoupper((string)$code);
        if (strlen($code) !== 2 || !ctype_alpha($code)) return '🏳️';
        $a = function_exists('mb_chr') ? 'mb_chr' : null;
        $f = '';
        for ($i = 0; $i < 2; $i++) {
            $cp = 0x1F1E6 + (ord($code[$i]) - 65);
            $f .= $a ? mb_chr($cp, 'UTF-8')
                     : html_entity_decode('&#' . $cp . ';', ENT_QUOTES, 'UTF-8');
        }
        return $f;
    }


    // ⚠️ SourceForge manda i paesi come LISTA DI COPPIE — [["Kenya",435], ...] —
    // e con nomi per esteso, non codici ISO. Il codice che la trattava come una
    // mappa stampava l'indice numerico al posto del paese, una bandierina di
    // ripiego sempre uguale, e un conteggio sempre 1 (in PHP (int) su un array
    // fa 1). Qui si normalizza una volta sola: dentro o fuori, sempre
    // [nome, quanti, codice ISO].
    function sfstats_iso($nome) {
        static $m = array(
        'Algeria'                  => 'DZ',
        'Argentina'                => 'AR',
        'Australia'                => 'AU',
        'Austria'                  => 'AT',
        'Belgium'                  => 'BE',
        'Bolivia'                  => 'BO',
        'Brazil'                   => 'BR',
        'Bulgaria'                 => 'BG',
        'Canada'                   => 'CA',
        'Chile'                    => 'CL',
        'China'                    => 'CN',
        'Colombia'                 => 'CO',
        'Costa Rica'               => 'CR',
        'Croatia'                  => 'HR',
        'Cyprus'                   => 'CY',
        'Czech Republic'           => 'CZ',
        'Czechia'                  => 'CZ',
        'Denmark'                  => 'DK',
        'Dominican Republic'       => 'DO',
        'Egypt'                    => 'EG',
        'El Salvador'              => 'SV',
        'Estonia'                  => 'EE',
        'Finland'                  => 'FI',
        'France'                   => 'FR',
        'Germany'                  => 'DE',
        'Greece'                   => 'GR',
        'Guadeloupe'               => 'GP',
        'Guatemala'                => 'GT',
        'Hong Kong'                => 'HK',
        'Hungary'                  => 'HU',
        'India'                    => 'IN',
        'Indonesia'                => 'ID',
        'Ireland'                  => 'IE',
        'Israel'                   => 'IL',
        'Italy'                    => 'IT',
        'Japan'                    => 'JP',
        'Kenya'                    => 'KE',
        'Korea'                    => 'KR',
        'Latvia'                   => 'LV',
        'Lebanon'                  => 'LB',
        'Lithuania'                => 'LT',
        'Luxembourg'               => 'LU',
        'Malaysia'                 => 'MY',
        'Mexico'                   => 'MX',
        'Morocco'                  => 'MA',
        'Netherlands'              => 'NL',
        'New Zealand'              => 'NZ',
        'Norway'                   => 'NO',
        'Pakistan'                 => 'PK',
        'Peru'                     => 'PE',
        'Philippines'              => 'PH',
        'Poland'                   => 'PL',
        'Portugal'                 => 'PT',
        'Romania'                  => 'RO',
        'Russia'                   => 'RU',
        'Russian Federation'       => 'RU',
        'Saudi Arabia'             => 'SA',
        'Serbia'                   => 'RS',
        'Seychelles'               => 'SC',
        'Singapore'                => 'SG',
        'Slovakia'                 => 'SK',
        'Slovenia'                 => 'SI',
        'South Africa'             => 'ZA',
        'South Korea'              => 'KR',
        'Spain'                    => 'ES',
        'Sweden'                   => 'SE',
        'Switzerland'              => 'CH',
        'Taiwan'                   => 'TW',
        'Thailand'                 => 'TH',
        'Trinidad and Tobago'      => 'TT',
        'Tunisia'                  => 'TN',
        'Turkey'                   => 'TR',
        'Ukraine'                  => 'UA',
        'United Arab Emirates'     => 'AE',
        'United Kingdom'           => 'GB',
        'United States'            => 'US',
        'Uruguay'                  => 'UY',
        'Venezuela'                => 'VE',
        'Viet Nam'                 => 'VN',
        'Vietnam'                  => 'VN'
        );
        $n = trim((string)$nome);
        if (isset($m[$n])) return $m[$n];
        // gia' un codice a due lettere? capita con altre fonti
        if (strlen($n) === 2 && ctype_alpha($n)) return strtoupper($n);
        return '';
    }

    function sfstats_paesi($dato, $quanti = 8) {
        $out = array();
        foreach ((array)$dato as $k => $v) {
            if (is_array($v)) {                 // ["Kenya", 435]
                $nome = (string)($v[0] ?? '');
                $n    = (int)($v[1] ?? 0);
            } else {                             // "Kenya" => 435
                $nome = (string)$k;
                $n    = (int)$v;
            }
            if ($nome === '') continue;
            $out[] = array('nome' => $nome, 'n' => $n, 'iso' => sfstats_iso($nome));
        }
        usort($out, function ($a, $b) { return $b['n'] - $a['n']; });
        return $quanti ? array_slice($out, 0, $quanti) : $out;
    }


    // Spacca i download di un paese fra browser riconosciuti e "Unknown".
    // ⚠️ Unknown non vuol dire per forza robot: chi usa wget, aria2 o un client
    // torrent (i nostri .torrent hanno SourceForge come web seed) e' una persona
    // vera che finisce li' dentro. Serve a non leggere il totale grezzo come
    // "utenti": il Kenya, 435 su 435 Unknown e una sola visita al sito, non e'
    // 435 persone.
    function sfstats_paesi_os($obc, $nome) {
        $o = null;
        if (is_array($obc)) {
            if (isset($obc[$nome]) && is_array($obc[$nome])) $o = $obc[$nome];
            else foreach ($obc as $v) {
                if (is_array($v) && isset($v[0]) && $v[0] === $nome && isset($v[1]) && is_array($v[1])) { $o = $v[1]; break; }
            }
        }
        if (!is_array($o)) return null;
        $unk = 0; $br = 0;
        foreach ($o as $k => $n) {
            if ((string)$k === 'Unknown') $unk += (int)$n; else $br += (int)$n;
        }
        return array('browser' => $br, 'auto' => $unk);
    }

    function sfstats_os($ua) {
        if (preg_match('/Android/i', $ua)) return 'Android';
        if (preg_match('/iPhone|iPad|iOS/i', $ua)) return 'iOS';
        if (preg_match('/Windows/i', $ua)) return 'Windows';
        if (preg_match('/Mac OS X|Macintosh/i', $ua)) return 'macOS';
        if (preg_match('/Linux/i', $ua)) return 'Linux';
        return 'Altro';
    }
}
