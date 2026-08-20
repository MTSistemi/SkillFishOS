---
title: Häufige Fragen
description: Die üblichsten Fragen zu SkillFishOS und der BC-250, mit kurzen Antworten.
group: Nachschlagen
order: 2
---

Kurze Antworten auf die häufigsten Fragen. Wer es genauer wissen will, folgt aus jeder Antwort dem Verweis auf die passende Seite.

## Allgemeines

**Was ist SkillFishOS?**
Eine Linux-Distribution (Debian + KDE Plasma 6), entworfen und abgestimmt für die Platine **AMD BC-250**: Spiele, Emulation, lokale KI und ganz normale Schreibtischarbeit, alles fertig eingerichtet. Siehe [Einführung](/de/docs/introduzione).

**Auf welcher Hardware läuft es?**
Die Platine, für die es gebaut ist, ist die **AMD BC-250** (APU Zen 2 + RDNA 2 „gfx1013“, 16 GB GDDR6), und dort kann es alles, was es kann: 40 freigeschaltete Recheneinheiten, SMU-Governor, acht Kerne. Es gibt außerdem eine Ausgabe **Generic x86-64**, die auf jedem PC und in jeder virtuellen Maschine läuft — ein gewöhnlicher Kernel, wobei sich die platinenspezifischen Teile verstecken, statt zu scheitern. Siehe [BC-250-Hardware](/de/docs/hardware-bc250).

**Was kostet es? Ist es quelloffen?**
Es ist **kostenlos**. Es fügt quelloffene Software aus vielen Gemeinschaften zusammen; der Code des Projekts liegt auf [GitHub](https://github.com/MTSistemi/SkillFishOS). Siehe [Quellen](/de/docs/fonti).

**Sind Spiele, ROMs oder BIOS-Dateien enthalten?**
Nein. SkillFishOS liefert die **Werkzeuge** (Steam, EmuDeck, Emulatoren, Oberflächen); die Inhalte bringst du selbst mit, auf legalem Weg. Siehe [Spiele](/de/docs/gaming).

## Installation

**Wie installiere ich es?**
Schreibe die ISO auf einen USB-Stick und starte das grafische Installationsprogramm **Calamares**. Alles mit der Maus. Siehe [Installation](/de/docs/installazione).

**Kann ich es ausprobieren, ohne zu installieren?**
Ja: die ISO ist **live**, du kannst dich auf dem Schreibtisch umsehen, bevor du installierst.

**Löscht es meine Platte?**
Die automatische Installation („Platte löschen“) tut das. Um vorhandene Daten zu behalten, teile die Platte von Hand auf. SkillFishOS verwendet **Btrfs** mit getrennten Unterbänden: `@` für das System, `@home` für deine Daten, dazu `@cache`, `@log` und `@games`.

**Brauche ich eine Internetverbindung?**
Zum Installieren nicht; danach für Steam, Aktualisierungen und die KI schon.

## Leistung und Übertaktung

**Warum startet es „langsam“, im Profil Stock?**
Aus Sicherheit: jede BC-250 ist anders (*Silizium-Lotterie*). Die Profile hebst du im **[Tuner](/de/docs/app-native)** an, der alles auf deiner eigenen Platine prüft. Siehe [GPU und Übertaktung](/de/docs/gpu-overclock).

**Ist Übertakten gefährlich?**
Der Tuner setzt ein Profil, **prüft** es und **nimmt es zurück**, wenn die Platine nicht mitmacht; die Grenze von 85 °C und der Temperaturschutz sind immer aktiv. Es ist so gebaut, dass es sicher ist.

**Wie viele Bilder pro Sekunde im Spiel X?**
Kommt darauf an: manche Spiele hängen an der **CPU** (etwa *Black Myth: Wukong*) und werden mit einer schnelleren GPU nicht besser. Siehe [Leistung und Messungen](/de/docs/prestazioni).

**Kann ich FSR 4 nutzen?**
Nein, das verlangt RDNA-4-Hardware. Nimm gamescope (FSR1/NIS) oder OptiScaler. Siehe [Spiele](/de/docs/gaming).

## Täglicher Gebrauch

**Warum bleibt der Bildschirm manchmal schwarz?**
Auf der BC-250 ist das **HPD des DisplayPort defekt**: SkillFishOS umgeht das mit einem eigenen Dienst. Nimm einen DP-Bildschirm oder einen **passiven** Adapter. Siehe [Fehlersuche](/de/docs/risoluzione-problemi).

**Warum kommt kein Ton aus dem Fernseher?**
Meist liegt es an einem **aktiven** DP→HDMI-Adapter: nimm einen passiven, einen DP-Bildschirm, eine USB-Soundkarte oder Ton über Bluetooth.

**Kann ich den Rechner schlafen legen?**
Nein. **Der Ruhezustand ist kaputt**, auf Hardware-Ebene, und die Platine wacht nicht wieder auf: SkillFishOS schaltet ihn absichtlich ab. **Schalte ihn nicht wieder ein.** Siehe [Schreibtisch](/de/docs/desktop).

**Kann ich ihn von einem anderen Rechner aus benutzen?**
Ja: die voreingestellte Sitzung ist X11 und **x11vnc** läuft, du kannst den Schreibtisch also über VNC im eigenen Netz bedienen. Siehe [Schreibtisch](/de/docs/desktop).

## Lokale KI

**Welches KI-Modell kann ich verwenden?**
Der Motor ist **Unsloth Studio** auf **Vulkan** (nicht ROCm, das auf gfx1013 nicht unterstützt wird), und die Modelle sind GGUF-Dateien von Hugging Face. Auf der Platine gemessen: **210,7 Token/s** beim Erzeugen gegenüber 41,5 auf der CPU. Siehe [KI auf dem Gerät](/de/docs/ai-locale).

**Kann ich spielen, während die KI läuft?**
Nein: KI und anspruchsvolle Spiele teilen sich GPU und Speicher. Schalte die KI vor dem Spielen ab.

## Aktualisierungen

**Wie aktualisiere ich das System?**
`sudo apt update && sudo apt full-upgrade` oder die Anwendung **Discover**. Vor und nach jeder Aktualisierung wird von selbst ein Schnappschuss angelegt. Siehe [Aktualisierungen](/de/docs/aggiornamenti).

**Eine Aktualisierung hat etwas kaputt gemacht — was nun?**
Starte neu und wähle einen Schnappschuss unter **GRUB → „SkillFishOS snapshots“**. Siehe [Speicher und Schnappschüsse](/de/docs/storage-snapshot).

**Aktualisiert Debian den Kernel?**
Nein: der Kernel von SkillFishOS ist **festgehalten** (`apt-mark hold`) und wird nur aus unserer geprüften Paketquelle aktualisiert. Siehe [Kernel](/de/docs/kernel).

## Projekt

**Kann ich mitmachen oder einen Fehler melden?**
Ja, über die **Issues** auf [GitHub](https://github.com/MTSistemi/SkillFishOS/issues).

**Wo lade ich die ISO herunter?**
Auf der Seite [Herunterladen](/de/download) (die Dateien liegen auf SourceForge).
