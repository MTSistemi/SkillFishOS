"use strict";
// SkillFishOS Remote Manager - dynamic, module-composed dashboard frontend (IT/EN).
const $ = (s, r = document) => r.querySelector(s);
const api = (p, opt) => fetch(p, Object.assign({ credentials: "same-origin" }, opt));
const post = (p, body) => api(p, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });

// ---------------- i18n ----------------
// Il rilevamento riconosceva SOLO l'italiano e mandava tutti gli altri
// sull'inglese, polacchi e ucraini compresi. Ora si guarda il prefisso della
// lingua del browser; se non e' una delle nostre resta l'inglese, che e' il
// ripiego giusto.
let LANG = localStorage.getItem("sflang") || (function () {
  var n = (navigator.language || "en").toLowerCase();
  if (n.startsWith("it")) return "it";
  if (n.startsWith("pl")) return "pl";
  if (n.startsWith("uk") || n.startsWith("ua")) return "uk";
  return "en";
})();
const STR = {
  x_zthint: { it: "Dopo «Entra», autorizza il nodo su my.zerotier.com. Poi raggiungi la dashboard da ovunque: https://&lt;IP ZeroTier&gt;:8443",
              en: "After Join, authorize the node on my.zerotier.com. Then reach the dashboard from anywhere: https://&lt;ZeroTier IP&gt;:8443",
              pl: "Po «Dołącz» autoryzuj węzeł na my.zerotier.com. Potem otwórz panel z dowolnego miejsca: https://&lt;IP ZeroTier&gt;:8443",
              uk: "Після «Приєднатися» авторизуйте вузол на my.zerotier.com. Далі відкривайте панель звідусіль: https://&lt;IP ZeroTier&gt;:8443" },
  x_ztsent: { it: "Richiesta inviata — autorizza su my.zerotier.com",
              en: "Request sent — authorize on my.zerotier.com",
              pl: "Wysłano prośbę — autoryzuj na my.zerotier.com",
              uk: "Запит надіслано — авторизуйте на my.zerotier.com" },
  x_kvhint2: { it: "q8_0 dimezza la KV cache (più contesto). Sbloccare la GTT permette modelli più grandi ma richiede il riavvio.", en: "q8_0 halves the KV cache (more context). Unlocking GTT allows bigger models but needs a reboot.", pl: "q8_0 zmniejsza KV cache o połowę (więcej kontekstu). Odblokowanie GTT pozwala na większe modele, ale wymaga restartu.", uk: "q8_0 зменшує KV cache удвічі (більше контексту). Розблокування GTT дозволяє більші моделі, але потребує перезавантаження." },
  x_qgtt: { it: "Sbloccare la GTT? Modifica il boot e richiede il RIAVVIO.", en: "Unlock GTT? Edits boot config, needs a REBOOT.", pl: "Odblokować GTT? Zmienia konfigurację startu i wymaga RESTARTU.", uk: "Розблокувати GTT? Змінює конфігурацію завантаження і потребує ПЕРЕЗАВАНТАЖЕННЯ." },
  x_qkv: { it: "KV cache → q8_0? Riavvia il motore AI locale.", en: "KV cache → q8_0? Restarts the local AI engine.", pl: "KV cache → q8_0? Uruchamia ponownie lokalny silnik SI.", uk: "KV cache → q8_0? Перезапускає локальний рушій ШІ." },
  x_open: { it: "Apri ", en: "Open ", pl: "Otwórz ", uk: "Відкрити " },
  // Chiavi arrivate dallo schema `const it = LANG === "it"` + `it ? ... : ...`,
  // che era testo fuori dal dizionario: chi non usava italiano o inglese
  // vedeva l'inglese comunque, qualunque lingua avesse scelto.
  x_ctx: { it: "Contesto", en: "Context", pl: "Kontekst", uk: "Контекст" },
  x_gttcap: { it: "Cap GTT", en: "GTT cap", pl: "Limit GTT", uk: "Ліміт GTT" },
  x_unlocked: { it: "sbloccato", en: "unlocked", pl: "odblokowane", uk: "розблоковано" },
  x_kv: { it: "KV cache q8_0", en: "KV cache q8_0", pl: "KV cache q8_0", uk: "KV cache q8_0" },
  x_gttbtn: { it: "Sblocca GTT (riavvio)", en: "Unlock GTT (reboot)", pl: "Odblokuj GTT (restart)", uk: "Розблокувати GTT (перезавантаження)" },
  x_optdone: { it: "Già ottimizzato ✓", en: "Already optimized ✓", pl: "Już zoptymalizowane ✓", uk: "Уже оптимізовано ✓" },
  x_applying: { it: "Applico…", en: "Applying…", pl: "Stosowanie…", uk: "Застосування…" },
  x_mods: { it: "Moduli esposti", en: "Exposed modules", pl: "Udostępnione moduły", uk: "Відкриті модулі" },
  x_updated: { it: "Aggiornato", en: "Updated", pl: "Zaktualizowano", uk: "Оновлено" },
  x_localai: { it: "AI locale", en: "On-device AI", pl: "SI lokalna", uk: "Локальний ШІ" },
  x_nomodels: { it: "nessun modello installato", en: "no models installed", pl: "brak zainstalowanych modeli", uk: "моделі не встановлені" },
  x_engine: { it: "Motore", en: "Engine", pl: "Silnik", uk: "Рушій" },
  x_accel: { it: "Accelerazione", en: "Acceleration", pl: "Akceleracja", uk: "Прискорення" },
  x_apikey: { it: "Chiave API di Unsloth", en: "Unsloth API key", pl: "Klucz API Unsloth", uk: "Ключ API Unsloth" },
  x_save: { it: "Salva", en: "Save", pl: "Zapisz", uk: "Зберегти" },
  x_first: { it: "Primo accesso a Unsloth Studio", en: "First sign-in to Unsloth Studio", pl: "Pierwsze logowanie do Unsloth Studio", uk: "Перший вхід до Unsloth Studio" },
  x_user: { it: "Utente", en: "User", pl: "Użytkownik", uk: "Користувач" },
  x_initpw: { it: "Password iniziale", en: "Initial password", pl: "Hasło początkowe", uk: "Початковий пароль" },
  x_chat: { it: "Chat", en: "Chat", pl: "Czat", uk: "Чат" },
  x_models: { it: "Modelli installati", en: "Installed models", pl: "Zainstalowane modele", uk: "Встановлені моделі" },
  x_pullph: { it: "scarica modello (es. qwen3:14b)", en: "pull model (e.g. qwen3:14b)", pl: "pobierz model (np. qwen3:14b)", uk: "завантажити модель (напр. qwen3:14b)" },
  x_pull: { it: "Scarica", en: "Pull", pl: "Pobierz", uk: "Завантажити" },
  x_optai: { it: "Ottimizza per AI", en: "Optimize for AI", pl: "Zoptymalizuj pod SI", uk: "Оптимізувати для ШІ" },
  x_keysaved: { it: "Chiave salvata", en: "Key saved", pl: "Zapisano klucz", uk: "Ключ збережено" },
  x_dlstart: { it: "Download avviato…", en: "Download started…", pl: "Rozpoczęto pobieranie…", uk: "Завантаження розпочато…" },
  x_nonet: { it: "Nessuna rete.", en: "No networks.", pl: "Brak sieci.", uk: "Немає мереж." },
  x_node: { it: "Nodo", en: "Node", pl: "Węzeł", uk: "Вузол" },
  x_state: { it: "Stato", en: "Status", pl: "Stan", uk: "Стан" },
  x_nets: { it: "Reti", en: "Networks", pl: "Sieci", uk: "Мережі" },
  x_join: { it: "Entra", en: "Join", pl: "Dołącz", uk: "Приєднатися" },
  x_left: { it: "Uscito dalla rete", en: "Left network", pl: "Opuszczono sieć", uk: "Мережу покинуто" },
  x_closed: { it: "Schede chiuse", en: "Closed cards", pl: "Zamknięte karty", uk: "Закриті картки" },
  // Chiavi arrivate dai ternari LANG === "it" ? ... : ... , che erano
  // testo fuori dal dizionario e quindi NON traducibile in altre lingue.
  ly_saved: { it: "Disposizione salvata", en: "Layout saved", pl: "Zapisano układ", uk: "Розташування збережено" },
  m_telem: { it: "Telemetria", en: "Telemetry", pl: "Telemetria", uk: "Телеметрія" },
  m_sys: { it: "Stato sistema", en: "System status", pl: "Stan systemu", uk: "Стан системи" },
  m_ctrl: { it: "Controlli", en: "Controls", pl: "Sterowanie", uk: "Керування" },
  m_apps: { it: "App e pacchetti", en: "Apps & packages", pl: "Aplikacje i pakiety", uk: "Програми та пакунки" },
  m_launch: { it: "Avvio app", en: "Launcher", pl: "Uruchamianie aplikacji", uk: "Запуск програм" },
  m_term: { it: "Terminale", en: "Terminal", pl: "Terminal", uk: "Термінал" },
  m_rules: { it: "Regole auto", en: "Auto rules", pl: "Reguły automatyczne", uk: "Автоматичні правила" },
  m_soon: { it: "Modulo attivo — interfaccia in arrivo.", en: "Module on — UI coming soon.", pl: "Moduł włączony — interfejs wkrótce.", uk: "Модуль увімкнено — інтерфейс незабаром." },
  w_move: { it: "Sposta", en: "Move", pl: "Przenieś", uk: "Перемістити" },
  w_coll: { it: "Comprimi", en: "Collapse", pl: "Zwiń", uk: "Згорнути" },
  w_close: { it: "Chiudi", en: "Close", pl: "Zamknij", uk: "Закрити" },
  ly_reset: { it: "Ripristinare la disposizione predefinita?", en: "Reset to the default layout?", pl: "Przywrócić domyślny układ?", uk: "Відновити типове розташування?" },
  login_sub: { it: "SkillFishOS · accedi con le credenziali di sistema", en: "SkillFishOS · sign in with your system credentials", pl: "SkillFishOS · zaloguj się danymi systemowymi", uk: "SkillFishOS · увійдіть за системними обліковими даними" },
  user: { it: "Utente", en: "User", pl: "Użytkownik", uk: "Користувач" }, pass: { it: "Password", en: "Password", pl: "Hasło", uk: "Пароль" },
  enter: { it: "Entra", en: "Sign in", pl: "Zaloguj się", uk: "Увійти" }, denied: { it: "accesso negato", en: "access denied", pl: "odmowa dostępu", uk: "доступ заборонено" },
  logout: { it: "Esci", en: "Log out", pl: "Wyloguj", uk: "Вийти" }, neterr: { it: "errore di rete", en: "network error", pl: "błąd sieci", uk: "помилка мережі" },
  copied: { it: "Copiato", en: "Copied", pl: "Skopiowano", uk: "Скопійовано" }, done: { it: "fatto", en: "done", pl: "gotowe", uk: "готово" },
  g_monitor: { it: "Monitoraggio", en: "Monitoring", pl: "Monitorowanie", uk: "Моніторинг" }, g_control: { it: "Controllo", en: "Control", pl: "Sterowanie", uk: "Керування" },
  g_remote: { it: "Accesso remoto", en: "Remote access", pl: "Dostęp zdalny", uk: "Віддалений доступ" }, g_ai: { it: "Intelligenza artificiale", en: "AI", pl: "SI", uk: "ШІ" },
  g_other: { it: "Altro", en: "Other", pl: "Inne", uk: "Інше" },
  // telemetry
  t_temp: { it: "Temperatura", en: "Temperature", pl: "Temperatura", uk: "Температура" }, t_load: { it: "Carico", en: "Load", pl: "Obciążenie", uk: "Навантаження" },
  t_freq: { it: "Frequenza", en: "Frequency", pl: "Częstotliwość", uk: "Частота" }, t_pow: { it: "Potenza", en: "Power", pl: "Moc", uk: "Потужність" },
  t_volt: { it: "Voltaggio", en: "Voltage", pl: "Napięcie", uk: "Напруга" }, t_fan: { it: "Ventola", en: "Fan", pl: "Wentylator", uk: "Вентилятор" }, live: { it: "live", en: "live", pl: "na żywo", uk: "наживо" },
  t_percore: { it: "Frequenza per core/thread", en: "Per core/thread frequency", pl: "Częstotliwość na rdzeń/wątek", uk: "Частота на ядро/потік" },
  c_off: { it: "off", en: "off", pl: "wył.", uk: "вимк." }, c_avg: { it: "med", en: "avg", pl: "śr.", uk: "сер." }, c_online: { it: "attivi", en: "online", pl: "aktywne", uk: "активні" },
  // status
  s_you: { it: "Sei connesso a", en: "Connected to", pl: "Połączono z", uk: "З'єднано з" }, s_host: { it: "Host", en: "Host", pl: "Host", uk: "Вузол" },
  s_ip: { it: "IP (rotta)", en: "IP (route)", pl: "IP (trasa)", uk: "IP (маршрут)" }, s_kernel: { it: "Kernel", en: "Kernel", pl: "Jądro", uk: "Ядро" },
  s_up: { it: "Uptime", en: "Uptime", pl: "Czas działania", uk: "Час роботи" }, s_cu: { it: "CU attive", en: "Active CUs", pl: "Aktywne CU", uk: "Активні CU" }, s_ram: { it: "RAM", en: "RAM", pl: "RAM", uk: "RAM" },
  s_disk: { it: "Disco /", en: "Disk /", pl: "Dysk /", uk: "Диск /" }, s_frz: { it: "Freeze rilevati", en: "Freezes detected", pl: "Wykryte zawieszenia", uk: "Виявлені зависання" },
  // tuner
  c_preset: { it: "Preset", en: "Presets", pl: "Profile", uk: "Профілі" }, c_gov: { it: "Governor GPU", en: "GPU governor", pl: "Regulator GPU", uk: "Регулятор ГП" },
  c_bal: { it: "Bilanciato", en: "Balanced", pl: "Zrównoważony", uk: "Збалансований" }, c_perf: { it: "Performance", en: "Performance", pl: "Wydajność", uk: "Продуктивність" },
  c_fan: { it: "Ventola", en: "Fan", pl: "Wentylator", uk: "Вентилятор" }, c_auto: { it: "Auto", en: "Auto", pl: "Auto", uk: "Авто" }, c_man: { it: "Manuale", en: "Manual", pl: "Ręcznie", uk: "Вручну" },
  c_applied: { it: "Preset {x} applicato", en: "Preset {x} applied", pl: "Zastosowano profil {x}", uk: "Застосовано профіль {x}" },
  c_full: { it: "Apri Tuner completo", en: "Open full Tuner", pl: "Otwórz pełny Tuner", uk: "Відкрити повний Tuner" },
  // hub
  h_open: { it: "Apri Hub", en: "Open Hub", pl: "Otwórz Hub", uk: "Відкрити Hub" }, h_updates: { it: "aggiornamenti", en: "updates", pl: "aktualizacji", uk: "оновлень" },
  // power
  p_reboot: { it: "Riavvia", en: "Reboot", pl: "Uruchom ponownie", uk: "Перезавантажити" }, p_off: { it: "Spegni", en: "Shut down", pl: "Wyłącz", uk: "Вимкнути" },
  p_conf: { it: "Richiede conferma.", en: "Asks for confirmation.", pl: "Poprosi o potwierdzenie.", uk: "Запитає підтвердження." },
  p_qreb: { it: "Riavviare la BC-250?", en: "Reboot the BC-250?", pl: "Uruchomić ponownie BC-250?", uk: "Перезавантажити BC-250?" }, p_qoff: { it: "Spegnere la BC-250?", en: "Shut down the BC-250?", pl: "Wyłączyć BC-250?", uk: "Вимкнути BC-250?" },
  p_rebing: { it: "Riavvio…", en: "Rebooting…", pl: "Ponowne uruchamianie…", uk: "Перезавантаження…" }, p_offing: { it: "Spegnimento…", en: "Shutting down…", pl: "Wyłączanie…", uk: "Вимкнення…" },
  // logs / launcher / rec
  l_refresh: { it: "aggiorna", en: "refresh", pl: "odśwież", uk: "оновити" }, empty: { it: "(vuoto)", en: "(empty)", pl: "(pusto)", uk: "(порожньо)" },
  la_hint: { it: "Si apre sullo schermo della scheda.", en: "Opens on the board's screen.", pl: "Otwiera się na ekranie płyty.", uk: "Відкриється на екрані плати." },
  la_started: { it: "Avviato: {x}", en: "Launched: {x}", pl: "Uruchomiono: {x}", uk: "Запущено: {x}" },
  r_none: { it: "Nessuna registrazione.", en: "No recordings.", pl: "Brak nagrań.", uk: "Немає записів." }, r_saved: { it: "Registrazione salvata", en: "Recording saved", pl: "Nagranie zapisane", uk: "Запис збережено" },
  r_started: { it: "Registrazione avviata", en: "Recording started", pl: "Rozpoczęto nagrywanie", uk: "Запис розпочато" },
  // kvm / terminal
  k_open: { it: "▶ Apri desktop remoto", en: "▶ Open remote desktop", pl: "▶ Otwórz zdalny pulpit", uk: "▶ Відкрити віддалений робочий стіл" },
  k_hint: { it: "Schermo, tastiera e mouse della scheda — stessa sessione, nessuna password in più.", en: "Screen, keyboard and mouse of the board — same session, no extra password.", pl: "Ekran, klawiatura i mysz płyty — ta sama sesja, bez dodatkowego hasła.", uk: "Екран, клавіатура і миша плати — та сама сесія, без додаткового пароля." },
  k_ready: { it: "Desktop pronto", en: "Desktop ready", pl: "Pulpit gotowy", uk: "Робочий стіл готовий" }, k_vncpw: { it: "Aperto. Password VNC (se richiesta): ", en: "Opened. VNC password (if asked): ", pl: "Otwarto. Hasło VNC (jeśli zapyta): ", uk: "Відкрито. Пароль VNC (якщо запитає): " },
  term_open: { it: "▶ Apri terminale", en: "▶ Open terminal", pl: "▶ Otwórz terminal", uk: "▶ Відкрити термінал" },
  term_hint: { it: "Shell della scheda — stessa sessione, nessuna password in più.", en: "Board shell — same session, no extra password.", pl: "Powłoka płyty — ta sama sesja, bez dodatkowego hasła.", uk: "Оболонка плати — та сама сесія, без додаткового пароля." },
  // ai
  ai_engine: { it: "Motore", en: "Engine", pl: "Silnik", uk: "Рушій" }, ai_on: { it: "● acceso", en: "● on", pl: "● wł.", uk: "● увімк." }, ai_off: { it: "○ spento", en: "○ off", pl: "○ wył.", uk: "○ вимк." },
  ai_start: { it: "▶ Accendi AI", en: "▶ Turn on AI", pl: "▶ Włącz SI", uk: "▶ Увімкнути ШІ" }, ai_stop: { it: "■ Spegni AI", en: "■ Turn off AI", pl: "■ Wyłącz SI", uk: "■ Вимкнути ШІ" },
  ai_open: { it: "Apri l’interfaccia ↗", en: "Open the UI ↗", pl: "Otwórz interfejs ↗", uk: "Відкрити інтерфейс ↗" }, ai_ready: { it: "● pronto", en: "● ready", pl: "● gotowy", uk: "● готово" },
  ai_hint: { it: "Lo stack gira sulla GPU: spegnilo quando giochi.", en: "The stack runs on the GPU: turn it off when gaming.", pl: "Silnik działa na GPU: wyłącz go przed graniem.", uk: "Рушій працює на ГП: вимкніть його перед грою." },
  ai_starting: { it: "Avvio AI… (può richiedere un minuto)", en: "Starting AI… (may take a minute)", pl: "Uruchamianie SI… (może potrwać minutę)", uk: "Запуск ШІ… (може зайняти хвилину)" }, ai_stopping: { it: "Spengo AI", en: "Stopping AI", pl: "Zatrzymywanie SI", uk: "Зупинка ШІ" },
  // wol
  w_wol: { it: "Wake-on-LAN", en: "Wake-on-LAN", pl: "Wake-on-LAN", uk: "Wake-on-LAN" }, w_en: { it: "● abilitato", en: "● enabled", pl: "● włączone", uk: "● увімкнено" }, w_dis: { it: "○ disabilitato", en: "○ disabled", pl: "○ wyłączone", uk: "○ вимкнено" },
  w_enbtn: { it: "Abilita WoL", en: "Enable WoL", pl: "Włącz WoL", uk: "Увімкнути WoL" }, w_disbtn: { it: "Disabilita WoL", en: "Disable WoL", pl: "Wyłącz WoL", uk: "Вимкнути WoL" },
  w_wake: { it: "Sveglia un altro dispositivo", en: "Wake another device", pl: "Obudź inne urządzenie", uk: "Розбудити інший пристрій" }, w_send: { it: "Invia", en: "Send", pl: "Wyślij", uk: "Надіслати" }, w_sent: { it: "Magic packet inviato", en: "Magic packet sent", pl: "Wysłano magic packet", uk: "Magic packet надіслано" },
  w_sched: { it: "Programma spegnimento/riavvio", en: "Schedule power off/reboot", pl: "Zaplanuj wyłączenie/restart", uk: "Запланувати вимкнення/перезавантаження" }, w_cancel: { it: "Annulla", en: "Cancel", pl: "Anuluj", uk: "Скасувати" },
  w_qreb: { it: "Riavviare tra {x} min?", en: "Reboot in {x} min?", pl: "Uruchomić ponownie za {x} min?", uk: "Перезавантажити через {x} хв?" }, w_qoff: { it: "Spegnere tra {x} min?", en: "Shut down in {x} min?", pl: "Wyłączyć za {x} min?", uk: "Вимкнути через {x} хв?" },
  w_updated: { it: "WoL aggiornato", en: "WoL updated", pl: "Zaktualizowano WoL", uk: "WoL оновлено" }, w_rsched: { it: "Riavvio programmato", en: "Reboot scheduled", pl: "Zaplanowano ponowne uruchomienie", uk: "Перезавантаження заплановано" }, w_osched: { it: "Spegnimento programmato", en: "Shutdown scheduled", pl: "Zaplanowano wyłączenie", uk: "Вимкнення заплановано" }, w_canc: { it: "Programmazione annullata", en: "Schedule cancelled", pl: "Anulowano plan", uk: "Планування скасовано" },
  // rules
  ru_throttle: { it: "Auto-throttle a Stock se troppo caldo", en: "Auto-throttle to Stock when too hot", pl: "Automatycznie na Stock przy przegrzaniu", uk: "Автоматично на Stock при перегріві" },
  ru_thresh: { it: "Soglia", en: "Threshold", pl: "Próg", uk: "Поріг" }, ru_last: { it: "Ultima azione", en: "Last action", pl: "Ostatnia akcja", uk: "Остання дія" },
  ru_on: { it: "● attivo", en: "● on", pl: "● wł.", uk: "● увімк." }, ru_off: { it: "○ spento", en: "○ off", pl: "○ wył.", uk: "○ вимк." }, ru_enable: { it: "Attiva", en: "Enable", pl: "Włącz", uk: "Увімкнути" }, ru_disable: { it: "Disattiva", en: "Disable", pl: "Wyłącz", uk: "Вимкнути" },
  ru_set: { it: "Imposta", en: "Set", pl: "Ustaw", uk: "Встановити" }, ru_updated: { it: "Regola aggiornata", en: "Rule updated", pl: "Zaktualizowano regułę", uk: "Правило оновлено" }, ru_setdone: { it: "Soglia impostata", en: "Threshold set", pl: "Ustawiono próg", uk: "Поріг встановлено" },
  ru_frame: { it: "Ultimo fotogramma dello schermo", en: "Last screen frame", pl: "Ostatnia klatka ekranu", uk: "Останній кадр екрана" }, ru_noframe: { it: "Nessun fotogramma ancora (attiva il modulo e attendi ~20s).", en: "No frame yet (enable the module and wait ~20s).", pl: "Brak klatki (włącz moduł i poczekaj ~20 s).", uk: "Кадру ще немає (увімкніть модуль і зачекайте ~20 с)." },
  // aiops
  ao_q: { it: "Domanda (opzionale): perché si è bloccata?", en: "Question (optional): why did it freeze?", pl: "Pytanie (opcjonalnie): dlaczego się zawiesiło?", uk: "Питання (необов'язково): чому воно зависло?" },
  ao_btn: { it: "Diagnostica", en: "Diagnose", pl: "Diagnozuj", uk: "Діагностувати" }, ao_running: { it: "Analisi in corso col modello locale… (può richiedere un minuto)", en: "Analyzing with the local model… (may take a minute)", pl: "Analiza modelem lokalnym… (może potrwać minutę)", uk: "Аналіз локальною моделлю… (може зайняти хвилину)" },
  ao_hint: { it: "Il modello locale legge log e telemetria e spiega cosa succede. Richiede il motore AI acceso.", en: "The local model reads logs and telemetry and explains what's going on. Needs the AI engine on.", pl: "Model lokalny czyta logi i telemetrię i wyjaśnia, co się dzieje. Wymaga włączonego silnika SI.", uk: "Локальна модель читає журнали й телеметрію і пояснює, що відбувається. Потрібен увімкнений рушій ШІ." },
  ao_none: { it: "(nessuna risposta)", en: "(no answer)", pl: "(brak odpowiedzi)", uk: "(немає відповіді)" }, err: { it: "Errore: ", en: "Error: ", pl: "Błąd:", uk: "Помилка:" },
};
function T(k, vars) {
  let s = (STR[k] && STR[k][LANG]) || (STR[k] && STR[k].en) || k;
  if (vars) for (const v in vars) s = s.replace("{" + v + "}", vars[v]);
  return s;
}

