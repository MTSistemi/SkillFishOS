---
title: "Control Center"
description: "Alle SkillFishOS-Werkzeuge in einem Fenster: Tuner, Lüfter, Monitor, Spiele, Profile, Kernel, Snapshots, KI, Emulatoren, Konsole, ISO."
group: Benutzung
order: 4
---

Alle SkillFishOS-Werkzeuge stecken in einem Fenster. Es öffnet sich über das Menü (SkillFishOS → Control Center) oder mit `skillfish-control-center`. Auch ein Controller bedient es: Steuerkreuz oder Stick zum Bewegen, A bestätigt, B geht zurück, LB und RB wechseln den Bereich.

![der Bereich Status im SkillFishOS Control Center](/img/control-center-stato.png)

## Die Bereiche

- **Status**: eine Zahl pro Karte: GPU-Takt und Obergrenze, CPU, Recheneinheiten, Lüfter, Kernel, Governor, Vulkan-Treiber, ob der letzte Start nach einem sauberen Herunterfahren kam. Hier wird nichts eingestellt.
- **Tuner**: die Spannungs-/Frequenzkurve des GPU-Governors, die CPU, die Kerne, die Recheneinheiten, der VRAM-Anteil.
- **Lüfter**: die Lüfterkurve mit Vorlauf, die Quellsensoren, die Sicherheitsgrenzen, der PWM-Test.
- **Monitor**: jeder Messwert in einem Diagramm pro Einheit, dazu die Taktbalken pro Thread. REC zeichnet auf, CSV exportiert.
- **Spiele**: unsere Mesa pro Launcher oder systemweit, der Scheduler scx_bpfland, FSR 4, GE-Proton installieren und als Standard setzen.
- **Profile**: Obergrenze, CPU, Lüfter und Scheduler mit einem Klick; eigene speichern.
- **Kernel**: die installierten Kernel, der Standard, einmal starten, deinstallieren.
- **Snapshots**: System-Snapshots und der btrfs-Wartungsplan.
- **KI**: Unsloth Studio über Vulkan: Motor, Aktualisierung, Modelle aus dem Hugging-Face-Hub, Chat-Test, Speicher und Netz.
- **Emulatoren**: EmuDeck oder die Emulatoren einzeln aus Flathub.
- **Konsole**: Steam Big Picture in gamescope, jetzt oder vom Anmeldebildschirm.
- **ISO**: Datenträgerabbilder, über udisks eingehängt.

## Tuner

![der Bereich Tuner im SkillFishOS Control Center](/img/control-center-tuner.png)

Die Kurve ist das Diagramm: MHz waagerecht, Millivolt senkrecht. Einen Punkt ziehen, Doppelklick fügt einen hinzu, Rechtsklick entfernt ihn, oder die Zahlen in die Tabelle neben dem Diagramm tippen (+ und − fügen Punkte hinzu und entfernen sie). Die gestrichelte senkrechte Linie ist die Obergrenze, der blaue Punkt die GPU im Moment. Drei Presets: **Cautious 1850** (der beste Punkt mit dem Serienkühler, fast dieselben Bilder und zehn Grad weniger), **Balanced 2000**, **Performance 2100** (die auf der Entwicklungskarte gemessene Kurve mit fünfzehn Punkten, die wir ausliefern).

**Anwenden ist eine Probe.** Eine Kurve mit zu wenig Spannung hängt die Karte auf, und auf der BC-250 hilft dann nur der Stecker. Deshalb startet Anwenden die Kandidatin, während die vorherige Kurve auf der Platte bleibt, und zählt 25 Sekunden herunter: Behalten drücken, und die Kandidatin wird endgültig geschrieben; nichts tun, oder die Karte stirbt und kommt zurück, und die vorherige Kurve startet.

Die Bereiche öffnen sich bei Bedarf:

