---
title: Spiele und Emulation
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android und Controller.
group: Benutzung
order: 1
---

SkillFishOS ist zum Spielen entstanden. Die gesamte Spiele-Ausstattung ist vorinstalliert und eingerichtet; du bringst **deine** Spiele und **deine** ROMs mit.

## Steam und Proton

**Steam** (über [Flatpak](https://flatpak.org/)) ist mit **[gamescope](https://github.com/ValveSoftware/gamescope)** (dem Mikro-Compositor von Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** und **[MangoHud](https://github.com/flightlessmango/MangoHud)** verbunden. Eine eigene **Konsolensitzung** (gamescope, im Stil von Big Picture) lässt sich auf dem Anmeldebildschirm wählen. Windows-Spiele laufen über **Proton**.

## Spiele außerhalb von Steam: Heroic

Der **[Heroic Games Launcher](https://heroicgameslauncher.com/)** verwaltet Titel von **Epic Games** und **GOG** und Windows-Spiele über **GE-Proton**. Mit **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** installierst du Proton- und Wine-Fassungen ohne Umstände. Spiele aus Heroic lassen sich zu Steam hinzufügen (samt Titelbildern).

## Emulation: EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** installiert und richtet mit wenigen Klicks eine vollständige Sammlung von Emulatoren (Flatpak) ein: **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** und weitere. Die Oberfläche ist **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

Unter SkillFishOS kann der Ordner `~/Emulation` auf einen **NAS** im Netz zeigen (BIOS-Dateien, ROMs und Spielstände über mehrere Rechner hinweg geteilt).

> **Achtung:** ES-DE schreibt seine Einstellungsdatei beim Beenden neu: ändere sie, während das Programm **geschlossen** ist.
>
> **Achtung:** Bei **Ryujinx** bringt der Benutzer Firmware und Schlüssel selbst ein: die Firmware erwartet jedes NCA als Verzeichnis. **Spiele, ROMs, BIOS-Dateien und Schlüssel sind nicht enthalten** — eine bewusste rechtliche Entscheidung: SkillFishOS liefert die Werkzeuge, die Inhalte bringst du mit.

## Android und mehr

- **[Waydroid](https://waydro.id/)** für Android-Anwendungen und -Spiele (binder im Kernel, iptables-Unterstützung und ARM-Bibliotheken);
- **[Sober](https://sober.vinegarhq.org/)** als Roblox-Abspieler — nicht vorinstalliert, hol ihn aus der Anwendungsverwaltung mit `flatpak install flathub org.vinegarhq.Sober`. Es ist eine Anwendung von 18 MB, die 1,1 GB GNOME-Bibliotheken nach sich zieht: gerade weil sie draußen bleibt, bleibt die ISO klein.

> Hinweis: Lokale KI und Android sollten nicht zusammen mit anspruchsvollen Spielen laufen, weil sie sich dieselbe GPU und denselben Speicher teilen.

## Controller

Die empfohlene, erprobte Zusammenstellung:

- **2× DualShock 4 über Bluetooth** — mit Lagesensor (nützlich für Bewegungssteuerung, etwa bei Mario Kart), verbunden mit dem eingebauten Realtek-Adapter;
- **Controller über USB** — mit einem **Datenkabel** erscheint er als Xbox 360 (Treiber `xpad`, XInput), ohne Lagesensor.

Die Treiber `xpad`, `hid_playstation` und `hid_nintendo` stecken im Kernel. Um einen DS4 neu zu koppeln: *Share + PS* gedrückt halten, bis er blinkt, dann im Bluetooth-Fenster koppeln.

## Hochskalieren

**FSR 4 gibt es auf der BC-250 nicht** (es verlangt RDNA-4-Hardware). Die Alternativen sind das Hochskalieren in **gamescope** (FSR1/NIS) oder **[OptiScaler](https://github.com/optiscaler/OptiScaler)** für einzelne Spiele. Bei Titeln, die an der *CPU* hängen (etwa *Black Myth: Wukong*), hilft weder eine niedrigere Auflösung noch ein niedrigerer GPU-Takt — siehe [GPU und Übertaktung](/de/docs/gpu-overclock).

## Quellen

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)