function toast(msg, ok = true) {
  let t = $("#toast");
  if (!t) { t = document.createElement("div"); t.id = "toast"; document.body.appendChild(t); }
  t.textContent = msg; t.style.cssText =
    "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:99;padding:10px 18px;border-radius:10px;" +
    "font-weight:600;font-size:.9rem;color:#1a130a;background:" + (ok ? "#d8a849" : "#e07b5a") +
    ";box-shadow:0 8px 24px rgba(0,0,0,.5);opacity:1;transition:opacity .4s";
  clearTimeout(toast._t); toast._t = setTimeout(() => { t.style.opacity = "0"; }, 2200);
}
async function action(p, body, okmsg) {
  try { const j = await (await post(p, body)).json(); toast(j.ok === false ? (j.error || T("err").trim()) : (okmsg || T("done")), j.ok !== false); return j; }
  catch (e) { toast(T("neterr"), false); }
}
// centered modal with an embedded web app (same-origin via the dashboard proxy)
function openFrame(title, url) {
  let m = $("#frame");
  if (!m) {
    m = document.createElement("div"); m.id = "frame";
    m.innerHTML = '<div class="fr-box"><div class="fr-bar"><span class="fr-title"></span><span class="fr-sp"></span><button class="fr-btn" id="fr-pop" title="Nuova scheda">⤢</button><button class="fr-btn" id="fr-x">✕</button></div><iframe class="fr-if" allow="clipboard-read; clipboard-write"></iframe></div>';
    document.body.appendChild(m);
    const close = () => { m.style.display = "none"; $(".fr-if", m).src = "about:blank"; };
    $("#fr-x", m).onclick = close;
    $("#fr-pop", m).onclick = () => window.open($(".fr-if", m).dataset.url, "_blank");
    m.addEventListener("click", e => { if (e.target === m) close(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && m.style.display === "flex") close(); });
  }
  $(".fr-title", m).textContent = title;
  const f = $(".fr-if", m); f.dataset.url = url; f.src = url; m.style.display = "flex";
}
// "Optimize for AI" (#5): show current tuning + apply recommended tweaks
async function aiTune(card, it) {
  const box = card.querySelector("#aitune"); if (!box) return;
  box.innerHTML = '<div class="stub">…</div>';
  let s; try { s = await (await api("/api/ai/tune")).json(); } catch (e) { box.innerHTML = '<div class="stub">errore</div>'; return; }
  const row = (a, b) => `<div class="r"><span>${a}</span><span>${b}</span></div>`;
  // KV cache, contesto e flash-attention sono parametri del compose di Ollama:
  // con Unsloth stanno dentro Studio, quindi qui restano solo le leve di sistema.
  const uns = s.engine === "unsloth";
  let h = '<div class="rows" style="margin-top:8px">' +
    (uns ? "" : row("KV cache", s.kv_cache || "-") + row(T("x_ctx"), s.context || "-")) +
    row(T("x_gttcap"), s.gtt_cap_mb ? (s.gtt_cap_mb + " MB") : (T("x_unlocked"))) +
    row("Swap", (s.swap_mb || 0) + " MB") +
    row(uns ? "Vulkan" : "Vulkan / Flash-Attn",
        uns ? "✓" : ((s.vulkan ? "✓" : "✗") + " / " + (s.flash_attention ? "✓" : "✗"))) +
    '</div><div class="brow" style="margin-top:8px">';
  const recs = s.recommend || [];
  if (recs.includes("kv_q8")) h += '<button class="dbtn" data-tune="kv_q8">' + (T("x_kv")) + "</button>";
  if (recs.includes("gtt_unlock")) h += '<button class="dbtn" data-tune="gtt_unlock">' + (T("x_gttbtn")) + "</button>";
  if (!recs.length) h += '<span class="stub">' + (T("x_optdone")) + "</span>";
  h += '</div><div class="stub" style="margin-top:6px">' + (T("x_kvhint2")) + "</div>";
  box.innerHTML = h;
  box.querySelectorAll("[data-tune]").forEach(b => b.onclick = async () => {
    const act = b.dataset.tune;
    const msg = act === "gtt_unlock" ? (T("x_qgtt"))
      : (T("x_qkv"));
    if (!confirm(msg)) return;
    await action("/api/ai/tune", { action: act }, T("x_applying"));
    setTimeout(() => aiTune(card, it), 1500);
  });
}
// settings modal: pick which modules the web dashboard exposes
async function openSettings() {
  const it = LANG === "it";
  let d; try { d = await (await api("/api/config")).json(); } catch (e) { return; }
  let m = $("#settings");
  if (!m) { m = document.createElement("div"); m.id = "settings"; m.className = "overlay"; document.body.appendChild(m); m.addEventListener("click", e => { if (e.target === m) m.style.display = "none"; }); }
  const rows = (d.catalogue || []).map(c => `<label class="setrow"><input type="checkbox" data-m="${c.id}" ${d.modules[c.id] ? "checked" : ""}> ${c.icon} ${it ? c.name : (c.name_en || c.name)}</label>`).join("");
  m.innerHTML = '<div class="setbox"><div class="fr-bar"><span class="fr-title">' + (T("x_mods")) + '</span><span class="fr-sp"></span><button class="fr-btn" id="set-x">✕</button></div><div class="setgrid">' + rows + "</div></div>";
  m.style.display = "flex";
  $("#set-x", m).onclick = () => m.style.display = "none";
  m.querySelectorAll("[data-m]").forEach(cb => cb.onchange = async () => { await action("/api/config", { module: cb.dataset.m, on: cb.checked }, T("x_updated")); buildDashboard(); });
}
function copyable(value) {
  return '<span class="cpw"><b style="user-select:all">' + value + '</b> <button class="cpy" type="button" data-cp="' +
    String(value).replace(/"/g, "&quot;") + '" title="' + T("copied") + '">📋</button></span>';
}
document.addEventListener("click", (e) => {
  const b = e.target.closest(".cpy"); if (!b) return;
  const v = b.dataset.cp;
  (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(() => toast(T("copied")))
    .catch(() => { const t = document.createElement("textarea"); t.value = v; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); toast(T("copied")); } catch (_) {} t.remove(); });
});

