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
                ru: "Спросите что-нибудь у локальной модели. Она работает на видеоядре BC-250, без облака.", es: "Pregúntale algo al modelo local. Corre en la GPU de la BC-250, sin nube.", pt: "Pergunte algo ao modelo local. Ele roda na GPU da BC-250, sem nuvem.", de: "Frag das örtliche Modell etwas. Es läuft auf der GPU der BC-250, ohne Cloud." },

  // --- messaggi che erano cablati in italiano dentro le
  // pagine: li vedeva cosi' anche chi usava l'inglese ---
  p_maxstable: { it: "🏁 Massimo stabile: ", en: "🏁 Stable maximum: ", pl: "🏁 Stabilne maksimum: ", uk: "🏁 Стійкий максимум: ", ru: "🏁 Устойчивый максимум: ", es: "🏁 Máximo estable: ", pt: "🏁 Máximo estável: ", de: "🏁 Stabiles Maximum: " },
  p_presetapp: { it: "Preset {x} applicato", en: "Preset {x} applied", pl: "Zastosowano profil {x}", uk: "Профіль {x} застосовано", ru: "Набор {x} применён", es: "Perfil {x} aplicado", pt: "Perfil {x} aplicado", de: "Vorgabe {x} angewendet" },
  p_profsavedn: { it: "Profilo «{x}» salvato", en: "Profile “{x}” saved", pl: "Zapisano profil „{x}”", uk: "Профіль «{x}» збережено", ru: "Набор «{x}» сохранён", es: "Perfil «{x}» guardado", pt: "Perfil “{x}” salvo", de: "Vorgabe „{x}“ gesichert" },
  p_profdelq2: { it: "Eliminare il profilo «{x}»?", en: "Delete the profile “{x}”?", pl: "Usunąć profil „{x}”?", uk: "Вилучити профіль «{x}»?", ru: "Удалить набор «{x}»?", es: "¿Eliminar el perfil «{x}»?", pt: "Excluir o perfil “{x}”?", de: "Die Vorgabe „{x}“ löschen?" },
  p_explore: { it: "Esplora", en: "Explore", pl: "Przeglądaj", uk: "Огляд", ru: "Обзор", es: "Explorar", pt: "Explorar", de: "Stöbern" },
  p_sources: { it: "Sorgenti", en: "Sources", pl: "Źródła", uk: "Джерела", ru: "Источники", es: "Fuentes", pt: "Fontes", de: "Quellen" },
  p_nupdates: { it: "{x} aggiornamenti", en: "{x} updates", pl: "aktualizacji: {x}", uk: "оновлень: {x}", ru: "обновлений: {x}", es: "{x} actualizaciones", pt: "{x} atualizações", de: "{x} Aktualisierungen" },
  p_removeq: { it: "Rimuovere {x}?", en: "Remove {x}?", pl: "Usunąć {x}?", uk: "Вилучити {x}?", ru: "Удалить {x}?", es: "¿Quitar {x}?", pt: "Remover {x}?", de: "{x} entfernen?" },
  p_instappsn: { it: "App installate ({x})", en: "Installed apps ({x})", pl: "Zainstalowane aplikacje ({x})", uk: "Встановлені програми ({x})", ru: "Установленные приложения ({x})", es: "Aplicaciones instaladas ({x})", pt: "Aplicativos instalados ({x})", de: "Eingerichtete Anwendungen ({x})" },
  p_resultsforq: { it: "Risultati per «{x}»", en: "Results for “{x}”", pl: "Wyniki dla „{x}”", uk: "Результати для «{x}»", ru: "Результаты по запросу «{x}»", es: "Resultados de «{x}»", pt: "Resultados para “{x}”", de: "Treffer für „{x}“" },
  p_cuhint: { it: "Le prime 3 colonne (24 CU) sono il minimo del driver e restano bloccate. 1 WGP = 2 CU. Salva la griglia come profilo per richiamarla al volo.", en: "The first 3 columns (24 CUs) are the driver minimum and stay locked. 1 WGP = 2 CUs. Save the grid as a profile to recall it in one click.", pl: "Pierwsze 3 kolumny (24 CU) to minimum sterownika i pozostają zablokowane. 1 WGP = 2 CU. Zapisz siatkę jako profil, żeby przywołać ją jednym kliknięciem.", uk: "Перші 3 стовпці (24 CU) — це мінімум драйвера, вони заблоковані. 1 WGP = 2 CU. Збережіть сітку як профіль, щоб викликати її одним клацом.", ru: "Первые 3 столбца (24 CU) — минимум драйвера, они закреплены. 1 WGP = 2 CU. Сохраните сетку как набор, чтобы вызвать её одним щелчком.", es: "Las 3 primeras columnas (24 CU) son el mínimo del controlador y quedan fijas. 1 WGP = 2 CU. Guarda la rejilla como perfil para recuperarla de un clic.", pt: "As 3 primeiras colunas (24 CU) são o mínimo do driver e ficam travadas. 1 WGP = 2 CU. Salve a grade como perfil para chamá-la com um clique.", de: "Die ersten 3 Spalten (24 CU) sind der Mindestwert des Treibers und bleiben fest. 1 WGP = 2 CU. Sichere das Raster als Vorgabe, um es mit einem Klick zurückzuholen." },
  p_fchint: { it: "Punti temperatura → % ventola. Tra un punto e l'altro la velocità è interpolata. «Off» restituisce la ventola al firmware.", en: "Temperature points → fan %. Between two points the speed is interpolated. “Off” hands the fan back to the firmware.", pl: "Punkty temperatury → % wentylatora. Między punktami prędkość jest interpolowana. „Off” oddaje wentylator firmware'owi.", uk: "Точки температури → % вентилятора. Між точками швидкість інтерполюється. «Off» повертає вентилятор прошивці.", ru: "Точки температуры → % вентилятора. Между точками скорость вычисляется по прямой. «Off» возвращает вентилятор прошивке.", es: "Puntos de temperatura → % del ventilador. Entre dos puntos la velocidad se interpola. «Off» devuelve el ventilador al firmware.", pt: "Pontos de temperatura → % da ventoinha. Entre dois pontos a velocidade é interpolada. “Off” devolve a ventoinha ao firmware.", de: "Temperaturpunkte → Lüfter in %. Zwischen zwei Punkten wird die Drehzahl dazwischengerechnet. „Off“ gibt den Lüfter an die Firmware zurück." },
  p_cpuapp: { it: "CPU applicata", en: "CPU applied", pl: "Zastosowano CPU", uk: "ЦП застосовано", ru: "Процессор применён", es: "CPU aplicada", pt: "CPU aplicada", de: "CPU angewendet" },
  p_savedboot: { it: "Salvato al boot", en: "Saved at boot", pl: "Zapisano przy starcie", uk: "Збережено при завантаженні", ru: "Сохранено при загрузке", es: "Guardado al arranque", pt: "Salvo no boot", de: "Beim Start gesichert" },
  p_gpuapp: { it: "GPU applicata", en: "GPU applied", pl: "Zastosowano GPU", uk: "ГП застосовано", ru: "Видеоядро применено", es: "GPU aplicada", pt: "GPU aplicada", de: "GPU angewendet" },
  p_uvsearch: { it: "▶ Cerco il miglior undervolt a ", en: "▶ Looking for the best undervolt at ", pl: "▶ Szukam najlepszego undervoltu przy ", uk: "▶ Шукаю найкращий undervolt на ", ru: "▶ Ищу лучший undervolt на ", es: "▶ Buscando el mejor undervolt a ", pt: "▶ Procurando o melhor undervolt a ", de: "▶ Suche das beste Undervolting bei " },
  p_uvfound: { it: "✓ Scale suggerito: ", en: "✓ Suggested scale: ", pl: "✓ Proponowana skala: ", uk: "✓ Запропонована шкала: ", ru: "✓ Предложенная шкала: ", es: "✓ Escala sugerida: ", pt: "✓ Escala sugerida: ", de: "✓ Vorgeschlagene Skala: " },
  p_uvsugg: { it: "UV suggerito: ", en: "Suggested UV: ", pl: "Proponowany UV: ", uk: "Запропонований UV: ", ru: "Предложенный UV: ", es: "UV sugerido: ", pt: "UV sugerido: ", de: "Vorgeschlagenes UV: " },
  p_wizcpu: { it: "Il wizard prova frequenze crescenti (può richiedere alcuni minuti e stressa la CPU). Procedere?", en: "The wizard steps through rising frequencies (it can take a few minutes and stresses the CPU). Proceed?", pl: "Kreator próbuje coraz wyższych częstotliwości (może potrwać kilka minut i obciąża procesor). Kontynuować?", uk: "Майстер пробує щораз вищі частоти (може зайняти кілька хвилин і навантажує ЦП). Продовжити?", ru: "Мастер пробует всё более высокие частоты (может занять несколько минут и нагружает процессор). Продолжить?", es: "El asistente prueba frecuencias cada vez más altas (puede tardar unos minutos y esfuerza la CPU). ¿Seguimos?", pt: "O assistente testa frequências cada vez mais altas (pode levar alguns minutos e força a CPU). Seguimos?", de: "Der Assistent probiert immer höhere Takte (das kann ein paar Minuten dauern und belastet die CPU). Weiter?" },
  p_wizgpu: { it: "Il wizard prova frequenze GPU crescenti (può richiedere alcuni minuti). Procedere?", en: "The wizard steps through rising GPU frequencies (it can take a few minutes). Proceed?", pl: "Kreator próbuje coraz wyższych częstotliwości GPU (może potrwać kilka minut). Kontynuować?", uk: "Майстер пробує щораз вищі частоти ГП (може зайняти кілька хвилин). Продовжити?", ru: "Мастер пробует всё более высокие частоты видеоядра (может занять несколько минут). Продолжить?", es: "El asistente prueba frecuencias de GPU cada vez más altas (puede tardar unos minutos). ¿Seguimos?", pt: "O assistente testa frequências de GPU cada vez mais altas (pode levar alguns minutos). Seguimos?", de: "Der Assistent probiert immer höhere GPU-Takte (das kann ein paar Minuten dauern). Weiter?" },
  p_appsaved: { it: " (applicato e salvato)", en: " (applied and saved)", pl: " (zastosowano i zapisano)", uk: " (застосовано і збережено)", ru: " (применено и сохранено)", es: " (aplicado y guardado)", pt: " (aplicado e salvo)", de: " (angewendet und gesichert)" },
  p_applied: { it: " (applicato)", en: " (applied)", pl: " (zastosowano)", uk: " (застосовано)", ru: " (применено)", es: " (aplicado)", pt: " (aplicado)", de: " (angewendet)" },
  p_govbal: { it: "Governor: bilanciato", en: "Governor: balanced", pl: "Regulator: zrównoważony", uk: "Регулятор: збалансований", ru: "Регулятор: уравновешенный", es: "Gobernador: equilibrado", pt: "Governador: equilibrado", de: "Governor: ausgewogen" },
  p_govperf: { it: "Governor: prestazioni", en: "Governor: performance", pl: "Regulator: wydajność", uk: "Регулятор: продуктивність", ru: "Регулятор: производительность", es: "Gobernador: rendimiento", pt: "Governador: desempenho", de: "Governor: Leistung" },
  p_coresapp: { it: "Core applicati — ", en: "Cores applied — ", pl: "Zastosowano rdzenie — ", uk: "Ядра застосовано — ", ru: "Ядра применены — ", es: "Núcleos aplicados — ", pt: "Núcleos aplicados — ", de: "Kerne angewendet — " },
  p_cuapp: { it: "CU applicate: ", en: "CUs applied: ", pl: "Zastosowano CU: ", uk: "CU застосовано: ", ru: "CU применены: ", es: "CU aplicadas: ", pt: "CU aplicadas: ", de: "CU angewendet: " },
  p_cutest: { it: "Test CU in corso (può richiedere 1-2 min)…", en: "CU test running (may take 1-2 min)…", pl: "Trwa test CU (może potrwać 1-2 min)…", uk: "Триває перевірка CU (може зайняти 1-2 хв)…", ru: "Идёт проверка CU (может занять 1-2 мин)…", es: "Prueba de CU en marcha (puede tardar 1-2 min)…", pt: "Teste de CU em andamento (pode levar 1-2 min)…", de: "CU-Prüfung läuft (kann 1-2 Min. dauern)…" },
  p_cudone: { it: "Test CU completato", en: "CU test finished", pl: "Test CU zakończony", uk: "Перевірку CU завершено", ru: "Проверка CU завершена", es: "Prueba de CU terminada", pt: "Teste de CU concluído", de: "CU-Prüfung abgeschlossen" },
  p_fanapply: { it: "Applico ventola…", en: "Applying the fan setting…", pl: "Stosowanie ustawień wentylatora…", uk: "Застосування налаштувань вентилятора…", ru: "Применяю настройку вентилятора…", es: "Aplicando el ajuste del ventilador…", pt: "Aplicando o ajuste da ventoinha…", de: "Lüftereinstellung wird angewendet…" },
  p_fanis: { it: "Ventola: ", en: "Fan: ", pl: "Wentylator: ", uk: "Вентилятор: ", ru: "Вентилятор: ", es: "Ventilador: ", pt: "Ventoinha: ", de: "Lüfter: " },
  p_fanerr: { it: "Errore ventola", en: "Fan error", pl: "Błąd wentylatora", uk: "Помилка вентилятора", ru: "Ошибка вентилятора", es: "Error del ventilador", pt: "Erro da ventoinha", de: "Lüfterfehler" },
  p_vramset: { it: "VRAM impostata — riavvia per applicare", en: "VRAM set — reboot to apply", pl: "Ustawiono VRAM — uruchom ponownie, aby zadziałało", uk: "VRAM встановлено — перезавантажте, щоб подіяло", ru: "Видеопамять задана — перезагрузите, чтобы применить", es: "VRAM fijada — reinicia para aplicarlo", pt: "VRAM definida — reinicie para valer", de: "Grafikspeicher gesetzt — zum Anwenden neu starten" },
  p_cuprofname: { it: "Nome del profilo CU:", en: "CU profile name:", pl: "Nazwa profilu CU:", uk: "Назва профілю CU:", ru: "Название набора CU:", es: "Nombre del perfil de CU:", pt: "Nome do perfil de CU:", de: "Name der CU-Vorgabe:" },
  p_profsaved: { it: "Profilo salvato", en: "Profile saved", pl: "Zapisano profil", uk: "Профіль збережено", ru: "Набор сохранён", es: "Perfil guardado", pt: "Perfil salvo", de: "Vorgabe gesichert" },
  p_profapp: { it: "Profilo applicato: ", en: "Profile applied: ", pl: "Zastosowano profil: ", uk: "Профіль застосовано: ", ru: "Набор применён: ", es: "Perfil aplicado: ", pt: "Perfil aplicado: ", de: "Vorgabe angewendet: " },
  p_profdelq: { it: "Eliminare il profilo", en: "Delete the profile", pl: "Usunąć profil", uk: "Вилучити профіль", ru: "Удалить набор", es: "¿Eliminar el perfil", pt: "Excluir o perfil", de: "Die Vorgabe löschen" },
  p_profdel: { it: "Profilo eliminato", en: "Profile deleted", pl: "Usunięto profil", uk: "Профіль вилучено", ru: "Набор удалён", es: "Perfil eliminado", pt: "Perfil excluído", de: "Vorgabe gelöscht" },
  p_navail: { it: "non disponibile", en: "not available", pl: "niedostępne", uk: "недоступно", ru: "недоступно", es: "no disponible", pt: "indisponível", de: "nicht verfügbar" },
  p_fcsaved: { it: "Curva ventola salvata", en: "Fan curve saved", pl: "Zapisano krzywą wentylatora", uk: "Криву вентилятора збережено", ru: "Кривая вентилятора сохранена", es: "Curva del ventilador guardada", pt: "Curva da ventoinha salva", de: "Lüfterkurve gesichert" },
  p_andon: { it: " e attiva", en: " and active", pl: " i aktywna", uk: " і діє", ru: " и включена", es: " y activa", pt: " e ativa", de: " und aktiv" },
  p_installed1: { it: "installata", en: "installed", pl: "zainstalowana", uk: "встановлено", ru: "установлено", es: "instalada", pt: "instalado", de: "eingerichtet" },
  p_installedn: { it: "Installate", en: "Installed", pl: "Zainstalowane", uk: "Встановлені", ru: "Установленные", es: "Instaladas", pt: "Instalados", de: "Eingerichtet" },
  p_updates: { it: "Aggiornamenti", en: "Updates", pl: "Aktualizacje", uk: "Оновлення", ru: "Обновления", es: "Actualizaciones", pt: "Atualizações", de: "Aktualisierungen" },
  p_building: { it: "Sto costruendo il catalogo… (qualche secondo)", en: "Building the catalogue… (a few seconds)", pl: "Buduję katalog… (kilka sekund)", uk: "Будую каталог… (кілька секунд)", ru: "Строю каталог… (несколько секунд)", es: "Construyendo el catálogo… (unos segundos)", pt: "Construindo o catálogo… (alguns segundos)", de: "Der Katalog wird aufgebaut… (ein paar Sekunden)" },
  p_rebuilding: { it: "Ricostruisco il catalogo…", en: "Rebuilding the catalogue…", pl: "Przebudowuję katalog…", uk: "Перебудовую каталог…", ru: "Перестраиваю каталог…", es: "Reconstruyendo el catálogo…", pt: "Reconstruindo o catálogo…", de: "Der Katalog wird neu aufgebaut…" },
  p_popular: { it: "Più popolari", en: "Most popular", pl: "Najpopularniejsze", uk: "Найпопулярніші", ru: "Самые популярные", es: "Lo más popular", pt: "Mais populares", de: "Am beliebtesten" },
  p_checkupd: { it: "Controllo aggiornamenti…", en: "Checking for updates…", pl: "Sprawdzanie aktualizacji…", uk: "Перевірка оновлень…", ru: "Проверка обновлений…", es: "Buscando actualizaciones…", pt: "Procurando atualizações…", de: "Suche nach Aktualisierungen…" },
  p_alluptodate: { it: "Tutto aggiornato ✓", en: "Everything is up to date ✓", pl: "Wszystko aktualne ✓", uk: "Усе свіже ✓", ru: "Всё свежее ✓", es: "Todo está al día ✓", pt: "Está tudo em dia ✓", de: "Alles ist aktuell ✓" },
  p_alluptodate2: { it: "Tutto aggiornato.", en: "Everything is up to date.", pl: "Wszystko aktualne.", uk: "Усе свіже.", ru: "Всё свежее.", es: "Todo está al día.", pt: "Está tudo em dia.", de: "Alles ist aktuell." },
  p_updall: { it: "Aggiornamento di tutti i pacchetti", en: "Updating every package", pl: "Aktualizowanie wszystkich pakietów", uk: "Оновлення всіх пакунків", ru: "Обновление всех пакетов", es: "Actualizando todos los paquetes", pt: "Atualizando todos os pacotes", de: "Alle Pakete werden aktualisiert" },
  p_loadsrc: { it: "Carico le sorgenti…", en: "Loading the sources…", pl: "Wczytywanie źródeł…", uk: "Завантаження джерел…", ru: "Загрузка источников…", es: "Cargando las fuentes…", pt: "Carregando as fontes…", de: "Die Quellen werden geladen…" },
  p_refreshsrc: { it: "Aggiorno l'elenco dopo modifica sorgenti", en: "Refreshing the list after the source change", pl: "Odświeżanie listy po zmianie źródeł", uk: "Оновлення переліку після зміни джерел", ru: "Обновляю перечень после смены источников", es: "Actualizando la lista tras cambiar las fuentes", pt: "Atualizando a lista depois de mudar as fontes", de: "Die Liste wird nach der Quellenänderung aufgefrischt" },
  p_website: { it: "sito web ↗", en: "website ↗", pl: "strona ↗", uk: "сайт ↗", ru: "сайт ↗", es: "sitio web ↗", pt: "site ↗", de: "Netzseite ↗" },
  p_desc: { it: "Descrizione", en: "Description", pl: "Opis", uk: "Опис", ru: "Описание", es: "Descripción", pt: "Descrição", de: "Beschreibung" },
  p_whatsnew: { it: "Novità", en: "What's new", pl: "Nowości", uk: "Новини", ru: "Что нового", es: "Novedades", pt: "Novidades", de: "Was ist neu" },
  p_remove: { it: "Rimuovere", en: "Remove", pl: "Usunąć", uk: "Вилучити", ru: "Удалить", es: "Quitar", pt: "Remover", de: "Entfernen" },
  p_instapps: { it: "App installate", en: "Installed apps", pl: "Zainstalowane aplikacje", uk: "Встановлені програми", ru: "Установленные приложения", es: "Aplicaciones instaladas", pt: "Aplicativos instalados", de: "Eingerichtete Anwendungen" },
  p_resultsfor: { it: "Risultati per", en: "Results for", pl: "Wyniki dla", uk: "Результати для", ru: "Результаты по запросу", es: "Resultados de", pt: "Resultados para", de: "Treffer für" },
  p_noresults: { it: "Nessun risultato.", en: "No results.", pl: "Brak wyników.", uk: "Немає результатів.", ru: "Ничего не найдено.", es: "Sin resultados.", pt: "Sem resultados.", de: "Keine Treffer." },
  p_ours: { it: "le nostre", en: "ours", pl: "nasze", uk: "наші", ru: "наши", es: "nuestras", pt: "nossos", de: "unsere" },
  p_searchph: { it: "Cerca app e pacchetti…", en: "Search apps and packages…", pl: "Szukaj aplikacji i pakietów…", uk: "Пошук програм і пакунків…", ru: "Поиск программ и пакетов…", es: "Buscar aplicaciones y paquetes…", pt: "Buscar aplicativos e pacotes…", de: "Anwendungen und Pakete suchen…" },
  p_nomodel: { it: "Nessun modello installato. Scaricane uno dal modulo AI.", en: "No model installed. Download one from the AI module.", pl: "Brak zainstalowanego modelu. Pobierz jakiś z modułu SI.", uk: "Жодної моделі не встановлено. Завантажте якусь із модуля ШІ.", ru: "Ни одной модели не установлено. Скачайте её из модуля ИИ.", es: "No hay ningún modelo instalado. Descarga uno desde el módulo de IA.", pt: "Nenhum modelo instalado. Baixe um pelo módulo de IA.", de: "Kein Modell eingerichtet. Hol dir eines über das KI-Modul." },
};

