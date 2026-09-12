#!/usr/bin/env python3
"""The Control Center page of the website documentation, in the nine languages.

    docs-sito-control-center.py <repo>

Writes website/src/content/docs/<lang>/control-center.md. The "?" buttons in
the window carry one sentence each; the longer explanations live here, and
the window links to this page in the language of the system.
"""
import os
import sys

repo = sys.argv[1]
GRUPPO = {"it": "Uso", "en": "Usage", "pl": "Używanie", "uk": "Користування", "ru": "Использование",
          "es": "Uso", "pt": "Uso", "de": "Benutzung", "fr": "Utilisation"}

T = {
"en": dict(
    title="Control Center", desc="Every SkillFishOS tool in one window: Tuner, Fan, Monitor, Games, Profiles, Kernel, Snapshots, AI, Emulators, Console, ISO.",
    intro="Every SkillFishOS tool lives in one window. Open it from the menu (SkillFishOS → Control Center) or with `skillfish-control-center`. A controller drives it too: D-pad or stick to move, A confirms, B goes back, LB and RB switch section.",
    sezioni="## The sections",
    voci=[("Status", "one number per card: GPU clock and ceiling, CPU, compute units, fan, kernel, governor, Vulkan driver, whether the last boot followed a clean shutdown. Nothing to set."),
          ("Tuner", "the voltage/frequency curve of the GPU governor, the CPU, the cores, the compute units, the VRAM split."),
          ("Fan", "the fan curve with its lead, the source sensors, the safety limits, the PWM test."),
          ("Monitor", "every reading in one chart per unit, plus the per-thread clock bars. REC records, CSV exports."),
          ("Games", "our Mesa per launcher or system-wide, the scx_bpfland scheduler, FSR 4, GE-Proton install and default."),
          ("Profiles", "ceiling, CPU, fan and scheduler in one click; save your own."),
          ("Kernel", "the installed kernels, the default one, boot once, uninstall."),
          ("Snapshots", "system snapshots and the btrfs maintenance schedule."),
          ("AI", "Unsloth Studio on Vulkan: engine, update, models from the Hugging Face Hub, a chat test, memory and network."),
          ("Emulators", "EmuDeck, or the emulators one by one from Flathub."),
          ("Console", "Steam Big Picture inside gamescope, now or from the login screen."),
          ("ISO", "disk images mounted through udisks.")],
    tuner_t="## Tuner",
    tuner="""The curve is the chart: MHz across, millivolts up. Drag a knot, double-click to add one, right-click to remove it, or type the numbers in the table beside the chart (+ and − add and remove knots). The dashed vertical line is the ceiling, the blue dot is the GPU right now. Three presets: **Cautious 1850** (the sweet spot with the stock heatsink, nearly the same frames and ten degrees less), **Balanced 2000**, **Performance 2100** (the fifteen-point curve measured on the development board, the one we ship).

**Apply is a trial.** A curve that asks too little voltage hangs the board, and on the BC-250 a hang means pulling the plug. So Apply starts the candidate with the previous curve still on disk and counts down 25 seconds: press Keep and the candidate is written for good; do nothing, or let the board die and come back, and the previous curve is what boots.

The panels open on demand:

- **CPU**: clock, undervolt step (6.25 mV each) and thermal limit, each with a slider and a number box at step 1. *Suggest UV* walks the undervolt down two steps at a time with twelve seconds of load per step; *Find my max* climbs from 3600 to 4000 MHz; *Test 60 s* loads the current values. Every run shows a countdown and a Stop button; the values under test are never written to disk, so a hang boots the previous ones. Above 3500 MHz with eight cores the gain is nil: heat is in charge.
- **Cores**: which cores are online, SMT, the 8-core unlock (6c/12t becomes 8c/16t, +20% measured) and *Before boot (EFI)*: the unlock done before GRUB in a single boot, instead of the extra reboot of the in-system service.
- **CU**: the 40 compute units as 20 cells (pairs): green on, red off, grey kept on by the driver. Type the number of CUs you want (24 to 40, in pairs) or click the cells; *Test CU* turns the extra pairs on one at a time under vkpeak and reports errors, for the silicon lottery.
- **VRAM**: the UMA split in the CMOS, applied at the next boot. With the 512 MB dynamic split some games pick low textures: if they look blurry, try 4 or 6 GB fixed. Anything from 512 MB to 12 GB, with presets at 512 MB, 1, 2, 4, 6 and 8 GB.
- **Advanced**: the governor's own knobs: ascent margin, step, descent confirmations, thermal and power thresholds, droop.
- **Test**: vkpeak and the helper log.""",
    monitor_t="## Monitor",
    monitor="One chart per quantity, each with its own true scale: temperatures (CPU, GPU, VRM, system, NVMe), clocks (CPU average, min, max, GPU and its ceiling), load, power, voltages, fan and memory (RAM, VRAM, GTT), plus one bar per thread. Click a legend entry to hide a line; hover to read every chart at the same instant. REC writes a `.sfmon` file (CSV) that Open reloads with a scrubber; CSV exports it for a spreadsheet.",
    giochi_t="## Games",
    giochi="""- **Vulkan driver**: our Mesa opens the compute queues the stock driver keeps closed on this GPU: +4% in Cyberpunk 2077, +12% with FSR 4 on. Per launcher (Steam, Heroic) through a flatpak override, or for the whole system. It needs the SkillFishOS kernel: on another kernel those queues wedge the GPU, and the system-wide switch refuses to start there. The card shows the kernel that is running.
- **Scheduler**: scx_bpfland, loaded only while a game runs (GameMode raises it at launch and drops it at exit): +1.5-2% in Cyberpunk and steadier frames. If the kernel ejects it twice the service stops until you reset the counter: that is the "Ejected by the kernel" row.
- **FSR 4**: through OptiScaler on the game's DLSS path. GE-Proton 11 downloads OptiScaler by itself when it finds `PROTON_USE_OPTISCALER=1`, the game must be set to DLSS, and AMD's FSR 4 library (`amdxcffx64.dll`, from AMD's Windows driver) goes next to the game. XeSS, where a game has it built in, costs the same as FSR 3 at 1080p.
- **Proton**: the GE-Proton 11 releases; Install downloads one (about 500 MB) into the Steam and Heroic folders, Default picks it. Steam must be closed for its default to be written.""",
    ai_t='## AI',
    ai="""The engine is **Unsloth Studio**: it runs GGUF models through llama.cpp on the **Vulkan** backend, which on the BC-250's gfx1013 is the only accelerated path, because ROCm does not support it. Measured on the board with Qwen3-1.7B Q4_K_M: 210 tokens per second against 41 on the CPU alone.

- **Engine**: on, off, at boot. On, it holds GPU memory, so turn it off before gaming. Beside it sit the version, the update check and *Update*, which reruns the official installer with the Vulkan bundle of llama.cpp.
- **Access**: Unsloth generates a random password when it installs, and shuts itself down after an hour if that password is not changed. The first sign-in happens here: choose the Studio password and the API key is created with it, and shared with the Remote Manager.
- **Models**: the ones on disk with quantization and size. To download one you need the repository name on Hugging Face (for example `unsloth/Qwen3-4B-GGUF`) and the variant picked from the list, sizes included.
- **Chat**: a quick run over the OpenAI-compatible API (`http://127.0.0.1:8888/v1`), with the measured tokens per second. The full chat, with files and search, is inside Studio.
- **Memory**: VRAM, GTT, RAM, swap and the model budget. The GTT limit is a kernel parameter: it takes effect at the next boot.
- **Network**: open on the local network, Studio answers the other devices at home too, with its own user and password. Parallel chats are llama-server's slots.""",
    fine_t="## Fan, profiles and the rest",
    fine="The **Fan** page draws the curve inside the chart of the sensors: at this temperature the fan turns like this, with a lead so the speed rises before the temperature does. **Profiles** move the ceiling within the curve that is already there and set CPU, fan preset and scheduler together. **Snapshots** are pictures of the system, your files are not touched. **AI** holds GPU memory while on: turn it off before gaming. **Console** starts Steam Big Picture inside gamescope on top of the desktop, or as a session from the login screen. The **Remote Manager** mirrors the Tuner, Games and Profiles pages in a browser."),
"it": dict(
    title="Control Center", desc="Tutti gli strumenti di SkillFishOS in una finestra: Tuner, Ventola, Monitor, Giochi, Profili, Kernel, Snapshot, AI, Emulatori, Console, ISO.",
    intro="Tutti gli strumenti di SkillFishOS stanno in una finestra. Si apre dal menu (SkillFishOS → Control Center) o con `skillfish-control-center`. Si guida anche col controller: croce o levetta per muoversi, A conferma, B torna indietro, LB e RB cambiano sezione.",
    sezioni="## Le sezioni",
    voci=[("Stato", "un numero per scheda: frequenza e tetto della GPU, CPU, unità di calcolo, ventola, kernel, governor, driver Vulkan, se l'ultimo avvio è seguito a uno spegnimento pulito. Qui non si imposta niente."),
          ("Tuner", "la curva tensione/frequenza del governor della GPU, la CPU, i core, le unità di calcolo, la VRAM."),
          ("Ventola", "la curva della ventola con l'anticipo, i sensori sorgente, i limiti di sicurezza, la prova del PWM."),
          ("Monitor", "tutte le letture, un grafico per unità, più le barre di frequenza per thread. REC registra, CSV esporta."),
          ("Giochi", "la nostra Mesa per lanciatore o per tutto il sistema, lo schedulatore scx_bpfland, FSR 4, installazione e predefinita di GE-Proton."),
          ("Profili", "tetto, CPU, ventola e schedulatore in un clic; salva i tuoi."),
          ("Kernel", "i kernel installati, quello predefinito, avvia una volta, disinstalla."),
          ("Snapshot", "le fotografie del sistema e la manutenzione btrfs programmata."),
          ("AI", "Unsloth Studio su Vulkan: motore, aggiornamento, modelli dall'Hub di Hugging Face, chat di prova, memoria e rete."),
          ("Emulatori", "EmuDeck, oppure gli emulatori uno per uno da Flathub."),
          ("Console", "Steam Big Picture dentro gamescope, adesso o dalla schermata di accesso."),
          ("ISO", "immagini disco montate attraverso udisks.")],
    tuner_t="## Tuner",
    tuner="""La curva è il grafico: MHz in orizzontale, millivolt in verticale. Trascina un punto, doppio clic per aggiungerne uno, tasto destro per toglierlo, oppure scrivi i numeri nella tabella accanto al grafico (+ e − aggiungono e tolgono punti). La riga tratteggiata verticale è il tetto, il pallino azzurro è la GPU adesso. Tre preset: **Cautious 1850** (il punto dolce col dissipatore di serie, quasi gli stessi fotogrammi e dieci gradi in meno), **Balanced 2000**, **Performance 2100** (la curva a quindici punti misurata sulla scheda di sviluppo, quella che spediamo).

**Applica è una prova.** Una curva che chiede troppo poca tensione pianta la scheda, e sulla BC-250 un blocco si risolve staccando la corrente. Perciò Applica fa partire la candidata con la curva di prima ancora su disco e conta 25 secondi: premi Tieni e la candidata viene scritta per davvero; non fai niente, o la scheda muore e riparte, e all'avvio torna la curva di prima.

I pannelli si aprono quando servono:

- **CPU**: frequenza, scalino di undervolt (6,25 mV l'uno) e limite termico, ognuno con un cursore e una casella numerica a passo 1. *Suggerisci UV* scende di due scalini alla volta con dodici secondi di carico per scalino; *Trova il massimo* sale da 3600 a 4000 MHz; *Test 60 s* carica i valori attuali. Ogni prova mostra un conto alla rovescia e un bottone Stop; i valori in prova non vengono mai scritti su disco, quindi un blocco riavvia con quelli di prima. Sopra i 3500 MHz con otto core il guadagno è zero: comanda il calore.
- **Core**: quali core sono attivi, SMT, lo sblocco degli 8 core (6c/12t diventa 8c/16t, +20% misurato) e *Prima dell'avvio (EFI)*: lo sblocco fatto prima di GRUB in un avvio solo, invece del riavvio in più del servizio dentro al sistema.
- **CU**: le 40 unità di calcolo come 20 caselle (coppie): verde accesa, rossa spenta, grigia tenuta accesa dal driver. Scrivi quante CU vuoi (da 24 a 40, a coppie) o clicca le caselle; *Test CU* accende le coppie extra una alla volta sotto vkpeak e riporta gli errori, per la lotteria del silicio.
- **VRAM**: la quota UMA nel CMOS, applicata al prossimo avvio. Con i 512 MB dinamici alcuni giochi scelgono texture basse: se sono sfocate, prova 4 o 6 GB fissi. Va da 512 MB a 12 GB, con i preset 512 MB, 1, 2, 4, 6 e 8 GB.
- **Avanzate**: le manopole del governor: margine in salita, gradino, conferme in discesa, soglie termiche e di potenza, droop.
- **Test**: vkpeak e il registro dell'helper.""",
    monitor_t="## Monitor",
    monitor="Un grafico per grandezza, ognuno con la sua scala vera: temperature (CPU, GPU, VRM, sistema, NVMe), frequenze (CPU media, minima, massima, GPU e il suo tetto), carico, potenza, tensioni, ventola e memoria (RAM, VRAM, GTT), più una barra per thread. Clic su una voce della legenda per nascondere una linea; passa il mouse per leggere tutti i grafici nello stesso istante. REC scrive un file `.sfmon` (CSV) che Apri ricarica con uno scrubber; CSV lo esporta per un foglio di calcolo.",
    giochi_t="## Giochi",
    giochi="""- **Driver Vulkan**: la nostra Mesa apre le code compute che il driver di serie tiene chiuse su questa GPU: +4% in Cyberpunk 2077, +12% con FSR 4 acceso. Per lanciatore (Steam, Heroic) con un override flatpak, o per tutto il sistema. Serve il kernel di SkillFishOS: su un altro kernel quelle code piantano la GPU, e l'interruttore di sistema si rifiuta di partire. La scheda mostra il kernel in esecuzione.
- **Schedulatore**: scx_bpfland, caricato solo mentre gira un gioco (lo alza GameMode all'avvio e lo toglie alla chiusura): +1,5-2% in Cyberpunk e fotogrammi più regolari. Se il kernel lo espelle due volte il servizio si ferma finché non azzeri il contatore: è la riga «Espulso dal kernel».
- **FSR 4**: attraverso OptiScaler sul percorso DLSS del gioco. GE-Proton 11 scarica OptiScaler da solo quando trova `PROTON_USE_OPTISCALER=1`, il gioco va messo su DLSS, e la libreria FSR 4 di AMD (`amdxcffx64.dll`, dal driver Windows di AMD) va accanto al gioco. XeSS, dove un gioco ce l'ha di suo, costa quanto FSR 3 a 1080p.
- **Proton**: le versioni GE-Proton 11; Installa ne scarica una (circa 500 MB) nelle cartelle di Steam e Heroic, Predefinita la sceglie. Steam va chiuso perché la sua predefinita venga scritta.""",
    ai_t='## AI',
    ai="""Il motore è **Unsloth Studio**: fa girare i modelli GGUF con llama.cpp sul backend **Vulkan**, che sulla gfx1013 della BC-250 è l'unica strada accelerata, perché ROCm non la supporta. Misurato sulla scheda con Qwen3-1.7B Q4_K_M: 210 token al secondo contro i 41 della sola CPU.

- **Motore**: acceso, spento, all'avvio. Acceso tiene la memoria della GPU, quindi si spegne prima di giocare. Accanto stanno la versione, il controllo degli aggiornamenti e *Aggiorna*, che rilancia l'installatore ufficiale con il pacchetto Vulkan di llama.cpp.
- **Accesso**: Unsloth genera una password a caso quando si installa, e si spegne da solo dopo un'ora se non viene cambiata. Il primo accesso si fa da qui: scegli la password di Studio e la chiave API viene creata insieme, e condivisa con il Remote Manager.
- **Modelli**: quelli sul disco con quantizzazione e dimensione. Per scaricarne uno serve il nome del repository su Hugging Face (per esempio `unsloth/Qwen3-4B-GGUF`) e la variante scelta dall'elenco, che riporta le dimensioni.
- **Chat**: una prova rapida sull'API compatibile OpenAI (`http://127.0.0.1:8888/v1`), con i token al secondo misurati. La chat completa, con i file e la ricerca, è dentro Studio.
- **Memoria**: VRAM, GTT, RAM, swap e il budget del modello. Il limite del GTT è un parametro del kernel: vale dal riavvio.
- **Rete**: aperto sulla rete locale, Studio risponde anche agli altri dispositivi di casa, con il suo utente e la sua password. Le chat in parallelo sono i posti di llama-server.""",
    fine_t="## Ventola, profili e il resto",
    fine="La pagina **Ventola** disegna la curva dentro il grafico dei sensori: a questa temperatura la ventola gira così, con un anticipo perché la velocità salga prima della temperatura. I **Profili** spostano il tetto dentro alla curva che c'è già e impostano insieme CPU, preset della ventola e schedulatore. Gli **Snapshot** sono fotografie del sistema, i tuoi file non vengono toccati. **AI** tiene la memoria della GPU finché è acceso: spegnilo prima di giocare. **Console** avvia Steam Big Picture dentro gamescope sopra al desktop, o come sessione dalla schermata di accesso. Il **Remote Manager** replica le pagine Tuner, Giochi e Profili in un browser."),
}

