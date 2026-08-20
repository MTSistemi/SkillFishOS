// Spanish UI strings. Any key missing here falls back to English (see t() in i18n.ts),
// so this file can grow without ever leaving a blank on the page.
// Inline HTML and &nbsp; entities are part of the copy — keep them.
//
// Spain became the largest non-English source of downloads in three days, after
// a Spanish video ("Nunca había visto un sistema para PC como este") — the same
// thing the Polish review did in June. Over the last thirty days on SourceForge,
// scraper day excluded, Spain is 14.5% and rising, Mexico shows up too.
//
// ⚠️ NOT reviewed by a native speaker. Written by the SkillFishOS team, like the
// Russian and Ukrainian ones; the Polish is Cyryl Sochacki's. Corrections are
// welcome and cost one file: this one.
export const es: Record<string, string> = {
  title: "SkillFishOS — Linux para jugar en la AMD BC-250",
  "meta.desc":
    "SkillFishOS: el sistema operativo steampunk para jugar en la placa AMD BC-250. Ajustado y listo, sin tocar nada. Emulación, Steam, IA en el propio equipo. Basado en Debian + KDE Plasma.",

  "nav.feat": "Funciones",
  "nav.shots": "Capturas",
  "nav.hw": "Hardware",
  "nav.download": "Descargar",
  "nav.docs": "Documentación",
  "nav.gallery": "Galería",
  "nav.contact": "Contacto",
  "nav.donate": "Apóyanos",
  "nav.news": "Novedades",
  "nav.road": "Hoja de ruta",

  "hero.soon": "Versión 26.06 «Aetherium»",
  "hero.tag": "El sistema operativo para jugar, forjado para la <b>AMD BC-250</b>.",
  "hero.sub":
    "Linux steampunk, listo para jugar desde el primer arranque. Todo ajustado de fábrica, sin tocar nada. Emulación, Steam e IA en el propio equipo. Basado en Debian y KDE&nbsp;Plasma.",
  "hero.btn1": "Verlo en acción",
  "hero.btn2": "Qué lleva dentro",
  "hero.pill": "APU AMD · Zen&nbsp;2 + RDNA&nbsp;2 · 16&nbsp;GB GDDR6",

  "intro.eye": "Qué es",
  "intro.h2": "Un PC-consola,<br>listo para usar.",
  "intro.p1":
    "SkillFishOS convierte la placa <strong>AMD BC-250</strong> — una APU semipersonalizada de la <strong>familia AMD Zen&nbsp;2 + RDNA&nbsp;2</strong> (CPU «Oberon», gráfica «Cyan&nbsp;Skillfish», 16&nbsp;GB GDDR6) — en un sistema completo para jugar y trabajar.",
  "intro.p2":
    "Gobernadores, parches del núcleo, overclock y perfiles térmicos vienen <strong>ya ajustados</strong>: un sistema que rinde al máximo <strong>sin tocar nada</strong>. Una estética <strong>steampunk</strong> coherente desde el arranque hasta el escritorio, pensada también para que <strong>los niños aprendan Linux</strong> mientras juegan.",

  "feat.eye": "Funciones",
  "feat.h2": "Todo listo, nada más encender.",
  "feat.sub": "No hay nada que configurar a mano: el sistema ya está ajustado para la BC-250.",

  "f1.t": "Listo para jugar",
  "f1.d":
    "Steam, EmuDeck, ES-DE, Heroic y Proton listos. EmuDeck instala y configura los emuladores en unos clics: los juegos y las ROMs los pones tú.",
  "f2.t": "Núcleo a medida",
  "f2.d":
    "Un núcleo tkg ajustado para la BC-250: <b>40 unidades de cómputo</b> desbloqueadas, overclock de CPU y GPU y un gobernador SMU propio para exprimir cada TFLOPS.",
  "f3.t": "Listo, sin tocar nada",
  "f3.d":
    "Gobernadores, parches, overclock y una protección térmica <b>ya configurados y probados</b>. Enciendes y va a pleno rendimiento: sin terminal y sin ajustes manuales.",
  "f4.t": "Estética steampunk",
  "f4.d":
    "Un escritorio KDE&nbsp;Plasma oscuro de estilo steampunk: iconos, cursores, fondo y un HUD del sistema con aire mecánico-victoriano.",
  "f5.t": "Instantáneas Btrfs",
  "f5.d":
    "Experimenta sin miedo: cada cambio queda protegido por instantáneas automáticas. ¿Algo se ha roto? <b>Vuelves atrás con un clic</b> desde el menú de arranque.",
  "f6.t": "IA en el propio equipo",
  "f6.d":
    "<b>Unsloth Studio</b> acelerado con <b>Vulkan</b> en la GPU integrada: <b>5,1×</b> más rápido que en CPU, medido. Modelos de chat y de programación funcionando en casa, sin nube.",
  "f7.t": "Control remoto",
  "f7.d":
    "<b>Remote Manager</b>: un panel web para manejar la placa desde el navegador o el móvil — telemetría, KVM, terminal, Tuner, tienda de aplicaciones e IA. Acceso con las credenciales del sistema por HTTPS, y desde cualquier sitio con ZeroTier.",

  "show.eye": "Capturas",
  "show.h2": "Bonito de ver, fácil de usar.",
  "s1.t": "El escritorio steampunk",
  "s1.d":
    "KDE Plasma con estética steampunk: fondo temático, detalles dorados y un HUD en vivo con CPU, GPU, temperaturas, ventilador y batería del mando Bluetooth, siempre a la vista.",
  "s2.t": "Emulación fácil con EmuDeck",
  "s2.d":
    "EmuDeck instala y configura los emuladores (RetroArch, Dolphin, PCSX2, PPSSPP, RPCS3 y más) y la interfaz ES-DE en unos clics. El sistema pone las herramientas: los juegos y las ROMs los pones tú.",
  "s4.t": "IA en el equipo, a un clic",
  "s4.d":
    "Un panel dedicado enciende y apaga el motor de IA local (Qwen en la GPU con Vulkan). Chat web, terminal para programar y gestión: la IA funciona en casa y libera la GPU cuando toca jugar.",
  "s5.t": "Ajuste en un clic",
  "s5.d":
    "El Tuner ajusta frecuencias, undervolt, ventilador y unidades de cómputo con cuatro perfiles listos (Stock, Performance, Turbo, Crazy) y una protección térmica que cuida el hardware. Toda la potencia, con seguridad y sin línea de comandos.",

  "hw.eye": "Hardware",
  "hw.h2": "Nacido para la AMD BC-250.",
  "hw.sub": "Toda la potencia de la familia AMD Zen 2 + RDNA 2, liberada en Linux.",
  "hw.c1": "CPU «Oberon» · hasta 4,0 GHz",
  "hw.c2": "GPU «Cyan Skillfish» · 40 CU",
  "hw.c3": "FP32 · aceleración Vulkan",
  "hw.c4": "GDDR6 compartida",

  "cta.h2": "Enciende. <span class=\"gold-text\">Juega.</span> Aprende.",
  "cta.p":
    "Un sistema operativo de código abierto que convierte una placa desnuda en un verdadero PC-consola. Disponible en dos ediciones: AMD BC-250 y Generic (cualquier PC o máquina virtual x86-64).",
  "cta.btn": "Descargar SkillFishOS",
  "foot.based": "Código abierto · Basado en Debian · KDE Plasma · © 2026 SkillFishOS",

  "dl.title": "Descargar — SkillFishOS",
  "dl.eye": "Descargar",
  "dl.h2": "Descargar SkillFish<span class=\"gold-text\">OS</span>",
  "dl.sub":
    "Las ISO instalables, con la marca y listas para usar — para la AMD BC-250 y para cualquier PC x86-64.",
  "dl.badge": "26.06.4 «Aetherium»",
  "dl.notice":
    "La versión <strong>26.06.4 «Aetherium»</strong> de SkillFishOS llega en <strong>dos ediciones</strong>: <strong>BC-250</strong> (la placa de AMD) y <strong>Generic</strong> (cualquier PC o máquina virtual x86-64). Completa y lista para usar. Proyecto de <strong>código abierto</strong>.",
  "dl.btnsoon": "ISO disponible en breve",
  "dl.btn": "Descargar la ISO",
  "dl.ed.bc250": "BC-250",
  "dl.ed.generic": "Generic (PC/VM)",
  "dl.ed.slim": "Slim (BC-250)",
  "dl.ed.all": "Todos los archivos en SourceForge →",
  "dl.size": "amd64 · ~{size} GB · btrfs + KDE Plasma · 2 ediciones en SourceForge",
  "dl.ver":
    "Versión <strong>26.06.4 «Aetherium»</strong> · <strong>2 ediciones</strong> (BC-250 · Generic) · arranca en inglés, el idioma se elige al instalar",
  "dl.fast.h": "La vía más rápida, desde Europa",
  "dl.fast.sub":
    "Internet Archive guarda nuestras ISO y las sirve desde sus propios servidores. Medido desde una línea italiana: <strong>unos 5 MB/s</strong> frente a 0,4 desde SourceForge, que lo sirve todo desde San Diego. Mismo archivo, misma suma de verificación.",
  "dl.fast.bc250": "BC-250",
  "dl.fast.generic": "Generic (PC/VM)",
  "dl.sf.h": "O desde SourceForge",
  "dl.sf.sub":
    "El servidor espejo de siempre del proyecto: más lento desde Europa, pero de ahí salen nuestros contadores de descargas.",
  "dl.tor.h": "O por torrent",
  "dl.tor.sub":
    "Más rápido cuando descargan varias personas a la vez, y continúa donde lo dejaste. Funciona incluso sin nadie más conectado: el torrent puede tirar directamente de nuestros espejos.",
  "dl.tor.bc250": "⇅ BC-250 · torrent",
  "dl.tor.generic": "⇅ Generic · torrent",
  "dl.tor.magnet": "magnet",
  "dl.bugs.h": "¿Has encontrado un problema?",
  "dl.bugs.d":
    "SkillFishOS mejora continuamente. Para informar de fallos o problemas, abre una <em>issue</em> en GitHub. (Pronto añadiremos una dirección de correo.)",
  "dl.bugs.btn": "Informar en GitHub",
  "dl.req.h": "Requisitos",
  "dl.req.d":
    "Una placa <strong>AMD BC-250</strong> (APU Zen&nbsp;2 + RDNA&nbsp;2, 16&nbsp;GB GDDR6), un SSD o NVMe, un monitor con <strong>DisplayPort</strong> y una memoria USB de 8&nbsp;GB o más para el instalador.",
  "dl.inc.h": "Qué incluye",
  "dl.inc.d":
    "Un núcleo optimizado (40&nbsp;CU, gobernador, OC), la estética steampunk completa, Steam + EmuDeck + ES-DE, IA local, instantáneas Btrfs y las herramientas Tuner y AI listas para usar.",
  "dl.steps.h": "Instalación",
  "dl.step1": "Graba la ISO en una memoria USB (Etcher, Ventoy o <code>dd</code>).",
  "dl.step2": "Arranca la BC-250 desde el USB y sigue el instalador gráfico (Calamares).",
  "dl.step3": "En el primer arranque está todo configurado: enciende y juega.",
  "dl.repo.h": "Actualizaciones",
  "dl.repo.d":
    "SkillFishOS se actualiza desde su <strong>repositorio oficial</strong>: núcleo, aplicaciones y temas vienen de nosotros y están probados, así las actualizaciones de Debian sid no pueden romper el sistema.",

  "news.title": "Novedades",
  "news.eye": "Al día",
  "news.h1": "Qué ha cambiado,<br>y cuándo",
  "news.sub":
    "A un proyecto pequeño también se le juzga por la frecuencia con la que cuenta algo. Aquí están las novedades por fecha y el camino que viene, con el estado de cada punto — incluidos los que aún no están listos.",
  "news.h.news": "Novedades",
  "news.h.road": "Hoja de ruta",
  "news.road.sub":
    "En qué estamos trabajando, qué viene después y qué ya ha llegado. No prometemos fechas mientras no las tengamos de verdad.",
  "news.foot":
    "¿Tienes una idea o echas algo en falta? Las peticiones son bienvenidas: escríbenos desde la página de <a href=\"/es/contact\">contacto</a> o abre una discusión en GitHub. Construir lo que alguien necesita de verdad es mejor que acertar por casualidad.",
  "news.diroad": "¿Quieres saber qué viene después? Está en la <a href=\"/es/roadmap\">hoja de ruta</a>.",

  "road.title": "Hoja de ruta",
  "road.eye": "Hacia dónde vamos",
  "road.h1": "Qué está por llegar,<br>y qué ya está aquí",
  "road.sub":
    "No prometemos fechas mientras no las tengamos de verdad. Los puntos terminados se quedan abajo, porque responden a la pregunta que más nos hacen: si el proyecto sigue vivo.",
  "road.dinews": "¿Buscas qué ha cambiado? Eso está en las <a href=\"/es/news\">novedades</a>.",

  "gal.title": "Galería — SkillFishOS",
  "gal.eye": "Galería",
  "gal.h2": "Bonito de ver, fácil de usar.",
  "gal.sub": "SkillFishOS en acción: escritorio, juegos, emulación y herramientas.",
  "gal.desktop.t": "El escritorio steampunk",
  "gal.desktop.d": "KDE Plasma con la estética del sistema y un HUD en vivo arriba a la derecha.",
  "gal.about.t": "Información del sistema",
  "gal.about.d": "Marca completa: nombre, logotipo y hardware reconocidos como SkillFishOS.",
  "gal.emudeck.t": "EmuDeck",
  "gal.emudeck.d": "Instalación y configuración de los emuladores en unos clics.",
  "gal.esde1.t": "ES-DE — interfaz",
  "gal.esde1.d": "La interfaz ES-DE para explorar y lanzar tus bibliotecas.",
  "gal.ai.t": "Panel de IA",
  "gal.ai.d": "Enciende y apaga la IA local (Vulkan) con un solo clic.",
  "gal.tuner.t": "Tuner — unidades de cómputo en vivo",
  "gal.tuner.d":
    "Rejilla de CU (verde = activa, rojo = apagada), perfiles 24/32/40 y prueba, sin reiniciar.",
  "gal.tunerctl.t": "Tuner — perfiles, gobernador y asistentes",
  "gal.tunerctl.d":
    "Perfiles Stock/Performance/Turbo/Crazy, el panel «Mi silicio», el modo de gobernador Balanced/Performance y los asistentes «Encuentra mi máximo» para CPU y GPU.",
  "gal.monitor.t": "Telemetría en vivo durante las pruebas",
  "gal.monitor.d": "Gráficas de temperatura, frecuencia, voltaje y ventilador en tiempo real.",
  "gal.cutest.t": "Prueba de CU — lotería del silicio",
  "gal.cutest.d":
    "Comprueba que las 40 CU aguantan la carga sin defectos (útil en chips de segunda mano).",
  "gal.wukong.t": "Black Myth: Wukong — 112 FPS",
  "gal.wukong.d": "Media a 1080p en la BC-250 (máximo 128, 1% low 101).",
  "gal.super.t": "Unigine Superposition — 12.938",
  "gal.super.d": "1080p High: rendimiento de una Radeon RX 6600 en una placa de unos 50 €.",
  "gal.heaven.t": "Unigine Heaven — 113,7 FPS",
  "gal.heaven.d": "2865 puntos a 1080p Ultra, 8× AA, teselado Extreme.",
  "gal.boot.t": "Arranque steampunk",
  "gal.boot.d": "Una presentación de latón coherente desde GRUB hasta el escritorio.",
  "gal.b1.t": "Mismo hardware, +34% — frente a Bazzite",
  "gal.b1.d":
    "Superposition 1080p Extreme: la misma BC-250 saca 4102 a frecuencias de fábrica en otra distribución; con SkillFishOS llega a 5513. Tabla oficial de Unigine.",
  "gal.b2.t": "A la altura de una Radeon RX 6600",
  "gal.b2.d":
    "Superposition 1080p High: la BC-250 con SkillFishOS (12.938) iguala a una RX 6600/6600 XT de más de 200 € (12.454). Tabla oficial de Unigine.",

  "hwp.title": "Hardware AMD BC-250 — SkillFishOS",
  "hwp.eye": "Hardware",
  "hwp.h2": "Nacido para la <span class=\"gold-text\">AMD BC-250</span>.",
  "hwp.sub": "Una APU semipersonalizada AMD Zen 2 + RDNA 2 con 16 GB de GDDR6, liberada en Linux.",
  "hwp.specs.h": "Especificaciones",
  "hwp.cpu.t": "CPU — 8× Zen 2",
  "hwp.cpu.d":
    "«Oberon», <strong>8 núcleos / 16 hilos</strong> (la placa muestra 6, SkillFishOS desbloquea los otros dos por el SMU: <strong>+20%</strong> medido), hasta <strong>4,0 GHz en todos los núcleos</strong> con overclock.",
  "hwp.gpu.t": "GPU — RDNA 2",
  "hwp.gpu.d": "«Cyan Skillfish» (gfx1013), hasta 40 unidades de cómputo desbloqueables.",
  "hwp.mem.t": "Memoria — 16 GB GDDR6",
  "hwp.mem.d":
    "Compartida (UMA) entre CPU y GPU; en Linux el GTT amplía la memoria de vídeo.",
  "hwp.perf.t": "Cómputo — ~11 TFLOPS",
  "hwp.perf.d": "FP32 con 40 CU / 2000 MHz (vkpeak), con aceleración Vulkan.",
  "hwp.quirks.h": "Defectos del hardware (y cómo los resolvemos)",
  "hwp.q1.t": "HPD del DisplayPort averiado",
  "hwp.q1.d":
    "La detección del monitor no funciona → servicio dedicado + parámetro del núcleo <code>video=DP-1:e</code>.",
  "hwp.q2.t": "Suspensión rota",
  "hwp.q2.d": "La placa no despierta → todos los estados de reposo desactivados de forma permanente.",
  "hwp.q3.t": "IOMMU inestable",
  "hwp.q3.d": "No debe activarse nunca → el sistema arranca siempre sin IOMMU.",
  "hwp.q4.t": "Refrigeración justa",
  "hwp.q4.d":
    "Solo sensor de borde, sin sensor de VRAM → una protección térmica a 85 °C siempre activa.",
  "hwp.cta": "Más detalles en la documentación →",

  "bm.h": "Rendimiento medido",
  "bm.sub":
    "Medidas de vkpeak FP32-scalar (GFLOPS) en la <strong>misma</strong> BC-250, antes y después de SkillFishOS.",
  "bm.bar1": "Base — XanMod, 24 CU",
  "bm.bar2": "tkg + gobernador, 24 CU",
  "bm.bar3": "SkillFishOS — tkg + gobernador + 40 CU",
  "bm.unit": "GFLOPS",
  "bm.note":
    "Medidas con <strong>vkpeak</strong> (cómputo Vulkan) en la misma placa, en frío y en reposo. Con las 40 CU activas la GPU rinde <strong>1,84×</strong> más que el sistema de partida. En reposo el gobernador baja a 350 MHz; borde ~54 °C tras la carga de cómputo.",
  "bm.s1.l": "FP32 frente a la base",
  "bm.s2.l": "GFLOPS FP32 (≈11,3 TFLOPS)",
  "bm.s3.l": "GFLOPS FP16 (vec4)",
  "bm.s4.l": "GIOPS int8 (producto escalar)",
  "bm.src": "Fuente: medidas del proyecto sobre hardware real (vkpeak). Detalles en",
  "bm.gpulink": "GPU, gobernador y overclock",

  "wk.h": "Carga real — Black Myth: Wukong (1080p)",
  "wk.note":
    "Unos 4 minutos de telemetría dentro del juego: <strong>CPU y GPU mantienen todo el overclock</strong> dentro del límite térmico de 85 °C — gobernador, OC y protección térmica aguantan un AAA exigente. (Wukong depende de la <em>CPU y de las llamadas de dibujo</em>: aquí importa la estabilidad bajo carga, no la resolución.)",
  "wk.l.gpu": "GPU (punto seguro)",
  "wk.l.gpuc": "Borde de la GPU (máx. 81)",
  "wk.l.pwr": "Consumo (pico 182 W)",
  "wk.l.cpu": "CPU (overclock)",
  "wk.l.vram": "VRAM en uso",
  "wk.l.fan": "Ventilador",

  "bs.h": "Capturas reales — tomadas en nuestro propio hardware",
  "bs.sub":
    "Ni renders ni maquetas: capturas de pantalla reales tomadas durante las pruebas, en <strong>nuestra propia</strong> BC-250 con SkillFishOS. Toca una imagen para ampliarla.",
  "bs.wk.c":
    "Black Myth: Wukong — <strong>112 FPS</strong> de media a 1080p (máximo 128, 1% low 101). APU AMD BC-250, GPU RADV gfx1013.",
  "bs.hv.c":
    "Unigine Heaven 4.0 — <strong>113,7 FPS</strong>, puntuación <strong>2865</strong> (1080p Ultra, 8× AA, teselado Extreme). Núcleo 7.0.10-skillfishos.",
  "bs.sc.c":
    "Unigine Heaven — la escena renderizada en tiempo real en la BC-250 durante la prueba.",

  "gb.h": "Pruebas con juegos — resultados reales",
  "gb.sub":
    "Medido en la BC-250 con SkillFishOS, a 1080p. Una placa de <strong>unos 50 €</strong> jugando al nivel de una <strong>Radeon RX&nbsp;6600</strong>.",
  "gb.wk.v": "112 FPS",
  "gb.wk.l": "Black Myth: Wukong · media a 1080p",
  "gb.hv.v": "2865",
  "gb.hv.l": "Unigine Heaven · 1080p Ultra/Extreme · 8× AA · 113 FPS",
  "gb.sp.v": "12.938",
  "gb.sp.l": "Unigine Superposition · 1080p High · (5513 en Extreme)",

  "cmp.os.h": "Mismo hardware, +34% solo por cambiar de sistema",
  "cmp.os.sub":
    "Superposition 1080p Extreme, en la <strong>misma BC-250</strong>: SkillFishOS frente a otra distribución a frecuencias de fábrica.",
  "cmp.os.b1": "SkillFishOS — GPU 2230 · CPU 3900",
  "cmp.os.b2": "Otra distribución (Bazzite) — GPU 2100 · CPU 3436",
  "cmp.os.note":
    "40 CU desbloqueadas, un gobernador que lleva la GPU a 2230 MHz y overclock con undervolt en la CPU: <strong>+34% de rendimiento real</strong> del mismísimo chip. Fuente: la tabla oficial de Unigine.",
  "cmp.gpu.h": "Cara a cara con las Radeon de sobremesa",
  "cmp.gpu.sub":
    "Superposition 1080p High: la BC-250 con SkillFishOS iguala a una <strong>RX&nbsp;6600/6600&nbsp;XT</strong> de más de 200 €.",
  "cmp.gpu.b1": "SkillFishOS — BC-250 (~50 €)",
  "cmp.gpu.b2": "Radeon RX 6600 / 6600 XT",
  "cmp.gpu.b3": "Radeon RX 6700 / 6750 XT",
  "cmp.gpu.note":
    "Cómputo bruto de una RX&nbsp;6700 (~11,3 TFLOPS) y rendimiento en juegos de una RX&nbsp;6600/6600&nbsp;XT — en una placa de unos 50 €. Un <strong>chip RDNA&nbsp;2 semipersonalizado, de clase consola</strong> («Oberon», gfx1013), liberado en Linux.",
  "cmp.axis": "Puntuación de Superposition",

  "oc.h": "Overclock y undervolt — caracterizados a mano",
  "oc.sub":
    "Curvas de voltaje y frecuencia medidas por el SMU en la APU «Oberon», con validación térmica real. Todo manejable desde el <strong>Tuner</strong> con perfiles listos.",
  "oc.cpu.v": "4,0 GHz",
  "oc.cpu.l": "CPU de 8 núcleos, todos a la vez · vuelto a medir paso a paso · 0 errores MCE",
  "oc.uv.v": "−194 mV",
  "oc.uv.l": "Undervolt de la CPU a 3,7 GHz (1206→1012 mV) sin pérdidas",
  "oc.gpu.v": "2230 MHz",
  "oc.gpu.l": "GPU · 40 CU · gobernador SMU propio",
  "oc.cap.v": "85 °C",
  "oc.cap.l": "Límite térmico de CPU y GPU: baja la frecuencia, nunca rompe",
  "oc.note":
    "Para cada frecuencia buscamos el <strong>voltaje estable más bajo</strong> leyendo el VID real del SMU y validando con 120 s de estrés. Los perfiles <strong>Stock · Performance · Turbo · Crazy</strong> aplican estos ajustes con un clic; una protección térmica lo mantiene todo por debajo de 85 °C. Todos los detalles en la documentación.",

  "don.title": "Apóyanos — Invítanos a un café",
  "don.eye": "Apoya el proyecto",
  "don.h2": "Ayúdanos a forjar el <span class=\"gold-text\">futuro</span> de SkillFishOS",
  "don.sub":
    "SkillFishOS es y seguirá siendo <strong>gratuito y de código abierto</strong>. Pero detrás hay un <strong>equipo pequeño</strong> y una sola placa: una pequeña aportación mantiene el desarrollo rápido — y vivo.",
  "don.why.h": "Un equipo pequeño. Una placa.",
  "don.why.p1":
    "Detrás de SkillFishOS hay un <strong>equipo pequeño</strong> que desarrolla, prueba y mantiene todo — núcleo, aplicaciones, tema, repositorio y web — en su tiempo libre y <strong>enteramente de su bolsillo</strong>. El sistema es y seguirá siendo gratuito y de código abierto: sin muros de pago ni anuncios.",
  "don.why.p2":
    "Hoy tenemos <strong>una sola BC-250</strong>. Cada parche de núcleo, gobernador u overclock hay que probarlo en la única placa que tenemos: si se cuelga a mitad de la prueba, el desarrollo se para. Ni pruebas en paralelo, ni comparación entre chips distintos (la «lotería del silicio»), ni margen para experimentar con tranquilidad. <strong>Tu ayuda lo cambia todo.</strong>",
  "don.use.h": "A dónde va el dinero",
  "don.use.sub": "Transparencia total: cada euro va a un desarrollo más rápido y mejor.",
  "don.u1.t": "Más placas BC-250",
  "don.u1.d":
    "Más placas = desarrollo más rápido y seguro: pruebas en paralelo, comparación del silicio y una de repuesto si alguna muere.",
  "don.u2.t": "Cajas y disipadores",
  "don.u2.d":
    "Mejor refrigeración para subir el overclock y la estabilidad — y para validar soluciones térmicas que merezca la pena recomendarte.",
  "don.u3.t": "Infraestructura",
  "don.u3.d":
    "Dominio, alojamiento, espejos e integración continua: los gastos que mantienen en línea la web, el repositorio APT y las descargas — hoy todos a nuestra costa.",
  "don.u4.t": "Tiempo de desarrollo",
  "don.u4.d":
    "Cada aportación nos permite dedicar más horas a nuevas funciones, arreglos y soporte, en lugar de a otra cosa.",
  "don.give.h": "Invítanos a un café ",
  "don.give.p":
    "Elige un importe: PayPal se abre con la cantidad ya puesta. Incluso <strong>1, 2 o 5 €</strong> marcan una diferencia enorme.",
  "don.give.custom": "Cualquier importe",
  "don.give.or": "o escanea el QR con el móvil",
  "don.give.scan": "Escanea para donar",
  "don.give.note":
    "Donación única por <strong>PayPal</strong>: sin compromiso ni suscripción. SkillFishOS seguirá siendo gratuito y de código abierto para siempre.",
  "don.thanks":
    "Gracias, de verdad — cada aportación enciende otra pieza de esta consola. ",

  "comm.h": "¿No puedes donar? Ayuda igualmente — es gratis",
  "comm.sub": "Tres gestos de un minuto que hacen crecer el proyecto tanto como una donación.",
  "comm.star.t": "Danos una estrella en GitHub",
  "comm.star.d":
    "Más estrellas = más visibilidad = más gente descubriendo SkillFishOS y colaborando. Es la forma más rápida de ayudar.",
  "comm.star.btn": "Dar estrella al repositorio →",
  "comm.review.t": "Deja una reseña",
  "comm.review.d":
    "¿Has probado SkillFishOS? Cuenta a los demás qué tal fue en SourceForge: las reseñas convencen a quien llega nuevo y a nosotros nos dicen qué mejorar.",
  "comm.review.btn": "Reseña en SourceForge →",
  "comm.idea.t": "Propón una idea",
  "comm.idea.d":
    "¿Qué función te haría la vida más fácil? Abre una discusión: las ideas de quienes lo usan marcan las próximas versiones de SkillFishOS.",
  "comm.idea.btn": "Proponer una función →",

  "ct.title": "Contacto — SkillFishOS",
  "ct.eye": "Contacto",
  "ct.h2": "Ponte en contacto",
  "ct.sub":
    "Soporte, información o cualquier otra cosa: rellena el formulario y te respondemos por correo.",
  "ct.f.name": "Nombre",
  "ct.f.email": "Tu correo",
  "ct.f.type": "Tipo de consulta",
  "ct.f.msg": "Mensaje",
  "ct.f.captcha": "Cuánto es",
  "ct.type.support": "Soporte",
  "ct.type.info": "Información",
  "ct.type.other": "Otro",
  "ct.send": "Enviar consulta",
  "ct.privacy":
    "No publicamos nuestro correo para reducir el spam: el formulario lo reenvía de forma segura. Los datos que introduces solo se usan para responderte.",
  "ct.ok": "¡Mensaje enviado! Te respondemos en breve.",
  "ct.err.captcha": "La comprobación antispam ha fallado. Inténtalo de nuevo.",
  "ct.err.fields":
    "Revisa los campos: hacen falta el nombre, un correo válido y un mensaje.",
  "ct.err.send": "No se ha podido enviar. Inténtalo más tarde o escríbenos en GitHub.",
  "ct.err.generic": "Algo ha salido mal. Inténtalo de nuevo.",
};
