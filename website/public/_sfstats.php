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

    function sfstats_os($ua) {
        if (preg_match('/Android/i', $ua)) return 'Android';
        if (preg_match('/iPhone|iPad|iOS/i', $ua)) return 'iOS';
        if (preg_match('/Windows/i', $ua)) return 'Windows';
        if (preg_match('/Mac OS X|Macintosh/i', $ua)) return 'macOS';
        if (preg_match('/Linux/i', $ua)) return 'Linux';
        return 'Altro';
    }
}