# the other seven languages: same structure, translated
T["de"] = dict(
    title="Control Center", desc="Alle SkillFishOS-Werkzeuge in einem Fenster: Tuner, Lüfter, Monitor, Spiele, Profile, Kernel, Snapshots, KI, Emulatoren, Konsole, ISO.",
    intro="Alle SkillFishOS-Werkzeuge stecken in einem Fenster. Es öffnet sich über das Menü (SkillFishOS → Control Center) oder mit `skillfish-control-center`. Auch ein Controller bedient es: Steuerkreuz oder Stick zum Bewegen, A bestätigt, B geht zurück, LB und RB wechseln den Bereich.",
    sezioni="## Die Bereiche",
    voci=[("Status", "eine Zahl pro Karte: GPU-Takt und Obergrenze, CPU, Recheneinheiten, Lüfter, Kernel, Governor, Vulkan-Treiber, ob der letzte Start nach einem sauberen Herunterfahren kam. Hier wird nichts eingestellt."),
          ("Tuner", "die Spannungs-/Frequenzkurve des GPU-Governors, die CPU, die Kerne, die Recheneinheiten, der VRAM-Anteil."),
          ("Lüfter", "die Lüfterkurve mit Vorlauf, die Quellsensoren, die Sicherheitsgrenzen, der PWM-Test."),
          ("Monitor", "jeder Messwert in einem Diagramm pro Einheit, dazu die Taktbalken pro Thread. REC zeichnet auf, CSV exportiert."),
          ("Spiele", "unsere Mesa pro Launcher oder systemweit, der Scheduler scx_bpfland, FSR 4, GE-Proton installieren und als Standard setzen."),
          ("Profile", "Obergrenze, CPU, Lüfter und Scheduler mit einem Klick; eigene speichern."),
          ("Kernel", "die installierten Kernel, der Standard, einmal starten, deinstallieren."),
          ("Snapshots", "System-Snapshots und der btrfs-Wartungsplan."),
          ("KI", "Unsloth Studio über Vulkan: Motor, Aktualisierung, Modelle aus dem Hugging-Face-Hub, Chat-Test, Speicher und Netz."),
          ("Emulatoren", "EmuDeck oder die Emulatoren einzeln aus Flathub."),
          ("Konsole", "Steam Big Picture in gamescope, jetzt oder vom Anmeldebildschirm."),
          ("ISO", "Datenträgerabbilder, über udisks eingehängt.")],
    tuner_t="## Tuner",
    tuner="""Die Kurve ist das Diagramm: MHz waagerecht, Millivolt senkrecht. Einen Punkt ziehen, Doppelklick fügt einen hinzu, Rechtsklick entfernt ihn, oder die Zahlen in die Tabelle neben dem Diagramm tippen (+ und − fügen Punkte hinzu und entfernen sie). Die gestrichelte senkrechte Linie ist die Obergrenze, der blaue Punkt die GPU im Moment. Drei Presets: **Cautious 1850** (der beste Punkt mit dem Serienkühler, fast dieselben Bilder und zehn Grad weniger), **Balanced 2000**, **Performance 2100** (die auf der Entwicklungskarte gemessene Kurve mit fünfzehn Punkten, die wir ausliefern).

**Anwenden ist eine Probe.** Eine Kurve mit zu wenig Spannung hängt die Karte auf, und auf der BC-250 hilft dann nur der Stecker. Deshalb startet Anwenden die Kandidatin, während die vorherige Kurve auf der Platte bleibt, und zählt 25 Sekunden herunter: Behalten drücken, und die Kandidatin wird endgültig geschrieben; nichts tun, oder die Karte stirbt und kommt zurück, und die vorherige Kurve startet.

Die Bereiche öffnen sich bei Bedarf:

- **CPU**: Takt, Undervolt-Stufe (je 6,25 mV) und Temperaturgrenze, jeweils mit Schieber und Zahlenfeld in Schritt 1. *UV vorschlagen* geht den Undervolt in Zweierschritten mit zwölf Sekunden Last pro Stufe hinunter; *Mein Maximum* klettert von 3600 auf 4000 MHz; *Test 60 s* belastet die aktuellen Werte. Jeder Lauf zeigt einen Countdown und einen Stop-Knopf; die getesteten Werte landen nie auf der Platte, ein Hänger startet also mit den vorherigen. Über 3500 MHz mit acht Kernen bringt nichts: die Hitze hat das Sagen.
- **Kerne**: welche Kerne aktiv sind, SMT, die 8-Kern-Freischaltung (aus 6c/12t wird 8c/16t, +20 % gemessen) und *Vor dem Start (EFI)*: die Freischaltung vor GRUB in einem einzigen Start statt des zusätzlichen Neustarts des Dienstes im System.
- **CU**: die 40 Recheneinheiten als 20 Zellen (Paare): grün an, rot aus, grau vom Treiber gehalten. Die gewünschte Anzahl eintippen (24 bis 40, paarweise) oder die Zellen anklicken; *Test CU* schaltet die zusätzlichen Paare einzeln unter vkpeak ein und meldet Fehler, für die Silizium-Lotterie.
- **VRAM**: der UMA-Anteil im CMOS, gültig ab dem nächsten Start. Mit der dynamischen 512-MB-Aufteilung wählen manche Spiele niedrige Texturen: wirken sie unscharf, 4 oder 6 GB fest probieren. Von 512 MB bis 12 GB, mit den Vorgaben 512 MB, 1, 2, 4, 6 und 8 GB.
- **Erweitert**: die Regler des Governors: Aufstiegsmarge, Stufe, Abstiegsbestätigungen, Temperatur- und Leistungsschwellen, Droop.
- **Test**: vkpeak und das Helper-Protokoll.""",
    monitor_t="## Monitor",
    monitor="Ein Diagramm pro Größe, jedes mit echter Skala: Temperaturen (CPU, GPU, VRM, System, NVMe), Takte (CPU-Mittel, Minimum, Maximum, GPU und ihre Obergrenze), Last, Leistung, Spannungen, Lüfter und Speicher (RAM, VRAM, GTT), dazu ein Balken pro Thread. Klick auf einen Legendeneintrag blendet eine Linie aus; mit der Maus liest man alle Diagramme im selben Augenblick. REC schreibt eine `.sfmon`-Datei (CSV), die Öffnen mit einem Schieber wieder lädt; CSV exportiert sie für eine Tabellenkalkulation.",
    giochi_t="## Spiele",
    giochi="""- **Vulkan-Treiber**: unsere Mesa öffnet die Compute-Warteschlangen, die der Serientreiber auf dieser GPU geschlossen hält: +4 % in Cyberpunk 2077, +12 % mit FSR 4. Pro Launcher (Steam, Heroic) über einen Flatpak-Override oder systemweit. Braucht den SkillFishOS-Kernel: auf einem anderen Kernel blockieren diese Warteschlangen die GPU, und der Systemschalter startet dort nicht. Die Karte zeigt den laufenden Kernel.
- **Scheduler**: scx_bpfland, nur geladen, solange ein Spiel läuft (GameMode startet ihn und beendet ihn wieder): +1,5-2 % in Cyberpunk und gleichmäßigere Bilder. Wirft der Kernel ihn zweimal hinaus, hält der Dienst an, bis der Zähler zurückgesetzt wird: das ist die Zeile „Vom Kernel hinausgeworfen“.
- **FSR 4**: über OptiScaler auf dem DLSS-Pfad des Spiels. GE-Proton 11 lädt OptiScaler selbst, wenn es `PROTON_USE_OPTISCALER=1` findet, das Spiel muss auf DLSS stehen, und AMDs FSR-4-Bibliothek (`amdxcffx64.dll`, aus AMDs Windows-Treiber) kommt neben das Spiel. XeSS, wo ein Spiel es eingebaut hat, kostet bei 1080p so viel wie FSR 3.
- **Proton**: die GE-Proton-11-Versionen; Installieren lädt eine (etwa 500 MB) in die Ordner von Steam und Heroic, Standard wählt sie. Steam muss geschlossen sein, damit sein Standard geschrieben wird.""",
    ai_t='## KI',
    ai="""Der Motor ist **Unsloth Studio**: er führt GGUF-Modelle mit llama.cpp über das **Vulkan**-Backend aus, das auf der gfx1013 der BC-250 der einzige beschleunigte Weg ist, denn ROCm unterstützt sie nicht. Auf der Platine mit Qwen3-1.7B Q4_K_M gemessen: 210 Token pro Sekunde gegenüber 41 auf der CPU allein.

- **Motor**: an, aus, beim Systemstart. Eingeschaltet belegt er GPU-Speicher, vor dem Spielen also ausschalten. Daneben stehen die Version, die Aktualisierungsprüfung und *Aktualisieren*, das den offiziellen Installer mit dem Vulkan-Paket von llama.cpp erneut ausführt.
- **Zugang**: Unsloth erzeugt bei der Installation ein zufälliges Passwort und schaltet sich nach einer Stunde selbst ab, wenn es nicht geändert wird. Die erste Anmeldung geschieht hier: du wählst das Studio-Passwort, der API-Schlüssel entsteht dabei und wird mit dem Remote Manager geteilt.
- **Modelle**: die auf der Platte, mit Quantisierung und Größe. Zum Herunterladen brauchst du den Namen des Repositorys auf Hugging Face (zum Beispiel `unsloth/Qwen3-4B-GGUF`) und die Variante aus der Liste, Größen inklusive.
- **Chat**: ein schneller Lauf über die OpenAI-kompatible API (`http://127.0.0.1:8888/v1`), mit den gemessenen Token pro Sekunde. Der volle Chat, mit Dateien und Suche, steckt in Studio.
- **Speicher**: VRAM, GTT, RAM, Swap und das Budget des Modells. Die GTT-Grenze ist ein Kernel-Parameter: sie gilt ab dem nächsten Start.
- **Netz**: im lokalen Netz geöffnet antwortet Studio auch den anderen Geräten zu Hause, mit eigenem Benutzer und Passwort. Parallele Chats sind die Slots von llama-server.""",
    fine_t="## Lüfter, Profile und der Rest",
    fine="Die Seite **Lüfter** zeichnet die Kurve ins Diagramm der Sensoren: bei dieser Temperatur dreht der Lüfter so, mit Vorlauf, damit die Drehzahl vor der Temperatur steigt. **Profile** verschieben die Obergrenze innerhalb der vorhandenen Kurve und setzen CPU, Lüfter-Preset und Scheduler zusammen. **Snapshots** sind Aufnahmen des Systems, die eigenen Dateien bleiben unberührt. **KI** hält GPU-Speicher, solange es an ist: vor dem Spielen ausschalten. **Konsole** startet Steam Big Picture in gamescope über dem Desktop oder als Sitzung vom Anmeldebildschirm. Der **Remote Manager** spiegelt Tuner, Spiele und Profile im Browser.")