// ---------------- charts ----------------
// Round the axis to human numbers (0/1000/2000, not -160/1394/2948). Two rules
// beyond plain rounding: zero becomes the floor when the data sits near it (a MHz
// or RPM chart must never show a negative baseline), and the step comes from the
// *unpadded* range, or the padding inflates it and 3992 MHz lands on a 0-6000 axis.
function niceStep(raw) {
  if (!(raw > 0)) return 1;
  const mag = Math.pow(10, Math.floor(Math.log10(raw))), n = raw / mag;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * mag;
}
function niceScale(lo, hi, ticks) {
  // a dead-flat series must not get a wildly zoomed axis: 800/800 MHz would
  // otherwise be drawn on a 799.8-801.2 scale, amplifying nothing into noise
  if (hi - lo < Math.max(1e-9, Math.abs(hi) * 0.005)) {
    if (hi === 0) { lo = 0; hi = 1; }
    else { const band = Math.abs(hi) * 0.05; lo = hi - band; hi = hi + band; }
  }
  const nonneg = lo >= 0;
  if (nonneg && lo < hi - lo) lo = 0;
  const span = hi - lo, step = niceStep(span / Math.max(1, ticks)), pad = span * 0.06;
  let nlo = (nonneg && lo === 0) ? 0 : Math.floor((lo - pad) / step) * step;
  if (nonneg) nlo = Math.max(0, nlo);
  return { lo: nlo, hi: Math.ceil((hi + pad) / step) * step, step };
}
class Mini {
  constructor(canvas, series) { this.c = canvas; this.series = series; this.data = series.map(() => []); this.max = 90; }
  push(vals) { vals.forEach((v, i) => { const d = this.data[i]; d.push(v == null ? (d.length ? d[d.length - 1] : 0) : v); if (d.length > this.max) d.shift(); }); this.draw(); }
  draw() {
    const cv = this.c, dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
    if (cv.width !== w * dpr) { cv.width = w * dpr; cv.height = h * dpr; }
    const x = cv.getContext("2d"); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
    let all = []; this.data.forEach(d => all = all.concat(d)); if (!all.length) return;
    const sc = niceScale(Math.min(...all), Math.max(...all), 4);   // padding included
    let lo = sc.lo, hi = sc.hi;
    // plot area: a left gutter carries the y-axis values, otherwise the scale is unreadable
    const gx = 40, gw = Math.max(4, w - gx - 3), gy = 7, gh = Math.max(4, h - 14), span = hi - lo;
    let dec = 0;   // exactly the decimals the step needs: 0.25 -> "0.25", never "0.2"
    while (dec < 3 && Math.abs(+sc.step.toFixed(dec) - sc.step) > 1e-9) dec++;
    x.font = "10px 'DejaVu Sans Mono',monospace"; x.textAlign = "right"; x.textBaseline = "middle";
    x.lineWidth = 1;
    for (let v = lo; v <= hi + sc.step / 2; v += sc.step) {
      const yy = Math.round(gy + gh - gh * (v - lo) / span) + 0.5;
      x.strokeStyle = "rgba(216,168,73,.10)"; x.beginPath(); x.moveTo(gx, yy); x.lineTo(gx + gw, yy); x.stroke();
      x.fillStyle = "rgba(185,160,122,.8)"; x.fillText(v.toFixed(dec), gx - 6, yy);
    }
    this.data.forEach((d, i) => { if (d.length < 2) return; x.beginPath(); d.forEach((v, j) => { const px = gx + gw * j / (d.length - 1), py = gy + gh - gh * (v - lo) / span; j ? x.lineTo(px, py) : x.moveTo(px, py); }); x.strokeStyle = this.series[i].c; x.lineWidth = 1.6; x.lineJoin = "round"; x.stroke(); });
  }
}

