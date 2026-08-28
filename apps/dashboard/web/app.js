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
  if (n.startsWith("ru")) return "ru";
  if (n.startsWith("es")) return "es";
  if (n.startsWith("pt")) return "pt";
  if (n.startsWith("de")) return "de";
  if (n.startsWith("fr")) return "fr";
  return "en";
})();
const STR = {
  x_zthint: { it: "Dopo «Entra», autorizza il nodo su my.zerotier.com. Poi raggiungi la dashboard da ovunque: https://&lt;IP ZeroTier&gt;:8443",
              en: "After Join, authorize the node on my.zerotier.com. Then reach the dashboard from anywhere: https://&lt;ZeroTier IP&gt;:8443",
              pl: "Po «Dołącz» autoryzuj węzeł na my.zerotier.com. Potem otwórz panel z dowolnego miejsca: https://&lt;IP ZeroTier&gt;:8443",
              uk: "Після «Приєднатися» авторизуйте вузол на my.zerotier.com. Далі відкривайте панель звідусіль: https://&lt;IP ZeroTier&gt;:8443",
              ru: "После «Присоединиться» разрешите узел на my.zerotier.com. Дальше панель открывается откуда угодно: https://&lt;IP ZeroTier&gt;:8443", es: "Tras «Unirse», autoriza el nodo en my.zerotier.com. Luego abre el panel desde cualquier sitio: https://&lt;IP de ZeroTier&gt;:8443", pt: "Depois de “Entrar”, autorize o nó em my.zerotier.com. Aí abra o painel de qualquer lugar: https://&lt;IP do ZeroTier&gt;:8443", de: "Nach „Beitreten“ den Knoten auf my.zerotier.com freigeben. Danach erreichst du die Leiste von überall: https://&lt;ZeroTier-IP&gt;:8443",
              fr: "Après « Rejoindre », autorisez le nœud sur my.zerotier.com. Ensuite le panneau s'ouvre de n'importe où : https://&lt;IP ZeroTier&gt;:8443" },
  x_ztsent: { it: "Richiesta inviata — autorizza su my.zerotier.com",
              en: "Request sent — authorize on my.zerotier.com",
              pl: "Wysłano prośbę — autoryzuj na my.zerotier.com",
              uk: "Запит надіслано — авторизуйте на my.zerotier.com",
              ru: "Запрос отправлен — разрешите на my.zerotier.com", es: "Petición enviada — autoriza en my.zerotier.com", pt: "Pedido enviado — autorize em my.zerotier.com", de: "Anfrage gesendet — auf my.zerotier.com freigeben",
              fr: "Demande envoyée — autorisez sur my.zerotier.com" },
  x_kvhint2: { it: "q8_0 dimezza la KV cache (più contesto). Sbloccare la GTT permette modelli più grandi ma richiede il riavvio.", en: "q8_0 halves the KV cache (more context). Unlocking GTT allows bigger models but needs a reboot.", pl: "q8_0 zmniejsza KV cache o połowę (więcej kontekstu). Odblokowanie GTT pozwala na większe modele, ale wymaga restartu.", uk: "q8_0 зменшує KV cache удвічі (більше контексту). Розблокування GTT дозволяє більші моделі, але потребує перезавантаження.",
               ru: "q8_0 уменьшает KV cache вдвое (больше контекста). Разблокировка GTT позволяет модели побольше, но требует перезагрузки.", es: "q8_0 reduce a la mitad la KV cache (más contexto). Desbloquear el GTT permite modelos más grandes pero necesita reiniciar.", pt: "q8_0 corta a KV cache pela metade (mais contexto). Liberar o GTT permite modelos maiores, mas exige reiniciar.", de: "q8_0 halbiert den KV-Zwischenspeicher (mehr Kontext). Das Freigeben des GTT erlaubt größere Modelle, braucht aber einen Neustart.",
               fr: "q8_0 réduit de moitié le cache KV (plus de contexte). Déverrouiller le GTT permet des modèles plus gros mais demande un redémarrage." },
  x_qgtt: { it: "Sbloccare la GTT? Modifica il boot e richiede il RIAVVIO.", en: "Unlock GTT? Edits boot config, needs a REBOOT.", pl: "Odblokować GTT? Zmienia konfigurację startu i wymaga RESTARTU.", uk: "Розблокувати GTT? Змінює конфігурацію завантаження і потребує ПЕРЕЗАВАНТАЖЕННЯ.",
            ru: "Разблокировать GTT? Меняет настройки загрузки и требует ПЕРЕЗАГРУЗКИ.", es: "¿Desbloquear el GTT? Cambia la configuración de arranque y necesita REINICIAR.", pt: "Liberar o GTT? Muda a configuração de boot e exige REINICIAR.", de: "GTT freigeben? Ändert die Starteinstellungen und braucht einen NEUSTART.",
            fr: "Déverrouiller le GTT ? Modifie la configuration de démarrage et demande un REDÉMARRAGE." },
  x_qkv: { it: "KV cache → q8_0? Riavvia il motore AI locale.", en: "KV cache → q8_0? Restarts the local AI engine.", pl: "KV cache → q8_0? Uruchamia ponownie lokalny silnik SI.", uk: "KV cache → q8_0? Перезапускає локальний рушій ШІ.",
           ru: "KV cache → q8_0? Перезапустит локальный движок ИИ.", es: "¿KV cache → q8_0? Reinicia el motor de IA local.", pt: "KV cache → q8_0? Reinicia o motor de IA local.", de: "KV-Zwischenspeicher → q8_0? Startet den örtlichen KI-Motor neu.",
           fr: "Cache KV → q8_0 ? Relance le moteur d'IA local." },
  x_open: { it: "Apri ", en: "Open ", pl: "Otwórz ", uk: "Відкрити ", ru: "Открыть ", es: "Abrir ", pt: "Abrir ", de: "Öffnen ", fr: "Ouvrir " },
  // Chiavi arrivate dallo schema `const it = LANG === "it"` + `it ? ... : ...`,
  // che era testo fuori dal dizionario: chi non usava italiano o inglese
  // vedeva l'inglese comunque, qualunque lingua avesse scelto.
  x_ctx: { it: "Contesto", en: "Context", pl: "Kontekst", uk: "Контекст", ru: "Контекст", es: "Contexto", pt: "Contexto", de: "Kontext", fr: "Contexte" },
  x_gttcap: { it: "Cap GTT", en: "GTT cap", pl: "Limit GTT", uk: "Ліміт GTT", ru: "Предел GTT", es: "Límite del GTT", pt: "Limite do GTT", de: "GTT-Grenze", fr: "Limite du GTT" },
  x_unlocked: { it: "sbloccato", en: "unlocked", pl: "odblokowane", uk: "розблоковано", ru: "разблокировано", es: "desbloqueado", pt: "liberado", de: "freigegeben", fr: "déverrouillé" },
  x_kv: { it: "KV cache q8_0", en: "KV cache q8_0", pl: "KV cache q8_0", uk: "KV cache q8_0", ru: "KV cache q8_0", es: "KV cache q8_0", pt: "KV cache q8_0", de: "KV-Zwischenspeicher q8_0",
          fr: "Cache KV q8_0" },
  x_gttbtn: { it: "Sblocca GTT (riavvio)", en: "Unlock GTT (reboot)", pl: "Odblokuj GTT (restart)", uk: "Розблокувати GTT (перезавантаження)",
              ru: "Разблокировать GTT (перезагрузка)", es: "Desbloquear GTT (reinicio)", pt: "Liberar o GTT (reinício)", de: "GTT freigeben (Neustart)",
              fr: "Déverrouiller le GTT (redémarrage)" },
  x_optdone: { it: "Già ottimizzato ✓", en: "Already optimized ✓", pl: "Już zoptymalizowane ✓", uk: "Уже оптимізовано ✓",
               ru: "Уже настроено ✓", es: "Ya optimizado ✓", pt: "Já otimizado ✓", de: "Bereits abgestimmt ✓",
               fr: "Déjà optimisé ✓" },
  x_applying: { it: "Applico…", en: "Applying…", pl: "Stosowanie…", uk: "Застосування…", ru: "Применяю…", es: "Aplicando…", pt: "Aplicando…", de: "Wird angewendet…", fr: "Application…" },
  x_mods: { it: "Moduli esposti", en: "Exposed modules", pl: "Udostępnione moduły", uk: "Відкриті модулі",
            ru: "Открытые модули", es: "Módulos expuestos", pt: "Módulos expostos", de: "Offene Module",
            fr: "Modules exposés" },
  x_updated: { it: "Aggiornato", en: "Updated", pl: "Zaktualizowano", uk: "Оновлено", ru: "Обновлено", es: "Actualizado", pt: "Atualizado", de: "Aktualisiert", fr: "Mis à jour" },
  x_localai: { it: "AI locale", en: "On-device AI", pl: "SI lokalna", uk: "Локальний ШІ", ru: "Локальный ИИ", es: "IA local", pt: "IA local", de: "Örtliche KI", fr: "IA locale" },
  x_nomodels: { it: "nessun modello installato", en: "no models installed", pl: "brak zainstalowanych modeli", uk: "моделі не встановлені",
                ru: "модели не установлены", es: "no hay modelos instalados", pt: "nenhum modelo instalado", de: "keine Modelle eingerichtet",
                fr: "aucun modèle installé" },
  x_engine: { it: "Motore", en: "Engine", pl: "Silnik", uk: "Рушій", ru: "Движок", es: "Motor", pt: "Motor", de: "Motor", fr: "Moteur" },
  x_accel: { it: "Accelerazione", en: "Acceleration", pl: "Akceleracja", uk: "Прискорення", ru: "Ускорение", es: "Aceleración", pt: "Aceleração", de: "Beschleunigung", fr: "Accélération" },
  x_apikey: { it: "Chiave API di Unsloth", en: "Unsloth API key", pl: "Klucz API Unsloth", uk: "Ключ API Unsloth",
              ru: "Ключ API Unsloth", es: "Clave de API de Unsloth", pt: "Chave de API do Unsloth", de: "API-Schlüssel von Unsloth",
              fr: "Clé d'API Unsloth" },
  x_save: { it: "Salva", en: "Save", pl: "Zapisz", uk: "Зберегти", ru: "Сохранить", es: "Guardar", pt: "Salvar", de: "Sichern", fr: "Enregistrer" },
  x_first: { it: "Primo accesso a Unsloth Studio", en: "First sign-in to Unsloth Studio", pl: "Pierwsze logowanie do Unsloth Studio", uk: "Перший вхід до Unsloth Studio",
             ru: "Первый вход в Unsloth Studio", es: "Primer acceso a Unsloth Studio", pt: "Primeiro acesso ao Unsloth Studio", de: "Erste Anmeldung bei Unsloth Studio",
             fr: "Première connexion à Unsloth Studio" },
  x_user: { it: "Utente", en: "User", pl: "Użytkownik", uk: "Користувач", ru: "Пользователь", es: "Usuario", pt: "Usuário", de: "Benutzer", fr: "Utilisateur" },
  x_initpw: { it: "Password iniziale", en: "Initial password", pl: "Hasło początkowe", uk: "Початковий пароль",
              ru: "Начальный пароль", es: "Contraseña inicial", pt: "Senha inicial", de: "Anfangskennwort",
              fr: "Mot de passe initial" },
  x_chat: { it: "Chat", en: "Chat", pl: "Czat", uk: "Чат", ru: "Чат", es: "Chat", pt: "Chat", de: "Chat", fr: "Discussion" },
  x_models: { it: "Modelli installati", en: "Installed models", pl: "Zainstalowane modele", uk: "Встановлені моделі",
              ru: "Установленные модели", es: "Modelos instalados", pt: "Modelos instalados", de: "Eingerichtete Modelle",
              fr: "Modèles installés" },
  x_pullph: { it: "scarica modello (es. qwen3:14b)", en: "pull model (e.g. qwen3:14b)", pl: "pobierz model (np. qwen3:14b)", uk: "завантажити модель (напр. qwen3:14b)",
              ru: "скачать модель (напр. qwen3:14b)", es: "descargar modelo (p. ej. qwen3:14b)", pt: "baixar modelo (ex.: qwen3:14b)", de: "Modell holen (z. B. qwen3:14b)",
              fr: "télécharger un modèle (p. ex. qwen3:14b)" },
  x_pull: { it: "Scarica", en: "Pull", pl: "Pobierz", uk: "Завантажити", ru: "Скачать", es: "Descargar", pt: "Baixar", de: "Holen", fr: "Télécharger" },
  x_optai: { it: "Ottimizza per AI", en: "Optimize for AI", pl: "Zoptymalizuj pod SI", uk: "Оптимізувати для ШІ",
             ru: "Настроить под ИИ", es: "Optimizar para IA", pt: "Otimizar para IA", de: "Auf KI abstimmen",
             fr: "Optimiser pour l'IA" },
  x_keysaved: { it: "Chiave salvata", en: "Key saved", pl: "Zapisano klucz", uk: "Ключ збережено", ru: "Ключ сохранён", es: "Clave guardada", pt: "Chave salva", de: "Schlüssel gesichert",
                fr: "Clé enregistrée" },
  x_dlstart: { it: "Download avviato…", en: "Download started…", pl: "Rozpoczęto pobieranie…", uk: "Завантаження розпочато…",
               ru: "Загрузка начата…", es: "Descarga iniciada…", pt: "Download iniciado…", de: "Herunterladen begonnen…",
               fr: "Téléchargement lancé…" },
  x_nonet: { it: "Nessuna rete.", en: "No networks.", pl: "Brak sieci.", uk: "Немає мереж.", ru: "Сетей нет.", es: "No hay redes.", pt: "Nenhuma rede.", de: "Keine Netze.",
             fr: "Aucun réseau." },
  x_node: { it: "Nodo", en: "Node", pl: "Węzeł", uk: "Вузол", ru: "Узел", es: "Nodo", pt: "Nó", de: "Knoten", fr: "Nœud" },
  x_state: { it: "Stato", en: "Status", pl: "Stan", uk: "Стан", ru: "Состояние", es: "Estado", pt: "Estado", de: "Zustand", fr: "État" },
  x_nets: { it: "Reti", en: "Networks", pl: "Sieci", uk: "Мережі", ru: "Сети", es: "Redes", pt: "Redes", de: "Netze", fr: "Réseaux" },
  x_join: { it: "Entra", en: "Join", pl: "Dołącz", uk: "Приєднатися", ru: "Присоединиться", es: "Unirse", pt: "Entrar", de: "Beitreten", fr: "Rejoindre" },
  x_left: { it: "Uscito dalla rete", en: "Left network", pl: "Opuszczono sieć", uk: "Мережу покинуто",
            ru: "Сеть покинута", es: "Has salido de la red", pt: "Você saiu da rede", de: "Netz verlassen",
            fr: "Réseau quitté" },
  x_closed: { it: "Schede chiuse", en: "Closed cards", pl: "Zamknięte karty", uk: "Закриті картки",
              ru: "Закрытые карточки", es: "Fichas cerradas", pt: "Cartões fechados", de: "Geschlossene Karten",
              fr: "Cartes fermées" },
  // Chiavi arrivate dai ternari LANG === "it" ? ... : ... , che erano
  // testo fuori dal dizionario e quindi NON traducibile in altre lingue.
  ly_saved: { it: "Disposizione salvata", en: "Layout saved", pl: "Zapisano układ", uk: "Розташування збережено",
              ru: "Расположение сохранено", es: "Disposición guardada", pt: "Disposição salva", de: "Anordnung gesichert",
              fr: "Disposition enregistrée" },
  m_telem: { it: "Telemetria", en: "Telemetry", pl: "Telemetria", uk: "Телеметрія", ru: "Телеметрия", es: "Telemetría", pt: "Telemetria", de: "Messwerte", fr: "Télémétrie" },
  m_sys: { it: "Stato sistema", en: "System status", pl: "Stan systemu", uk: "Стан системи",
           ru: "Состояние системы", es: "Estado del sistema", pt: "Estado do sistema", de: "Zustand des Systems",
           fr: "État du système" },
  m_ctrl: { it: "Controlli", en: "Controls", pl: "Sterowanie", uk: "Керування", ru: "Управление", es: "Controles", pt: "Controles", de: "Steuerung", fr: "Commandes" },
  m_apps: { it: "App e pacchetti", en: "Apps & packages", pl: "Aplikacje i pakiety", uk: "Програми та пакунки",
            ru: "Программы и пакеты", es: "Aplicaciones y paquetes", pt: "Aplicativos e pacotes", de: "Anwendungen und Pakete",
            fr: "Applications et paquets" },
  m_launch: { it: "Avvio app", en: "Launcher", pl: "Uruchamianie aplikacji", uk: "Запуск програм", ru: "Запуск программ", es: "Lanzador", pt: "Lançador", de: "Starter", fr: "Lanceur" },
  m_term: { it: "Terminale", en: "Terminal", pl: "Terminal", uk: "Термінал", ru: "Терминал", es: "Terminal", pt: "Terminal", de: "Terminal", fr: "Terminal" },
  m_rules: { it: "Regole auto", en: "Auto rules", pl: "Reguły automatyczne", uk: "Автоматичні правила",
             ru: "Автоматические правила", es: "Reglas automáticas", pt: "Regras automáticas", de: "Selbsttätige Regeln",
             fr: "Règles automatiques" },
  m_soon: { it: "Modulo attivo — interfaccia in arrivo.", en: "Module on — UI coming soon.", pl: "Moduł włączony — interfejs wkrótce.", uk: "Модуль увімкнено — інтерфейс незабаром.",
            ru: "Модуль включён — окно скоро появится.", es: "Módulo encendido — la interfaz llega pronto.", pt: "Módulo ligado — a interface chega em breve.", de: "Modul an — die Oberfläche kommt bald.",
            fr: "Module allumé — l'interface arrive bientôt." },
  w_move: { it: "Sposta", en: "Move", pl: "Przenieś", uk: "Перемістити", ru: "Переместить", es: "Mover", pt: "Mover", de: "Verschieben", fr: "Déplacer" },
  w_coll: { it: "Comprimi", en: "Collapse", pl: "Zwiń", uk: "Згорнути", ru: "Свернуть", es: "Plegar", pt: "Recolher", de: "Einklappen", fr: "Replier" },
  w_close: { it: "Chiudi", en: "Close", pl: "Zamknij", uk: "Закрити", ru: "Закрыть", es: "Cerrar", pt: "Fechar", de: "Schließen", fr: "Fermer" },
  ly_save: { it: "Salva disposizione", en: "Save layout", pl: "Zapisz układ", uk: "Зберегти розташування",
             ru: "Сохранить расположение", es: "Guardar la disposición", pt: "Salvar a disposição", de: "Anordnung sichern",
             fr: "Enregistrer la disposition" },
  ly_resetb: { it: "Ripristina disposizione", en: "Reset layout", pl: "Przywróć układ", uk: "Відновити розташування",
             ru: "Вернуть расположение", es: "Restablecer la disposición", pt: "Restaurar a disposição", de: "Anordnung zurücksetzen",
               fr: "Rétablir la disposition" },
  ly_reset: { it: "Ripristinare la disposizione predefinita?", en: "Reset to the default layout?", pl: "Przywrócić domyślny układ?", uk: "Відновити типове розташування?",
              ru: "Вернуть расположение по умолчанию?", es: "¿Volver a la disposición por defecto?", pt: "Voltar à disposição padrão?", de: "Auf die vorgegebene Anordnung zurücksetzen?",
              fr: "Rétablir la disposition par défaut ?" },
  login_sub: { it: "SkillFishOS · accedi con le credenziali di sistema", en: "SkillFishOS · sign in with your system credentials", pl: "SkillFishOS · zaloguj się danymi systemowymi", uk: "SkillFishOS · увійдіть за системними обліковими даними",
               ru: "SkillFishOS · войдите с системными учётными данными", es: "SkillFishOS · entra con tus credenciales del sistema", pt: "SkillFishOS · entre com as suas credenciais do sistema", de: "SkillFishOS · mit deinen Systemzugangsdaten anmelden",
               fr: "SkillFishOS · connectez-vous avec vos identifiants système" },
  user: { it: "Utente", en: "User", pl: "Użytkownik", uk: "Користувач", ru: "Пользователь", es: "Usuario", pt: "Usuário", de: "Benutzer", fr: "Utilisateur" }, pass: { it: "Password", en: "Password", pl: "Hasło", uk: "Пароль",
                                                                                  ru: "Пароль", es: "Contraseña", pt: "Senha", de: "Kennwort",
                                                                                                                                                    fr: "Mot de passe" },
  enter: { it: "Entra", en: "Sign in", pl: "Zaloguj się", uk: "Увійти", ru: "Войти", es: "Entrar", pt: "Entrar", de: "Anmelden", fr: "Se connecter" }, denied: { it: "accesso negato", en: "access denied", pl: "odmowa dostępu", uk: "доступ заборонено",
                                                                                    ru: "доступ запрещён", es: "acceso denegado", pt: "acesso negado", de: "Zugang verweigert",
                                                                                                                                             fr: "accès refusé" },
  logout: { it: "Esci", en: "Log out", pl: "Wyloguj", uk: "Вийти", ru: "Выйти", es: "Salir", pt: "Sair", de: "Abmelden", fr: "Se déconnecter" }, neterr: { it: "errore di rete", en: "network error", pl: "błąd sieci", uk: "помилка мережі",
                                                                               ru: "ошибка сети", es: "error de red", pt: "erro de rede", de: "Netzfehler",
                                                                                                                                     fr: "erreur réseau" },
  copied: { it: "Copiato", en: "Copied", pl: "Skopiowano", uk: "Скопійовано", ru: "Скопировано", es: "Copiado", pt: "Copiado", de: "Kopiert", fr: "Copié" }, done: { it: "fatto", en: "done", pl: "gotowe", uk: "готово",
                                                                                        ru: "готово", es: "hecho", pt: "pronto", de: "fertig",
                                                                                                                                                        fr: "terminé" },
  g_monitor: { it: "Monitoraggio", en: "Monitoring", pl: "Monitorowanie", uk: "Моніторинг", ru: "Наблюдение", es: "Vigilancia", pt: "Monitoramento", de: "Überwachung", fr: "Surveillance" }, g_control: { it: "Controllo", en: "Control", pl: "Sterowanie", uk: "Керування",
                                                                                                           ru: "Управление", es: "Control", pt: "Controle", de: "Steuerung",
                                                                                                                                                                                       fr: "Commande" },
  g_remote: { it: "Accesso remoto", en: "Remote access", pl: "Dostęp zdalny", uk: "Віддалений доступ", ru: "Доступ издалека", es: "Acceso remoto", pt: "Acesso remoto", de: "Fernzugriff",
              fr: "Accès à distance" }, g_ai: { it: "Intelligenza artificiale", en: "AI", pl: "SI", uk: "ШІ",
                                                                                                                 ru: "ИИ", es: "IA", pt: "IA", de: "KI",
                                                                                                                                                                                                     fr: "IA" },
  g_other: { it: "Altro", en: "Other", pl: "Inne", uk: "Інше", ru: "Прочее", es: "Otros", pt: "Outros", de: "Sonstiges", fr: "Autres" },
  // telemetry
  t_temp: { it: "Temperatura", en: "Temperature", pl: "Temperatura", uk: "Температура", ru: "Температура", es: "Temperatura", pt: "Temperatura", de: "Temperatur", fr: "Température" }, t_load: { it: "Carico", en: "Load", pl: "Obciążenie", uk: "Навантаження",
                                                                                                    ru: "Нагрузка", es: "Carga", pt: "Carga", de: "Last",
                                                                                                                                                                               fr: "Charge" },
  t_freq: { it: "Frequenza", en: "Frequency", pl: "Częstotliwość", uk: "Частота", ru: "Частота", es: "Frecuencia", pt: "Frequência", de: "Takt", fr: "Fréquence" }, t_pow: { it: "Potenza", en: "Power", pl: "Moc", uk: "Потужність",
                                                                                             ru: "Мощность", es: "Potencia", pt: "Potência", de: "Leistungsaufnahme",
                                                                                                                                                            fr: "Puissance" },
  t_volt: { it: "Voltaggio", en: "Voltage", pl: "Napięcie", uk: "Напруга", ru: "Напряжение", es: "Voltaje", pt: "Tensão", de: "Spannung", fr: "Tension" }, t_fan: { it: "Ventola", en: "Fan", pl: "Wentylator", uk: "Вентилятор",
                                                                                      ru: "Вентилятор", es: "Ventilador", pt: "Ventoinha", de: "Lüfter",
                                                                                                                                                     fr: "Ventilateur" }, live: { it: "live", en: "live", pl: "na żywo", uk: "наживо",
                                                                                                                                                              ru: "вживую", es: "en vivo", pt: "ao vivo", de: "live",
                                                                                                                                                                   fr: "en direct" },
  t_percore: { it: "Frequenza per core/thread", en: "Per core/thread frequency", pl: "Częstotliwość na rdzeń/wątek", uk: "Частота на ядро/потік",
               ru: "Частота на ядро/поток", es: "Frecuencia por núcleo/hilo", pt: "Frequência por núcleo/thread", de: "Takt je Kern/Thread",
               fr: "Fréquence par cœur/fil" },
  c_off: { it: "off", en: "off", pl: "wył.", uk: "вимк.", ru: "выкл.", es: "apag.", pt: "deslig.", de: "aus", fr: "éteint" }, c_avg: { it: "med", en: "avg", pl: "śr.", uk: "сер.", ru: "сред.", es: "med.", pt: "méd.", de: "Mittel",
                                                                                                                         fr: "moy" }, c_online: { it: "attivi", en: "online", pl: "aktywne", uk: "активні",
                                                                                                                                ru: "активны", es: "activos", pt: "ativos", de: "aktiv",
                                                                                                                                                                                                                                       fr: "actifs" },
  // status
  s_you: { it: "Sei connesso a", en: "Connected to", pl: "Połączono z", uk: "З'єднано з",
           ru: "Вы подключены к", es: "Estás conectado a", pt: "Você está conectado a", de: "Du bist verbunden mit",
           fr: "Vous êtes connecté à" }, s_host: { it: "Host", en: "Host", pl: "Host", uk: "Вузол",
                                                                                                      ru: "Узел", es: "Equipo", pt: "Máquina", de: "Rechner",
                                                                                                                                 fr: "Machine" },
  s_ip: { it: "IP (rotta)", en: "IP (route)", pl: "IP (trasa)", uk: "IP (маршрут)", ru: "IP (маршрут)", es: "IP (ruta)", pt: "IP (rota)", de: "IP (Route)", fr: "IP (route)" }, s_kernel: { it: "Kernel", en: "Kernel", pl: "Jądro", uk: "Ядро",
                                                                                                  ru: "Ядро", es: "Núcleo", pt: "Kernel", de: "Kernel",
                                                                                                                                                                          fr: "Noyau" },
  s_up: { it: "Uptime", en: "Uptime", pl: "Czas działania", uk: "Час роботи", ru: "Время работы", es: "Tiempo encendido", pt: "Tempo ligado", de: "Laufzeit", fr: "Temps de fonctionnement" }, s_cu: { it: "CU attive", en: "Active CUs", pl: "Aktywne CU", uk: "Активні CU",
                                                                                        ru: "Активные CU", es: "CU activas", pt: "CU ativas", de: "Aktive CU",
                                                                                                                                                                        fr: "CU actives" }, s_ram: { it: "RAM", en: "RAM", pl: "RAM", uk: "RAM",
                                                                                                                                                                          ru: "ОЗУ", es: "RAM", pt: "RAM", de: "RAM",
                                                                                                                                                                          fr: "Mémoire" },
  s_frz_none: { it: "nessuno", en: "none", pl: "brak", uk: "немає", ru: "нет", es: "ninguno", pt: "nenhum", de: "keine", fr: "aucun" },
  s_frz_last: { it: "ultimo il", en: "last on", pl: "ostatnie", uk: "останнє", ru: "последнее", es: "el último", pt: "o último", de: "zuletzt am", fr: "le dernier" },
  s_disk: { it: "Disco /", en: "Disk /", pl: "Dysk /", uk: "Диск /", ru: "Диск /", es: "Disco /", pt: "Disco /", de: "Platte /", fr: "Disque /" }, s_frz: { it: "Freeze rilevati", en: "Freezes detected", pl: "Wykryte zawieszenia", uk: "Виявлені зависання",
                                                                                ru: "Замечено зависаний", es: "Cuelgues detectados", pt: "Travamentos detectados", de: "Erkannte Einfrierer",
                                                                                                                                            fr: "Blocages détectés" },
  // tuner
  c_preset: { it: "Preset", en: "Presets", pl: "Profile", uk: "Профілі", ru: "Наборы", es: "Perfiles", pt: "Perfis", de: "Vorgaben", fr: "Profils" }, c_gov: { it: "Governor GPU", en: "GPU governor", pl: "Regulator GPU", uk: "Регулятор ГП",
                                                                                    ru: "Регулятор видеоядра", es: "Gobernador de la GPU", pt: "Governador da GPU", de: "Governor der GPU",
                                                                                                                                                fr: "Gouverneur du GPU" },
  c_bal: { it: "Bilanciato", en: "Balanced", pl: "Zrównoważony", uk: "Збалансований", ru: "Уравновешенный", es: "Equilibrado", pt: "Equilibrado", de: "Ausgewogen", fr: "Équilibré" }, c_perf: { it: "Performance", en: "Performance", pl: "Wydajność", uk: "Продуктивність",
                                                                                                  ru: "Производительность", es: "Rendimiento", pt: "Desempenho", de: "Leistung",
                                                                                                                                                                                fr: "Performance" },
  c_fan: { it: "Ventola", en: "Fan", pl: "Wentylator", uk: "Вентилятор", ru: "Вентилятор", es: "Ventilador", pt: "Ventoinha", de: "Lüfter", fr: "Ventilateur" }, c_auto: { it: "Auto", en: "Auto", pl: "Auto", uk: "Авто", ru: "Авто", es: "Auto", pt: "Auto", de: "Auto",
                                                                                                                                                        fr: "Auto" }, c_man: { it: "Manuale", en: "Manual", pl: "Ręcznie", uk: "Вручну",
                                                                                                                                                ru: "Вручную", es: "Manual", pt: "Manual", de: "Von Hand",
                                                                                                                                                                                                                                                                   fr: "À la main" },
  c_applied: { it: "Preset {x} applicato", en: "Preset {x} applied", pl: "Zastosowano profil {x}", uk: "Застосовано профіль {x}",
               ru: "Набор {x} применён", es: "Perfil {x} aplicado", pt: "Perfil {x} aplicado", de: "Vorgabe {x} angewendet",
               fr: "Profil {x} appliqué" },
  c_full: { it: "Apri Tuner completo", en: "Open full Tuner", pl: "Otwórz pełny Tuner", uk: "Відкрити повний Tuner",
            ru: "Открыть полный Tuner", es: "Abrir el Tuner completo", pt: "Abrir o Tuner completo", de: "Den vollen Tuner öffnen",
            fr: "Ouvrir le Tuner complet" },
  // hub
  h_open: { it: "Apri Hub", en: "Open Hub", pl: "Otwórz Hub", uk: "Відкрити Hub", ru: "Открыть Hub", es: "Abrir el Hub", pt: "Abrir o Hub", de: "Hub öffnen", fr: "Ouvrir le Hub" }, h_updates: { it: "aggiornamenti", en: "updates", pl: "aktualizacji", uk: "оновлень",
                                                                                                 ru: "обновлений", es: "actualizaciones", pt: "atualizações", de: "Aktualisierungen",
                                                                                                                                                                             fr: "mises à jour" },
  // power
  p_reboot: { it: "Riavvia", en: "Reboot", pl: "Uruchom ponownie", uk: "Перезавантажити", ru: "Перезагрузить", es: "Reiniciar", pt: "Reiniciar", de: "Neu starten", fr: "Redémarrer" }, p_off: { it: "Spegni", en: "Shut down", pl: "Wyłącz", uk: "Вимкнути",
                                                                                                     ru: "Выключить", es: "Apagar", pt: "Desligar", de: "Herunterfahren",
                                                                                                                                                                               fr: "Éteindre" },
  p_conf: { it: "Richiede conferma.", en: "Asks for confirmation.", pl: "Poprosi o potwierdzenie.", uk: "Запитає підтвердження.",
            ru: "Спросит подтверждение.", es: "Pide confirmación.", pt: "Pede confirmação.", de: "Fragt nach einer Bestätigung.",
            fr: "Demande une confirmation." },
  p_qreb: { it: "Riavviare la BC-250?", en: "Reboot the BC-250?", pl: "Uruchomić ponownie BC-250?", uk: "Перезавантажити BC-250?",
            ru: "Перезагрузить BC-250?", es: "¿Reiniciar la BC-250?", pt: "Reiniciar a BC-250?", de: "Die BC-250 neu starten?",
            fr: "Redémarrer la BC-250 ?" }, p_qoff: { it: "Spegnere la BC-250?", en: "Shut down the BC-250?", pl: "Wyłączyć BC-250?", uk: "Вимкнути BC-250?",
                                                                                                                                               ru: "Выключить BC-250?", es: "¿Apagar la BC-250?", pt: "Desligar a BC-250?", de: "Die BC-250 herunterfahren?",
                                                                                                                                            fr: "Éteindre la BC-250 ?" },
  p_rebing: { it: "Riavvio…", en: "Rebooting…", pl: "Ponowne uruchamianie…", uk: "Перезавантаження…", ru: "Перезагрузка…", es: "Reiniciando…", pt: "Reiniciando…", de: "Wird neu gestartet…",
              fr: "Redémarrage…" }, p_offing: { it: "Spegnimento…", en: "Shutting down…", pl: "Wyłączanie…", uk: "Вимкнення…",
                                                                                                                    ru: "Выключение…", es: "Apagando…", pt: "Desligando…", de: "Wird heruntergefahren…",
                                                                                                                                                                                                            fr: "Extinction…" },
  // logs / launcher / rec
  l_refresh: { it: "aggiorna", en: "refresh", pl: "odśwież", uk: "оновити", ru: "обновить", es: "actualizar", pt: "atualizar", de: "auffrischen", fr: "actualiser" }, empty: { it: "(vuoto)", en: "(empty)", pl: "(pusto)", uk: "(порожньо)",
                                                                                       ru: "(пусто)", es: "(vacío)", pt: "(vazio)", de: "(leer)",
                                                                                                                                                             fr: "(vide)" },
  la_hint: { it: "Si apre sullo schermo della scheda.", en: "Opens on the board's screen.", pl: "Otwiera się na ekranie płyty.", uk: "Відкриється на екрані плати.",
             ru: "Откроется на экране самой платы.", es: "Se abre en la pantalla de la placa.", pt: "Abre na tela da placa.", de: "Öffnet sich auf dem Bildschirm der Platine.",
             fr: "S'ouvre sur l'écran de la carte." },
  la_started: { it: "Avviato: {x}", en: "Launched: {x}", pl: "Uruchomiono: {x}", uk: "Запущено: {x}", ru: "Запущено: {x}", es: "Lanzado: {x}", pt: "Iniciado: {x}", de: "Gestartet: {x}",
                fr: "Lancé : {x}" },
  r_none: { it: "Nessuna registrazione.", en: "No recordings.", pl: "Brak nagrań.", uk: "Немає записів.",
            ru: "Записей нет.", es: "No hay grabaciones.", pt: "Nenhuma gravação.", de: "Keine Aufzeichnungen.",
            fr: "Aucun enregistrement." }, r_saved: { it: "Registrazione salvata", en: "Recording saved", pl: "Nagranie zapisane", uk: "Запис збережено",
                                                                                                                       ru: "Запись сохранена", es: "Grabación guardada", pt: "Gravação salva", de: "Aufzeichnung gesichert",
                                                                                                                              fr: "Enregistrement conservé" },
  r_started: { it: "Registrazione avviata", en: "Recording started", pl: "Rozpoczęto nagrywanie", uk: "Запис розпочато",
               ru: "Запись начата", es: "Grabación iniciada", pt: "Gravação iniciada", de: "Aufzeichnung begonnen",
               fr: "Enregistrement lancé" },
  // kvm / terminal
  k_open: { it: "▶ Apri desktop remoto", en: "▶ Open remote desktop", pl: "▶ Otwórz zdalny pulpit", uk: "▶ Відкрити віддалений робочий стіл",
            ru: "▶ Открыть удалённый рабочий стол", es: "▶ Abrir el escritorio remoto", pt: "▶ Abrir a área de trabalho remota", de: "▶ Entfernte Arbeitsfläche öffnen",
            fr: "▶ Ouvrir le bureau à distance" },
  k_hint: { it: "Schermo, tastiera e mouse della scheda — stessa sessione, nessuna password in più.", en: "Screen, keyboard and mouse of the board — same session, no extra password.", pl: "Ekran, klawiatura i mysz płyty — ta sama sesja, bez dodatkowego hasła.", uk: "Екран, клавіатура і миша плати — та сама сесія, без додаткового пароля.",
            ru: "Экран, клавиатура и мышь платы — тот же сеанс, без лишнего пароля.", es: "Pantalla, teclado y ratón de la placa — la misma sesión, sin otra contraseña.", pt: "Tela, teclado e mouse da placa — a mesma sessão, sem outra senha.", de: "Bildschirm, Tastatur und Maus der Platine — dieselbe Sitzung, ohne weiteres Kennwort.",
            fr: "Écran, clavier et souris de la carte — la même session, sans mot de passe en plus." },
  k_ready: { it: "Desktop pronto", en: "Desktop ready", pl: "Pulpit gotowy", uk: "Робочий стіл готовий",
             ru: "Рабочий стол готов", es: "Escritorio listo", pt: "Área de trabalho pronta", de: "Arbeitsfläche bereit",
             fr: "Bureau prêt" }, k_vncpw: { it: "Aperto. Password VNC (se richiesta): ", en: "Opened. VNC password (if asked): ", pl: "Otwarto. Hasło VNC (jeśli zapyta): ", uk: "Відкрито. Пароль VNC (якщо запитає): ",
                                                                                                                      ru: "Открыто. Пароль VNC (если спросит): ", es: "Abierto. Contraseña VNC (si la pide): ", pt: "Aberto. Senha do VNC (se pedir): ", de: "Geöffnet. VNC-Kennwort (falls gefragt): ",
                                                                                                                                       fr: "Ouvert. Mot de passe VNC (s'il est demandé) : " },
  term_open: { it: "▶ Apri terminale", en: "▶ Open terminal", pl: "▶ Otwórz terminal", uk: "▶ Відкрити термінал",
               ru: "▶ Открыть терминал", es: "▶ Abrir la terminal", pt: "▶ Abrir o terminal", de: "▶ Terminal öffnen",
               fr: "▶ Ouvrir le terminal" },
  term_hint: { it: "Shell della scheda — stessa sessione, nessuna password in più.", en: "Board shell — same session, no extra password.", pl: "Powłoka płyty — ta sama sesja, bez dodatkowego hasła.", uk: "Оболонка плати — та сама сесія, без додаткового пароля.",
               ru: "Оболочка платы — тот же сеанс, без лишнего пароля.", es: "Consola de la placa — la misma sesión, sin otra contraseña.", pt: "Console da placa — a mesma sessão, sem outra senha.", de: "Eingabeaufforderung der Platine — dieselbe Sitzung, ohne weiteres Kennwort.",
               fr: "Ligne de commande de la carte — la même session, sans mot de passe en plus." },
  // ai
  ai_engine: { it: "Motore", en: "Engine", pl: "Silnik", uk: "Рушій", ru: "Движок", es: "Motor", pt: "Motor", de: "Motor", fr: "Moteur" }, ai_on: { it: "● acceso", en: "● on", pl: "● wł.", uk: "● увімк.",
                                                                                 ru: "● включён", es: "● encendido", pt: "● ligado", de: "● an",
                                                                                                                                      fr: "● allumé" }, ai_off: { it: "○ spento", en: "○ off", pl: "○ wył.", uk: "○ вимк.",
                                                                                                                                                      ru: "○ выключен", es: "○ apagado", pt: "○ desligado", de: "○ aus",
                                                                                                                                                             fr: "○ éteint" },
  ai_start: { it: "▶ Accendi AI", en: "▶ Turn on AI", pl: "▶ Włącz SI", uk: "▶ Увімкнути ШІ", ru: "▶ Включить ИИ", es: "▶ Encender la IA", pt: "▶ Ligar a IA", de: "▶ KI einschalten",
              fr: "▶ Allumer l'IA" }, ai_stop: { it: "■ Spegni AI", en: "■ Turn off AI", pl: "■ Wyłącz SI", uk: "■ Вимкнути ШІ",
                                                                                                           ru: "■ Выключить ИИ", es: "■ Apagar la IA", pt: "■ Desligar a IA", de: "■ KI ausschalten",
                                                                                                                                                                                                    fr: "■ Éteindre l'IA" },
  ai_open: { it: "Apri l’interfaccia ↗", en: "Open the UI ↗", pl: "Otwórz interfejs ↗", uk: "Відкрити інтерфейс ↗",
             ru: "Открыть окно ↗", es: "Abrir la interfaz ↗", pt: "Abrir a interface ↗", de: "Die Oberfläche öffnen ↗",
             fr: "Ouvrir l'interface ↗" }, ai_ready: { it: "● pronto", en: "● ready", pl: "● gotowy", uk: "● готово",
                                                                                                                                  ru: "● готово", es: "● listo", pt: "● pronto", de: "● bereit",
                                                                                                                                      fr: "● prêt" },
  ai_hint: { it: "Lo stack gira sulla GPU: spegnilo quando giochi.", en: "The stack runs on the GPU: turn it off when gaming.", pl: "Silnik działa na GPU: wyłącz go przed graniem.", uk: "Рушій працює на ГП: вимкніть його перед грою.",
             ru: "Движок работает на видеоядре: выключайте его перед игрой.", es: "El motor corre en la GPU: apágalo cuando vayas a jugar.", pt: "O motor roda na GPU: desligue-o quando for jogar.", de: "Der Motor läuft auf der GPU: schalte ihn zum Spielen aus.",
             fr: "Le moteur tourne sur le GPU : éteignez-le avant de jouer." },
  ai_starting: { it: "Avvio AI… (può richiedere un minuto)", en: "Starting AI… (may take a minute)", pl: "Uruchamianie SI… (może potrwać minutę)", uk: "Запуск ШІ… (може зайняти хвилину)",
                 ru: "Запуск ИИ… (может занять минуту)", es: "Arrancando la IA… (puede tardar un minuto)", pt: "Iniciando a IA… (pode levar um minuto)", de: "KI wird gestartet… (kann eine Minute dauern)",
                 fr: "Démarrage de l'IA… (cela peut prendre une minute)" }, ai_stopping: { it: "Spengo AI", en: "Stopping AI", pl: "Zatrzymywanie SI", uk: "Зупинка ШІ",
                                                                                                                                                                                                             ru: "Выключаю ИИ", es: "Apagando la IA", pt: "Desligando a IA", de: "KI wird ausgeschaltet",
                                                                                                                                                                                                                              fr: "Extinction de l'IA" },
  // wol
  w_wol: { it: "Wake-on-LAN", en: "Wake-on-LAN", pl: "Wake-on-LAN", uk: "Wake-on-LAN", ru: "Wake-on-LAN", es: "Wake-on-LAN", pt: "Wake-on-LAN", de: "Wake-on-LAN", fr: "Wake-on-LAN" }, w_en: { it: "● abilitato", en: "● enabled", pl: "● włączone", uk: "● увімкнено",
                                                                                                 ru: "● включено", es: "● activado", pt: "● ativado", de: "● eingeschaltet",
                                                                                                                                                                             fr: "● activé" }, w_dis: { it: "○ disabilitato", en: "○ disabled", pl: "○ wyłączone", uk: "○ вимкнено",
                                                                                                                                                                                     ru: "○ выключено", es: "○ desactivado", pt: "○ desativado", de: "○ ausgeschaltet",
                                                                                                                                                                                        fr: "○ désactivé" },
  w_enbtn: { it: "Abilita WoL", en: "Enable WoL", pl: "Włącz WoL", uk: "Увімкнути WoL", ru: "Включить WoL", es: "Activar WoL", pt: "Ativar o WoL", de: "WoL einschalten",
             fr: "Activer le WoL" }, w_disbtn: { it: "Disabilita WoL", en: "Disable WoL", pl: "Wyłącz WoL", uk: "Вимкнути WoL",
                                                                                                      ru: "Выключить WoL", es: "Desactivar WoL", pt: "Desativar o WoL", de: "WoL ausschalten",
                                                                                                                                                                                        fr: "Désactiver le WoL" },
  w_wake: { it: "Sveglia un altro dispositivo", en: "Wake another device", pl: "Obudź inne urządzenie", uk: "Розбудити інший пристрій",
            ru: "Разбудить другое устройство", es: "Despertar otro dispositivo", pt: "Acordar outro dispositivo", de: "Ein anderes Gerät aufwecken",
            fr: "Réveiller un autre appareil" }, w_send: { it: "Invia", en: "Send", pl: "Wyślij", uk: "Надіслати",
                                                                                                                                                    ru: "Отправить", es: "Enviar", pt: "Enviar", de: "Senden",
                                                                                                                                                                 fr: "Envoyer" }, w_sent: { it: "Magic packet inviato", en: "Magic packet sent", pl: "Wysłano magic packet", uk: "Magic packet надіслано",
                                                                                                                                                                                                                        ru: "Magic packet отправлен", es: "Magic packet enviado", pt: "Magic packet enviado", de: "Magic Packet gesendet",
                                                                                                                                                                                                                           fr: "Magic packet envoyé" },
  w_sched: { it: "Programma spegnimento/riavvio", en: "Schedule power off/reboot", pl: "Zaplanuj wyłączenie/restart", uk: "Запланувати вимкнення/перезавантаження",
             ru: "Запланировать выключение или перезагрузку", es: "Programar apagado o reinicio", pt: "Agendar desligamento ou reinício", de: "Herunterfahren oder Neustart planen",
             fr: "Programmer l'extinction ou le redémarrage" }, w_cancel: { it: "Annulla", en: "Cancel", pl: "Anuluj", uk: "Скасувати",
                                                                                                                                                                                  ru: "Отменить", es: "Cancelar", pt: "Cancelar", de: "Abbrechen",
                                                                                                                                                                                                   fr: "Annuler" },
  w_qreb: { it: "Riavviare tra {x} min?", en: "Reboot in {x} min?", pl: "Uruchomić ponownie za {x} min?", uk: "Перезавантажити через {x} хв?",
            ru: "Перезагрузить через {x} мин?", es: "¿Reiniciar dentro de {x} min?", pt: "Reiniciar daqui a {x} min?", de: "In {x} Min. neu starten?",
            fr: "Redémarrer dans {x} min ?" }, w_qoff: { it: "Spegnere tra {x} min?", en: "Shut down in {x} min?", pl: "Wyłączyć za {x} min?", uk: "Вимкнути через {x} хв?",
                                                                                                                                                           ru: "Выключить через {x} мин?", es: "¿Apagar dentro de {x} min?", pt: "Desligar daqui a {x} min?", de: "In {x} Min. herunterfahren?",
                                                                                                                                                                   fr: "Éteindre dans {x} min ?" },
  w_updated: { it: "WoL aggiornato", en: "WoL updated", pl: "Zaktualizowano WoL", uk: "WoL оновлено", ru: "WoL обновлён", es: "WoL actualizado", pt: "WoL atualizado", de: "WoL aktualisiert",
               fr: "WoL mis à jour" }, w_rsched: { it: "Riavvio programmato", en: "Reboot scheduled", pl: "Zaplanowano ponowne uruchomienie", uk: "Перезавантаження заплановано",
                                                                                                                    ru: "Перезагрузка запланирована", es: "Reinicio programado", pt: "Reinício agendado", de: "Neustart geplant",
                                                                                                                                                                                                             fr: "Redémarrage programmé" }, w_osched: { it: "Spegnimento programmato", en: "Shutdown scheduled", pl: "Zaplanowano wyłączenie", uk: "Вимкнення заплановано",
                                                                                                                                                                                                                                                                 ru: "Выключение запланировано", es: "Apagado programado", pt: "Desligamento agendado", de: "Herunterfahren geplant",
                                                                                                                                                                                                                                                fr: "Extinction programmée" }, w_canc: { it: "Programmazione annullata", en: "Schedule cancelled", pl: "Anulowano plan", uk: "Планування скасовано",
                                                                                                                                                                                                                                                                                                                                                                                                 ru: "Расписание отменено", es: "Programación cancelada", pt: "Agendamento cancelado", de: "Planung abgebrochen",
                                                                                                                                                                                                                                                                                                                                                                                                  fr: "Programmation annulée" },
  // rules
  ru_throttle: { it: "Auto-throttle a Stock se troppo caldo", en: "Auto-throttle to Stock when too hot", pl: "Automatycznie na Stock przy przegrzaniu", uk: "Автоматично на Stock при перегріві",
                 ru: "Само возвращаться на Stock при перегреве", es: "Bajar solo a Stock si se calienta demasiado", pt: "Voltar sozinho para Stock se esquentar demais", de: "Bei zu viel Wärme von selbst auf Stock zurückgehen",
                 fr: "Revenir tout seul sur Stock s'il fait trop chaud" },
  ru_thresh: { it: "Soglia", en: "Threshold", pl: "Próg", uk: "Поріг", ru: "Порог", es: "Umbral", pt: "Limite", de: "Schwelle", fr: "Seuil" }, ru_last: { it: "Ultima azione", en: "Last action", pl: "Ostatnia akcja", uk: "Остання дія",
                                                                                    ru: "Последнее действие", es: "Última acción", pt: "Última ação", de: "Letzte Aktion",
                                                                                                                                             fr: "Dernière action" },
  ru_on: { it: "● attivo", en: "● on", pl: "● wł.", uk: "● увімк.", ru: "● включено", es: "● activa", pt: "● ativa", de: "● an", fr: "● active" }, ru_off: { it: "○ spento", en: "○ off", pl: "○ wył.", uk: "○ вимк.",
                                                                                ru: "○ выключено", es: "○ apagada", pt: "○ desligada", de: "○ aus",
                                                                                                                                             fr: "○ éteinte" }, ru_enable: { it: "Attiva", en: "Enable", pl: "Włącz", uk: "Увімкнути",
                                                                                                                                                         ru: "Включить", es: "Activar", pt: "Ativar", de: "Einschalten",
                                                                                                                                                                   fr: "Activer" }, ru_disable: { it: "Disattiva", en: "Disable", pl: "Wyłącz", uk: "Вимкнути",
                                                                                                                                                                                                                                   ru: "Выключить", es: "Desactivar", pt: "Desativar", de: "Ausschalten",
                                                                                                                                                                                                                                         fr: "Désactiver" },
  ru_set: { it: "Imposta", en: "Set", pl: "Ustaw", uk: "Встановити", ru: "Задать", es: "Fijar", pt: "Definir", de: "Setzen", fr: "Régler" }, ru_updated: { it: "Regola aggiornata", en: "Rule updated", pl: "Zaktualizowano regułę", uk: "Правило оновлено",
                                                                                     ru: "Правило обновлено", es: "Regla actualizada", pt: "Regra atualizada", de: "Regel aktualisiert",
                                                                                                                                             fr: "Règle mise à jour" }, ru_setdone: { it: "Soglia impostata", en: "Threshold set", pl: "Ustawiono próg", uk: "Поріг встановлено",
                                                                                                                                                                                                       ru: "Порог задан", es: "Umbral fijado", pt: "Limite definido", de: "Schwelle gesetzt",
                                                                                                                                                                                                         fr: "Seuil réglé" },
  ru_frame: { it: "Ultimo fotogramma dello schermo", en: "Last screen frame", pl: "Ostatnia klatka ekranu", uk: "Останній кадр екрана",
              ru: "Последний кадр экрана", es: "Último fotograma de la pantalla", pt: "Último quadro da tela", de: "Letztes Bild des Bildschirms",
              fr: "Dernière image de l'écran" }, ru_noframe: { it: "Nessun fotogramma ancora (attiva il modulo e attendi ~20s).", en: "No frame yet (enable the module and wait ~20s).", pl: "Brak klatki (włącz moduł i poczekaj ~20 s).", uk: "Кадру ще немає (увімкніть модуль і зачекайте ~20 с).",
                                                                                                                                                        ru: "Кадра ещё нет (включите модуль и подождите ~20 с).", es: "Aún no hay fotograma (activa el módulo y espera ~20 s).", pt: "Ainda não há quadro (ative o módulo e espere ~20 s).", de: "Noch kein Bild (schalte das Modul ein und warte ~20 s).",
                                                                                                                                                                   fr: "Pas encore d'image (activez le module et attendez ~20 s)." },
  // aiops
  ao_q: { it: "Domanda (opzionale): perché si è bloccata?", en: "Question (optional): why did it freeze?", pl: "Pytanie (opcjonalnie): dlaczego się zawiesiło?", uk: "Питання (необов'язково): чому воно зависло?",
          ru: "Вопрос (необязательно): почему оно зависло?", es: "Pregunta (opcional): ¿por qué se colgó?", pt: "Pergunta (opcional): por que travou?", de: "Frage (wahlweise): warum ist es eingefroren?",
          fr: "Question (facultatif) : pourquoi s'est-il bloqué ?" },
  ao_btn: { it: "Diagnostica", en: "Diagnose", pl: "Diagnozuj", uk: "Діагностувати", ru: "Разобраться", es: "Diagnosticar", pt: "Diagnosticar", de: "Untersuchen", fr: "Diagnostiquer" }, ao_running: { it: "Analisi in corso col modello locale… (può richiedere un minuto)", en: "Analyzing with the local model… (may take a minute)", pl: "Analiza modelem lokalnym… (może potrwać minutę)", uk: "Аналіз локальною моделлю… (може зайняти хвилину)",
                                                                                                     ru: "Разбор локальной моделью… (может занять минуту)", es: "Analizando con el modelo local… (puede tardar un minuto)", pt: "Analisando com o modelo local… (pode levar um minuto)", de: "Wird mit dem örtlichen Modell untersucht… (kann eine Minute dauern)",
                                                                                                                                                                                   fr: "Analyse avec le modèle local… (cela peut prendre une minute)" },
  ao_hint: { it: "Il modello locale legge log e telemetria e spiega cosa succede. Richiede il motore AI acceso.", en: "The local model reads logs and telemetry and explains what's going on. Needs the AI engine on.", pl: "Model lokalny czyta logi i telemetrię i wyjaśnia, co się dzieje. Wymaga włączonego silnika SI.", uk: "Локальна модель читає журнали й телеметрію і пояснює, що відбувається. Потрібен увімкнений рушій ШІ.",
             ru: "Локальная модель читает журналы и телеметрию и объясняет, что происходит. Нужен включённый движок ИИ.", es: "El modelo local lee los registros y la telemetría y explica qué pasa. Hace falta el motor de IA encendido.", pt: "O modelo local lê os registros e a telemetria e explica o que está acontecendo. Precisa do motor de IA ligado.", de: "Das örtliche Modell liest Protokolle und Messwerte und erklärt, was los ist. Der KI-Motor muss an sein.",
             fr: "Le modèle local lit les journaux et la télémétrie et explique ce qui se passe. Le moteur d'IA doit être allumé." },
  ao_none: { it: "(nessuna risposta)", en: "(no answer)", pl: "(brak odpowiedzi)", uk: "(немає відповіді)",
             ru: "(нет ответа)", es: "(sin respuesta)", pt: "(sem resposta)", de: "(keine Antwort)",
             fr: "(aucune réponse)" }, err: { it: "Errore: ", en: "Error: ", pl: "Błąd: ", uk: "Помилка: ",
                                                                                                                     ru: "Ошибка: ", es: "Error: ", pt: "Erro: ", de: "Fehler: ",
                                                                                                              fr: "Erreur : " },
};
function T(k, vars) {
  let s = (STR[k] && STR[k][LANG]) || (STR[k] && STR[k].en) || k;
  if (vars) for (const v in vars) s = s.replace("{" + v + "}", vars[v]);
  return s;
}