T["fr"] = dict(
    title="Control Center", desc="Tous les outils SkillFishOS dans une fenêtre : Tuner, Ventilateur, Moniteur, Jeux, Profils, Noyau, Instantanés, IA, Émulateurs, Console, ISO.",
    intro="Tous les outils SkillFishOS tiennent dans une fenêtre. Elle s'ouvre depuis le menu (SkillFishOS → Control Center) ou avec `skillfish-control-center`. Une manette la pilote aussi : croix ou stick pour se déplacer, A confirme, B revient, LB et RB changent de section.",
    sezioni="## Les sections",
    voci=[("État", "un chiffre par carte : fréquence et plafond du GPU, CPU, unités de calcul, ventilateur, noyau, governor, pilote Vulkan, si le dernier démarrage a suivi un arrêt propre. Rien ne se règle ici."),
          ("Tuner", "la courbe tension/fréquence du governor du GPU, le CPU, les cœurs, les unités de calcul, la VRAM."),
          ("Ventilateur", "la courbe du ventilateur avec son avance, les capteurs sources, les limites de sécurité, le test PWM."),
          ("Moniteur", "toutes les mesures, un graphique par unité, plus les barres de fréquence par thread. REC enregistre, CSV exporte."),
          ("Jeux", "notre Mesa par lanceur ou pour tout le système, l'ordonnanceur scx_bpfland, FSR 4, installation et défaut de GE-Proton."),
          ("Profils", "plafond, CPU, ventilateur et ordonnanceur en un clic ; enregistrez les vôtres."),
          ("Noyau", "les noyaux installés, celui par défaut, démarrer une fois, désinstaller."),
          ("Instantanés", "les instantanés du système et l'entretien btrfs planifié."),
          ("IA", "Unsloth Studio sur Vulkan : moteur, mise à jour, modèles depuis le Hub Hugging Face, essai de chat, mémoire et réseau."),
          ("Émulateurs", "EmuDeck, ou les émulateurs un par un depuis Flathub."),
          ("Console", "Steam Big Picture dans gamescope, maintenant ou depuis l'écran de connexion."),
          ("ISO", "images disque montées via udisks.")],
    tuner_t="## Tuner",
    tuner="""La courbe est le graphique : MHz en abscisse, millivolts en ordonnée. Glissez un point, double-clic pour en ajouter un, clic droit pour le retirer, ou tapez les nombres dans le tableau à côté du graphique (+ et − ajoutent et retirent des points). La ligne verticale en pointillés est le plafond, le point bleu est le GPU à l'instant. Trois presets : **Cautious 1850** (le point idéal avec le dissipateur d'origine, presque les mêmes images et dix degrés de moins), **Balanced 2000**, **Performance 2100** (la courbe à quinze points mesurée sur la carte de développement, celle que nous livrons).

**Appliquer est un essai.** Une courbe qui demande trop peu de tension bloque la carte, et sur la BC-250 un blocage se règle en débranchant. Appliquer lance donc la candidate en gardant l'ancienne courbe sur le disque et compte 25 secondes : appuyez sur Garder et la candidate est écrite pour de bon ; ne faites rien, ou la carte meurt et revient, et c'est l'ancienne courbe qui démarre.

Les panneaux s'ouvrent à la demande :

- **CPU** : fréquence, palier d'undervolt (6,25 mV chacun) et limite thermique, chacun avec un curseur et un champ numérique au pas de 1. *Suggérer UV* descend l'undervolt de deux paliers à la fois avec douze secondes de charge par palier ; *Trouver mon max* monte de 3600 à 4000 MHz ; *Test 60 s* charge les valeurs actuelles. Chaque essai affiche un compte à rebours et un bouton Stop ; les valeurs testées ne sont jamais écrites sur le disque, un blocage redémarre donc avec les précédentes. Au-dessus de 3500 MHz avec huit cœurs le gain est nul : c'est la chaleur qui commande.
- **Cœurs** : quels cœurs sont actifs, le SMT, le déblocage des 8 cœurs (6c/12t devient 8c/16t, +20 % mesuré) et *Avant le démarrage (EFI)* : le déblocage fait avant GRUB en un seul démarrage, au lieu du redémarrage supplémentaire du service dans le système.
- **CU** : les 40 unités de calcul en 20 cases (paires) : vert allumé, rouge éteint, gris gardé allumé par le pilote. Tapez le nombre de CU voulu (24 à 40, par paires) ou cliquez les cases ; *Test CU* allume les paires supplémentaires une à une sous vkpeak et signale les erreurs, pour la loterie du silicium.
- **VRAM** : le partage UMA dans la CMOS, appliqué au prochain démarrage. Avec les 512 Mo dynamiques certains jeux choisissent des textures basses : si elles sont floues, essayez 4 ou 6 Go fixes. De 512 Mo à 12 Go, avec les préréglages 512 Mo, 1, 2, 4, 6 et 8 Go.
- **Avancé** : les réglages propres du governor : marge en montée, pas, confirmations en descente, seuils thermiques et de puissance, droop.
- **Test** : vkpeak et le journal de l'assistant.""",
    monitor_t="## Moniteur",
    monitor="Un graphique par grandeur, chacun avec sa vraie échelle : températures (CPU, GPU, VRM, système, NVMe), fréquences (CPU moyenne, min, max, GPU et son plafond), charge, puissance, tensions, ventilateur et mémoire (RAM, VRAM, GTT), plus une barre par thread. Cliquez sur une entrée de la légende pour masquer une ligne ; survolez pour lire tous les graphiques au même instant. REC écrit un fichier `.sfmon` (CSV) qu'Ouvrir recharge avec un curseur ; CSV l'exporte pour un tableur.",
    giochi_t="## Jeux",
    giochi="""- **Pilote Vulkan** : notre Mesa ouvre les files de calcul que le pilote d'origine garde fermées sur ce GPU : +4 % dans Cyberpunk 2077, +12 % avec FSR 4. Par lanceur (Steam, Heroic) via un override flatpak, ou pour tout le système. Il faut le noyau SkillFishOS : sur un autre noyau ces files bloquent le GPU, et l'interrupteur système refuse d'y démarrer. La carte affiche le noyau en cours.
- **Ordonnanceur** : scx_bpfland, chargé seulement pendant qu'un jeu tourne (GameMode le lance et l'arrête) : +1,5-2 % dans Cyberpunk et des images plus régulières. Si le noyau l'éjecte deux fois, le service s'arrête jusqu'à la remise à zéro du compteur : c'est la ligne « Éjecté par le noyau ».
- **FSR 4** : via OptiScaler sur le chemin DLSS du jeu. GE-Proton 11 télécharge OptiScaler tout seul quand il trouve `PROTON_USE_OPTISCALER=1`, le jeu doit être réglé sur DLSS, et la bibliothèque FSR 4 d'AMD (`amdxcffx64.dll`, du pilote Windows d'AMD) va à côté du jeu. XeSS, quand un jeu l'intègre, coûte autant que FSR 3 en 1080p.
- **Proton** : les versions GE-Proton 11 ; Installer en télécharge une (environ 500 Mo) dans les dossiers de Steam et Heroic, Par défaut la choisit. Steam doit être fermé pour que son défaut soit écrit.""",
    ai_t='## IA',
    ai="""Le moteur est **Unsloth Studio** : il fait tourner les modèles GGUF avec llama.cpp sur le backend **Vulkan**, qui sur le gfx1013 de la BC-250 est la seule voie accélérée, car ROCm ne le prend pas en charge. Mesuré sur la carte avec Qwen3-1.7B Q4_K_M : 210 tokens par seconde contre 41 sur le seul CPU.

- **Moteur** : allumé, éteint, au démarrage. Allumé, il garde la mémoire du GPU : éteins-le avant de jouer. À côté se trouvent la version, la vérification des mises à jour et *Mettre à jour*, qui relance l'installateur officiel avec le paquet Vulkan de llama.cpp.
- **Accès** : Unsloth génère un mot de passe au hasard à l'installation, et s'éteint tout seul au bout d'une heure s'il n'est pas changé. La première connexion se fait ici : tu choisis le mot de passe de Studio, la clé API est créée en même temps et partagée avec le Remote Manager.
- **Modèles** : ceux qui sont sur le disque, avec quantification et taille. Pour en télécharger un, il faut le nom du dépôt sur Hugging Face (par exemple `unsloth/Qwen3-4B-GGUF`) et la variante choisie dans la liste, tailles comprises.
- **Chat** : un essai rapide sur l'API compatible OpenAI (`http://127.0.0.1:8888/v1`), avec les tokens par seconde mesurés. Le chat complet, avec les fichiers et la recherche, est dans Studio.
- **Mémoire** : VRAM, GTT, RAM, swap et le budget du modèle. La limite du GTT est un paramètre du noyau : elle s'applique au redémarrage.
- **Réseau** : ouvert sur le réseau local, Studio répond aussi aux autres appareils de la maison, avec son propre utilisateur et mot de passe. Les chats en parallèle sont les slots de llama-server.""",
    fine_t="## Ventilateur, profils et le reste",
    fine="La page **Ventilateur** dessine la courbe dans le graphique des capteurs : à cette température le ventilateur tourne ainsi, avec une avance pour que la vitesse monte avant la température. Les **Profils** déplacent le plafond dans la courbe déjà en place et règlent ensemble CPU, preset du ventilateur et ordonnanceur. Les **Instantanés** sont des photos du système, vos fichiers ne sont pas touchés. **IA** garde la mémoire du GPU tant qu'elle est allumée : éteignez-la avant de jouer. **Console** lance Steam Big Picture dans gamescope par-dessus le bureau, ou comme session depuis l'écran de connexion. Le **Remote Manager** reprend les pages Tuner, Jeux et Profils dans un navigateur.")