// Per core/thread frequency bars. `threads` is [[cpu, core, mhz|null], ...] straight
// off the telemetry stream; a null MHz means the Tuner has that thread parked.
function coreColor(t) {
  const a = t < 0.5 ? [0x6b, 0x5a, 0x34] : [0xd8, 0xa8, 0x49],
        b = t < 0.5 ? [0xd8, 0xa8, 0x49] : [0xe0, 0x6b, 0x39],
        k = t < 0.5 ? t / 0.5 : (t - 0.5) / 0.5;
  return "rgb(" + a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(",") + ")";
}
function renderCores(root, threads) {
  if (!Array.isArray(threads) || !threads.length) return;
  const bars = $(".cbars", root), axis = $(".cat", root), stat = $(".cstat", root);
  const live = threads.filter(t => t[2] != null).map(t => t[2]);
  let hi = Math.max(1000, live.length ? Math.max(...live) : 0);
  hi = Math.ceil(hi / 500) * 500;                       // round, stable scale
  if (root._n !== threads.length) {                     // rebuild only on hotplug
    root._n = threads.length;
    bars.innerHTML = threads.map(t =>
      `<div class="cbar"><span class="v"></span><span class="t"><i class="b"></i></span><span class="n">${t[1]}·${t[0]}</span></div>`).join("");
  }
  if (root._hi !== hi) {
    root._hi = hi;
    axis.innerHTML = [0, 1, 2, 3, 4].map(i =>
      `<span style="top:${i * 25}%">${Math.round(hi - hi * i / 4)}</span>`).join("");
  }
  const els = bars.children;
  threads.forEach((t, i) => {
    const el = els[i]; if (!el) return;
    const mhz = t[2], b = $(".b", el);
    el.classList.toggle("off", mhz == null);
    if (mhz == null) { $(".v", el).textContent = T("c_off"); b.style.background = ""; return; }
    const k = Math.max(0, Math.min(1, mhz / hi));
    $(".v", el).textContent = Math.round(mhz);
    b.style.height = (k * 100).toFixed(1) + "%";
    b.style.background = "linear-gradient(180deg," + coreColor(k) + " 0%, rgba(0,0,0,0) 260%)";
    b.style.borderTop = "1px solid " + coreColor(k);
  });
  if (stat) stat.innerHTML = live.length
    ? `min <b>${Math.round(Math.min(...live))}</b> · ${T("c_avg")} <b>${Math.round(live.reduce((a, v) => a + v, 0) / live.length)}</b> · max <b>${Math.round(Math.max(...live))}</b> · ${T("c_online")} <b>${live.length}/${threads.length}</b>`
    : "";
}
const TELEM = [
  { t: "t_temp", u: "°C", s: [{ k: "cpu_temp", l: "CPU", c: "#e8c878" }, { k: "gpu_temp", l: "GPU", c: "#e07b39" }] },
  { t: "t_load", u: "%", s: [{ k: "cpu_load", l: "CPU", c: "#5fd24f" }, { k: "gpu_util", l: "GPU", c: "#49b6e0" }] },
  { t: "t_freq", u: "MHz", s: [{ k: "cpu_mhz", l: "CPU", c: "#9bd24f" }, { k: "gpu_freq", l: "GPU", c: "#49b6e0" }] },
  { t: "t_pow", u: "W", s: [{ k: "gpu_power", l: "GPU", c: "#e0d24f" }] },
  { t: "t_volt", u: "mV", s: [{ k: "gpu_mv", l: "GPU", c: "#c98be0" }, { k: "cpu_mv", l: "CPU", c: "#e8a878" }] },
  { t: "t_fan", u: "RPM", s: [{ k: "fan", l: "FAN", c: "#d8a849" }] },
];