// ⚠️ Il numero da solo non si puo' interpretare. Con la data accanto la riga
// si archivia da sola: chi legge «4 · ultimo il 30/07/2026» capisce subito che
// e' storia vecchia, e chi legge «2 · ultimo oggi» capisce che deve guardare.
function frzTesto(s){
  const n = s.freezes || 0;
  if (!n) return T("s_frz_none");
  const q = s.freeze_last ? new Date(s.freeze_last) : null;
  if (!q || isNaN(q)) return String(n);
  return n + " · " + T("s_frz_last") + " " + q.toLocaleDateString();
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
  m.querySelectorAll("[data-m]").forEach(cb => cb.onchange = async () => {
    await action("/api/config", { module: cb.dataset.m, on: cb.checked }, T("x_updated"));
    // ⚠️ DUE MECCANISMI, NON UNO. Oltre a `modules` sul server, c'e'
    // `layout.hidden` nel localStorage, dove finisce ogni scheda chiusa con la
    // ✕. buildDashboard() controlla anche quello e vince lui. Senza questa
    // riga, chi aveva chiuso una scheda la trovava gia' spuntata qui, la
    // toglieva, la rimetteva, e non succedeva niente: un interruttore che
    // mente. Chi accende un modulo lo vuole vedere.
    if (cb.checked && layout.hidden.includes(cb.dataset.m)) {
      _toggleArr(layout.hidden, cb.dataset.m, false);
      localStorage.setItem("sflayout", JSON.stringify(layout));
    }
    buildDashboard();
  });
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
    // ⤢ apre la telemetria a schermo intero, in una scheda sua, come fanno
    // gia' HUD, Hub, Tuner e AI. La pagina usa lo stesso flusso /api/telemetry
    // e lo stesso telem.js: non e' una seconda telemetria, e' la stessa vista
    // larga.
    card.innerHTML = '<h3>📊 ' + (T("m_telem")) + ' <span class="pill" id="tlive">' + T("live") + '</span>'
      + '<button class="fr-btn" id="tfull" title="' + T("m_telem") + '" style="float:right;background:none;border:0;color:inherit;cursor:pointer">⤢</button>'
      + '</h3><div class="charts"></div>' +
      '<div class="cores"><div class="lab"><span>' + T("t_percore") + ' (MHz)</span><span class="cstat"></span></div>' +
      '<div class="cwrap"><div class="cax"><i></i><div class="cat"></div><i></i></div><div class="cgrid"></div><div class="cbars"></div></div></div>';
    const box = $(".charts", card); const charts = [];
    TELEM.forEach(spec => {
      const el = document.createElement("div"); el.className = "chart";
      const labs = spec.s.map(s => `<span style="color:${s.c}">${s.l} <b class="val" data-k="${s.k}">–</b></span>`).join(" ");
      el.innerHTML = `<div class="lab"><span>${T(spec.t)} (${spec.u})</span><span>${labs}</span></div><canvas></canvas>`;
      box.appendChild(el); charts.push({ spec, m: new Mini($("canvas", el), spec.s), el });
    });
    const bfull = $("#tfull", card);
    if (bfull) bfull.onclick = () => openFrame("SkillFishOS " + T("m_telem"), "/static/telemetria.html");
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
      // Una riga per scheda di rete: cavo, Wi-Fi o ZeroTier, con l'indirizzo
      // oppure «non connessa». Un indirizzo solo, come c'era prima, non dice
      // da quale delle due sta passando ne' se l'altra e' attaccata.
      const reti = (s.reti || []).map(r => {
        const segno = r.tipo === "wifi" ? "📶" : (r.tipo === "zerotier" ? "🌐" : "🔌");
        const che = r.tipo === "wifi" ? "Wi-Fi" : (r.tipo === "zerotier" ? "ZeroTier" : (LANG === "it" ? "cavo" : "wired"));
        const dove = (r.indirizzi && r.indirizzi.length) ? r.indirizzi.join(" ")
                     : (LANG === "it" ? "non connessa" : "not connected");
        return row(segno + " " + r.nome + " (" + che + ")", dove);
      }).join("");
      $("#srows", card).innerHTML = row(T("s_host"), s.host) + reti +
        (s.gateway ? row("↗ gateway", s.gateway) : "") +
        row(T("s_kernel"), s.kernel) +
        row(T("s_up"), s.uptime) + row(T("s_cu"), s.cu) + row(T("s_ram"), s.ram_used_mb ? `${s.ram_used_mb} / ${s.ram_total_mb} MB` : "") +
        row(T("s_disk"), s.disk_used ? `${s.disk_used} / ${s.disk_total} (${s.disk_pct})` : "") + row(T("s_frz"), frzTesto(s));
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
      // La ventola non si comanda da qui: ha il suo modulo, con la curva
      // vera e la pagina a schermo intero. Due posti sullo stesso PWM si
      // sovrascrivono a vicenda.
      "";
    $("#opentuner", card).onclick = () => openFrame("SkillFishOS Tuner", "/static/tuner.html");
    card.querySelectorAll("[data-preset]").forEach(b => b.onclick = () => action("/api/tuner/preset", { name: b.dataset.preset }, T("c_applied", { x: b.dataset.preset })));
    card.querySelectorAll("[data-gov]").forEach(b => b.onclick = () => action("/api/tuner/govmode", { mode: b.dataset.gov }, "Governor: " + b.dataset.gov));
  },
  async ventola(card) {
    // ⚠️ La scheda mostra i due numeri che si guardano e apre il modulo vero.
    // Non rifà il controllo: quello è di skillfish-fand, e due controllori
    // sullo stesso PWM li abbiamo già avuti una volta.
    const nome = (typeof sfT === "function" ? sfT("v_fanmod") : "Ventola");
    card.innerHTML = "<h3>🌀 " + nome + '</h3><div id="vk">…</div>';
    let d = {};
    try { d = await (await api("/api/ventola")).json(); } catch (e) {}
    const s = d.stato || {};
    const t = s.temperatura != null ? s.temperatura.toFixed(1) + " °C" : "—";
    const p = s.duty != null ? Math.round(s.duty) + "%" : "—";
    const g = (s.sensori || []).find(x => x.type === "fan" && x.value);
    $("#vk", card).innerHTML =
      '<div class="stub" style="margin-bottom:8px">' + t + "  ·  " + p +
      (g ? "  ·  " + Math.round(g.value) + " rpm" : "") + "</div>" +
      '<div class="brow"><button class="dbtn" id="openventola" style="border-color:var(--gold)">🌀 ' +
      nome + "</button></div>";
    $("#openventola", card).onclick =
      () => openFrame("SkillFishOS Ventola", "/static/ventola.html");
  },
  async snapshots(card) {
    // ⚠️ La scheda NON gestisce gli snapshot: mostra quanti sono, quando e'
    // stato fatto l'ultimo, e apre la pagina. Due posti che cancellano gli
    // stessi snapshot sono due posti in cui sbagliare.
    const nome = (typeof sfT === "function" ? sfT("s_mod") : "Snapshot");
    card.innerHTML = "<h3>🕒 " + nome + '</h3><div id="snk">…</div>';
    let d = {};
    try { d = await (await api("/api/snapshots")).json(); } catch (e) {}
    const s = d.snapshot || [];
    const daparte = d.daparte || [];
    const ultimo = s.length ? s[0] : null;
    // La data arriva in UTC senza fuso scritto: la Z dice a Date() come leggerla.
    let quando = "—";
    if (ultimo && ultimo.data) {
      const t = new Date(ultimo.data.replace(" ", "T") + "Z");
      if (!isNaN(t)) quando = t.toLocaleString();
    }
    $("#snk", card).innerHTML =
      '<div class="stub" style="margin-bottom:8px">' +
      (typeof sfT === "function" ? sfT("s_count").replace("%s", s.length)
                                 : s.length + " snapshot") +
      (ultimo ? "  ·  " + quando : "") + "</div>" +
      (daparte.length
        ? '<div class="stub" style="margin-bottom:8px;color:var(--copper)">' +
          (typeof sfT === "function" ? sfT("s_aside") : "") + "</div>"
        : "") +
      '<div class="brow"><button class="dbtn" id="opensnap" style="border-color:var(--gold)">🕒 ' +
      nome + "</button></div>";
    $("#opensnap", card).onclick =
      () => openFrame("SkillFishOS " + nome, "/static/snapshots.html");
  },
  async hud(card) {
    // ⚠️ La scheda non configura niente: dice se il pannello e' acceso, di chi
    // e' e quante voci mostra, e apre il modulo. Il HUD appartiene all'utente
    // del desktop — non a chi e' collegato da qui — ed e' giusto vederlo.
    card.innerHTML = '<h3>🪟 HUD</h3><div id="hdk">…</div>';
    let d = {};
    try { d = await (await api("/api/hud")).json(); } catch (e) {}
    const scelte = (d.pref && d.pref.voci) ? d.pref.voci.length : 0;
    const tutte = (d.voci || []).length;
    $("#hdk", card).innerHTML =
      '<div class="stub" style="margin-bottom:8px">' +
      (d.acceso ? "● " : "○ ") + (d.utente || "—") +
      "  ·  " + scelte + "/" + tutte + "</div>" +
      '<div class="brow"><button class="dbtn" id="openhud" style="border-color:var(--gold)">🪟 HUD</button></div>';
    $("#openhud", card).onclick =
      () => openFrame("SkillFishOS HUD", "/static/hud.html");
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
      // Ollama e OpenWebUI sono usciti dal progetto mesi fa: se il motore non
      // e' Unsloth non sappiamo cosa sia, e chiamarlo col nome di un pezzo che
      // non spediamo piu' e' peggio che non nominarlo.
      const engName = uns ? "Unsloth Studio" : "AI stack";
      const uiName = uns ? "Unsloth Studio" : "AI stack";
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
  $("#logout").textContent = T("logout"); applicaTitoli();
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
// I suggerimenti dei bottoni: erano scritti in italiano dentro l'HTML e li
// vedevano tutti cosi'. Adesso l'HTML porta l'inglese e qui si traduce.
function applicaTitoli() {
  document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
    var t = T(el.getAttribute("data-i18n-title"));
    if (t) el.title = t;
  });
}

// Il riquadro chiuso della tendina mostra la lingua in uso. Senza questo
// resterebbe "IT · Italiano" scritto nell'HTML per tutti, che e' il genere di
// difetto che non si vede finche' qualcuno non cambia lingua.
const LANGNAMES = { it: "Italiano", en: "English", de: "Deutsch", es: "Español",
                    fr: "Français", pl: "Polski", pt: "Português (BR)",
                    ru: "Русский", uk: "Українська" };
function mostraLingua() {
  document.querySelectorAll("#lang-code").forEach(e => e.textContent = LANG.toUpperCase());
  document.querySelectorAll("#lang-name").forEach(e => e.textContent = LANGNAMES[LANG] || LANG);
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
  mostraLingua();
  try { const r = await api("/api/me"); if (r.ok) buildDashboard(); else showLogin(); } catch (e) { showLogin(); }
})();