T["es"] = dict(
    title="Control Center", desc="Todas las herramientas de SkillFishOS en una ventana: Tuner, Ventilador, Monitor, Juegos, Perfiles, Kernel, Instantáneas, IA, Emuladores, Consola, ISO.",
    intro="Todas las herramientas de SkillFishOS están en una ventana. Se abre desde el menú (SkillFishOS → Control Center) o con `skillfish-control-center`. También se maneja con el mando: cruceta o palanca para moverse, A confirma, B vuelve atrás, LB y RB cambian de sección.",
    sezioni="## Las secciones",
    voci=[("Estado", "un número por tarjeta: frecuencia y techo de la GPU, CPU, unidades de cálculo, ventilador, kernel, governor, driver Vulkan, si el último arranque siguió a un apagado limpio. Aquí no se ajusta nada."),
          ("Tuner", "la curva tensión/frecuencia del governor de la GPU, la CPU, los núcleos, las unidades de cálculo, la VRAM."),
          ("Ventilador", "la curva del ventilador con su adelanto, los sensores fuente, los límites de seguridad, la prueba PWM."),
          ("Monitor", "todas las lecturas, un gráfico por unidad, más las barras de frecuencia por hilo. REC graba, CSV exporta."),
          ("Juegos", "nuestra Mesa por lanzador o para todo el sistema, el planificador scx_bpfland, FSR 4, instalación y predeterminado de GE-Proton."),
          ("Perfiles", "techo, CPU, ventilador y planificador en un clic; guarda los tuyos."),
          ("Kernel", "los kernels instalados, el predeterminado, arrancar una vez, desinstalar."),
          ("Instantáneas", "las instantáneas del sistema y el mantenimiento btrfs programado."),
          ("IA", "Unsloth Studio sobre Vulkan: motor, actualización, modelos del Hub de Hugging Face, prueba de chat, memoria y red."),
          ("Emuladores", "EmuDeck, o los emuladores uno a uno desde Flathub."),
          ("Consola", "Steam Big Picture dentro de gamescope, ahora o desde la pantalla de inicio de sesión."),
          ("ISO", "imágenes de disco montadas a través de udisks.")],
    tuner_t="## Tuner",
    tuner="""La curva es el gráfico: MHz en horizontal, milivoltios en vertical. Arrastra un punto, doble clic para añadir uno, clic derecho para quitarlo, o escribe los números en la tabla junto al gráfico (+ y − añaden y quitan puntos). La línea vertical discontinua es el techo, el punto azul es la GPU ahora mismo. Tres presets: **Cautious 1850** (el punto dulce con el disipador de serie, casi los mismos fotogramas y diez grados menos), **Balanced 2000**, **Performance 2100** (la curva de quince puntos medida en la placa de desarrollo, la que enviamos).

**Aplicar es una prueba.** Una curva que pide muy poca tensión cuelga la placa, y en la BC-250 un cuelgue se arregla desenchufando. Por eso Aplicar arranca la candidata con la curva anterior todavía en disco y cuenta 25 segundos: pulsa Mantener y la candidata se escribe de verdad; no hagas nada, o la placa muere y vuelve, y arranca la curva anterior.

Los paneles se abren cuando hacen falta:

- **CPU**: frecuencia, escalón de undervolt (6,25 mV cada uno) y límite térmico, cada uno con un deslizador y una casilla numérica de paso 1. *Sugerir UV* baja el undervolt de dos en dos escalones con doce segundos de carga por escalón; *Buscar mi máximo* sube de 3600 a 4000 MHz; *Test 60 s* carga los valores actuales. Cada prueba muestra una cuenta atrás y un botón Stop; los valores en prueba nunca se escriben en disco, así que un cuelgue arranca con los anteriores. Por encima de 3500 MHz con ocho núcleos la ganancia es nula: manda el calor.
- **Núcleos**: qué núcleos están activos, SMT, el desbloqueo de los 8 núcleos (6c/12t pasa a 8c/16t, +20 % medido) y *Antes del arranque (EFI)*: el desbloqueo hecho antes de GRUB en un solo arranque, en vez del reinicio extra del servicio dentro del sistema.
- **CU**: las 40 unidades de cálculo como 20 celdas (pares): verde encendida, roja apagada, gris mantenida encendida por el driver. Escribe cuántas CU quieres (de 24 a 40, en pares) o pulsa las celdas; *Test CU* enciende los pares extra uno a uno bajo vkpeak e informa de errores, para la lotería del silicio.
- **VRAM**: el reparto UMA en la CMOS, aplicado en el próximo arranque. Con los 512 MB dinámicos algunos juegos eligen texturas bajas: si se ven borrosas, prueba 4 o 6 GB fijos. De 512 MB a 12 GB, con los preajustes 512 MB, 1, 2, 4, 6 y 8 GB.
- **Avanzado**: los mandos propios del governor: margen en subida, escalón, confirmaciones en bajada, umbrales térmicos y de potencia, droop.
- **Test**: vkpeak y el registro del asistente.""",
    monitor_t="## Monitor",
    monitor="Un gráfico por magnitud, cada uno con su escala real: temperaturas (CPU, GPU, VRM, sistema, NVMe), frecuencias (CPU media, mínima, máxima, GPU y su techo), carga, potencia, tensiones, ventilador y memoria (RAM, VRAM, GTT), más una barra por hilo. Clic en una entrada de la leyenda para ocultar una línea; pasa el ratón para leer todos los gráficos en el mismo instante. REC escribe un archivo `.sfmon` (CSV) que Abrir recarga con un deslizador; CSV lo exporta para una hoja de cálculo.",
    giochi_t="## Juegos",
    giochi="""- **Driver Vulkan**: nuestra Mesa abre las colas de cómputo que el driver de serie mantiene cerradas en esta GPU: +4 % en Cyberpunk 2077, +12 % con FSR 4. Por lanzador (Steam, Heroic) con un override flatpak, o para todo el sistema. Necesita el kernel de SkillFishOS: en otro kernel esas colas cuelgan la GPU, y el interruptor de sistema se niega a arrancar ahí. La tarjeta muestra el kernel en ejecución.
- **Planificador**: scx_bpfland, cargado solo mientras corre un juego (GameMode lo levanta y lo retira): +1,5-2 % en Cyberpunk y fotogramas más regulares. Si el kernel lo expulsa dos veces, el servicio se para hasta que pongas a cero el contador: es la fila «Expulsado por el kernel».
- **FSR 4**: a través de OptiScaler en la ruta DLSS del juego. GE-Proton 11 descarga OptiScaler solo cuando encuentra `PROTON_USE_OPTISCALER=1`, el juego debe ponerse en DLSS, y la biblioteca FSR 4 de AMD (`amdxcffx64.dll`, del driver Windows de AMD) va junto al juego. XeSS, donde un juego lo trae de serie, cuesta lo mismo que FSR 3 a 1080p.
- **Proton**: las versiones GE-Proton 11; Instalar descarga una (unos 500 MB) en las carpetas de Steam y Heroic, Predeterminada la elige. Steam debe estar cerrado para que se escriba su predeterminada.""",
    ai_t='## IA',
    ai="""El motor es **Unsloth Studio**: ejecuta modelos GGUF con llama.cpp sobre el backend **Vulkan**, que en la gfx1013 de la BC-250 es el único camino acelerado, porque ROCm no la soporta. Medido en la placa con Qwen3-1.7B Q4_K_M: 210 tokens por segundo frente a 41 solo con la CPU.

- **Motor**: encendido, apagado, al arrancar. Encendido retiene memoria de la GPU, así que se apaga antes de jugar. Al lado están la versión, la comprobación de actualizaciones y *Actualizar*, que vuelve a ejecutar el instalador oficial con el paquete Vulkan de llama.cpp.
- **Acceso**: Unsloth genera una contraseña al azar al instalarse, y se apaga solo al cabo de una hora si no se cambia. El primer acceso se hace aquí: eliges la contraseña de Studio y la clave API se crea a la vez, y se comparte con el Remote Manager.
- **Modelos**: los que hay en disco, con cuantización y tamaño. Para descargar uno hace falta el nombre del repositorio en Hugging Face (por ejemplo `unsloth/Qwen3-4B-GGUF`) y la variante elegida de la lista, con los tamaños.
- **Chat**: una prueba rápida sobre la API compatible con OpenAI (`http://127.0.0.1:8888/v1`), con los tokens por segundo medidos. El chat completo, con archivos y búsqueda, está dentro de Studio.
- **Memoria**: VRAM, GTT, RAM, swap y el presupuesto del modelo. El límite del GTT es un parámetro del kernel: vale desde el siguiente arranque.
- **Red**: abierto en la red local, Studio responde también a los demás dispositivos de casa, con su propio usuario y contraseña. Los chats en paralelo son los slots de llama-server.""",
    fine_t="## Ventilador, perfiles y el resto",
    fine="La página **Ventilador** dibuja la curva dentro del gráfico de los sensores: a esta temperatura el ventilador gira así, con un adelanto para que la velocidad suba antes que la temperatura. Los **Perfiles** mueven el techo dentro de la curva que ya está y ajustan juntos CPU, preset del ventilador y planificador. Las **Instantáneas** son fotos del sistema, tus archivos no se tocan. **IA** retiene la memoria de la GPU mientras está encendida: apágala antes de jugar. **Consola** arranca Steam Big Picture dentro de gamescope sobre el escritorio, o como sesión desde la pantalla de inicio. El **Remote Manager** replica las páginas Tuner, Juegos y Perfiles en un navegador.")