// ---------------- layout (order, hidden, collapsed) ----------------
const DEFAULT_ORDER = ["telemetry", "status", "zerotier", "rules", "logs", "tuner", "hub",
                       "launcher", "kvm", "terminal", "ai", "aiops", "wol", "gamestream"];
let layout = (() => { try { return JSON.parse(localStorage.getItem("sflayout")) || {}; } catch (e) { return {}; } })();
layout.order = layout.order || []; layout.hidden = layout.hidden || []; layout.collapsed = layout.collapsed || [];
function _toggleArr(a, id, on) { const i = a.indexOf(id); if (on && i < 0) a.push(id); if (!on && i >= 0) a.splice(i, 1); }
function captureOrder() { const g = $("#grid"); if (g && g.children.length) layout.order = [...g.querySelectorAll(".mod")].map(c => c.dataset.mid); }
function saveLayout() { captureOrder(); localStorage.setItem("sflayout", JSON.stringify(layout)); toast(T("ly_saved")); }
function resetLayout() { localStorage.removeItem("sflayout"); layout = { order: [], hidden: [], collapsed: [] }; buildDashboard(); }

const RENDER = {
  telemetry(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>📊 ' + (T("m_telem")) + ' <span class="pill" id="tlive">' + T("live") + '</span></h3><div class="charts"></div>' +
      '<div class="cores"><div class="lab"><span>' + T("t_percore") + ' (MHz)</span><span class="cstat"></span></div>' +
      '<div class="cwrap"><div class="cax"><i></i><div class="cat"></div><i></i></div><div class="cgrid"></div><div class="cbars"></div></div></div>';
    const box = $(".charts", card); const charts = [];
    TELEM.forEach(spec => {
      const el = document.createElement("div"); el.className = "chart";
      const labs = spec.s.map(s => `<span style="color:${s.c}">${s.l} <b class="val" data-k="${s.k}">–</b></span>`).join(" ");
      el.innerHTML = `<div class="lab"><span>${T(spec.t)} (${spec.u})</span><span>${labs}</span></div><canvas></canvas>`;
      box.appendChild(el); charts.push({ spec, m: new Mini($("canvas", el), spec.s), el });
    });
    const cores = $(".cores", card);
    const es = new EventSource("/api/telemetry");
    es.onmessage = ev => { let v; try { v = JSON.parse(ev.data); } catch (e) { return; }
      try { renderCores(cores, v.cpu_threads); } catch (e) {}
      charts.forEach(c => { c.m.push(c.spec.s.map(s => v[s.k])); c.spec.s.forEach(s => { const b = c.el.querySelector(`[data-k="${s.k}"]`); if (b && v[s.k] != null) b.textContent = Math.abs(v[s.k]) >= 10 ? Math.round(v[s.k]) : v[s.k].toFixed(2); }); });
    };
    card._es = es;
  },
  status(card) {
    card.innerHTML = "<h3>🧊 " + (T("m_sys")) + '</h3><div class="rows" id="srows">…</div>';
    const fill = async () => { try { const s = await (await api("/api/status")).json();
      const row = (a, b) => `<div class="r"><span>${a}</span><span>${b || "–"}</span></div>`;
      $("#srows", card).innerHTML = row(T("s_you"), s.you) + row(T("s_host"), s.host) + row(T("s_ip"), s.ip) + row(T("s_kernel"), s.kernel) +
        row(T("s_up"), s.uptime) + row(T("s_cu"), s.cu) + row(T("s_ram"), s.ram_used_mb ? `${s.ram_used_mb} / ${s.ram_total_mb} MB` : "") +
        row(T("s_disk"), s.disk_used ? `${s.disk_used} / ${s.disk_total} (${s.disk_pct})` : "") + row(T("s_frz"), s.freezes);
    } catch (e) {} };
    fill(); card._iv = setInterval(fill, 5000);
  },
  async tuner(card) {
    card.innerHTML = "<h3>🎛️ " + (T("m_ctrl")) + '</h3><div id="tk">…</div>';
    let d; try { d = await (await api("/api/tuner")).json(); } catch (e) { return; }
    const presets = (d.presets || []).map(p => `<button class="dbtn" data-preset="${p.name}" title="${(p.desc || "").replace(/"/g, "")}">${p.name}</button>`).join("");
    $("#tk", card).innerHTML =
      `<div class="brow" style="margin-bottom:10px"><button class="dbtn" id="opentuner" style="border-color:var(--gold)">🎛️ ${T("c_full")}</button></div>` +
      `<div class="grp"><div class="gl">${T("c_preset")}</div><div class="brow">${presets}</div></div>` +
      `<div class="grp"><div class="gl">${T("c_gov")}</div><div class="brow"><button class="dbtn" data-gov="balanced">${T("c_bal")}</button><button class="dbtn" data-gov="performance">${T("c_perf")}</button></div></div>` +
      `<div class="grp"><div class="gl">${T("c_fan")}</div><div class="brow"><button class="dbtn" data-fan="auto">${T("c_auto")}</button><input id="fanp" type="range" min="20" max="100" value="60" style="flex:1"><button class="dbtn" data-fanmanual="1">${T("c_man")}</button></div></div>`;
    $("#opentuner", card).onclick = () => openFrame("SkillFishOS Tuner", "/static/tuner.html");
    card.querySelectorAll("[data-preset]").forEach(b => b.onclick = () => action("/api/tuner/preset", { name: b.dataset.preset }, T("c_applied", { x: b.dataset.preset })));
    card.querySelectorAll("[data-gov]").forEach(b => b.onclick = () => action("/api/tuner/govmode", { mode: b.dataset.gov }, "Governor: " + b.dataset.gov));
    card.querySelector("[data-fan]").onclick = () => action("/api/tuner/fan", { mode: "auto" }, T("c_fan") + ": " + T("c_auto"));
    card.querySelector("[data-fanmanual]").onclick = () => action("/api/tuner/fan", { mode: "manual", pct: +$("#fanp", card).value }, T("c_fan") + ": " + $("#fanp", card).value + "%");
  },
  async hub(card) {
    card.innerHTML = "<h3>📦 " + (T("m_apps")) + '</h3><div id="hk">…</div>';
    let upd = ""; try { const u = await (await api("/api/hub/updates")).json(); upd = (u.count || 0) + " " + T("h_updates"); } catch (e) {}
    $("#hk", card).innerHTML =
      `<div class="stub" style="margin-bottom:8px">${upd}</div>` +
      `<div class="brow"><button class="dbtn" id="openhub" style="border-color:var(--gold)">📦 ${T("h_open")}</button></div>`;
    $("#openhub", card).onclick = () => openFrame("SkillFishOS Hub", "/static/hub.html");
  },
  logs(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>📜 Log <select id="lw" class="dsel"><option value="journal">journal</option><option value="kernel">kernel</option><option value="freeze">freeze</option></select> <button class="dbtn" id="lref">⟳</button></h3><pre class="logbox" id="lb">…</pre>';
    const load = async () => { try { const j = await (await api("/api/logs?n=200&which=" + $("#lw", card).value)).json(); const lb = $("#lb", card); lb.textContent = (j.lines || []).join("\n") || T("empty"); lb.scrollTop = lb.scrollHeight; } catch (e) {} };
    $("#lw", card).onchange = load; $("#lref", card).onclick = load; load();
  },
  launcher(card) {
    card.innerHTML = "<h3>🚀 " + (T("m_launch")) + '</h3><div class="brow">' +
      [["console", "🎮 Console"], ["monitor", "📊 Telemetry"], ["tuner", "🎛️ Tuner"], ["hub", "📦 Hub"], ["ai", "🧠 AI"]].map(([k, l]) => `<button class="dbtn" data-app="${k}">${l}</button>`).join("") + "</div>" +
      '<div class="stub" style="margin-top:8px">' + T("la_hint") + "</div>";
    card.querySelectorAll("[data-app]").forEach(b => b.onclick = () => action("/api/launch", { what: b.dataset.app }, T("la_started", { x: b.dataset.app })));
  },
  kvm(card) {
    card.innerHTML = '<h3>🖥️ Desktop (KVM)</h3><div class="brow"><button class="dbtn" id="kvmgo">' + T("k_open") + '</button></div><div class="stub" id="kvmi" style="margin-top:8px">' + T("k_hint") + "</div>";
    $("#kvmgo", card).onclick = async () => { const j = await action("/api/kvm/start", {}, T("k_ready"));
      if (j && j.password != null) { openFrame("Desktop (KVM)", "/kvm/vnc.html?autoconnect=1&resize=scale&reconnect=1&path=" + encodeURIComponent("kvm/websockify") + "&password=" + encodeURIComponent(j.password)); $("#kvmi", card).innerHTML = T("k_vncpw") + copyable(j.password); } };
  },
  terminal(card) {
    card.innerHTML = "<h3>⌨️ " + (T("m_term")) + '</h3><div class="brow"><button class="dbtn" id="tgo">' + T("term_open") + '</button></div><div class="stub" style="margin-top:8px">' + T("term_hint") + "</div>";
    $("#tgo", card).onclick = () => openFrame(T("m_term"), "/terminal/");
  },
  ai(card) {
    const it = LANG === "it";
    card.innerHTML = "<h3>🧠 " + (T("x_localai")) + "</h3><div id=\"ai\">…</div>";
    const refresh = async () => { let s; try { s = await (await api("/api/ai")).json(); } catch (e) { return; }
      const models = (s.models || []).map(mn => `<span class="pill" style="display:inline-block;margin:2px">${mn}</span>`).join(" ") || `<span class="stub">${T("x_nomodels")}</span>`;
      // Unsloth serves its own UI and manages models there; the legacy Ollama stack
      // exposes them through the dashboard, so only that one gets the model list/pull.
      const uns = s.engine === "unsloth";
      const fl = s.first_login || {};
      const engName = uns ? "Unsloth Studio" : "Ollama";
      const uiName = uns ? "Unsloth Studio" : "OpenWebUI";
      $("#ai", card).innerHTML = '<div class="rows"><div class="r"><span>' + (T("x_engine")) + " (" + engName + ")</span><span>" + (s.running ? T("ai_on") : T("ai_off")) + '</span></div><div class="r"><span>' + uiName + "</span><span>" + (s.webui ? T("ai_ready") : T("ai_off")) + "</span></div>" +
        (uns ? '<div class="r"><span>' + (T("x_accel")) + "</span><span>Vulkan · GPU</span></div>" : "") + "</div>" +
        // Le credenziali del primo accesso. Unsloth non ha una password fissa:
        // ne genera una a caso a ogni installazione, la annuncia una volta sola
        // in un log e poi si SPEGNE dopo un'ora se non viene cambiata. Senza
        // questo riquadro l'utente cerca su internet una risposta che non esiste,
        // e intanto il motore gli muore addosso. Sparisce da solo appena la
        // password viene cambiata.
        // La chiave API. Chat e AI-Ops parlano con Unsloth attraverso la sua API,
        // che senza chiave risponde 401: i due pulsanti sembravano rotti. La
        // chiave si crea dentro Studio e finora andava incollata a mano nel file
        // di configurazione via SSH, cioe' fuori portata per quasi tutti.
        (s.running && !s.has_key
          ? '<div class="gl" style="margin-top:12px">' + (T("x_apikey")) + '</div>' +
            '<div style="font-size:12px;opacity:.75;margin:4px 0 6px">' +
            (it ? "Serve a Chat e AI-Ops. Creala in Studio: Impostazioni &rarr; API keys, poi incollala qui."
                : "Needed by Chat and AI-Ops. Create it in Studio: Settings &rarr; API keys, then paste it here.") + "</div>" +
            '<div class="brow"><input id="aikey" class="dsel" placeholder="sk-unsloth-..." style="flex:1"/>' +
            '<button class="dbtn" id="aikeysave">' + (T("x_save")) + "</button></div>"
          : "") +
        (fl.password
          ? '<div class="gl" style="margin-top:12px">' + (T("x_first")) + '</div>' +
            '<div class="rows"><div class="r"><span>' + (T("x_user")) + '</span><span><code>' + fl.user + '</code></span></div>' +
            '<div class="r"><span>' + (T("x_initpw")) + '</span><span><code>' + fl.password + '</code></span></div></div>' +
            '<div style="margin-top:6px;font-size:12px;opacity:.75">' +
            (it ? "Cambiala al primo accesso: se resta questa, Unsloth si spegne da solo dopo un'ora."
                : "Change it on first sign-in: left as is, Unsloth shuts itself down after an hour.") + "</div>"
          : "") +
        '<div class="brow" style="margin-top:10px">' + (s.running ? '<button class="dbtn danger" id="aistop">' + T("ai_stop") + "</button>" : '<button class="dbtn" id="aistart">' + T("ai_start") + "</button>") +
        '<button class="dbtn" id="aichat"' + (s.running && s.has_key ? "" : " disabled") + ">💬 " + (T("x_chat")) + "</button>" +
        '<button class="dbtn" id="aiweb"' + (s.webui ? "" : " disabled") + ">" + (T("x_open")) + uiName + " ↗</button></div>" +
        (uns ? ""
             : '<div class="gl" style="margin-top:12px">' + (T("x_models")) + '</div><div style="margin-top:4px">' + models + "</div>" +
               '<div class="brow" style="margin-top:10px"><input id="aipm" class="dsel" placeholder="' + (T("x_pullph")) + '" style="flex:1"><button class="dbtn" id="aipull"' + (s.running ? "" : " disabled") + ">" + (T("x_pull")) + "</button></div>") +
        '<div class="brow" style="margin-top:10px"><button class="dbtn" id="aitunebtn" style="border-color:var(--gold)">⚡ ' + (T("x_optai")) + "</button></div><div id=\"aitune\"></div>" +
        '<div class="stub" style="margin-top:8px">' + (uns ? (it ? "I modelli si scaricano dentro Unsloth Studio. Gira sulla GPU: spegnilo quando giochi."
                                                                : "Models are downloaded inside Unsloth Studio. It runs on the GPU: turn it off when gaming.")
                                                          : T("ai_hint")) + "</div>";
      if ($("#aistart", card)) $("#aistart", card).onclick = async () => { await action("/api/ai/start", {}, T("ai_starting")); setTimeout(refresh, 4000); };
      if ($("#aistop", card)) $("#aistop", card).onclick = async () => { await action("/api/ai/stop", {}, T("ai_stopping")); setTimeout(refresh, 2000); };
      if ($("#aikeysave", card)) $("#aikeysave", card).onclick = async () => {
        const v = $("#aikey", card).value.trim();
        if (!v) return;
        await action("/api/ai/key", { key: v }, T("x_keysaved"));
        setTimeout(refresh, 800);
      };
      if ($("#aichat", card)) $("#aichat", card).onclick = () => openFrame("SkillFishOS AI", "/static/aichat.html");
      if ($("#aiweb", card)) $("#aiweb", card).onclick = () => {
        // Si apre l'indirizzo DIRETTO, non il proxy della dashboard.
        // Le pagine di Unsloth chiedono i propri pezzi con percorsi assoluti
        // (/assets/...), quindi servite sotto /unsloth/ li cercano sulla radice
        // della dashboard e non li trovano: da locale funzionava, da remoto no.
        // Unsloth ha la propria autenticazione, quindi non resta scoperto.
        window.open("http://" + location.hostname + ":" + (s.port || 8888), "_blank");
      };
      if ($("#aipull", card)) $("#aipull", card).onclick = async () => { if ($("#aipm", card).value.trim()) { await action("/api/ai/pull", { model: $("#aipm", card).value }, T("x_dlstart")); $("#aipm", card).value = ""; } };
      if ($("#aitunebtn", card)) $("#aitunebtn", card).onclick = () => aiTune(card, it);
    };
    refresh(); card._iv = setInterval(refresh, 5000);
  },
  wol(card) {
    card.innerHTML = "<h3>🔋 Power schedule / WoL</h3><div id=\"wol\">…</div>";
    const refresh = async () => { let s; try { s = await (await api("/api/wol")).json(); } catch (e) { return; }
      $("#wol", card).innerHTML = '<div class="rows"><div class="r"><span>NIC</span><span>' + s.nic + '</span></div><div class="r"><span>MAC</span><span>' + copyable(s.mac) + '</span></div><div class="r"><span>' + T("w_wol") + "</span><span>" + (s.wol_enabled ? T("w_en") : T("w_dis")) + "</span></div></div>" +
        '<div class="brow" style="margin-top:10px"><button class="dbtn" id="wolt">' + (s.wol_enabled ? T("w_disbtn") : T("w_enbtn")) + "</button></div>" +
        '<div class="gl" style="margin-top:12px">' + T("w_wake") + '</div><div class="brow"><input id="wmac" class="dsel" placeholder="AA:BB:CC:DD:EE:FF" style="flex:1"><button class="dbtn" id="wsend">' + T("w_send") + "</button></div>" +
        '<div class="gl" style="margin-top:12px">' + T("w_sched") + '</div><div class="brow"><input id="wmin" class="dsel" type="number" value="10" min="1" style="width:64px"> min <button class="dbtn" id="wreb">↻ ' + T("p_reboot") + '</button><button class="dbtn danger" id="woff">⏻ ' + T("p_off") + '</button><button class="dbtn" id="wcan">' + T("w_cancel") + "</button></div>";
      $("#wolt", card).onclick = async () => { await action("/api/wol/enable", { on: !s.wol_enabled }, T("w_updated")); setTimeout(refresh, 800); };
      $("#wsend", card).onclick = () => action("/api/wol/send", { mac: $("#wmac", card).value }, T("w_sent"));
      $("#wreb", card).onclick = () => { if (confirm(T("w_qreb", { x: $("#wmin", card).value }))) action("/api/wol/schedule", { action: "reboot", minutes: +$("#wmin", card).value }, T("w_rsched")); };
      $("#woff", card).onclick = () => { if (confirm(T("w_qoff", { x: $("#wmin", card).value }))) action("/api/wol/schedule", { action: "poweroff", minutes: +$("#wmin", card).value }, T("w_osched")); };
      $("#wcan", card).onclick = () => action("/api/wol/schedule", { action: "cancel" }, T("w_canc"));
    };
    refresh();
  },
  rules(card) {
    card.innerHTML = "<h3>⚙️ " + (T("m_rules")) + '</h3><div id="ru">…</div>';
    const refresh = async () => { let s; try { s = await (await api("/api/rules")).json(); } catch (e) { return; }
      $("#ru", card).innerHTML = '<div class="rows"><div class="r"><span>' + T("ru_throttle") + "</span><span>" + (s.enabled ? T("ru_on") : T("ru_off")) + '</span></div><div class="r"><span>' + T("ru_thresh") + "</span><span>" + s.temp_limit + " °C</span></div>" + (s.last_action ? '<div class="r"><span>' + T("ru_last") + "</span><span>" + s.last_action + "</span></div>" : "") + "</div>" +
        '<div class="brow" style="margin-top:10px"><button class="dbtn" id="rtog">' + (s.enabled ? T("ru_disable") : T("ru_enable")) + '</button><input id="rlim" class="dsel" type="number" min="70" max="100" value="' + s.temp_limit + '" style="width:64px"> °C <button class="dbtn" id="rset">' + T("ru_set") + "</button></div>";
      $("#rtog", card).onclick = async () => { await action("/api/rules", { enabled: !s.enabled }, T("ru_updated")); setTimeout(refresh, 500); };
      $("#rset", card).onclick = async () => { await action("/api/rules", { temp_limit: +$("#rlim", card).value }, T("ru_setdone")); setTimeout(refresh, 500); };
    };
    refresh(); card._iv = setInterval(refresh, 15000);
  },
  aiops(card) {
    card.classList.add("span2");
    card.innerHTML = '<h3>🩺 AI-Ops</h3><div class="brow"><input id="aq" class="dsel" placeholder="' + T("ao_q") + '" style="flex:1"><button class="dbtn" id="adg">' + T("ao_btn") + '</button></div><div class="logbox" id="aout" style="margin-top:8px;display:none"></div><div class="stub" style="margin-top:8px">' + T("ao_hint") + "</div>";
    $("#adg", card).onclick = async () => { const out = $("#aout", card); out.style.display = "block"; out.textContent = T("ao_running");
      const j = await (await post("/api/aiops/diagnose", { question: $("#aq", card).value })).json().catch(() => ({})); out.textContent = j.ok ? (j.answer || T("ao_none")) : (T("err") + (j.error || "")); };
  },
  zerotier(card) {
    const it = LANG === "it";
    card.innerHTML = "<h3>🌐 ZeroTier</h3><div id=\"zt\">…</div>";
    const refresh = async () => {
      let s; try { s = await (await api("/api/zerotier")).json(); } catch (e) { return; }
      const nets = (s.networks || []).map(n => {
        const ip = (n.ip && n.ip !== "-") ? copyable(n.ip.split(",")[0]) : "—";
        const ok = n.status === "OK";
        return `<div class="r"><span>${n.nwid} ${ok ? "●" : "○"} ${n.status}</span><span>${ip} <button class="dbtn" data-leave="${n.nwid}" style="padding:1px 8px">×</button></span></div>`;
      }).join("") || `<div class="stub">${T("x_nonet")}</div>`;
      $("#zt", card).innerHTML =
        '<div class="rows"><div class="r"><span>' + (T("x_node")) + "</span><span>" + copyable(s.address) + '</span></div><div class="r"><span>' + (T("x_state")) + "</span><span>" + (s.online ? "● ONLINE" : "○ offline") + "</span></div></div>" +
        '<div class="gl" style="margin-top:10px">' + (T("x_nets")) + '</div><div class="rows">' + nets + "</div>" +
        '<div class="brow" style="margin-top:8px"><input id="ztnw" class="dsel" placeholder="Network ID (16 hex)" style="flex:1"><button class="dbtn" id="ztj">' + (T("x_join")) + "</button></div>" +
        '<div class="stub" style="margin-top:8px">' + T("x_zthint") + "</div>";
      card.querySelectorAll("[data-leave]").forEach(b => b.onclick = async () => { await action("/api/zerotier/leave", { nwid: b.dataset.leave }, T("x_left")); setTimeout(refresh, 800); });
      $("#ztj", card).onclick = async () => { await action("/api/zerotier/join", { nwid: $("#ztnw", card).value.trim() }, T("x_ztsent")); setTimeout(refresh, 1500); };
    };
    refresh(); card._iv = setInterval(refresh, 8000);
  },
  _stub(card, mod) { card.innerHTML = `<h3>${mod.icon} ${LANG === "it" ? mod.name : (mod.name_en || mod.name)}</h3><div class="stub">${T("m_soon")}</div>`; },
};

