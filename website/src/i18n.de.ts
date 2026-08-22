// German UI strings. Any key missing here falls back to English (see t() in
// i18n.ts), so this file can grow without ever leaving a blank on the page.
// Inline HTML and &nbsp; entities are part of the copy — keep them.
//
// Germany looked enormous in the raw numbers — 202 downloads — until the spike
// of 17 August was isolated: 163 of those arrived on that single day, together
// with 435 from Kenya, from two exit points. That was a scraper. What is left is
// real and steady: 15.2% of the last three days, ahead of Poland.
//
// Addressed as "du": this is a console for playing at home, and half the point
// of the project is children learning Linux. "Sie" would sound like a bank.
//
// ⚠️ NOT reviewed by a native speaker. Written by the SkillFishOS team, like the
// Russian, Spanish, Portuguese and Ukrainian ones; the Polish is Cyryl
// Sochacki's. Corrections are welcome and cost one file: this one.
export const de: Record<string, string> = {
  title: "SkillFishOS — Gaming-Linux für die AMD BC-250",
  "meta.desc":
    "SkillFishOS: das Steampunk-Betriebssystem zum Spielen auf der AMD-BC-250-Platine. Fertig eingestellt, kein Basteln nötig. Emulation, Steam, KI auf dem Gerät selbst. Auf Basis von Debian + KDE Plasma.",

  "nav.feat": "Funktionen",
  "nav.shots": "Bildschirmfotos",
  "nav.hw": "Hardware",
  "nav.download": "Herunterladen",
  "nav.docs": "Dokumentation",
  "nav.gallery": "Galerie",
  "nav.contact": "Kontakt",
  "nav.donate": "Unterstützen",
  "nav.news": "Neuigkeiten",
  "nav.road": "Fahrplan",

  "hero.soon": "Version 26.06 „Aetherium“",
  "hero.tag": "Das Betriebssystem zum Spielen, geschmiedet für die <b>AMD BC-250</b>.",
  "hero.sub":
    "Steampunk-Linux, ab dem ersten Start spielbereit. Alles fertig eingestellt, kein Basteln nötig. Emulation, Steam und KI auf dem Gerät selbst. Auf Basis von Debian und KDE&nbsp;Plasma.",
  "hero.btn1": "In Aktion sehen",
  "hero.btn2": "Was drinsteckt",
  "hero.pill": "AMD-APU · Zen&nbsp;2 + RDNA&nbsp;2 · 16&nbsp;GB GDDR6",

  "intro.eye": "Was es ist",
  "intro.h2": "Ein Konsolen-PC,<br>sofort einsatzbereit.",
  "intro.p1":
    "SkillFishOS macht aus der <strong>AMD-BC-250</strong>-Platine — einer teilweise maßgefertigten APU aus der <strong>Familie AMD Zen&nbsp;2 + RDNA&nbsp;2</strong> (CPU „Oberon“, Grafik „Cyan&nbsp;Skillfish“, 16&nbsp;GB GDDR6) — ein vollständiges System zum Spielen und Arbeiten.",
  "intro.p2":
    "Governor, Kernel-Patches, Übertaktung und Temperaturprofile sind <strong>fertig eingestellt</strong>: ein System, das sein Bestes gibt, <strong>ohne dass du etwas machen musst</strong>. Ein durchgehendes <strong>Steampunk</strong>-Erscheinungsbild vom Start bis zum Schreibtisch, gedacht auch dafür, dass <strong>Kinder Linux lernen</strong>, während sie spielen.",

  "feat.eye": "Funktionen",
  "feat.h2": "Alles fertig, einfach einschalten.",
  "feat.sub": "Es gibt nichts von Hand einzurichten: das System ist bereits auf die BC-250 abgestimmt.",

  "f1.t": "Bereit zum Spielen",
  "f1.d":
    "Steam, EmuDeck, ES-DE, Heroic und Proton sind startklar. EmuDeck installiert und richtet die Emulatoren mit wenigen Klicks ein — Spiele und ROMs bringst du mit.",
  "f2.t": "Maßgeschneiderter Kernel",
  "f2.d":
    "Ein tkg-Kernel, abgestimmt auf die BC-250: <b>40 Recheneinheiten</b> freigeschaltet, Übertaktung von CPU und GPU und ein eigener SMU-Governor, um jedes TFLOPS herauszuholen.",
  "f3.t": "Fertig, ohne Basteln",
  "f3.d":
    "Governor, Patches, Übertaktung und ein Temperaturschutz sind <b>bereits eingerichtet und geprüft</b>. Einschalten, und es läuft mit voller Geschwindigkeit: kein Terminal, kein Nachjustieren.",
  "f4.t": "Steampunk-Gestaltung",
  "f4.d":
    "Ein dunkler KDE&nbsp;Plasma-Schreibtisch im Steampunk-Stil: Symbole, Zeiger, Hintergrundbild und ein System-HUD im mechanisch-viktorianischen Geist.",
  "f5.t": "Btrfs-Schnappschüsse",
  "f5.d":
    "Probier ruhig aus: jede Änderung ist durch automatische Schnappschüsse abgesichert. Etwas kaputt? <b>Mit einem Klick zurück</b> aus dem Startmenü.",
  "f6.t": "KI auf dem Gerät",
  "f6.d":
    "<b>Unsloth Studio</b> mit <b>Vulkan</b> auf der eingebauten GPU beschleunigt: gemessen <b>5,1×</b> schneller als auf der CPU. Modelle zum Chatten und Programmieren laufen zu Hause, ohne Cloud.",
  "f7.t": "Fernsteuerung",
  "f7.d":
    "<b>Remote Manager</b>: eine Weboberfläche, um die Platine vom Browser oder Handy aus zu steuern — Telemetrie, KVM, Terminal, Tuner, App-Verwaltung und KI. Anmeldung mit den Systemkonten über HTTPS, und mit ZeroTier von überall.",

  "show.eye": "Bildschirmfotos",
  "show.h2": "Schön anzusehen, einfach zu bedienen.",
  "s1.t": "Der Steampunk-Schreibtisch",
  "s1.d":
    "KDE Plasma im Steampunk-Stil: passendes Hintergrundbild, goldene Akzente und ein HUD in Echtzeit mit CPU, GPU, Temperaturen, Lüfter und Akkustand des Bluetooth-Controllers, immer im Blick.",
  "s2.t": "Einfache Emulation mit EmuDeck",
  "s2.d":
    "EmuDeck installiert und richtet die Emulatoren (RetroArch, Dolphin, PCSX2, PPSSPP, RPCS3 und weitere) und die ES-DE-Oberfläche mit wenigen Klicks ein. Das System stellt die Werkzeuge: Spiele und ROMs bringst du mit.",
  "s4.t": "KI auf dem Gerät, einen Klick entfernt",
  "s4.d":
    "Ein eigenes Fenster schaltet die lokale KI (Qwen auf der GPU über Vulkan) ein und aus. Web-Chat, ein Terminal zum Programmieren und die Verwaltung: die KI läuft zu Hause und gibt die GPU frei, wenn gespielt wird.",
  "s5.t": "Feinabstimmung mit einem Klick",
  "s5.d":
    "Der Tuner stellt Takt, Undervolting, Lüfter und Recheneinheiten ein — mit vier fertigen Profilen (Stock, Performance, Turbo, Crazy) und einem Temperaturschutz, der die Hardware bewahrt. Die volle Leistung, sicher und ohne Kommandozeile.",

  "hw.eye": "Hardware",
  "hw.h2": "Geboren für die AMD BC-250.",
  "hw.sub": "Die ganze Kraft der Familie AMD Zen 2 + RDNA 2, unter Linux entfesselt.",
  "hw.c1": "CPU „Oberon“ · bis 4,0 GHz",
  "hw.c2": "GPU „Cyan Skillfish“ · 40 CU",
  "hw.c3": "FP32 · Vulkan-Beschleunigung",
  "hw.c4": "gemeinsamer GDDR6",

  "cta.h2": "Einschalten. <span class=\"gold-text\">Spielen.</span> Lernen.",
  "cta.p":
    "Ein quelloffenes Betriebssystem, das aus einer nackten Platine einen echten Konsolen-PC macht. In zwei Ausgaben erhältlich: AMD BC-250 und Generic (jeder x86-64-PC oder jede virtuelle Maschine).",
  "cta.btn": "SkillFishOS herunterladen",
  "foot.based": "Quelloffen · Auf Basis von Debian · KDE Plasma · © 2026 SkillFishOS",

  "dl.title": "Herunterladen — SkillFishOS",
  "dl.eye": "Herunterladen",
  "dl.h2": "SkillFish<span class=\"gold-text\">OS</span> herunterladen",
  "dl.sub":
    "Die installierbaren, gebrandeten und sofort nutzbaren ISOs — für die AMD BC-250 und für jeden x86-64-PC.",
  "dl.badge": "26.06.4 „Aetherium“",
  "dl.notice":
    "Die Version <strong>26.06.4 „Aetherium“</strong> von SkillFishOS gibt es in <strong>zwei Ausgaben</strong>: <strong>BC-250</strong> (die AMD-Platine) und <strong>Generic</strong> (jeder x86-64-PC oder jede virtuelle Maschine). Vollständig und sofort nutzbar. Ein <strong>quelloffenes</strong> Projekt.",
  "dl.btnsoon": "ISO folgt in Kürze",
  "dl.btn": "ISO herunterladen",
  "dl.ed.bc250": "BC-250",
  "dl.ed.generic": "Generic (PC/VM)",
  "dl.ed.slim": "Slim (BC-250)",
  "dl.ed.all": "Alle Dateien auf SourceForge →",
  "dl.size": "amd64 · ~{size} GB · btrfs + KDE Plasma · 2 Ausgaben auf SourceForge",
  "dl.ver":
    "Version <strong>26.06.4 „Aetherium“</strong> · <strong>2 Ausgaben</strong> (BC-250 · Generic) · startet auf Englisch, die Sprache wird bei der Installation gewählt",
  "dl.fast.h": "Der schnellste Weg, aus Europa",
  "dl.fast.sub":
    "Das Internet Archive bewahrt unsere ISOs auf und liefert sie von seinen eigenen Servern aus. Von einer italienischen Leitung gemessen: <strong>etwa 5 MB/s</strong> gegenüber 0,4 von SourceForge, das alles aus San Diego ausliefert. Dieselbe Datei, dieselbe Prüfsumme.",
  "dl.fast.bc250": "BC-250",
  "dl.fast.generic": "Generic (PC/VM)",
  "dl.sf.h": "Oder von SourceForge",
  "dl.sf.sub":
    "Der langjährige Spiegelserver des Projekts: aus Europa langsamer, aber von dort stammen unsere Download-Zahlen.",
  "dl.tor.h": "Oder per Torrent",
  "dl.tor.sub":
    "Schneller, wenn mehrere gleichzeitig laden, und es macht dort weiter, wo es aufgehört hat. Es funktioniert auch, wenn sonst niemand verbunden ist: der Torrent zieht direkt von unseren Spiegelservern.",
  "dl.tor.bc250": "⇅ BC-250 · Torrent",
  "dl.tor.generic": "⇅ Generic · Torrent",
  "dl.tor.magnet": "magnet",
  "dl.bugs.h": "Ein Problem gefunden?",
  "dl.bugs.d":
    "SkillFishOS wird laufend besser. Um Fehler oder Probleme zu melden, öffne ein <em>Issue</em> auf GitHub. (Eine E-Mail-Adresse kommt bald dazu.)",
  "dl.bugs.btn": "Auf GitHub melden",
  "dl.req.h": "Voraussetzungen",
  "dl.req.d":
    "Eine <strong>AMD-BC-250</strong>-Platine (APU Zen&nbsp;2 + RDNA&nbsp;2, 16&nbsp;GB GDDR6), eine SSD oder NVMe, ein Bildschirm mit <strong>DisplayPort</strong> und ein USB-Stick ab 8&nbsp;GB für das Installationsprogramm.",
  "dl.inc.h": "Was dabei ist",
  "dl.inc.d":
    "Ein optimierter Kernel (40&nbsp;CU, Governor, Übertaktung), die vollständige Steampunk-Gestaltung, Steam + EmuDeck + ES-DE, lokale KI, Btrfs-Schnappschüsse und die Werkzeuge Tuner und AI, sofort nutzbar.",
  "dl.steps.h": "Installation",
  "dl.step1": "Schreibe die ISO auf einen USB-Stick (Etcher, Ventoy oder <code>dd</code>).",
  "dl.step2": "Starte die BC-250 vom Stick und folge dem grafischen Installationsprogramm (Calamares).",
  "dl.step3": "Beim ersten Start ist alles eingerichtet: einschalten und spielen.",
  "dl.repo.h": "Aktualisierungen",
  "dl.repo.d":
    "SkillFishOS aktualisiert sich aus seiner <strong>eigenen Paketquelle</strong>: Kernel, Anwendungen und Gestaltung kommen von uns und sind geprüft, damit Aktualisierungen von Debian sid das System nicht kaputt machen können.",

  "news.title": "Neuigkeiten",
  "news.eye": "Immer auf dem Laufenden",
  "news.h1": "Was sich geändert hat,<br>und wann",
  "news.sub":
    "Ein kleines Projekt wird auch daran gemessen, wie oft es etwas von sich hören lässt. Hier stehen die Neuigkeiten nach Datum und der Weg nach vorn, mit dem Stand jedes Punktes — auch der noch nicht fertigen.",
  "news.h.news": "Neuigkeiten",
  "news.h.road": "Fahrplan",
  "news.road.sub":
    "Woran wir arbeiten, was als Nächstes kommt und was schon da ist. Wir versprechen keine Termine, solange wir sie nicht wirklich haben.",
  "news.foot":
    "Hast du eine Idee, oder fehlt etwas? Wünsche sind willkommen: schreib uns über die <a href=\"/de/contact\">Kontaktseite</a> oder eröffne eine Diskussion auf GitHub. Das zu bauen, was jemand wirklich braucht, ist besser als gut zu raten.",
  "news.diroad": "Du willst wissen, was als Nächstes kommt? Das steht im <a href=\"/de/roadmap\">Fahrplan</a>.",

  "road.title": "Fahrplan",
  "road.eye": "Wohin wir gehen",
  "road.h1": "Was kommt,<br>und was schon da ist",
  "road.sub":
    "Wir versprechen keine Termine, solange wir sie nicht wirklich haben. Erledigte Punkte bleiben unten stehen, denn sie beantworten die Frage, die uns am häufigsten gestellt wird: ob das Projekt noch lebt.",
  "road.dinews": "Du suchst, was sich geändert hat? Das steht in den <a href=\"/de/news\">Neuigkeiten</a>.",

  "gal.title": "Galerie — SkillFishOS",
  "gal.eye": "Galerie",
  "gal.h2": "Schön anzusehen, einfach zu bedienen.",
  "gal.sub": "SkillFishOS in Aktion: Schreibtisch, Spiele, Emulation und Werkzeuge.",
  "gal.desktop.t": "Der Steampunk-Schreibtisch",
  "gal.desktop.d": "KDE Plasma in der Gestaltung des Systems, mit einem HUD in Echtzeit oben rechts.",
  "gal.about.t": "Systeminformationen",
  "gal.about.d": "Vollständiges Branding: Name, Logo und Hardware werden als SkillFishOS erkannt.",
  "gal.emudeck.t": "EmuDeck",
  "gal.emudeck.d": "Installation und Einrichtung der Emulatoren mit wenigen Klicks.",
  "gal.esde1.t": "ES-DE — Oberfläche",
  "gal.esde1.d": "Die ES-DE-Oberfläche, um deine Sammlungen zu durchstöbern und zu starten.",
  "gal.ai.t": "KI-Fenster",
  "gal.ai.d": "Schaltet die lokale KI (Vulkan) mit einem Klick ein und aus.",
  "gal.tuner.t": "Tuner — Recheneinheiten in Echtzeit",
  "gal.tuner.d":
    "CU-Raster (grün = an, rot = aus), Profile 24/32/40 und Prüfung, ohne Neustart.",
  "gal.tunerctl.t": "Tuner — Profile, Governor und Assistenten",
  "gal.tunerctl.d":
    "Profile Stock/Performance/Turbo/Crazy, das Fenster „Mein Silizium“, der Governor-Modus Balanced/Performance und die Assistenten „Finde mein Maximum“ für CPU und GPU.",
  "gal.monitor.t": "Telemetrie in Echtzeit während der Tests",
  "gal.monitor.d": "Kurven von Temperatur, Takt, Spannung und Lüfter in Echtzeit.",
  "gal.cutest.t": "CU-Prüfung — Silizium-Lotterie",
  "gal.cutest.d":
    "Prüft, ob alle 40 CU die Last ohne Fehler tragen (nützlich bei gebrauchten Chips).",
  "gal.wukong.t": "Black Myth: Wukong — 112 FPS",
  "gal.wukong.d": "Durchschnitt in 1080p auf der BC-250 (Maximum 128, 1% low 101).",
  "gal.super.t": "Unigine Superposition — 12.938",
  "gal.super.d": "1080p High: Leistung einer Radeon RX 6600 auf einer Platine für rund 50 Euro.",
  "gal.heaven.t": "Unigine Heaven — 113,7 FPS",
  "gal.heaven.d": "2865 Punkte in 1080p Ultra, 8× AA, Tessellation Extreme.",
  "gal.boot.t": "Steampunk-Start",
  "gal.boot.d": "Ein durchgehender Messing-Startbildschirm von GRUB bis zum Schreibtisch.",
  "gal.b1.t": "Dieselbe Hardware, +34% — gegen Bazzite",
  "gal.b1.d":
    "Superposition 1080p Extreme: dieselbe BC-250 erreicht mit Werkstakt in einer anderen Distribution 4102; mit SkillFishOS sind es 5513. Offizielle Bestenliste von Unigine.",
  "gal.b2.t": "Auf Augenhöhe mit einer Radeon RX 6600",
  "gal.b2.d":
    "Superposition 1080p High: die BC-250 mit SkillFishOS (12.938) zieht mit einer RX 6600/6600 XT für über 200 Euro gleich (12.454). Offizielle Bestenliste von Unigine.",

  "hwp.title": "AMD-BC-250-Hardware — SkillFishOS",
  "hwp.eye": "Hardware",
  "hwp.h2": "Geboren für die <span class=\"gold-text\">AMD BC-250</span>.",
  "hwp.sub": "Eine teilweise maßgefertigte APU AMD Zen 2 + RDNA 2 mit 16 GB GDDR6, unter Linux entfesselt.",
  "hwp.specs.h": "Technische Daten",
  "hwp.cpu.t": "CPU — 8× Zen 2",
  "hwp.cpu.d":
    "„Oberon“, <strong>8 Kerne / 16 Threads</strong> (die Platine zeigt 6, SkillFishOS schaltet die anderen beiden über die SMU frei: <strong>+20%</strong> gemessen), übertaktet bis <strong>4,0 GHz auf allen Kernen</strong>.",
  "hwp.gpu.t": "GPU — RDNA 2",
  "hwp.gpu.d": "„Cyan Skillfish“ (gfx1013), bis zu 40 freischaltbare Recheneinheiten.",
  "hwp.mem.t": "Speicher — 16 GB GDDR6",
  "hwp.mem.d":
    "Gemeinsam genutzt (UMA) von CPU und GPU; unter Linux erweitert der GTT den Grafikspeicher.",
  "hwp.perf.t": "Rechenleistung — ~11 TFLOPS",
  "hwp.perf.d": "FP32 bei 40 CU / 2000 MHz (vkpeak), mit Vulkan-Beschleunigung.",
  "hwp.quirks.h": "Schwächen der Hardware (und wie wir sie beheben)",
  "hwp.q1.t": "Defektes DisplayPort-HPD",
  "hwp.q1.d":
    "Die Bildschirmerkennung funktioniert nicht → eigener Dienst + Kernel-Parameter <code>video=DP-1:e</code>.",
  "hwp.q2.t": "Kaputter Ruhezustand",
  "hwp.q2.d": "Die Platine wacht nicht auf → alle Schlafzustände dauerhaft abgeschaltet.",
  "hwp.q3.t": "Instabile IOMMU",
  "hwp.q3.d": "Darf niemals eingeschaltet werden → das System startet immer ohne IOMMU.",
  "hwp.q4.t": "Knappe Kühlung",
  "hwp.q4.d":
    "Nur ein Randsensor, kein VRAM-Sensor → ein Temperaturschutz bei 85 °C ist immer aktiv.",
  "hwp.cta": "Mehr dazu in der Dokumentation →",

  "bm.h": "Gemessene Leistung",
  "bm.sub":
    "Messungen mit vkpeak FP32-scalar (GFLOPS) auf <strong>derselben</strong> BC-250, vor und nach SkillFishOS.",
  "bm.bar1": "Ausgangswert — XanMod, 24 CU",
  "bm.bar2": "tkg + Governor, 24 CU",
  "bm.bar3": "SkillFishOS — tkg + Governor + 40 CU",
  "bm.unit": "GFLOPS",
  "bm.note":
    "Messungen mit <strong>vkpeak</strong> (Vulkan-Rechenlast) auf derselben Platine, kalt und im Leerlauf. Mit 40 aktiven CU liefert die GPU das <strong>1,84-Fache</strong> des Ausgangssystems. Im Leerlauf geht der Governor auf 350 MHz zurück; Rand etwa 54 °C nach der Rechenlast.",
  "bm.s1.l": "FP32 gegenüber dem Ausgangswert",
  "bm.s2.l": "GFLOPS FP32 (≈11,3 TFLOPS)",
  "bm.s3.l": "GFLOPS FP16 (vec4)",
  "bm.s4.l": "GIOPS int8 (Skalarprodukt)",
  "bm.src": "Quelle: eigene Messungen auf echter Hardware (vkpeak). Einzelheiten in",
  "bm.gpulink": "GPU, Governor und Übertaktung",

  "wk.h": "Echte Last — Black Myth: Wukong (1080p)",
  "wk.note":
    "Rund 4 Minuten Telemetrie mitten im Spiel: <strong>CPU und GPU halten die volle Übertaktung</strong> innerhalb der Temperaturgrenze von 85 °C — Governor, Übertaktung und Temperaturschutz kommen mit einem anspruchsvollen AAA-Titel zurecht. (Wukong hängt an <em>CPU und Zeichenaufrufen</em>: hier zählt die Stabilität unter Last, nicht die Auflösung.)",
  "wk.l.gpu": "GPU (sicherer Punkt)",
  "wk.l.gpuc": "GPU-Rand (max. 81)",
  "wk.l.pwr": "Leistungsaufnahme (Spitze 182 W)",
  "wk.l.cpu": "CPU (Übertaktung)",
  "wk.l.vram": "Belegter Grafikspeicher",
  "wk.l.fan": "Lüfter",

  "bs.h": "Echte Bildschirmfotos — auf unserer eigenen Hardware aufgenommen",
  "bs.sub":
    "Keine Renderbilder, keine Entwürfe: echte Bildschirmfotos, aufgenommen während der Messungen auf <strong>unserer eigenen</strong> BC-250 mit SkillFishOS. Tippe ein Bild an, um es zu vergrößern.",
  "bs.wk.c":
    "Black Myth: Wukong — <strong>112 FPS</strong> im Schnitt bei 1080p (Maximum 128, 1% low 101). APU AMD BC-250, GPU RADV gfx1013.",
  "bs.hv.c":
    "Unigine Heaven 4.0 — <strong>113,7 FPS</strong>, Punktzahl <strong>2865</strong> (1080p Ultra, 8× AA, Tessellation Extreme). Kernel 7.0.10-skillfishos (heute liefern wir 7.2.0 aus).",
  "bs.sc.c":
    "Unigine Heaven — die Szene in Echtzeit auf der BC-250 während des Durchlaufs berechnet.",

  "gb.h": "Spiele-Messungen — echte Ergebnisse",
  "gb.sub":
    "Gemessen auf der BC-250 mit SkillFishOS, bei 1080p. Eine Platine für <strong>rund 50 Euro</strong>, die auf dem Niveau einer <strong>Radeon RX&nbsp;6600</strong> spielt.",
  "gb.wk.v": "112 FPS",
  "gb.wk.l": "Black Myth: Wukong · Durchschnitt bei 1080p",
  "gb.hv.v": "2865",
  "gb.hv.l": "Unigine Heaven · 1080p Ultra/Extreme · 8× AA · 113 FPS",
  "gb.sp.v": "12.938",
  "gb.sp.l": "Unigine Superposition · 1080p High · (5513 in Extreme)",

  "cmp.os.h": "Dieselbe Hardware, +34% nur durch den Systemwechsel",
  "cmp.os.sub":
    "Superposition 1080p Extreme, auf <strong>derselben BC-250</strong>: SkillFishOS gegen eine andere Distribution mit Werkstakt.",
  "cmp.os.b1": "SkillFishOS — GPU 2230 · CPU 3900",
  "cmp.os.b2": "Andere Distribution (Bazzite) — GPU 2100 · CPU 3436",
  "cmp.os.note":
    "40 freigeschaltete CU, ein Governor, der die GPU auf 2230 MHz bringt, und Übertaktung mit Undervolting bei der CPU: <strong>+34% echte Leistung</strong> aus demselben Chip. Quelle: die offizielle Bestenliste von Unigine.",
  "cmp.gpu.h": "Im direkten Vergleich mit Desktop-Radeons",
  "cmp.gpu.sub":
    "Superposition 1080p High: die BC-250 mit SkillFishOS zieht mit einer <strong>RX&nbsp;6600/6600&nbsp;XT</strong> für über 200 Euro gleich.",
  "cmp.gpu.b1": "SkillFishOS — BC-250 (~50 €)",
  "cmp.gpu.b2": "Radeon RX 6600 / 6600 XT",
  "cmp.gpu.b3": "Radeon RX 6700 / 6750 XT",
  "cmp.gpu.note":
    "Rohe Rechenleistung einer RX&nbsp;6700 (~11,3 TFLOPS), Spieleleistung einer RX&nbsp;6600/6600&nbsp;XT — auf einer Platine für rund 50 Euro. Ein <strong>teilweise maßgefertigter RDNA&nbsp;2-Chip aus der Konsolenwelt</strong> („Oberon“, gfx1013), unter Linux entfesselt.",
  "cmp.axis": "Superposition-Punktzahl",

  "oc.h": "Übertaktung und Undervolting — von Hand ermittelt",
  "oc.sub":
    "Spannungs- und Taktkurven über die SMU auf der APU „Oberon“ gemessen, mit echter Temperaturprüfung. Alles über den <strong>Tuner</strong> steuerbar, mit fertigen Profilen.",
  "oc.cpu.v": "4,0 GHz",
  "oc.cpu.l": "CPU mit 8 Kernen, alle gleichzeitig · Schritt für Schritt nachgemessen · 0 MCE-Fehler",
  "oc.uv.v": "−194 mV",
  "oc.uv.l": "Undervolting der CPU bei 3,7 GHz (1206→1012 mV) ohne Verlust",
  "oc.gpu.v": "2230 MHz",
  "oc.gpu.l": "GPU · 40 CU · eigener SMU-Governor",
  "oc.cap.v": "85 °C",
  "oc.cap.l": "Temperaturgrenze für CPU und GPU: senkt den Takt, geht nie kaputt",
  "oc.note":
    "Für jede Frequenz haben wir die <strong>niedrigste stabile Spannung</strong> gesucht, indem wir die echte VID aus der SMU gelesen und mit 120 s Last geprüft haben. Die Profile <strong>Stock · Performance · Turbo · Crazy</strong> setzen diese Werte mit einem Klick; ein Temperaturschutz hält alles unter 85 °C. Alle Einzelheiten in der Dokumentation.",

  "don.title": "Unterstütze uns — Spendier uns einen Kaffee",
  "don.eye": "Unterstütze das Projekt",
  "don.h2": "Hilf mit, die <span class=\"gold-text\">Zukunft</span> von SkillFishOS zu schmieden",
  "don.sub":
    "SkillFishOS ist und bleibt <strong>kostenlos und quelloffen</strong>. Dahinter stehen aber ein <strong>kleines Team</strong> und eine einzige Platine: ein kleiner Beitrag hält die Entwicklung schnell — und am Leben.",
  "don.why.h": "Ein kleines Team. Eine Platine.",
  "don.why.p1":
    "Hinter SkillFishOS steht ein <strong>kleines Team</strong>, das alles entwickelt, prüft und pflegt — Kernel, Anwendungen, Gestaltung, Paketquelle und Website — in seiner Freizeit und <strong>vollständig aus eigener Tasche</strong>. Das System ist und bleibt kostenlos und quelloffen: keine Bezahlschranke, keine Werbung.",
  "don.why.p2":
    "Heute haben wir <strong>nur eine einzige BC-250</strong>. Jeder Patch für Kernel, Governor oder Übertaktung muss auf der einzigen Platine geprüft werden, die wir besitzen: friert sie mitten im Test ein, steht die Entwicklung still. Keine parallelen Tests, kein Vergleich verschiedener Chips (die „Silizium-Lotterie“), kein Spielraum, um in Ruhe zu experimentieren. <strong>Deine Hilfe ändert das alles.</strong>",
  "don.use.h": "Wohin das Geld geht",
  "don.use.sub": "Vollständige Transparenz: jeder Euro wird zu schnellerer und besserer Entwicklung.",
  "don.u1.t": "Mehr BC-250-Platinen",
  "don.u1.d":
    "Mehr Platinen = schnellere und sicherere Entwicklung: Tests nebeneinander, Vergleich des Siliziums und eine Reserve, falls eine stirbt.",
  "don.u2.t": "Gehäuse und Kühlkörper",
  "don.u2.d":
    "Bessere Kühlung, um Übertaktung und Stabilität zu steigern — und um Kühllösungen zu prüfen, die wir dir guten Gewissens empfehlen können.",
  "don.u3.t": "Infrastruktur",
  "don.u3.d":
    "Domain, Hosting, Spiegelserver und Bausysteme: die Kosten, die Website, APT-Paketquelle und Downloads am Netz halten — heute vollständig auf unsere Rechnung.",
  "don.u4.t": "Entwicklungszeit",
  "don.u4.d":
    "Jeder Beitrag erlaubt es, mehr Stunden in neue Funktionen, Korrekturen und Unterstützung zu stecken statt woanders hin.",
  "don.give.h": "Spendier uns einen Kaffee ",
  "don.give.p":
    "Wähle einen Betrag: PayPal öffnet sich mit der Summe bereits eingetragen. Selbst <strong>1, 2 oder 5 €</strong> machen einen riesigen Unterschied.",
  "don.give.custom": "Beliebiger Betrag",
  "don.give.or": "oder scanne den QR-Code mit dem Handy",
  "don.give.scan": "Zum Spenden scannen",
  "don.give.note":
    "Einmalige Spende über <strong>PayPal</strong>: keine Verpflichtung, kein Abonnement. SkillFishOS bleibt für immer kostenlos und quelloffen.",
  "don.thanks":
    "Danke, wirklich — jeder Beitrag bringt ein weiteres Teil dieser Konsole zum Leuchten. ",

  "comm.h": "Kannst du nicht spenden? Hilf trotzdem — es kostet nichts",
  "comm.sub": "Drei Handgriffe von je einer Minute, die das Projekt so sehr wachsen lassen wie eine Spende.",
  "comm.star.t": "Gib uns einen Stern auf GitHub",
  "comm.star.d":
    "Mehr Sterne = mehr Sichtbarkeit = mehr Leute, die SkillFishOS entdecken und mitmachen. Das ist der schnellste Weg zu helfen.",
  "comm.star.btn": "Stern für das Repository →",
  "comm.review.t": "Schreib eine Bewertung",
  "comm.review.d":
    "SkillFishOS ausprobiert? Erzähl auf SourceForge, wie es gelaufen ist: Bewertungen überzeugen Neue, es zu versuchen, und sagen uns, was besser werden muss.",
  "comm.review.btn": "Auf SourceForge bewerten →",
  "comm.idea.t": "Schlag eine Idee vor",
  "comm.idea.d":
    "Welche Funktion würde dir das Leben leichter machen? Eröffne eine Diskussion: die Ideen der Nutzer bestimmen die nächsten Versionen von SkillFishOS.",
  "comm.idea.btn": "Funktion vorschlagen →",

  "ct.title": "Kontakt — SkillFishOS",
  "ct.eye": "Kontakt",
  "ct.h2": "Nimm Kontakt auf",
  "ct.sub":
    "Unterstützung, Auskunft oder sonst etwas: füll das Formular aus, und wir antworten per E-Mail.",
  "ct.f.name": "Name",
  "ct.f.email": "Deine E-Mail",
  "ct.f.type": "Art der Anfrage",
  "ct.f.msg": "Nachricht",
  "ct.f.captcha": "Wie viel ist",
  "ct.type.support": "Unterstützung",
  "ct.type.info": "Auskunft",
  "ct.type.other": "Sonstiges",
  "ct.send": "Anfrage senden",
  "ct.privacy":
    "Wir veröffentlichen unsere E-Mail-Adresse nicht, um Spam zu verringern: das Formular leitet sie sicher weiter. Die eingegebenen Daten werden nur verwendet, um dir zu antworten.",
  "ct.ok": "Nachricht gesendet! Wir melden uns bald.",
  "ct.err.captcha": "Die Spam-Prüfung ist fehlgeschlagen. Bitte versuch es noch einmal.",
  "ct.err.fields":
    "Prüf die Felder: Name, eine gültige E-Mail-Adresse und eine Nachricht sind nötig.",
  "ct.err.send": "Senden fehlgeschlagen. Versuch es später noch einmal oder schreib uns auf GitHub.",
  "ct.err.generic": "Etwas ist schiefgegangen. Bitte versuch es noch einmal.",
};