T["pt"] = dict(
    title="Control Center", desc="Todas as ferramentas do SkillFishOS numa janela: Tuner, Ventoinha, Monitor, Jogos, Perfis, Kernel, Snapshots, IA, Emuladores, Consola, ISO.",
    intro="Todas as ferramentas do SkillFishOS estão numa janela. Abre-se pelo menu (SkillFishOS → Control Center) ou com `skillfish-control-center`. Também se conduz com o comando: cruz ou alavanca para mover, A confirma, B volta, LB e RB mudam de secção.",
    sezioni="## As secções",
    voci=[("Estado", "um número por cartão: frequência e teto da GPU, CPU, unidades de cálculo, ventoinha, kernel, governor, driver Vulkan, se o último arranque seguiu um encerramento limpo. Aqui não se define nada."),
          ("Tuner", "a curva tensão/frequência do governor da GPU, a CPU, os núcleos, as unidades de cálculo, a VRAM."),
          ("Ventoinha", "a curva da ventoinha com o avanço, os sensores de origem, os limites de segurança, o teste PWM."),
          ("Monitor", "todas as leituras, um gráfico por unidade, mais as barras de frequência por thread. REC grava, CSV exporta."),
          ("Jogos", "a nossa Mesa por lançador ou para todo o sistema, o escalonador scx_bpfland, FSR 4, instalação e predefinição do GE-Proton."),
          ("Perfis", "teto, CPU, ventoinha e escalonador num clique; guarde os seus."),
          ("Kernel", "os kernels instalados, o predefinido, arrancar uma vez, desinstalar."),
          ("Snapshots", "os snapshots do sistema e a manutenção btrfs agendada."),
          ("IA", "Unsloth Studio em Vulkan: motor, atualização, modelos do Hub da Hugging Face, teste de chat, memória e rede."),
          ("Emuladores", "EmuDeck, ou os emuladores um a um a partir do Flathub."),
          ("Consola", "Steam Big Picture dentro do gamescope, agora ou a partir do ecrã de início de sessão."),
          ("ISO", "imagens de disco montadas através do udisks.")],
    tuner_t="## Tuner",
    tuner="""A curva é o gráfico: MHz na horizontal, milivolts na vertical. Arraste um ponto, duplo clique para acrescentar um, clique direito para o retirar, ou escreva os números na tabela ao lado do gráfico (+ e − acrescentam e retiram pontos). A linha vertical a tracejado é o teto, o ponto azul é a GPU neste momento. Três presets: **Cautious 1850** (o ponto ideal com o dissipador de série, quase os mesmos fotogramas e dez graus a menos), **Balanced 2000**, **Performance 2100** (a curva de quinze pontos medida na placa de desenvolvimento, a que enviamos).

**Aplicar é uma prova.** Uma curva que pede pouca tensão bloqueia a placa, e na BC-250 um bloqueio resolve-se a tirar a ficha. Por isso Aplicar arranca a candidata com a curva anterior ainda no disco e conta 25 segundos: carregue em Manter e a candidata fica escrita de vez; não faça nada, ou a placa morre e volta, e arranca a curva anterior.

Os painéis abrem-se quando são precisos:

- **CPU**: frequência, degrau de undervolt (6,25 mV cada) e limite térmico, cada um com um cursor e uma caixa numérica de passo 1. *Sugerir UV* desce o undervolt dois degraus de cada vez com doze segundos de carga por degrau; *Encontrar o máximo* sobe de 3600 a 4000 MHz; *Teste 60 s* carrega os valores atuais. Cada prova mostra uma contagem decrescente e um botão Stop; os valores em prova nunca são escritos no disco, por isso um bloqueio arranca com os anteriores. Acima de 3500 MHz com oito núcleos o ganho é nulo: manda o calor.
- **Núcleos**: que núcleos estão ativos, SMT, o desbloqueio dos 8 núcleos (6c/12t passa a 8c/16t, +20 % medido) e *Antes do arranque (EFI)*: o desbloqueio feito antes do GRUB num só arranque, em vez do reinício extra do serviço dentro do sistema.
- **CU**: as 40 unidades de cálculo em 20 células (pares): verde ligada, vermelha desligada, cinzenta mantida ligada pelo driver. Escreva quantas CU quer (de 24 a 40, aos pares) ou clique nas células; *Teste CU* liga os pares extra um a um sob o vkpeak e reporta erros, para a lotaria do silício.
- **VRAM**: a divisão UMA no CMOS, aplicada no próximo arranque. Com os 512 MB dinâmicos alguns jogos escolhem texturas baixas: se estiverem desfocadas, experimente 4 ou 6 GB fixos. Vai de 512 MB a 12 GB, com as predefinições 512 MB, 1, 2, 4, 6 e 8 GB.
- **Avançado**: os botões do próprio governor: margem a subir, degrau, confirmações a descer, limiares térmicos e de potência, droop.
- **Teste**: vkpeak e o registo do assistente.""",
    monitor_t="## Monitor",
    monitor="Um gráfico por grandeza, cada um com a sua escala real: temperaturas (CPU, GPU, VRM, sistema, NVMe), frequências (CPU média, mínima, máxima, GPU e o seu teto), carga, potência, tensões, ventoinha e memória (RAM, VRAM, GTT), mais uma barra por thread. Clique numa entrada da legenda para esconder uma linha; passe o rato para ler todos os gráficos no mesmo instante. REC escreve um ficheiro `.sfmon` (CSV) que Abrir recarrega com um cursor; CSV exporta-o para uma folha de cálculo.",
    giochi_t="## Jogos",
    giochi="""- **Driver Vulkan**: a nossa Mesa abre as filas de cálculo que o driver de série mantém fechadas nesta GPU: +4 % no Cyberpunk 2077, +12 % com FSR 4. Por lançador (Steam, Heroic) com um override flatpak, ou para todo o sistema. Precisa do kernel do SkillFishOS: noutro kernel essas filas bloqueiam a GPU, e o interruptor de sistema recusa-se a arrancar aí. O cartão mostra o kernel em execução.
- **Escalonador**: scx_bpfland, carregado só enquanto corre um jogo (o GameMode lança-o e retira-o): +1,5-2 % no Cyberpunk e fotogramas mais regulares. Se o kernel o expulsar duas vezes, o serviço pára até repor o contador a zero: é a linha «Expulso pelo kernel».
- **FSR 4**: através do OptiScaler no caminho DLSS do jogo. O GE-Proton 11 descarrega o OptiScaler sozinho quando encontra `PROTON_USE_OPTISCALER=1`, o jogo tem de ficar em DLSS, e a biblioteca FSR 4 da AMD (`amdxcffx64.dll`, do driver Windows da AMD) vai ao lado do jogo. O XeSS, onde um jogo o traz de série, custa o mesmo que o FSR 3 a 1080p.
- **Proton**: as versões GE-Proton 11; Instalar descarrega uma (cerca de 500 MB) para as pastas do Steam e do Heroic, Predefinida escolhe-a. O Steam tem de estar fechado para que a sua predefinição seja escrita.""",
    ai_t='## IA',
    ai="""O motor é o **Unsloth Studio**: corre modelos GGUF com o llama.cpp sobre o backend **Vulkan**, que na gfx1013 da BC-250 é o único caminho acelerado, porque o ROCm não a suporta. Medido na placa com Qwen3-1.7B Q4_K_M: 210 tokens por segundo contra 41 só com a CPU.

- **Motor**: ligado, desligado, no arranque. Ligado ocupa memória da GPU, por isso desliga-se antes de jogar. Ao lado estão a versão, a verificação de atualizações e *Atualizar*, que executa de novo o instalador oficial com o pacote Vulkan do llama.cpp.
- **Acesso**: o Unsloth gera uma senha ao acaso quando se instala, e desliga-se sozinho ao fim de uma hora se ela não for mudada. O primeiro acesso faz-se aqui: escolhes a senha do Studio e a chave API é criada com ela, e partilhada com o Remote Manager.
- **Modelos**: os que estão em disco, com quantização e tamanho. Para transferir um é preciso o nome do repositório na Hugging Face (por exemplo `unsloth/Qwen3-4B-GGUF`) e a variante escolhida da lista, com os tamanhos.
- **Chat**: um teste rápido sobre a API compatível com OpenAI (`http://127.0.0.1:8888/v1`), com os tokens por segundo medidos. O chat completo, com ficheiros e pesquisa, está dentro do Studio.
- **Memória**: VRAM, GTT, RAM, swap e o orçamento do modelo. O limite do GTT é um parâmetro do kernel: vale a partir do próximo arranque.
- **Rede**: aberto na rede local, o Studio responde também aos outros dispositivos de casa, com o seu próprio utilizador e senha. Os chats em paralelo são os slots do llama-server.""",
    fine_t="## Ventoinha, perfis e o resto",
    fine="A página **Ventoinha** desenha a curva dentro do gráfico dos sensores: a esta temperatura a ventoinha roda assim, com um avanço para que a velocidade suba antes da temperatura. Os **Perfis** movem o teto dentro da curva que já existe e definem em conjunto CPU, preset da ventoinha e escalonador. Os **Snapshots** são fotografias do sistema, os seus ficheiros não são tocados. **IA** retém a memória da GPU enquanto está ligada: desligue-a antes de jogar. **Consola** arranca o Steam Big Picture dentro do gamescope por cima do ambiente de trabalho, ou como sessão a partir do ecrã de início. O **Remote Manager** replica as páginas Tuner, Jogos e Perfis num navegador.")