let MODS = {};
function addCardTools(card, id) {
  const t = document.createElement("div"); t.className = "mod-tools";
  const collapsed = card.classList.contains("collapsed");
  t.innerHTML = '<button class="mt drag-h" draggable="true" title="' + (T("w_move")) + '">⠿</button>' +
    '<button class="mt" data-a="c" title="' + (T("w_coll")) + '">' + (collapsed ? "▸" : "▾") + '</button>' +
    '<button class="mt" data-a="x" title="' + (T("w_close")) + '">✕</button>';
  card.appendChild(t);
  t.querySelector('[data-a="c"]').onclick = e => { e.stopPropagation(); const on = !card.classList.contains("collapsed"); card.classList.toggle("collapsed", on); _toggleArr(layout.collapsed, id, on); e.target.textContent = on ? "▸" : "▾"; };
  t.querySelector('[data-a="x"]').onclick = e => { e.stopPropagation(); captureOrder(); _toggleArr(layout.hidden, id, true); buildDashboard(); };
}
function setupDrag(grid) {
  let drag = null;
  grid.addEventListener("dragstart", e => { const c = e.target.closest(".mod"); if (!c) return; drag = c; c.classList.add("dragging"); e.dataTransfer.effectAllowed = "move"; });
  grid.addEventListener("dragend", () => { if (drag) { drag.classList.remove("dragging"); drag = null; } });
  grid.addEventListener("dragover", e => {
    e.preventDefault(); if (!drag) return; const c = e.target.closest(".mod"); if (!c || c === drag) return;
    const b = c.getBoundingClientRect();
    const before = (e.clientY < b.top + b.height / 2) || (e.clientX < b.left + b.width / 2 && e.clientY < b.bottom);
    grid.insertBefore(drag, before ? c : c.nextSibling);
  });
}
function renderHidden() {
  const wrap = $("#hidden-wrap"); if (!wrap) return;
  const hid = layout.hidden.filter(id => MODS[id]);
  if (!hid.length) { wrap.innerHTML = ""; return; }
  wrap.innerHTML = '<button class="ghost" id="hbtn">➕ ' + hid.length + "</button>";
  $("#hbtn").onclick = () => {
    const it = LANG === "it";
    let m = $("#hidden-menu"); if (!m) { m = document.createElement("div"); m.id = "hidden-menu"; m.className = "overlay"; document.body.appendChild(m); m.addEventListener("click", e => { if (e.target === m) m.style.display = "none"; }); }
    m.innerHTML = '<div class="setbox"><div class="fr-bar"><span class="fr-title">' + (T("x_closed")) + '</span><span class="fr-sp"></span><button class="fr-btn" id="hm-x">✕</button></div><div class="setgrid">' +
      hid.map(id => `<button class="dbtn" data-r="${id}" style="text-align:left">${MODS[id].icon} ${it ? MODS[id].name : (MODS[id].name_en || MODS[id].name)}</button>`).join("") + "</div></div>";
    m.style.display = "flex"; $("#hm-x").onclick = () => m.style.display = "none";
    m.querySelectorAll("[data-r]").forEach(b => b.onclick = () => { captureOrder(); _toggleArr(layout.hidden, b.dataset.r, false); m.style.display = "none"; buildDashboard(); });
  };
}

