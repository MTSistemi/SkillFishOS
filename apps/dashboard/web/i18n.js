// Traduzione delle pagine della dashboard che NON caricano app.js.
//
// PERCHE' ESISTE
// index.html carica app.js e prende i testi dal dizionario STR. Le altre tre
// pagine — tuner.html, hub.html, aichat.html — hanno script propri e non
// vedevano quel dizionario: il loro testo era scritto direttamente nell'HTML,
// in ITALIANO. Non era "manca il polacco": lo vedeva in italiano anche chi
// usava l'inglese. tuner.html da solo aveva 49 stringhe cosi'.
//
// COME FUNZIONA
// Ogni elemento con data-i18n="chiave" riceve il testo dalla lingua scelta.
// Se una chiave manca in una lingua si ricade sull'inglese, mai sull'italiano.
// I nomi propri (SkillFishOS, VRAM, GPU, CU) restano come sono: non si
// traducono.

// Stessa scelta della lingua di app.js, e stessa chiave in localStorage, cosi'
// il selettore di index.html vale anche qui.
var SFLANG = localStorage.getItem("sflang") || (function () {
  var n = (navigator.language || "en").toLowerCase();
  if (n.startsWith("it")) return "it";
  if (n.startsWith("pl")) return "pl";
  if (n.startsWith("uk") || n.startsWith("ua")) return "uk";
  return "en";
})();