T["pl"] = dict(
    title="Control Center", desc="Wszystkie narzędzia SkillFishOS w jednym oknie: Tuner, Wentylator, Monitor, Gry, Profile, Jądro, Migawki, AI, Emulatory, Konsola, ISO.",
    intro="Wszystkie narzędzia SkillFishOS mieszczą się w jednym oknie. Otwiera się z menu (SkillFishOS → Control Center) albo poleceniem `skillfish-control-center`. Obsłuży je też kontroler: krzyżak lub gałka do poruszania, A potwierdza, B cofa, LB i RB zmieniają sekcję.",
    sezioni="## Sekcje",
    voci=[("Stan", "jedna liczba na kartę: zegar i sufit GPU, CPU, jednostki obliczeniowe, wentylator, jądro, governor, sterownik Vulkan, czy ostatni start nastąpił po czystym zamknięciu. Tu niczego się nie ustawia."),
          ("Tuner", "krzywa napięcie/częstotliwość governora GPU, CPU, rdzenie, jednostki obliczeniowe, VRAM."),
          ("Wentylator", "krzywa wentylatora z wyprzedzeniem, czujniki źródłowe, limity bezpieczeństwa, test PWM."),
          ("Monitor", "wszystkie odczyty, jeden wykres na jednostkę, plus słupki zegara na wątek. REC nagrywa, CSV eksportuje."),
          ("Gry", "nasza Mesa per launcher albo dla całego systemu, planista scx_bpfland, FSR 4, instalacja i domyślny GE-Proton."),
          ("Profile", "sufit, CPU, wentylator i planista jednym kliknięciem; zapisz własne."),
          ("Jądro", "zainstalowane jądra, domyślne, uruchom raz, odinstaluj."),
          ("Migawki", "migawki systemu i zaplanowana konserwacja btrfs."),
          ("AI", "Unsloth Studio na Vulkanie: silnik, aktualizacja, modele z Hubu Hugging Face, próbny czat, pamięć i sieć."),
          ("Emulatory", "EmuDeck albo emulatory pojedynczo z Flathuba."),
          ("Konsola", "Steam Big Picture w gamescope, teraz albo z ekranu logowania."),
          ("ISO", "obrazy dysków montowane przez udisks.")],
    tuner_t="## Tuner",
    tuner="""Krzywa jest wykresem: MHz w poziomie, miliwolty w pionie. Przeciągnij punkt, dwuklik dodaje punkt, prawy przycisk go usuwa, albo wpisz liczby w tabeli obok wykresu (+ i − dodają i usuwają punkty). Pionowa przerywana linia to sufit, niebieska kropka to GPU w tej chwili. Trzy presety: **Cautious 1850** (optymalny punkt z fabrycznym radiatorem, prawie te same klatki i dziesięć stopni mniej), **Balanced 2000**, **Performance 2100** (krzywa z piętnastu punktów zmierzona na płycie deweloperskiej, ta, którą wysyłamy).

**Zastosuj to próba.** Krzywa, która żąda za mało napięcia, zawiesza płytę, a na BC-250 zawieszenie leczy się wyjęciem wtyczki. Dlatego Zastosuj uruchamia kandydatkę, gdy poprzednia krzywa wciąż jest na dysku, i odlicza 25 sekund: naciśnij Zachowaj, a kandydatka zostanie zapisana na dobre; nic nie rób, albo płyta padnie i wróci, a wystartuje poprzednia krzywa.

Panele otwierają się na żądanie:

- **CPU**: zegar, stopień undervoltu (po 6,25 mV) i limit termiczny, każdy z suwakiem i polem liczbowym o kroku 1. *Zasugeruj UV* schodzi undervoltem po dwa stopnie z dwunastoma sekundami obciążenia na stopień; *Znajdź maksimum* wspina się od 3600 do 4000 MHz; *Test 60 s* obciąża bieżące wartości. Każdy przebieg pokazuje odliczanie i przycisk Stop; testowane wartości nigdy nie trafiają na dysk, więc zawieszenie startuje z poprzednimi. Powyżej 3500 MHz z ośmioma rdzeniami zysku nie ma: rządzi ciepło.
- **Rdzenie**: które rdzenie są włączone, SMT, odblokowanie 8 rdzeni (6c/12t staje się 8c/16t, zmierzone +20 %) oraz *Przed startem (EFI)*: odblokowanie wykonane przed GRUB-em w jednym starcie zamiast dodatkowego restartu usługi w systemie.
- **CU**: 40 jednostek obliczeniowych jako 20 komórek (pary): zielona włączona, czerwona wyłączona, szara trzymana przez sterownik. Wpisz, ile CU chcesz (24 do 40, parami) albo klikaj komórki; *Test CU* włącza dodatkowe pary pojedynczo pod vkpeak i zgłasza błędy, na loterię krzemową.
- **VRAM**: podział UMA w CMOS, stosowany przy następnym starcie. Przy dynamicznych 512 MB niektóre gry wybierają niskie tekstury: jeśli są rozmyte, spróbuj 4 lub 6 GB na stałe. Od 512 MB do 12 GB, z gotowymi wartościami 512 MB, 1, 2, 4, 6 i 8 GB.
- **Zaawansowane**: pokrętła samego governora: margines przy wchodzeniu, stopień, potwierdzenia przy schodzeniu, progi termiczne i mocy, droop.
- **Test**: vkpeak i dziennik pomocnika.""",
    monitor_t="## Monitor",
    monitor="Jeden wykres na wielkość, każdy z własną prawdziwą skalą: temperatury (CPU, GPU, VRM, system, NVMe), zegary (CPU średni, min, max, GPU i jego sufit), obciążenie, moc, napięcia, wentylator i pamięć (RAM, VRAM, GTT), plus jeden słupek na wątek. Kliknij wpis legendy, żeby ukryć linię; najedź myszą, żeby odczytać wszystkie wykresy w tej samej chwili. REC zapisuje plik `.sfmon` (CSV), który Otwórz wczytuje z suwakiem; CSV eksportuje go do arkusza.",
    giochi_t="## Gry",
    giochi="""- **Sterownik Vulkan**: nasza Mesa otwiera kolejki obliczeniowe, które fabryczny sterownik trzyma zamknięte na tym GPU: +4 % w Cyberpunk 2077, +12 % z FSR 4. Per launcher (Steam, Heroic) przez override flatpaka albo dla całego systemu. Wymaga jądra SkillFishOS: na innym jądrze te kolejki zawieszają GPU, a przełącznik systemowy odmawia tam startu. Karta pokazuje działające jądro.
- **Planista**: scx_bpfland, ładowany tylko gdy działa gra (GameMode go podnosi i zdejmuje): +1,5-2 % w Cyberpunk i równiejsze klatki. Jeśli jądro wyrzuci go dwa razy, usługa zatrzymuje się do wyzerowania licznika: to wiersz „Wyrzucony przez jądro”.
- **FSR 4**: przez OptiScaler na ścieżce DLSS gry. GE-Proton 11 sam pobiera OptiScaler, gdy znajdzie `PROTON_USE_OPTISCALER=1`, grę trzeba ustawić na DLSS, a biblioteka FSR 4 AMD (`amdxcffx64.dll`, ze sterownika Windows AMD) idzie obok gry. XeSS, tam gdzie gra ma go wbudowanego, kosztuje tyle co FSR 3 w 1080p.
- **Proton**: wydania GE-Proton 11; Zainstaluj pobiera jedno (około 500 MB) do folderów Steam i Heroic, Domyślny je wybiera. Steam musi być zamknięty, żeby jego domyślny został zapisany.""",
    ai_t='## AI',
    ai="""Silnikiem jest **Unsloth Studio**: uruchamia modele GGUF przez llama.cpp na backendzie **Vulkan**, który na gfx1013 w BC-250 jest jedyną przyspieszaną drogą, bo ROCm jej nie obsługuje. Zmierzone na płycie z Qwen3-1.7B Q4_K_M: 210 tokenów na sekundę wobec 41 na samym CPU.

- **Silnik**: włączony, wyłączony, przy starcie. Włączony zajmuje pamięć GPU, więc wyłącza się go przed graniem. Obok są wersja, sprawdzanie aktualizacji i *Aktualizuj*, które ponownie uruchamia oficjalny instalator z pakietem Vulkan dla llama.cpp.
- **Dostęp**: Unsloth przy instalacji tworzy losowe hasło i wyłącza się sam po godzinie, jeśli hasło nie zostanie zmienione. Pierwsze logowanie odbywa się tutaj: wybierasz hasło do Studio, a klucz API powstaje razem z nim i trafia też do Remote Managera.
- **Modele**: te na dysku, z kwantyzacją i rozmiarem. Żeby pobrać model, potrzebna jest nazwa repozytorium na Hugging Face (na przykład `unsloth/Qwen3-4B-GGUF`) i wariant wybrany z listy, z rozmiarami.
- **Czat**: szybka próba na API zgodnym z OpenAI (`http://127.0.0.1:8888/v1`), ze zmierzonymi tokenami na sekundę. Pełny czat, z plikami i wyszukiwaniem, jest w Studio.
- **Pamięć**: VRAM, GTT, RAM, swap i budżet modelu. Limit GTT to parametr jądra: działa od następnego startu.
- **Sieć**: otwarty w sieci lokalnej Studio odpowiada też innym urządzeniom w domu, z własnym użytkownikiem i hasłem. Równoległe czaty to sloty llama-server.""",
    fine_t="## Wentylator, profile i reszta",
    fine="Strona **Wentylator** rysuje krzywą wewnątrz wykresu czujników: w tej temperaturze wentylator kręci się tak, z wyprzedzeniem, żeby obroty rosły przed temperaturą. **Profile** przesuwają sufit w obrębie istniejącej krzywej i ustawiają razem CPU, preset wentylatora i planistę. **Migawki** to zdjęcia systemu, twoje pliki pozostają nietknięte. **AI** trzyma pamięć GPU, dopóki jest włączone: wyłącz przed graniem. **Konsola** uruchamia Steam Big Picture w gamescope nad pulpitem albo jako sesję z ekranu logowania. **Remote Manager** odwzorowuje strony Tuner, Gry i Profile w przeglądarce.")