async function buildDashboard() {
  $("#login").style.display = "none"; $("#app").style.display = "block";
  $("#logout").textContent = T("logout");
  let data; try { data = await (await api("/api/modules")).json(); } catch (e) { return showLogin(); }
  $("#host").textContent = data.host || "";
  MODS = {}; (data.modules || []).forEach(m => MODS[m.id] = m);
  let order = (layout.order.length ? layout.order : DEFAULT_ORDER).filter(id => MODS[id]);
  DEFAULT_ORDER.forEach(id => { if (MODS[id] && !order.includes(id)) order.push(id); });
  (data.modules || []).forEach(m => { if (!order.includes(m.id)) order.push(m.id); });
  const grid = $("#grid"); grid.innerHTML = "";
  order.forEach(id => {
    if (layout.hidden.includes(id)) return;
    const mod = MODS[id]; if (!mod) return;
    const card = document.createElement("div"); card.className = "mod"; card.dataset.mid = id;
    if (layout.collapsed.includes(id)) card.classList.add("collapsed");
    (RENDER[id] || ((c) => RENDER._stub(c, mod)))(card, mod);
    addCardTools(card, id);
    grid.appendChild(card);
  });
  setupDrag(grid); renderHidden();
  clearInterval(window._sw);
  window._sw = setInterval(async () => { try { const r = await api("/api/me"); if (!r.ok) location.reload(); } catch (e) {} }, 60000);
}
function showLogin() {
  $("#app").style.display = "none"; $("#login").style.display = "grid";
  $("#lsub").textContent = T("login_sub"); $("#u").placeholder = T("user"); $("#p").placeholder = T("pass"); $("#lbtn").textContent = T("enter");
  $("#u").focus();
}
function setLang(l) { LANG = l; localStorage.setItem("sflang", l); location.reload(); }

