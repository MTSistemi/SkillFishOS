---
title: Installation
description: Wie du die ISO schreibst, das Installationsprogramm startest und die Einrichtung abschließt.
group: Installation
order: 1
---

SkillFishOS wird von einer **Live-ISO** installiert, die das grafische Installationsprogramm [Calamares](https://calamares.io/) enthält. Der ganze Ablauf geht mit der Maus, ein Terminal ist nicht nötig.

> Die ISO **26.06.4 „Aetherium“** ist verfügbar — lade sie von der Seite [Herunterladen](/de/download). Sie startet auf **Englisch**, um überall zu passen, und lässt dich Sprache und Tastaturbelegung während der Installation wählen.

## Voraussetzungen

- eine **AMD-BC-250**-Platine (siehe [Hardware](/de/docs/hardware-bc250));
- eine **SSD oder NVMe**, auf die installiert wird;
- ein Bildschirm über **DisplayPort** (ein *passiver* DP→HDMI-Adapter kann gehen, siehe aber die Hinweise zu Bild und Ton unter [Fehlersuche](/de/docs/risoluzione-problemi));
- ein **USB-Stick mit mindestens 8 GB** für das Installationsprogramm;
- Tastatur und Maus für die Installation.

## 1. Die ISO auf den Stick schreiben

Lade die ISO von der Seite [Herunterladen](/de/download) und schreibe sie mit einem dieser Werkzeuge auf einen Stick:

- **[balenaEtcher](https://etcher.balena.io/)** (Windows/macOS/Linux, mit Fenster, empfohlen);
- **[Ventoy](https://www.ventoy.net/)** (erlaubt mehrere ISOs auf demselben Stick);
- aus einem Linux-Terminal mit `dd`:

```bash
sudo dd if=SkillFishOS_amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

> Ersetze `/dev/sdX` durch das richtige Gerät deines Sticks. **Achtung**: `dd` schreibt ohne Rückfrage und löscht alles auf dem Ziel.

## 2. Die BC-250 vom Stick starten

Steck den Stick an, schalte die Platine ein und geh ins Start- oder UEFI-Menü, um den USB-Stick als Startgerät zu wählen. Die **Live**-Umgebung von SkillFishOS (KDE Plasma) fährt hoch: du kannst dich im System umsehen, bevor du es installierst.

## 3. Mit Calamares installieren

Starte vom Live-Schreibtisch aus das Installationsprogramm (Symbol *Install SkillFishOS*). Calamares führt dich Schritt für Schritt:

1. **Sprache und Zeitzone.**
2. **Tastatur.**
3. **Aufteilung der Platte.** SkillFishOS verwendet **Btrfs** mit getrennten Unterbänden: `@` (System), `@home` (deine Daten), `@cache` und `@log` (aus den Schnappschüssen herausgehalten), `@games` (die Spielesammlung). So lässt sich das System *zurückrollen*, ohne deine Dateien anzufassen. Eine kleine **EFI**-Partition vervollständigt das Bild, und die Auslagerung ist eine **Datei**, keine Partition. Für die meisten reicht die automatische Variante („Platte löschen“).
4. **Benutzer.** Leg dein Konto an (es landet in den richtigen Gruppen für Spiele, Ton, Grafik und so weiter).
5. **Zusammenfassung und Installation.**

Wenn die Installation fertig ist, starte neu und zieh den Stick ab.

## 4. Erster Start

Beim ersten Start ist **alles schon eingerichtet**: optimierter Kernel, Governor, Übertaktung, Gestaltung, Spiele und Schnappschüsse sind aktiv. Von Hand ist nichts nachzustellen.

Von hier aus kannst du:

- deine [Controller](/de/docs/gaming) koppeln (DualShock 4 über Bluetooth oder einen Controller über USB);
- deine Spiele zu [Steam oder EmuDeck](/de/docs/gaming) hinzufügen;
- die [lokale KI](/de/docs/ai-locale) einschalten, wenn du sie brauchst;
- die Hardware mit dem [Tuner](/de/docs/app-native) feinjustieren, wenn du magst.

## Aufteilung der Platte

| Partition | Dateisystem | Inhalt |
|---|---|---|
| `nvme0n1p1` | FAT32 (EFI) | GRUB-Startverwalter |
| `nvme0n1p2` | **Btrfs** | `@` (System) · `@home` (Daten) · `@cache` · `@log` · `@games` · `@swap` |

Eine Auslagerungspartition gibt es nicht: die Auslagerung ist eine **Datei** im Unterband `@swap`. Auf Btrfs lässt sie sich vergrößern, ohne die Partitionstabelle anzufassen, und sie bleibt außerhalb der Schnappschüsse.

## Quellen

- [Calamares](https://calamares.io/) — das universelle Installationsprogramm
- [balenaEtcher](https://etcher.balena.io/) · [Ventoy](https://www.ventoy.net/)
- [Btrfs-Wiki](https://btrfs.readthedocs.io/) — Unterbände und Schnappschüsse