// --- il dizionario condiviso con le app native -------------------------------
// /usr/share/skillfish/i18n/<lingua>.json, servito dal server su /api/i18n.
//
// PERCHE' NON UN ALTRO DIZIONARIO QUI DENTRO
// I nomi delle categorie dell'Hub erano scritti in italiano dentro hub.html.
// Tradurli qui avrebbe fatto il TERZO dizionario del progetto — quello delle
// app, quello di queste pagine, e un altro — con gli stessi nomi ricopiati in
// tre posti, che prima o poi divergono. Quei nomi ci sono gia' tradotti nel
// dizionario delle app: si legge quello.
//
// Le chiavi sono le stringhe INGLESI, non le chiavi corte di SFSTR: per questo
// sfC() e' una funzione a parte e non un ripiego dentro sfT().
var SFVOCI = null;

function sfCarica() {
  if (SFVOCI) return Promise.resolve(SFVOCI);
  return fetch("/api/i18n?lang=" + encodeURIComponent(SFLANG))
    .then(function (r) { return r.ok ? r.json() : { voci: {} }; })
    .then(function (j) { SFVOCI = (j && j.voci) || {}; return SFVOCI; })
    // Se il server non risponde si va avanti in inglese. Una traduzione che
    // manca e' un fastidio, una pagina che non si disegna e' un guasto.
    .catch(function () { SFVOCI = {}; return SFVOCI; });
}

function sfC(en) {
  return (SFVOCI && SFVOCI[en]) || en;
}

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