$("#lform").addEventListener("submit", async ev => {
  ev.preventDefault(); $("#lerr").textContent = "";
  const r = await api("/api/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ user: $("#u").value, pass: $("#p").value }) });
  if (r.ok) { $("#p").value = ""; buildDashboard(); } else { const j = await r.json().catch(() => ({})); $("#lerr").textContent = j.error || T("denied"); }
});
$("#logout").addEventListener("click", async () => { await api("/api/logout", { method: "POST" }); location.reload(); });
$("#settings-btn").addEventListener("click", openSettings);
$("#save-btn").addEventListener("click", saveLayout);
$("#reset-btn").addEventListener("click", () => { if (confirm(T("ly_reset"))) resetLayout(); });
$("#reboot-top").addEventListener("click", () => { if (confirm(T("p_qreb"))) action("/api/power", { action: "reboot" }, T("p_rebing")); });
$("#off-top").addEventListener("click", () => { if (confirm(T("p_qoff"))) action("/api/power", { action: "poweroff" }, T("p_offing")); });
document.querySelectorAll(".lang-btn").forEach(b => b.addEventListener("click", () => setLang(b.dataset.l)));

(async () => {
  document.querySelectorAll(".lang-btn").forEach(b => b.classList.toggle("active", b.dataset.l === LANG));
  try { const r = await api("/api/me"); if (r.ok) buildDashboard(); else showLogin(); } catch (e) { showLogin(); }
})();