var SFSTR = {
  // --- comuni ---
  close:      { it: "Chiudi", en: "Close", pl: "Zamknij", uk: "Закрити" },
  apply:      { it: "Applica", en: "Apply", pl: "Zastosuj", uk: "Застосувати" },
  save:       { it: "Salva", en: "Save", pl: "Zapisz", uk: "Зберегти" },
  load:       { it: "Carica", en: "Load", pl: "Wczytaj", uk: "Завантажити" },
  del:        { it: "Elimina", en: "Delete", pl: "Usuń", uk: "Вилучити" },
  test:       { it: "Test", en: "Test", pl: "Test", uk: "Тест" },
  loading:    { it: "Carico…", en: "Loading…", pl: "Wczytywanie…", uk: "Завантаження…" },
  all:        { it: "Tutti", en: "All", pl: "Wszystkie", uk: "Усі" },
  auto:       { it: "Auto", en: "Auto", pl: "Auto", uk: "Авто" },
  manual:     { it: "Manuale", en: "Manual", pl: "Ręcznie", uk: "Вручну" },
  off:        { it: "Off", en: "Off", pl: "Wył.", uk: "Вимк." },

  // --- tuner ---
  t_maxfreq:  { it: "Frequenza max", en: "Max frequency",
                pl: "Maks. częstotliwość", uk: "Макс. частота" },
  t_maxvolt:  { it: "Voltaggio max", en: "Max voltage",
                pl: "Maks. napięcie", uk: "Макс. напруга" },
  t_templim:  { it: "Limite temperatura", en: "Temperature limit",
                pl: "Limit temperatury", uk: "Ліміт температури" },
  t_tempmax:  { it: "temp. max", en: "max temp.", pl: "maks. temp.", uk: "макс. темп." },
  t_persist:  { it: "Salva al boot", en: "Save at boot",
                pl: "Zapisz przy starcie", uk: "Зберегти при завантаженні" },
  t_gov:      { it: "Governor", en: "Governor", pl: "Regulator", uk: "Регулятор" },
  t_bal:      { it: "Bilanciato", en: "Balanced", pl: "Zrównoważony", uk: "Збалансований" },
  t_perf:     { it: "Prestazioni", en: "Performance", pl: "Wydajność", uk: "Продуктивність" },
  t_mode:     { it: "Modalità", en: "Mode", pl: "Tryb", uk: "Режим" },
  t_speed:    { it: "Velocità", en: "Speed", pl: "Prędkość", uk: "Швидкість" },
  t_uv:       { it: "Undervolt (scale)", en: "Undervolt (scale)",
                pl: "Undervolt (skala)", uk: "Undervolt (шкала)" },
  t_uvsugg:   { it: "Suggerisci UV", en: "Suggest UV",
                pl: "Zaproponuj UV", uk: "Запропонувати UV" },
  t_findmax:  { it: "🎰 Trova il massimo", en: "🎰 Find the maximum",
                pl: "🎰 Znajdź maksimum", uk: "🎰 Знайти максимум" },
  t_gpumem:   { it: "Memoria GPU", en: "GPU memory",
                pl: "Pamięć GPU", uk: "Пам'ять ГП" },
  t_applycu:  { it: "Applica CU", en: "Apply CUs", pl: "Zastosuj CU", uk: "Застосувати CU" },
  t_applyco:  { it: "Applica core", en: "Apply cores",
                pl: "Zastosuj rdzenie", uk: "Застосувати ядра" },
  t_testcu:   { it: "Test CU", en: "Test CUs", pl: "Test CU", uk: "Тест CU" },
  t_test60:   { it: "Test (60s)", en: "Test (60s)", pl: "Test (60 s)", uk: "Тест (60 с)" },
  t_curve:    { it: "Curva attiva", en: "Active curve",
                pl: "Aktywna krzywa", uk: "Активна крива" },
  t_curveauto:{ it: "Curva automatica", en: "Automatic curve",
                pl: "Krzywa automatyczna", uk: "Автоматична крива" },
  t_savecurve:{ it: "Salva curva", en: "Save curve",
                pl: "Zapisz krzywą", uk: "Зберегти криву" },
  t_saveas:   { it: "Salva come…", en: "Save as…", pl: "Zapisz jako…", uk: "Зберегти як…" },
  t_addpoint: { it: "+ punto", en: "+ point", pl: "+ punkt", uk: "+ точка" },
  t_profiles: { it: "Profili:", en: "Profiles:", pl: "Profile:", uk: "Профілі:" },
  t_activecu: { it: "– CU attive", en: "– active CUs",
                pl: "– aktywne CU", uk: "– активні CU" },
  t_activeco: { it: "– core attivi", en: "– active cores",
                pl: "– aktywne rdzenie", uk: "– активні ядра" },
  t_core0:    { it: "core 0", en: "core 0", pl: "rdzeń 0", uk: "ядро 0" },
  t_4core:    { it: "4 core", en: "4 cores", pl: "4 rdzenie", uk: "4 ядра" },
  t_6core:    { it: "6 core", en: "6 cores", pl: "6 rdzeni", uk: "6 ядер" },
  t_cmos:     { it: "⚠ Richiede riavvio (scrive nel CMOS BIOS).",
                en: "⚠ Needs a reboot (writes to the BIOS CMOS).",
                pl: "⚠ Wymaga restartu (zapisuje w CMOS BIOS-u).",
                uk: "⚠ Потребує перезавантаження (запис у CMOS BIOS)." },
  t_gridhint: { it: "Ogni riquadro = 1 core fisico con i suoi 2 thread. Il",
                en: "Each box = 1 physical core with its 2 threads. The",
                pl: "Każdy kwadrat = 1 rdzeń fizyczny z 2 wątkami.",
                uk: "Кожен квадрат = 1 фізичне ядро з 2 потоками." },
  t_h_preset: { it: "⚡ Preset", en: "⚡ Presets", pl: "⚡ Profile", uk: "⚡ Профілі" },
  t_h_fan:    { it: "🌀 Ventola", en: "🌀 Fan", pl: "🌀 Wentylator", uk: "🌀 Вентилятор" },
  t_h_gpu:    { it: "🎮 GPU", en: "🎮 GPU", pl: "🎮 GPU", uk: "🎮 ГП" },
  t_h_vram:   { it: "💾 VRAM (UMA)", en: "💾 VRAM (UMA)",
                pl: "💾 VRAM (UMA)", uk: "💾 VRAM (UMA)" },
  t_h_cu:     { it: "🔢 Compute Unit (CU) — a caldo, senza riavvio",
                en: "🔢 Compute Units (CUs) — live, no reboot",
                pl: "🔢 Jednostki obliczeniowe (CU) — na żywo, bez restartu",
                uk: "🔢 Обчислювальні блоки (CU) — наживо, без перезавантаження" },
  t_h_cpu:    { it: "🧠 CPU", en: "🧠 CPU", pl: "🧠 CPU", uk: "🧠 ЦП" },
  t_h_cores:  { it: "🧩 Core CPU — a caldo, senza riavvio",
                en: "🧩 CPU cores — live, no reboot",
                pl: "🧩 Rdzenie CPU — na żywo, bez restartu",
                uk: "🧩 Ядра ЦП — наживо, без перезавантаження" },
  t_noprof:   { it: "(nessun profilo)", en: "(no profile)",
                pl: "(brak profilu)", uk: "(немає профілю)" },

  t_hintcpu:  { it: "≥4000 MHz è solo da benchmark: su alcune board può causare freeze.",
                en: "≥4000 MHz is benchmark-only: on some boards it can cause freezes.",
                pl: "≥4000 MHz tylko do benchmarków: na niektórych płytach powoduje zawieszenia.",
                uk: "≥4000 МГц лише для тестів: на деяких платах спричиняє зависання." },
  t_hintgpu:  { it: "Oltre 2200 MHz con ≤1000 mV viene limitato a 2200 (anti-freeze).",
                en: "Above 2200 MHz with ≤1000 mV it is capped at 2200 (anti-freeze).",
                pl: "Powyżej 2200 MHz przy ≤1000 mV jest ograniczane do 2200 (ochrona przed zawieszeniem).",
                uk: "Вище 2200 МГц при ≤1000 мВ обмежується до 2200 (захист від зависання)." },
  t_coreshint:{ it: "Ogni riquadro = 1 core fisico con i suoi 2 thread. Il core 0 resta sempre acceso: ospita la CPU di avvio, il kernel non può spegnerlo. Spegnere core libera budget termico per far salire la frequenza dei rimanenti. Al riavvio tornano tutti accesi.",
                en: "Each box = 1 physical core with its 2 threads. Core 0 always stays on: it hosts the boot CPU and the kernel cannot switch it off. Turning cores off frees thermal budget so the remaining ones clock higher. A reboot brings them all back.",
                pl: "Każdy kwadrat = 1 rdzeń fizyczny z 2 wątkami. Rdzeń 0 zawsze pozostaje włączony: obsługuje procesor startowy i jądro nie może go wyłączyć. Wyłączanie rdzeni zwalnia budżet termiczny, więc pozostałe osiągają wyższe częstotliwości. Restart włącza wszystkie z powrotem.",
                uk: "Кожен квадрат = 1 фізичне ядро з 2 потоками. Ядро 0 завжди залишається увімкненим: на ньому працює завантажувальний ЦП, і ядро системи не може його вимкнути. Вимкнення ядер вивільняє тепловий бюджет, тож решта працюють на вищій частоті. Перезавантаження вмикає всі назад." },
  t_hintgrid: { it: "Layout fisico dei core (per affinità/pinning dei giochi). MHz live per core.",
                en: "Physical core layout (for game affinity/pinning). Live MHz per core.",
                pl: "Fizyczny układ rdzeni (do przypisywania gier). Częstotliwość na żywo dla każdego rdzenia.",
                uk: "Фізичне розташування ядер (для прив'язки ігор). Частота наживо для кожного ядра." },

  // --- hub ---
  h_cats:     { it: "Categorie", en: "Categories", pl: "Kategorie", uk: "Категорії" },
  h_loadcat:  { it: "Carico il catalogo…", en: "Loading the catalogue…",
                pl: "Wczytywanie katalogu…", uk: "Завантаження каталогу…" },

  // --- chat ---
  a_send:     { it: "Invia", en: "Send", pl: "Wyślij", uk: "Надіслати" },
  a_model:    { it: "modello", en: "model", pl: "model", uk: "модель" },
  a_intro:    { it: "Chiedi qualcosa al modello locale. Gira sulla GPU della BC-250, nessun cloud.",
                en: "Ask the local model something. It runs on the BC-250 GPU, no cloud.",
                pl: "Zapytaj o coś model lokalny. Działa na GPU BC-250, bez chmury.",
                uk: "Запитайте щось у локальної моделі. Працює на ГП BC-250, без хмари." }
};

function sfT(k) {
  var e = SFSTR[k];
  if (!e) return k;
  return e[SFLANG] !== undefined ? e[SFLANG] : e.en;
}

// Riempie ogni elemento con data-i18n. Da chiamare a pagina caricata.
function sfApply(root) {
  (root || document).querySelectorAll("[data-i18n]").forEach(function (el) {
    var k = el.getAttribute("data-i18n");
    var t = sfT(k);
    if (t !== k) el.textContent = t;
  });
  // anche i segnaposto dei campi di testo
  (root || document).querySelectorAll("[data-i18n-ph]").forEach(function (el) {
    var k = el.getAttribute("data-i18n-ph");
    var t = sfT(k);
    if (t !== k) el.placeholder = t;
  });
}

document.addEventListener("DOMContentLoaded", function () { sfApply(); });
