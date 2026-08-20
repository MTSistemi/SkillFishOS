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
  if (n.startsWith("ru")) return "ru";
  if (n.startsWith("es")) return "es";
  // il portoghese e' scritto per il Brasile e vale anche per pt-PT: meglio
  // del ripiego inglese.
  if (n.startsWith("pt")) return "pt";
  if (n.startsWith("de")) return "de";
  return "en";
})();

var SFSTR = {
  // --- comuni ---
  close:      { it: "Chiudi", en: "Close", pl: "Zamknij", uk: "Закрити",
                ru: "Закрыть", es: "Cerrar", pt: "Fechar", de: "Schließen" },
  apply:      { it: "Applica", en: "Apply", pl: "Zastosuj", uk: "Застосувати",
                ru: "Применить", es: "Aplicar", pt: "Aplicar", de: "Anwenden" },
  save:       { it: "Salva", en: "Save", pl: "Zapisz", uk: "Зберегти",
                ru: "Сохранить", es: "Guardar", pt: "Salvar", de: "Sichern" },
  load:       { it: "Carica", en: "Load", pl: "Wczytaj", uk: "Завантажити",
                ru: "Загрузить", es: "Cargar", pt: "Carregar", de: "Laden" },
  del:        { it: "Elimina", en: "Delete", pl: "Usuń", uk: "Вилучити",
                ru: "Удалить", es: "Eliminar", pt: "Excluir", de: "Löschen" },
  test:       { it: "Test", en: "Test", pl: "Test", uk: "Тест",
                ru: "Тест", es: "Probar", pt: "Testar", de: "Prüfen" },
  loading:    { it: "Carico…", en: "Loading…", pl: "Wczytywanie…", uk: "Завантаження…",
                ru: "Загрузка…", es: "Cargando…", pt: "Carregando…", de: "Wird geladen…" },
  all:        { it: "Tutti", en: "All", pl: "Wszystkie", uk: "Усі",
                ru: "Все", es: "Todos", pt: "Todos", de: "Alle" },
  auto:       { it: "Auto", en: "Auto", pl: "Auto", uk: "Авто",
                ru: "Авто", es: "Auto", pt: "Auto", de: "Auto" },
  manual:     { it: "Manuale", en: "Manual", pl: "Ręcznie", uk: "Вручну",
                ru: "Вручную", es: "Manual", pt: "Manual", de: "Von Hand" },
  off:        { it: "Off", en: "Off", pl: "Wył.", uk: "Вимк.",
                ru: "Выкл.", es: "Apag.", pt: "Deslig.", de: "Aus" },

  // --- tuner ---
  t_maxfreq:  { it: "Frequenza max", en: "Max frequency",
                pl: "Maks. częstotliwość", uk: "Макс. частота",
                ru: "Макс. частота", es: "Frecuencia máx.", pt: "Frequência máx.", de: "Höchster Takt" },
  t_maxvolt:  { it: "Voltaggio max", en: "Max voltage",
                pl: "Maks. napięcie", uk: "Макс. напруга",
                ru: "Макс. напряжение", es: "Voltaje máx.", pt: "Tensão máx.", de: "Höchste Spannung" },
  t_templim:  { it: "Limite temperatura", en: "Temperature limit",
                pl: "Limit temperatury", uk: "Ліміт температури",
                ru: "Предел температуры", es: "Límite de temperatura", pt: "Limite de temperatura", de: "Temperaturgrenze" },
  t_tempmax:  { it: "temp. max", en: "max temp.", pl: "maks. temp.", uk: "макс. темп.",
                ru: "макс. темп.", es: "temp. máx.", pt: "temp. máx.", de: "Höchsttemp." },
  t_persist:  { it: "Salva al boot", en: "Save at boot",
                pl: "Zapisz przy starcie", uk: "Зберегти при завантаженні",
                ru: "Сохранить при загрузке", es: "Guardar al arranque", pt: "Salvar no boot", de: "Beim Start sichern" },
  t_gov:      { it: "Governor", en: "Governor", pl: "Regulator", uk: "Регулятор",
                ru: "Регулятор", es: "Gobernador", pt: "Governador", de: "Governor" },
  t_bal:      { it: "Bilanciato", en: "Balanced", pl: "Zrównoważony", uk: "Збалансований",
                ru: "Уравновешенный", es: "Equilibrado", pt: "Equilibrado", de: "Ausgewogen" },
  t_perf:     { it: "Prestazioni", en: "Performance", pl: "Wydajność", uk: "Продуктивність",
                ru: "Производительность", es: "Rendimiento", pt: "Desempenho", de: "Leistung" },
  t_mode:     { it: "Modalità", en: "Mode", pl: "Tryb", uk: "Режим",
                ru: "Режим", es: "Modo", pt: "Modo", de: "Betriebsart" },
  t_speed:    { it: "Velocità", en: "Speed", pl: "Prędkość", uk: "Швидкість",
                ru: "Скорость", es: "Velocidad", pt: "Velocidade", de: "Drehzahl" },
  t_uv:       { it: "Undervolt (scale)", en: "Undervolt (scale)",
                pl: "Undervolt (skala)", uk: "Undervolt (шкала)",
                ru: "Undervolt (шкала)", es: "Undervolt (escala)", pt: "Undervolt (escala)", de: "Undervolting (Skala)" },
  t_uvsugg:   { it: "Suggerisci UV", en: "Suggest UV",
                pl: "Zaproponuj UV", uk: "Запропонувати UV",
                ru: "Предложить UV", es: "Sugerir UV", pt: "Sugerir UV", de: "UV vorschlagen" },
  t_findmax:  { it: "🎰 Trova il massimo", en: "🎰 Find the maximum",
                pl: "🎰 Znajdź maksimum", uk: "🎰 Знайти максимум",
                ru: "🎰 Найти максимум", es: "🎰 Busca el máximo", pt: "🎰 Ache o máximo", de: "🎰 Finde das Maximum" },
  t_gpumem:   { it: "Memoria GPU", en: "GPU memory",
                pl: "Pamięć GPU", uk: "Пам'ять ГП",
                ru: "Память видеоядра", es: "Memoria de la GPU", pt: "Memória da GPU", de: "Speicher der GPU" },
  t_applycu:  { it: "Applica CU", en: "Apply CUs", pl: "Zastosuj CU", uk: "Застосувати CU",
                ru: "Применить CU", es: "Aplicar CU", pt: "Aplicar CU", de: "CU anwenden" },
  t_applyco:  { it: "Applica core", en: "Apply cores",
                pl: "Zastosuj rdzenie", uk: "Застосувати ядра",
                ru: "Применить ядра", es: "Aplicar núcleos", pt: "Aplicar núcleos", de: "Kerne anwenden" },
  t_testcu:   { it: "Test CU", en: "Test CUs", pl: "Test CU", uk: "Тест CU",
                ru: "Проверить CU", es: "Probar CU", pt: "Testar CU", de: "CU prüfen" },
  t_test60:   { it: "Test (60s)", en: "Test (60s)", pl: "Test (60 s)", uk: "Тест (60 с)",
                ru: "Тест (60 с)", es: "Prueba (60 s)", pt: "Teste (60 s)", de: "Prüfung (60 s)" },
  t_curve:    { it: "Curva attiva", en: "Active curve",
                pl: "Aktywna krzywa", uk: "Активна крива",
                ru: "Действующая кривая", es: "Curva activa", pt: "Curva ativa", de: "Aktive Kurve" },
  t_curveauto:{ it: "Curva automatica", en: "Automatic curve",
                pl: "Krzywa automatyczna", uk: "Автоматична крива",
                ru: "Автоматическая кривая", es: "Curva automática", pt: "Curva automática", de: "Selbsttätige Kurve" },
  t_savecurve:{ it: "Salva curva", en: "Save curve",
                pl: "Zapisz krzywą", uk: "Зберегти криву",
                ru: "Сохранить кривую", es: "Guardar curva", pt: "Salvar curva", de: "Kurve sichern" },
  t_saveas:   { it: "Salva come…", en: "Save as…", pl: "Zapisz jako…", uk: "Зберегти як…",
                ru: "Сохранить как…", es: "Guardar como…", pt: "Salvar como…", de: "Sichern unter…" },
  t_addpoint: { it: "+ punto", en: "+ point", pl: "+ punkt", uk: "+ точка",
                ru: "+ точка", es: "+ punto", pt: "+ ponto", de: "+ Punkt" },
  t_profiles: { it: "Profili:", en: "Profiles:", pl: "Profile:", uk: "Профілі:",
                ru: "Наборы:", es: "Perfiles:", pt: "Perfis:", de: "Vorgaben:" },
  t_activecu: { it: "– CU attive", en: "– active CUs",
                pl: "– aktywne CU", uk: "– активні CU",
                ru: "– активные CU", es: "– CU activas", pt: "– CU ativas", de: "– aktive CU" },
  t_activeco: { it: "– core attivi", en: "– active cores",
                pl: "– aktywne rdzenie", uk: "– активні ядра",
                ru: "– активные ядра", es: "– núcleos activos", pt: "– núcleos ativos", de: "– aktive Kerne" },
  t_core0:    { it: "core 0", en: "core 0", pl: "rdzeń 0", uk: "ядро 0",
                ru: "ядро 0", es: "núcleo 0", pt: "núcleo 0", de: "Kern 0" },
  t_4core:    { it: "4 core", en: "4 cores", pl: "4 rdzenie", uk: "4 ядра",
                ru: "4 ядра", es: "4 núcleos", pt: "4 núcleos", de: "4 Kerne" },
  t_6core:    { it: "6 core", en: "6 cores", pl: "6 rdzeni", uk: "6 ядер",
                ru: "6 ядер", es: "6 núcleos", pt: "6 núcleos", de: "6 Kerne" },
  t_cmos:     { it: "⚠ Richiede riavvio (scrive nel CMOS BIOS).",
                en: "⚠ Needs a reboot (writes to the BIOS CMOS).",
                pl: "⚠ Wymaga restartu (zapisuje w CMOS BIOS-u).",
                uk: "⚠ Потребує перезавантаження (запис у CMOS BIOS).",
                ru: "⚠ Нужна перезагрузка (запись в CMOS BIOS).", es: "⚠ Necesita reiniciar (escribe en la CMOS de la BIOS).", pt: "⚠ Precisa reiniciar (grava na CMOS da BIOS).", de: "⚠ Braucht einen Neustart (schreibt in das CMOS des BIOS)." },
  t_gridhint: { it: "Ogni riquadro = 1 core fisico con i suoi 2 thread. Il",
                en: "Each box = 1 physical core with its 2 threads. The",
                pl: "Każdy kwadrat = 1 rdzeń fizyczny z 2 wątkami.",
                uk: "Кожен квадрат = 1 фізичне ядро з 2 потоками.",
                ru: "Каждый квадрат = 1 физическое ядро с двумя потоками.", es: "Cada casilla = 1 núcleo físico con sus 2 hilos.", pt: "Cada quadrado = 1 núcleo físico com suas 2 threads.", de: "Jedes Kästchen = 1 physischer Kern mit seinen 2 Threads." },
  t_h_preset: { it: "⚡ Preset", en: "⚡ Presets", pl: "⚡ Profile", uk: "⚡ Профілі",
                ru: "⚡ Наборы", es: "⚡ Perfiles", pt: "⚡ Perfis", de: "⚡ Vorgaben" },
  t_h_fan:    { it: "🌀 Ventola", en: "🌀 Fan", pl: "🌀 Wentylator", uk: "🌀 Вентилятор",
                ru: "🌀 Вентилятор", es: "🌀 Ventilador", pt: "🌀 Ventoinha", de: "🌀 Lüfter" },
  t_h_gpu:    { it: "🎮 GPU", en: "🎮 GPU", pl: "🎮 GPU", uk: "🎮 ГП",
                ru: "🎮 Видеоядро", es: "🎮 GPU", pt: "🎮 GPU", de: "🎮 GPU" },
  t_h_vram:   { it: "💾 VRAM (UMA)", en: "💾 VRAM (UMA)",
                pl: "💾 VRAM (UMA)", uk: "💾 VRAM (UMA)",
                ru: "💾 Видеопамять (UMA)", es: "💾 VRAM (UMA)", pt: "💾 VRAM (UMA)", de: "💾 Grafikspeicher (UMA)" },
  t_h_cu:     { it: "🔢 Compute Unit (CU) — a caldo, senza riavvio",
                en: "🔢 Compute Units (CUs) — live, no reboot",
                pl: "🔢 Jednostki obliczeniowe (CU) — na żywo, bez restartu",
                uk: "🔢 Обчислювальні блоки (CU) — наживо, без перезавантаження",
                ru: "🔢 Вычислительные блоки (CU) — на ходу, без перезагрузки", es: "🔢 Unidades de cómputo (CU) — en caliente, sin reiniciar", pt: "🔢 Unidades de computação (CU) — em tempo real, sem reiniciar", de: "🔢 Recheneinheiten (CU) — im Betrieb, ohne Neustart" },
  t_h_cpu:    { it: "🧠 CPU", en: "🧠 CPU", pl: "🧠 CPU", uk: "🧠 ЦП",
                ru: "🧠 Процессор", es: "🧠 CPU", pt: "🧠 CPU", de: "🧠 CPU" },
  t_h_cores:  { it: "🧩 Core CPU — a caldo, senza riavvio",
                en: "🧩 CPU cores — live, no reboot",
                pl: "🧩 Rdzenie CPU — na żywo, bez restartu",
                uk: "🧩 Ядра ЦП — наживо, без перезавантаження",
                ru: "🧩 Ядра процессора — на ходу, без перезагрузки", es: "🧩 Núcleos de la CPU — en caliente, sin reiniciar", pt: "🧩 Núcleos da CPU — em tempo real, sem reiniciar", de: "🧩 CPU-Kerne — im Betrieb, ohne Neustart" },
  t_noprof:   { it: "(nessun profilo)", en: "(no profile)",
                pl: "(brak profilu)", uk: "(немає профілю)",
                ru: "(нет набора)", es: "(sin perfil)", pt: "(sem perfil)", de: "(keine Vorgabe)" },

  t_hintcpu:  { it: "≥4000 MHz è solo da benchmark: su alcune board può causare freeze.",
                en: "≥4000 MHz is benchmark-only: on some boards it can cause freezes.",
                pl: "≥4000 MHz tylko do benchmarków: na niektórych płytach powoduje zawieszenia.",
                uk: "≥4000 МГц лише для тестів: на деяких платах спричиняє зависання.",
                ru: "≥4000 МГц — только для измерений: на некоторых платах вызывает зависания.", es: "≥4000 MHz es solo para medir: en algunas placas provoca cuelgues.", pt: "≥4000 MHz é só para medir: em algumas placas provoca travamentos.", de: "≥4000 MHz sind nur zum Messen: auf manchen Platinen frieren sie das System ein." },
  t_hintgpu:  { it: "Oltre 2200 MHz con ≤1000 mV viene limitato a 2200 (anti-freeze).",
                en: "Above 2200 MHz with ≤1000 mV it is capped at 2200 (anti-freeze).",
                pl: "Powyżej 2200 MHz przy ≤1000 mV jest ograniczane do 2200 (ochrona przed zawieszeniem).",
                uk: "Вище 2200 МГц при ≤1000 мВ обмежується до 2200 (захист від зависання).",
                ru: "Выше 2200 МГц при ≤1000 мВ ограничивается до 2200 (защита от зависания).", es: "Por encima de 2200 MHz con ≤1000 mV se limita a 2200 (anticuelgue).", pt: "Acima de 2200 MHz com ≤1000 mV é limitado a 2200 (antitravamento).", de: "Über 2200 MHz bei ≤1000 mV wird auf 2200 begrenzt (Schutz vor Einfrieren)." },
  t_coreshint:{ it: "Ogni riquadro = 1 core fisico con i suoi 2 thread. Il core 0 resta sempre acceso: ospita la CPU di avvio, il kernel non può spegnerlo. Spegnere core libera budget termico per far salire la frequenza dei rimanenti. Al riavvio tornano tutti accesi.",
                en: "Each box = 1 physical core with its 2 threads. Core 0 always stays on: it hosts the boot CPU and the kernel cannot switch it off. Turning cores off frees thermal budget so the remaining ones clock higher. A reboot brings them all back.",
                pl: "Każdy kwadrat = 1 rdzeń fizyczny z 2 wątkami. Rdzeń 0 zawsze pozostaje włączony: obsługuje procesor startowy i jądro nie może go wyłączyć. Wyłączanie rdzeni zwalnia budżet termiczny, więc pozostałe osiągają wyższe częstotliwości. Restart włącza wszystkie z powrotem.",
                uk: "Кожен квадрат = 1 фізичне ядро з 2 потоками. Ядро 0 завжди залишається увімкненим: на ньому працює завантажувальний ЦП, і ядро системи не може його вимкнути. Вимкнення ядер вивільняє тепловий бюджет, тож решта працюють на вищій частоті. Перезавантаження вмикає всі назад.",
                ru: "Каждый квадрат = 1 физическое ядро с двумя потоками. Ядро 0 всегда включено: на нём держится загрузочный процессор, и ядро системы не может его выключить. Выключение ядер освобождает тепловой запас, и оставшиеся поднимаются в частоте. После перезагрузки включаются все.", es: "Cada casilla = 1 núcleo físico con sus 2 hilos. El núcleo 0 se queda siempre encendido: lleva la CPU de arranque y el núcleo del sistema no puede apagarlo. Apagar núcleos libera presupuesto térmico, así los que quedan suben de frecuencia. Al reiniciar vuelven todos.", pt: "Cada quadrado = 1 núcleo físico com suas 2 threads. O núcleo 0 fica sempre ligado: é ele que segura a CPU de boot e o kernel não consegue desligá-lo. Desligar núcleos libera orçamento térmico, então os que sobram sobem de frequência. Ao reiniciar todos voltam.", de: "Jedes Kästchen = 1 physischer Kern mit seinen 2 Threads. Kern 0 bleibt immer an: er trägt die Start-CPU, und der Kernel kann ihn nicht abschalten. Abgeschaltete Kerne geben Wärmebudget frei, sodass die übrigen höher takten. Beim Neustart sind alle wieder an." },
  t_hintgrid: { it: "Layout fisico dei core (per affinità/pinning dei giochi). MHz live per core.",
                en: "Physical core layout (for game affinity/pinning). Live MHz per core.",
                pl: "Fizyczny układ rdzeni (do przypisywania gier). Częstotliwość na żywo dla każdego rdzenia.",
                uk: "Фізичне розташування ядер (для прив'язки ігор). Частота наживо для кожного ядра.",
                ru: "Физическое расположение ядер (для привязки игр). Частота каждого ядра вживую.", es: "Disposición física de los núcleos (para fijar juegos). MHz en vivo por núcleo.", pt: "Disposição física dos núcleos (para fixar jogos). MHz ao vivo por núcleo.", de: "Räumliche Anordnung der Kerne (zum Binden von Spielen). Takt je Kern in Echtzeit." },

  // --- hub ---
  h_rebuild:  { it: "Ricostruisci catalogo", en: "Rebuild the catalogue",
                pl: "Przebuduj katalog", uk: "Перебудувати каталог",
                ru: "Перестроить каталог", es: "Reconstruir el catálogo",
                pt: "Reconstruir o catálogo", de: "Den Katalog neu aufbauen" },
  h_cats:     { it: "Categorie", en: "Categories", pl: "Kategorie", uk: "Категорії",
                ru: "Разделы", es: "Categorías", pt: "Categorias", de: "Kategorien" },
  h_loadcat:  { it: "Carico il catalogo…", en: "Loading the catalogue…",
                pl: "Wczytywanie katalogu…", uk: "Завантаження каталогу…",
                ru: "Загрузка каталога…", es: "Cargando el catálogo…", pt: "Carregando o catálogo…", de: "Der Katalog wird geladen…" },

  // --- chat ---
  a_send:     { it: "Invia", en: "Send", pl: "Wyślij", uk: "Надіслати",
                ru: "Отправить", es: "Enviar", pt: "Enviar", de: "Senden" },
  a_model:    { it: "modello", en: "model", pl: "model", uk: "модель",
                ru: "модель", es: "modelo", pt: "modelo", de: "Modell" },
  a_intro:    { it: "Chiedi qualcosa al modello locale. Gira sulla GPU della BC-250, nessun cloud.",
                en: "Ask the local model something. It runs on the BC-250 GPU, no cloud.",
                pl: "Zapytaj o coś model lokalny. Działa na GPU BC-250, bez chmury.",
                uk: "Запитайте щось у локальної моделі. Працює на ГП BC-250, без хмари.",
                ru: "Спросите что-нибудь у локальной модели. Она работает на видеоядре BC-250, без облака.", es: "Pregúntale algo al modelo local. Corre en la GPU de la BC-250, sin nube.", pt: "Pergunte algo ao modelo local. Ele roda na GPU da BC-250, sem nuvem.", de: "Frag das örtliche Modell etwas. Es läuft auf der GPU der BC-250, ohne Cloud." }
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
  // e i suggerimenti dei bottoni, che erano scritti in italiano nell'HTML
  (root || document).querySelectorAll("[data-i18n-title]").forEach(function (el) {
    var k = el.getAttribute("data-i18n-title");
    var t = sfT(k);
    if (t !== k) el.title = t;
  });
  // anche i segnaposto dei campi di testo
  (root || document).querySelectorAll("[data-i18n-ph]").forEach(function (el) {
    var k = el.getAttribute("data-i18n-ph");
    var t = sfT(k);
    if (t !== k) el.placeholder = t;
  });
}

document.addEventListener("DOMContentLoaded", function () { sfApply(); });
