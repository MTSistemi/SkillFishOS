---
title: Aktualisierungen und Paketquelle
description: Wie sich SkillFishOS sicher aktualisiert, ohne von Debian sid zerlegt zu werden.
group: Benutzung
order: 4
---

SkillFishOS baut auf **Debian sid** (*unstable*) auf, dem Entwicklungszweig von Debian: immer aktuell, aber naturgemäß hin und wieder von Rückschritten betroffen. Auf ungewöhnlicher Hardware wie der BC-250 kann eine schlechte Aktualisierung (von Mesa, der Firmware oder des Kernels) das System zerlegen. SkillFishOS begegnet dem mit zwei Mitteln.

## 1. Eigene Bestandteile aus einer eigenen Paketquelle

Die heikelsten Teile bauen und verteilen **wir selbst**, aus einer **eigenen, signierten APT-Paketquelle**:

- den optimierten **[Kernel](/de/docs/kernel)** (Abbild und Header);
- den **SMU-Governor** und die Werkzeuge zur Übertaktung;
- die **eigenen Anwendungen** [Tuner und AI](/de/docs/app-native);
- die **Steampunk-Gestaltung** und das **Erscheinungsbild**;
- die Systemkonfiguration.

Einen Bestandteil aus der eigenen Paketquelle auszuliefern heißt, dass wir ihn **vorher prüfen** können, auf der echten Hardware, und ihn **nur dann aktualisieren, wenn es etwas bringt** — nicht immer dann, wenn sich flussaufwärts etwas ändert.

## 2. Die empfindlichen Pakete „festnageln“

Für Pakete, die von Debian kommen, auf dieser Hardware aber heikel sind, benutzt SkillFishOS das **Festnageln von APT** (*pinning*): sie bleiben auf einer **geprüften** Fassung, bis wir eine neuere getestet haben. Die wichtigsten Kandidaten dafür sind:

- **Mesa und die Vulkan-Treiber (RADV)** — eine Aktualisierung kann `gfx1013` verschlechtern;
- **AMD-Firmware / `linux-firmware`** — der Mikrocode der GPU;
- **der Standardkernel von Debian** — um die bekannt heiklen Fassungen zu sperren (siehe [Kernel](/de/docs/kernel));
- **KDE Plasma** — um keiner unruhigen Auslieferung aufzusitzen.

So kommen die „gewöhnlichen“ Aktualisierungen (der weitaus größte Teil des Systems) weiterhin regelmäßig an, während die Handvoll Pakete, die alles zerlegen könnten, auf Fassungen stehen bleibt, von denen wir wissen, dass sie laufen.

## Wie man aktualisiert

Wie bei jedem Debian-System, aus dem Terminal:

```bash
sudo apt update && sudo apt full-upgrade
```

… oder über die grafische Anwendung **Discover**, oder über den **SkillFishOS Hub** — unsere Anwendungsverwaltung im Stil von Discover, die an einer Stelle über **APT, Flatpak und Snap** installiert, entfernt und aktualisiert, mit Blättern nach Kategorien, Anwendungsseiten samt Bilderkarussell und einem „Alles aktualisieren“ mit einem Klick. Dank der Haken von [Snapper](/de/docs/storage-snapshot) entsteht **vor und nach** jeder Aktualisierung ein Btrfs-Schnappschuss: geht etwas schief, stellt die Rückkehr aus dem GRUB-Menü den vorherigen Stand wieder her.

> Kurz gesagt: **wir** liefern einen geprüften Kernel, geprüfte Anwendungen und Gestaltung; **Debian** liefert die übrige aktuelle Software; das **Festnageln** verhindert Überraschungen; **Btrfs** ist das Sicherheitsnetz. Drei Schutzschichten, damit Aktualisieren keine Angst macht.

## Die offizielle Paketquelle

Die APT-Paketquelle von SkillFishOS ist **in Betrieb**, mit GPG signiert und auf **GitHub Pages** untergebracht (Suite `aetherium`):

```bash
# 1. den Signaturschlüssel holen
sudo curl -fsSL https://mtsistemi.github.io/SkillFishOS/skillfishos-archive-keyring.gpg \
  -o /usr/share/keyrings/skillfishos-archive-keyring.gpg
# 2. die Paketquelle eintragen
echo "deb [signed-by=/usr/share/keyrings/skillfishos-archive-keyring.gpg] \
https://mtsistemi.github.io/SkillFishOS aetherium main" \
  | sudo tee /etc/apt/sources.list.d/skillfishos.list
# 3. den Kernel über apt installieren oder aktualisieren
sudo apt update && sudo apt install skillfishos-kernel
```

Neuere SkillFishOS-Abbilder bringen sie **fertig eingerichtet** mit; sonst richten die Befehle oben alles ein. Der [Kernel](/de/docs/kernel) (Abbild von 152 MB) wird als *release asset* auf GitHub veröffentlicht: das winzige Paket `skillfishos-kernel` lädt und installiert ihn von selbst, die Aktualisierung läuft also weiterhin über `apt`. Verwaltet wird die Paketquelle mit **[reprepro](https://salsa.debian.org/debian/reprepro)**, und der Client prüft die Signatur über den eigenen *keyring*.

## Quellen

- [Debian unstable (sid)](https://wiki.debian.org/DebianUnstable)
- [APT-Pinning — Debian-Handbuch](https://wiki.debian.org/AptConfiguration)
- [reprepro](https://salsa.debian.org/debian/reprepro) — Verwaltung der APT-Paketquelle
- [Snapper](http://snapper.io/) — Schnappschüsse vor und nach APT