- **CPU**: Takt, Undervolt-Stufe (je 6,25 mV) und Temperaturgrenze, jeweils mit Schieber und Zahlenfeld in Schritt 1. *UV vorschlagen* geht den Undervolt in Zweierschritten mit zwölf Sekunden Last pro Stufe hinunter; *Mein Maximum* klettert von 3600 auf 4000 MHz; *Test 60 s* belastet die aktuellen Werte. Jeder Lauf zeigt einen Countdown und einen Stop-Knopf; die getesteten Werte landen nie auf der Platte, ein Hänger startet also mit den vorherigen. Über 3500 MHz mit acht Kernen bringt nichts: die Hitze hat das Sagen.
- **Kerne**: welche Kerne aktiv sind, SMT, die 8-Kern-Freischaltung (aus 6c/12t wird 8c/16t, +20 % gemessen) und *Vor dem Start (EFI)*: die Freischaltung vor GRUB in einem einzigen Start statt des zusätzlichen Neustarts des Dienstes im System.
- **CU**: die 40 Recheneinheiten als 20 Zellen (Paare): grün an, rot aus, grau vom Treiber gehalten. Die gewünschte Anzahl eintippen (24 bis 40, paarweise) oder die Zellen anklicken; *Test CU* schaltet die zusätzlichen Paare einzeln unter vkpeak ein und meldet Fehler, für die Silizium-Lotterie.
- **VRAM**: der UMA-Anteil im CMOS, gültig ab dem nächsten Start. Mit der dynamischen 512-MB-Aufteilung wählen manche Spiele niedrige Texturen: wirken sie unscharf, 4 oder 6 GB fest probieren. Von 512 MB bis 12 GB, mit den Vorgaben 512 MB, 1, 2, 4, 6 und 8 GB.
- **Erweitert**: die Regler des Governors: Aufstiegsmarge, Stufe, Abstiegsbestätigungen, Temperatur- und Leistungsschwellen, Droop.
- **Test**: vkpeak und das Helper-Protokoll.

## Monitor

![der Bereich Monitor im SkillFishOS Control Center](/img/control-center-monitor.png)

Ein Diagramm pro Größe, jedes mit echter Skala: Temperaturen (CPU, GPU, VRM, System, NVMe), Takte (CPU-Mittel, Minimum, Maximum, GPU und ihre Obergrenze), Last, Leistung, Spannungen, Lüfter und Speicher (RAM, VRAM, GTT), dazu ein Balken pro Thread. Klick auf einen Legendeneintrag blendet eine Linie aus; mit der Maus liest man alle Diagramme im selben Augenblick. REC schreibt eine `.sfmon`-Datei (CSV), die Öffnen mit einem Schieber wieder lädt; CSV exportiert sie für eine Tabellenkalkulation.

## Spiele

![der Bereich Spiele im SkillFishOS Control Center](/img/control-center-giochi.png)

- **Vulkan-Treiber**: unsere Mesa öffnet die Compute-Warteschlangen, die der Serientreiber auf dieser GPU geschlossen hält: +4 % in Cyberpunk 2077, +12 % mit FSR 4. Pro Launcher (Steam, Heroic) über einen Flatpak-Override oder systemweit. Braucht den SkillFishOS-Kernel: auf einem anderen Kernel blockieren diese Warteschlangen die GPU, und der Systemschalter startet dort nicht. Die Karte zeigt den laufenden Kernel.
- **Scheduler**: scx_bpfland, nur geladen, solange ein Spiel läuft (GameMode startet ihn und beendet ihn wieder): +1,5-2 % in Cyberpunk und gleichmäßigere Bilder. Wirft der Kernel ihn zweimal hinaus, hält der Dienst an, bis der Zähler zurückgesetzt wird: das ist die Zeile „Vom Kernel hinausgeworfen“.
- **FSR 4**: über OptiScaler auf dem DLSS-Pfad des Spiels. GE-Proton 11 lädt OptiScaler selbst, wenn es `PROTON_USE_OPTISCALER=1` findet, das Spiel muss auf DLSS stehen, und AMDs FSR-4-Bibliothek (`amdxcffx64.dll`, aus AMDs Windows-Treiber) kommt neben das Spiel. XeSS, wo ein Spiel es eingebaut hat, kostet bei 1080p so viel wie FSR 3.
- **Proton**: die GE-Proton-11-Versionen; Installieren lädt eine (etwa 500 MB) in die Ordner von Steam und Heroic, Standard wählt sie. Steam muss geschlossen sein, damit sein Standard geschrieben wird.

