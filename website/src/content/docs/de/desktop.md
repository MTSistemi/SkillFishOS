---
title: Schreibtisch, Gestaltung und Fernzugriff
description: KDE Plasma 6, die Steampunk-Gestaltung, das System-HUD, die Sperre des Ruhezustands und der Zugriff aus der Ferne.
group: System
order: 4
---

SkillFishOS benutzt **[KDE Plasma 6](https://kde.org/plasma-desktop/)** als Arbeitsumgebung, eingekleidet in eine durchgehende Steampunk-Gestaltung und eine Reihe von Anpassungen speziell für die BC-250.

## Sitzungen

Auf dem Anmeldebildschirm (dafür sorgt **SDDM**, mit automatischer Anmeldung) stehen mehrere Sitzungen bereit:

- **KDE Plasma X11** — *Vorgabe*. Mit X11 wird der Fernzugriff zur Kleinigkeit (siehe unten);
- **KDE Plasma Wayland** — wählbar;
- **Gaming** — eine [gamescope](https://github.com/ValveSoftware/gamescope)-Sitzung im Stil von Big Picture (siehe [Spiele](/de/docs/gaming)).

## **Achtung:** Sperre des Ruhezustands (entscheidend)

Bei der BC-250 ist der **ACPI-Ruhezustand kaputt**: schläft sie ein, **wacht sie nicht wieder auf** und braucht einen harten Neustart (siehe [Hardware](/de/docs/hardware-bc250)). Deshalb schaltet SkillFishOS alle Schlafzustände **dauerhaft ab**:

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

Dazu kommen eine `logind`-Regel (`IdleAction=ignore`), das abgeschaltete automatische Sperren des Bildschirms und eine Energieverwaltung mit „unendlicher“ Leerlaufzeit. Das ist eine **zwingende** Maßnahme: eine schlafende Maschine ist obendrein aus der Ferne nicht erreichbar.

## Gestaltung „SkillFish Steampunk“

Das Erscheinungsbild ist eine abgestimmte Messing- und Kupferpalette (Akzent **`#d8a849`**, dunkle Flächen) und bleibt **vom Start bis zum Schreibtisch** gleich: GRUB-Gestaltung, Plymouth-Startbild, SDDM-Begrüßung, Hintergrundbild mit dem Fisch. Das Gestaltungspaket enthält:

- **Symbole** (`SkillFishSteampunk`, mit `breeze-dark` als Rückfall) und eigene **Mauszeiger**;
- einen **Kvantum**-Stil für Qt-Anwendungen und ein **Farbschema** für KDE;
- ein **Plasma-Design**, ein **Konsole**-Design, Fensterknöpfe und ein gesamtes **Erscheinungsbild** (`org.skillfish.steampunk`);
- passend gestaltete Benutzerbilder und eine Auswahl zum Wechseln.

> Die mitgelieferten **Breeze**-Designs bleiben als tragender Rückfall installiert (sie liefern insbesondere den Dialog zum Abmelden und Ausschalten). Sie dürfen nicht entfernt werden.

## System-HUD (Conky)

Oben rechts sitzt ein messingfarbenes **HUD**, gebaut mit **[Conky](https://github.com/brndnmtthws/conky)**, das in Echtzeit zeigt: CPU-Balken je Kern mit MHz, °C und Watt, Takt, Temperatur und Grafikspeicher der GPU, Arbeitsspeicher, Platte, Lüfter und die **verbundenen Bluetooth-Geräte** mit ihrem Ladestand (Controller, Kopfhörer …). Die Werte kommen von eigenen Helfern, die die Sensoren der Hardware direkt auslesen.

## Zugriff aus der Ferne (x11vnc)

Weil die voreingestellte Sitzung X11 ist, ist der Fernzugriff einfach: SkillFishOS startet **[x11vnc](https://github.com/LibVNC/x11vnc)** auf dem aktiven Bildschirm und teilt das echte Bild. Im eigenen Netz kann sich jeder VNC-Client verbinden. So lässt sich von einem anderen Rechner aus helfen und einrichten, ohne Tastatur und Maus an der Platine.

## Netzwerk, Ton und Anwendungen

- **Netzwerk**: um die Kabelverbindung kümmert sich der **NetworkManager**, sie ist also aus den Plasma-Fenstern heraus sichtbar und einstellbar.
- **Ton**: ein vollständiger **[PipeWire](https://pipewire.org/)**-Aufbau (mit Bluetooth-Unterstützung). Achtung: *aktive* DP→HDMI-Adapter können den Ton zerstören — siehe [Fehlersuche](/de/docs/risoluzione-problemi).
- **Grundanwendungen**: Dateiverwaltung Dolphin, Terminal Konsole, PDF-Betrachter Okular, Bildbetrachter Gwenview, Archivprogramm Ark, Bildschirmfotos mit Spectacle, Anwendungsverwaltung Discover (mit flatpak), Browser **Google Chrome**, **OnlyOffice**.
- **Eigene SkillFishOS-Anwendungen** (im Menü **„SkillFishOS“** zusammengefasst, jede als `.deb` aus der signierten Paketquelle installierbar und aktualisierbar): **Tuner** (Steuerung von Übertaktung, Undervolting, Lüfter und CU der BC-250), **AI** (lokales Sprachmodell auf der eingebauten GPU, bei Bedarf), **Monitor** (Kurven in Echtzeit für Temperatur, Takt, Spannung und Lüfter), **Kernel Manager** (Startkernel wählen und alte entfernen), **ISO Mount**, **Hub** — die Anwendungsverwaltung im Stil von Discover (APT + Flatpak + Snap) mit Anwendungsseiten, Bilderkarussell und Verwaltung der Quellen — dazu **Base** (Hardware-Wachhund und Einfrier-Melder mit Meldung auf dem Schreibtisch) und **Console**, eine Sitzung **„SkillFishOS Console (Big Picture)“** im Stil von SteamOS, wählbar auf dem Anmeldebildschirm.
- **Bildschirm**: ein Dienst (`skillfish-dp-hotswap`) übernimmt die Erkennung des Bildschirms — nötig, weil das HPD des DisplayPort defekt ist.

## Quellen

- [KDE Plasma](https://kde.org/plasma-desktop/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [Conky](https://github.com/brndnmtthws/conky) · [x11vnc](https://github.com/LibVNC/x11vnc)
- [PipeWire](https://pipewire.org/) · [SDDM](https://github.com/sddm/sddm)
- [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/) · [NetworkManager](https://networkmanager.dev/)
