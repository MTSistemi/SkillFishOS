---
title: Nützliche Befehle
description: Ein Spickzettel fürs Terminal, um SkillFishOS zu untersuchen und einzustellen.
group: Nachschlagen
order: 4
---

SkillFishOS ist so gebaut, dass das Terminal **nicht** nötig ist: für den gewöhnlichen Gebrauch reichen der [Tuner](/de/docs/app-native) und die grafischen Anwendungen. Diese Seite ist für alle, die **basteln** oder auf Fehlersuche gehen wollen. Befehle mit erhöhten Rechten laufen über `sudo`.

> Denk vor riskanten Versuchen an das Sicherheitsnetz: Btrfs-Schnappschüsse und die Rückkehr aus dem GRUB-Menü (siehe [Speicher und Schnappschüsse](/de/docs/storage-snapshot)).

## System und Kernel

```bash
uname -r                      # laufender Kernel (sollte auf -skillfishos enden)
cat /proc/cmdline             # geltende Startparameter
journalctl -b -p err          # Fehler des aktuellen Starts
inxi -Fxxxz                   # vollständige Übersicht der Hardware
```

## GPU, Takte und Temperaturen

```bash
# GPU-Temperatur aus dem sysfs von amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# Zustand des SMU-Governors
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # sichere Punkte aus Takt und Spannung
# GPU in Echtzeit beobachten
nvtop        # oder: radeontop
```

> Auf der BC-250 läuft die Taktsteuerung **nicht** über das übliche sysfs von amdgpu, sondern über den **SMU-Governor**. Ändere die Werte im [Tuner](/de/docs/app-native), nicht von Hand.

## CPU — Übertaktung und Undervolting

```bash
systemctl status bc250-smu-oc.service   # dass er nach dem Anwenden „inactive“ ist, gehört so (er läuft einmalig)
cat /etc/bc250-smu-oc.conf              # angewandter Takt und angewandte Spannung
lscpu | grep MHz                        # aktuelle Kerntakte
sensors                                 # Temperaturen und Spannungen (nct6686, k10temp)
```

## Recheneinheiten im Betrieb (skillfish-cu)

```bash
skillfish-cu get          # Zustand als JSON: aktive CU und Maske je Reihe (SE/SH)
sudo skillfish-cu max     # alle CU in Betrieb nehmen (40)
sudo skillfish-cu stock   # zurück auf 24 (Grundwert des Treibers)
sudo skillfish-cu set 0x1f   # WGP-Maske für alle Reihen (0x07=24 … 0x1f=40)
cat /run/skillfish/cu_active # „40/40“ (das liest auch das HUD)
vulkaninfo | grep -i "deviceName\|driverName"   # die GPU, wie Vulkan sie sieht (RADV)
```

Die CU verwaltet man am besten über das **Raster** im [Tuner](/de/docs/app-native) (Klick und Vorgaben, mit der „CU-Prüfung“). Die ersten 24 sind vom Treiber festgelegt und immer an.

Schnelle Messungen (dieselben, die der Tuner benutzt):

```bash
vkpeak                # FP32-Leistung (GFLOPS)
clpeak                # Speicherbandbreite (GB/s)
sysbench cpu run      # Last und Messung für die CPU
```

## Einheitlicher Speicher (Grafikspeicher und GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'ttm\.'   # Parameter zu GTT/TTM
glxinfo | grep -i "memory"                                 # Speicher, wie der Treiber ihn sieht
free -h                                                     # gemeinsamer RAM/GDDR6
```

## Spiele

```bash
flatpak list                         # Flatpak-Anwendungen (Steam, Emulatoren von EmuDeck …)
flatpak update                        # die Flatpak-Anwendungen aktualisieren
gamescope -- %command%               # (in den Startoptionen von Steam eintragen)
# Controller über Bluetooth
bluetoothctl                         # scan on / pair / connect / trust
```

## Lokale KI

```bash
# ein einziger nativer Dienst, keine Container: Docker ist nicht installiert
systemctl status skillfish-unsloth   # Zustand des KI-Motors
sudo systemctl start skillfish-unsloth   # starten
sudo systemctl stop skillfish-unsloth    # anhalten und GPU sowie Speicher freigeben
curl -s localhost:8888/              # die Oberfläche von Unsloth Studio (nur Loopback)
```

## Schnappschüsse und Rückkehr (Btrfs)

```bash
sudo snapper list                    # Schnappschüsse auflisten
sudo snapper create -d "vor X"       # Schnappschuss von Hand
sudo btrfs subvolume list /          # Unterbände (@, @home, @log, @cache, @games)

# wirklich zu einem Schnappschuss zurück (gilt ab dem nächsten Start)
sudo skillfish-rollback --list       # welche Schnappschüsse es gibt
sudo skillfish-rollback 12           # Schnappschuss 12 zum laufenden System machen
sudo skillfish-rollback --undo       # anders überlegt: den alten zurückholen
sudo skillfish-rollback --clean      # die von früheren Rückkehren beiseitegelegten Systeme entfernen

# über das GRUB-Menü → „SkillFishOS snapshots“ bekommst du denselben Schnappschuss
# NUR LESBAR: gut zum Umsehen und Retten von Dateien, danach den Befehl oben ausführen
```

## Aktualisierungen und Paketquelle

```bash
sudo apt update && sudo apt full-upgrade   # das System aktualisieren
apt-mark showhold                          # festgehaltene Pakete (samt Kernel)
sudo apt install skillfishos-kernel        # den Kernel aus der Paketquelle installieren oder aktualisieren
apt policy <Paket>                          # aus welcher Paketquelle und in welcher Fassung ein Paket kommt
```

## Netzwerk und Fernzugriff

```bash
nmcli device status                  # Zustand der Netzwerkgeräte
ip a                                 # IP-Adressen
systemctl status x11vnc              # VNC-Server für den entfernten Schreibtisch
hostname -I                          # IP für den VNC-Client
```

## Bildschirm (HPD des DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # Dienst, der das defekte HPD umgeht
xrandr                                   # Ausgänge und Auflösungen (X11-Sitzung)
```

## Quellen

- [Btrfs-Wiki](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — Nachschlagewerk für viele Linux-Befehle