## KI

![der Bereich KI im SkillFishOS Control Center](/img/control-center-ai.png)

Der Motor ist **Unsloth Studio**: er führt GGUF-Modelle mit llama.cpp über das **Vulkan**-Backend aus, das auf der gfx1013 der BC-250 der einzige beschleunigte Weg ist, denn ROCm unterstützt sie nicht. Auf der Platine mit Qwen3-1.7B Q4_K_M gemessen: 210 Token pro Sekunde gegenüber 41 auf der CPU allein.

- **Motor**: an, aus, beim Systemstart. Eingeschaltet belegt er GPU-Speicher, vor dem Spielen also ausschalten. Daneben stehen die Version, die Aktualisierungsprüfung und *Aktualisieren*, das den offiziellen Installer mit dem Vulkan-Paket von llama.cpp erneut ausführt.
- **Zugang**: Unsloth erzeugt bei der Installation ein zufälliges Passwort und schaltet sich nach einer Stunde selbst ab, wenn es nicht geändert wird. Die erste Anmeldung geschieht hier: du wählst das Studio-Passwort, der API-Schlüssel entsteht dabei und wird mit dem Remote Manager geteilt.
- **Modelle**: die auf der Platte, mit Quantisierung und Größe. Zum Herunterladen brauchst du den Namen des Repositorys auf Hugging Face (zum Beispiel `unsloth/Qwen3-4B-GGUF`) und die Variante aus der Liste, Größen inklusive.
- **Chat**: ein schneller Lauf über die OpenAI-kompatible API (`http://127.0.0.1:8888/v1`), mit den gemessenen Token pro Sekunde. Der volle Chat, mit Dateien und Suche, steckt in Studio.
- **Speicher**: VRAM, GTT, RAM, Swap und das Budget des Modells. Die GTT-Grenze ist ein Kernel-Parameter: sie gilt ab dem nächsten Start.
- **Netz**: im lokalen Netz geöffnet antwortet Studio auch den anderen Geräten zu Hause, mit eigenem Benutzer und Passwort. Parallele Chats sind die Slots von llama-server.

## Lüfter, Profile und der Rest

Die Seite **Lüfter** zeichnet die Kurve ins Diagramm der Sensoren: bei dieser Temperatur dreht der Lüfter so, mit Vorlauf, damit die Drehzahl vor der Temperatur steigt. **Profile** verschieben die Obergrenze innerhalb der vorhandenen Kurve und setzen CPU, Lüfter-Preset und Scheduler zusammen. **Snapshots** sind Aufnahmen des Systems, die eigenen Dateien bleiben unberührt. **KI** hält GPU-Speicher, solange es an ist: vor dem Spielen ausschalten. **Konsole** startet Steam Big Picture in gamescope über dem Desktop oder als Sitzung vom Anmeldebildschirm. Der **Remote Manager** spiegelt Tuner, Spiele und Profile im Browser.

## Die übrigen Bereiche auf einen Blick

So sehen sie aus, wenn man sie öffnet.

![der Bereich Lüfter im SkillFishOS Control Center](/img/control-center-ventola.png)

![der Bereich Profile im SkillFishOS Control Center](/img/control-center-profili.png)

![der Bereich Kernel im SkillFishOS Control Center](/img/control-center-kernel.png)

![der Bereich Emulatoren im SkillFishOS Control Center](/img/control-center-emulatori.png)

![der Bereich Konsole im SkillFishOS Control Center](/img/control-center-console.png)

![der Bereich ISO im SkillFishOS Control Center](/img/control-center-iso.png)