T["ru"] = dict(
    title="Control Center", desc="Все инструменты SkillFishOS в одном окне: Тюнер, Вентилятор, Монитор, Игры, Профили, Ядро, Снимки, ИИ, Эмуляторы, Консоль, ISO.",
    intro="Все инструменты SkillFishOS живут в одном окне. Открывается из меню (SkillFishOS → Control Center) или командой `skillfish-control-center`. Управляется и контроллером: крестовина или стик для перемещения, A подтверждает, B возвращает назад, LB и RB меняют раздел.",
    sezioni="## Разделы",
    voci=[("Состояние", "одно число на карточку: частота и потолок GPU, CPU, вычислительные блоки, вентилятор, ядро, governor, драйвер Vulkan, была ли последняя загрузка после чистого выключения. Здесь ничего не настраивается."),
          ("Тюнер", "кривая напряжение/частота governor GPU, CPU, ядра, вычислительные блоки, VRAM."),
          ("Вентилятор", "кривая вентилятора с упреждением, датчики-источники, пределы безопасности, тест PWM."),
          ("Монитор", "все показания, один график на единицу измерения, плюс столбцы частоты по потокам. REC записывает, CSV экспортирует."),
          ("Игры", "наша Mesa для лаунчера или всей системы, планировщик scx_bpfland, FSR 4, установка и выбор GE-Proton по умолчанию."),
          ("Профили", "потолок, CPU, вентилятор и планировщик одним щелчком; сохраняйте свои."),
          ("Ядро", "установленные ядра, ядро по умолчанию, загрузить один раз, удалить."),
          ("Снимки", "снимки системы и расписание обслуживания btrfs."),
          ("ИИ", "Unsloth Studio на Vulkan: движок, обновление, модели из Hub Hugging Face, проба чата, память и сеть."),
          ("Эмуляторы", "EmuDeck или эмуляторы по одному из Flathub."),
          ("Консоль", "Steam Big Picture внутри gamescope, сейчас или с экрана входа."),
          ("ISO", "образы дисков, смонтированные через udisks.")],
    tuner_t="## Тюнер",
    tuner="""Кривая и есть график: МГц по горизонтали, милливольты по вертикали. Перетащите узел, двойной щелчок добавляет узел, правая кнопка удаляет, или введите числа в таблице рядом с графиком (+ и − добавляют и удаляют узлы). Пунктирная вертикальная линия — потолок, синяя точка — GPU в данный момент. Три пресета: **Cautious 1850** (оптимум со штатным радиатором, почти те же кадры и на десять градусов меньше), **Balanced 2000**, **Performance 2100** (кривая из пятнадцати точек, измеренная на плате разработки, та, что мы поставляем).

**Применить — это проба.** Кривая, которая просит слишком мало напряжения, вешает плату, а на BC-250 зависание лечится выдёргиванием вилки. Поэтому «Применить» запускает кандидата, пока прежняя кривая ещё на диске, и отсчитывает 25 секунд: нажмите «Оставить», и кандидат записывается насовсем; ничего не делайте, или плата умрёт и вернётся, и загрузится прежняя кривая.

Панели открываются по требованию:

- **CPU**: частота, шаг андервольта (по 6,25 мВ) и тепловой предел, каждый со слайдером и числовым полем с шагом 1. *Предложить UV* опускает андервольт по два шага с двенадцатью секундами нагрузки на шаг; *Найти максимум* поднимается с 3600 до 4000 МГц; *Тест 60 с* нагружает текущие значения. Каждый прогон показывает обратный отсчёт и кнопку Stop; проверяемые значения никогда не пишутся на диск, так что зависание загрузится с прежними. Выше 3500 МГц с восемью ядрами прироста нет: командует тепло.
- **Ядра**: какие ядра включены, SMT, разблокировка 8 ядер (6c/12t становится 8c/16t, измерено +20 %) и *До загрузки (EFI)*: разблокировка до GRUB за одну загрузку вместо лишней перезагрузки сервиса внутри системы.
- **CU**: 40 вычислительных блоков в виде 20 ячеек (пар): зелёная включена, красная выключена, серая удерживается драйвером. Введите, сколько CU нужно (от 24 до 40, парами), или щёлкайте ячейки; *Тест CU* включает дополнительные пары по одной под vkpeak и сообщает об ошибках — для кремниевой лотереи.
- **VRAM**: раздел UMA в CMOS, применяется при следующей загрузке. При динамических 512 МБ некоторые игры выбирают низкие текстуры: если они размыты, попробуйте 4 или 6 ГБ фиксированно. От 512 МБ до 12 ГБ, с готовыми значениями 512 МБ, 1, 2, 4, 6 и 8 ГБ.
- **Дополнительно**: собственные ручки governor: запас при подъёме, шаг, подтверждения при спуске, тепловые и мощностные пороги, droop.
- **Тест**: vkpeak и журнал помощника.""",
    monitor_t="## Монитор",
    monitor="Один график на величину, каждый со своей настоящей шкалой: температуры (CPU, GPU, VRM, система, NVMe), частоты (CPU средняя, мин, макс, GPU и её потолок), нагрузка, мощность, напряжения, вентилятор и память (RAM, VRAM, GTT), плюс по столбцу на поток. Щёлкните пункт легенды, чтобы скрыть линию; наведите курсор, чтобы прочитать все графики в один и тот же момент. REC пишет файл `.sfmon` (CSV), который «Открыть» перезагружает с ползунком; CSV экспортирует его для таблицы.",
    giochi_t="## Игры",
    giochi="""- **Драйвер Vulkan**: наша Mesa открывает вычислительные очереди, которые штатный драйвер держит закрытыми на этом GPU: +4 % в Cyberpunk 2077, +12 % с FSR 4. Для лаунчера (Steam, Heroic) через override flatpak или для всей системы. Нужно ядро SkillFishOS: на другом ядре эти очереди вешают GPU, и системный переключатель там не запускается. Карточка показывает работающее ядро.
- **Планировщик**: scx_bpfland, загружается только пока идёт игра (GameMode поднимает и снимает его): +1,5-2 % в Cyberpunk и ровнее кадры. Если ядро выбросит его дважды, сервис останавливается до сброса счётчика: это строка «Выброшен ядром».
- **FSR 4**: через OptiScaler по пути DLSS игры. GE-Proton 11 сам скачивает OptiScaler, найдя `PROTON_USE_OPTISCALER=1`, игру нужно поставить на DLSS, а библиотека FSR 4 от AMD (`amdxcffx64.dll`, из драйвера AMD для Windows) кладётся рядом с игрой. XeSS там, где он встроен в игру, стоит столько же, сколько FSR 3 в 1080p.
- **Proton**: выпуски GE-Proton 11; «Установить» скачивает один (около 500 МБ) в папки Steam и Heroic, «По умолчанию» выбирает его. Steam должен быть закрыт, чтобы его умолчание записалось.""",
    ai_t='## ИИ',
    ai="""Движок это **Unsloth Studio**: он запускает модели GGUF через llama.cpp на бэкенде **Vulkan**, который на gfx1013 в BC-250 единственный ускоренный путь, потому что ROCm её не поддерживает. Измерено на плате с Qwen3-1.7B Q4_K_M: 210 токенов в секунду против 41 на одном CPU.

- **Движок**: включён, выключен, при запуске. Включённый держит память GPU, поэтому перед играми его выключают. Рядом версия, проверка обновлений и *Обновить*, которая заново запускает официальный установщик с пакетом Vulkan для llama.cpp.
- **Доступ**: Unsloth создаёт случайный пароль при установке и выключается сам через час, если пароль не сменить. Первый вход делается здесь: вы выбираете пароль Studio, ключ API создаётся вместе с ним и передаётся Remote Manager.
- **Модели**: те, что на диске, с квантованием и размером. Чтобы скачать модель, нужно имя репозитория на Hugging Face (например `unsloth/Qwen3-4B-GGUF`) и вариант из списка, с размерами.
- **Чат**: быстрая проба на API, совместимом с OpenAI (`http://127.0.0.1:8888/v1`), с измеренными токенами в секунду. Полный чат, с файлами и поиском, внутри Studio.
- **Память**: VRAM, GTT, RAM, swap и бюджет модели. Предел GTT это параметр ядра: действует со следующей загрузки.
- **Сеть**: открытый в локальной сети, Studio отвечает и другим устройствам дома, со своим пользователем и паролем. Параллельные чаты это слоты llama-server.""",
    fine_t="## Вентилятор, профили и остальное",
    fine="Страница **Вентилятор** рисует кривую внутри графика датчиков: при этой температуре вентилятор крутится так, с упреждением, чтобы обороты росли раньше температуры. **Профили** двигают потолок внутри уже имеющейся кривой и задают вместе CPU, пресет вентилятора и планировщик. **Снимки** — фотографии системы, ваши файлы не затрагиваются. **ИИ** держит память GPU, пока включён: выключите перед игрой. **Консоль** запускает Steam Big Picture внутри gamescope поверх рабочего стола или как сеанс с экрана входа. **Remote Manager** повторяет страницы Тюнер, Игры и Профили в браузере.")

T["uk"] = dict(
    title="Control Center", desc="Усі інструменти SkillFishOS в одному вікні: Тюнер, Вентилятор, Монітор, Ігри, Профілі, Ядро, Знімки, ШІ, Емулятори, Консоль, ISO.",
    intro="Усі інструменти SkillFishOS живуть в одному вікні. Відкривається з меню (SkillFishOS → Control Center) або командою `skillfish-control-center`. Керується і контролером: хрестовина або стік для руху, A підтверджує, B повертає назад, LB і RB змінюють розділ.",
    sezioni="## Розділи",
    voci=[("Стан", "одне число на картку: частота і стеля GPU, CPU, обчислювальні блоки, вентилятор, ядро, governor, драйвер Vulkan, чи було останнє завантаження після чистого вимкнення. Тут нічого не налаштовується."),
          ("Тюнер", "крива напруга/частота governor GPU, CPU, ядра, обчислювальні блоки, VRAM."),
          ("Вентилятор", "крива вентилятора з випередженням, датчики-джерела, межі безпеки, тест PWM."),
          ("Монітор", "усі показники, один графік на одиницю вимірювання, плюс стовпчики частоти на потік. REC записує, CSV експортує."),
          ("Ігри", "наша Mesa для лаунчера або всієї системи, планувальник scx_bpfland, FSR 4, встановлення і типовий GE-Proton."),
          ("Профілі", "стеля, CPU, вентилятор і планувальник одним клацанням; зберігайте свої."),
          ("Ядро", "встановлені ядра, типове, завантажити один раз, видалити."),
          ("Знімки", "знімки системи і розклад обслуговування btrfs."),
          ("ШІ", "Unsloth Studio на Vulkan: рушій, оновлення, моделі з Hub Hugging Face, проба чату, пам'ять і мережа."),
          ("Емулятори", "EmuDeck або емулятори по одному з Flathub."),
          ("Консоль", "Steam Big Picture всередині gamescope, зараз або з екрана входу."),
          ("ISO", "образи дисків, змонтовані через udisks.")],
    tuner_t="## Тюнер",
    tuner="""Крива і є графіком: МГц по горизонталі, мілівольти по вертикалі. Перетягніть вузол, подвійне клацання додає вузол, права кнопка вилучає, або введіть числа в таблиці поруч із графіком (+ і − додають і вилучають вузли). Пунктирна вертикальна лінія — стеля, синя крапка — GPU зараз. Три пресети: **Cautious 1850** (оптимум зі штатним радіатором, майже ті самі кадри і на десять градусів менше), **Balanced 2000**, **Performance 2100** (крива з п'ятнадцяти точок, виміряна на платі розробки, та, яку ми постачаємо).

**Застосувати — це проба.** Крива, що просить замало напруги, вішає плату, а на BC-250 зависання лікується висмикуванням вилки. Тому «Застосувати» запускає кандидата, поки попередня крива ще на диску, і відлічує 25 секунд: натисніть «Залишити», і кандидат записується назавжди; нічого не робіть, або плата помре і повернеться, і завантажиться попередня крива.

Панелі відкриваються за потреби:

- **CPU**: частота, крок андервольта (по 6,25 мВ) і тепловий ліміт, кожен зі слайдером і числовим полем із кроком 1. *Запропонувати UV* опускає андервольт по два кроки з дванадцятьма секундами навантаження на крок; *Знайти максимум* піднімається з 3600 до 4000 МГц; *Тест 60 с* навантажує поточні значення. Кожен прогін показує зворотний відлік і кнопку Stop; значення під пробою ніколи не пишуться на диск, тож зависання завантажиться з попередніми. Вище 3500 МГц з вісьмома ядрами приросту немає: керує тепло.
- **Ядра**: які ядра увімкнені, SMT, розблокування 8 ядер (6c/12t стає 8c/16t, виміряно +20 %) і *До завантаження (EFI)*: розблокування до GRUB за одне завантаження замість зайвого перезавантаження сервісу всередині системи.
- **CU**: 40 обчислювальних блоків як 20 комірок (пар): зелена увімкнена, червона вимкнена, сіра утримується драйвером. Введіть, скільки CU потрібно (від 24 до 40, парами), або клацайте комірки; *Тест CU* вмикає додаткові пари по одній під vkpeak і повідомляє про помилки — для кремнієвої лотереї.
- **VRAM**: розподіл UMA в CMOS, застосовується при наступному завантаженні. З динамічними 512 МБ деякі ігри обирають низькі текстури: якщо вони розмиті, спробуйте 4 або 6 ГБ фіксовано. Від 512 МБ до 12 ГБ, із готовими значеннями 512 МБ, 1, 2, 4, 6 і 8 ГБ.
- **Додатково**: власні ручки governor: запас на підйомі, крок, підтвердження на спуску, теплові й потужнісні пороги, droop.
- **Тест**: vkpeak і журнал помічника.""",
    monitor_t="## Монітор",
    monitor="Один графік на величину, кожен зі своєю справжньою шкалою: температури (CPU, GPU, VRM, система, NVMe), частоти (CPU середня, мін, макс, GPU і її стеля), навантаження, потужність, напруги, вентилятор і пам'ять (RAM, VRAM, GTT), плюс по стовпчику на потік. Клацніть пункт легенди, щоб сховати лінію; наведіть курсор, щоб прочитати всі графіки в одну мить. REC пише файл `.sfmon` (CSV), який «Відкрити» перезавантажує з повзунком; CSV експортує його для таблиці.",
    giochi_t="## Ігри",
    giochi="""- **Драйвер Vulkan**: наша Mesa відкриває обчислювальні черги, які штатний драйвер тримає закритими на цьому GPU: +4 % у Cyberpunk 2077, +12 % із FSR 4. Для лаунчера (Steam, Heroic) через override flatpak або для всієї системи. Потрібне ядро SkillFishOS: на іншому ядрі ці черги вішають GPU, і системний перемикач там не запускається. Картка показує ядро, що працює.
- **Планувальник**: scx_bpfland, завантажується лише поки йде гра (GameMode піднімає і знімає його): +1,5-2 % у Cyberpunk і рівніші кадри. Якщо ядро викине його двічі, сервіс зупиняється до скидання лічильника: це рядок «Викинутий ядром».
- **FSR 4**: через OptiScaler шляхом DLSS гри. GE-Proton 11 сам завантажує OptiScaler, знайшовши `PROTON_USE_OPTISCALER=1`, гру треба поставити на DLSS, а бібліотека FSR 4 від AMD (`amdxcffx64.dll`, з драйвера AMD для Windows) кладеться поруч із грою. XeSS там, де він вбудований у гру, коштує стільки ж, скільки FSR 3 у 1080p.
- **Proton**: випуски GE-Proton 11; «Встановити» завантажує один (близько 500 МБ) у теки Steam і Heroic, «Типовий» обирає його. Steam має бути закритий, щоб його типове записалося.""",
    ai_t='## ШІ',
    ai="""Рушій це **Unsloth Studio**: він запускає моделі GGUF через llama.cpp на бекенді **Vulkan**, який на gfx1013 у BC-250 є єдиним прискореним шляхом, бо ROCm її не підтримує. Виміряно на платі з Qwen3-1.7B Q4_K_M: 210 токенів за секунду проти 41 на самому CPU.

- **Рушій**: увімкнений, вимкнений, при запуску. Увімкнений тримає пам'ять GPU, тому перед іграми його вимикають. Поруч версія, перевірка оновлень і *Оновити*, яка знову запускає офіційний інсталятор із пакетом Vulkan для llama.cpp.
- **Доступ**: Unsloth створює випадковий пароль під час встановлення і вимикається сам через годину, якщо пароль не змінити. Перший вхід робиться тут: ви вибираєте пароль Studio, ключ API створюється разом із ним і передається Remote Manager.
- **Моделі**: ті, що на диску, з квантуванням і розміром. Щоб завантажити модель, потрібна назва репозиторію на Hugging Face (наприклад `unsloth/Qwen3-4B-GGUF`) і варіант зі списку, з розмірами.
- **Чат**: швидка проба на API, сумісному з OpenAI (`http://127.0.0.1:8888/v1`), із виміряними токенами за секунду. Повний чат, із файлами і пошуком, усередині Studio.
- **Пам'ять**: VRAM, GTT, RAM, swap і бюджет моделі. Межа GTT це параметр ядра: діє з наступного завантаження.
- **Мережа**: відкритий у локальній мережі, Studio відповідає й іншим пристроям удома, зі своїм користувачем і паролем. Паралельні чати це слоти llama-server.""",
    fine_t="## Вентилятор, профілі і решта",
    fine="Сторінка **Вентилятор** малює криву всередині графіка датчиків: за цієї температури вентилятор крутиться так, з випередженням, щоб оберти зростали раніше за температуру. **Профілі** рухають стелю всередині наявної кривої і задають разом CPU, пресет вентилятора і планувальник. **Знімки** — фотографії системи, ваші файли не чіпаються. **ШІ** тримає пам'ять GPU, поки увімкнений: вимкніть перед грою. **Консоль** запускає Steam Big Picture всередині gamescope поверх стільниці або як сеанс з екрана входу. **Remote Manager** повторює сторінки Тюнер, Ігри і Профілі у браузері.")

for lingua, d in T.items():
    p = os.path.join(repo, "website", "src", "content", "docs", lingua, "control-center.md")
    voci = "\n".join("- **%s**: %s" % (n, s) for n, s in d["voci"])
    # YAML: the description holds colons, so both strings go quoted
    q = lambda s: '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'  # noqa: E731
    pezzi = [d["intro"], d["sezioni"], voci, d["tuner_t"], d["tuner"],
             d["monitor_t"], d["monitor"], d["giochi_t"], d["giochi"],
             d["ai_t"], d["ai"], d["fine_t"], d["fine"]]
    testo = ("---\ntitle: %s\ndescription: %s\ngroup: %s\norder: 4\n---\n\n"
             % (q(d["title"]), q(d["desc"]), GRUPPO[lingua])
             + "\n\n".join(pezzi) + "\n")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(testo)
    print(lingua, len(testo))
