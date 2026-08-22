---
title: Quellen und Verweise
description: Alle Quellen, Ursprungsprojekte und Werkzeuge, auf denen SkillFishOS aufbaut.
group: Nachschlagen
order: 6
---

SkillFishOS ist eine Arbeit des Zusammenführens: es bringt die Mühe vieler quelloffener Gemeinschaften und Projekte zusammen. Diese Seite sammelt die in der Dokumentation genannten Quellen und die Projekte, auf denen das System ruht.

## Dokumentation zur BC-250-Hardware

- **[bc250.info](https://bc250.info)** — Wiki der Gemeinschaft rund um die Platine BC-250.
- **[elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)** — ausführliche technische Dokumentation.

## Projekte eigens für die BC-250

- **[cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor)** — SMU-Governor für die Takte der GPU.
- **[bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc)** — Übertaktung und Undervolting über die SMU.
- **[bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock)** — Freischalten der 8 CPU-Kerne.
- **[bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)** — Freischalten der 40 Recheneinheiten.
- **[bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg)** — Einrichtung des Speichers.

## Kühlung und im 3D-Druck herstellbare Gehäuse (kostenlose STL)

- **[Console Style Case (Arthrimus)](https://www.thingiverse.com/thing:7172528)** — Gehäuse mit Netzteil und 120-mm-Haube.
- **[ASRock BC-250 Shell Case (onemorecap)](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case)** — aufsteckbare Schale.
- **[Yet Another BC-250 Fan Shroud (ViRazY)](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud)** — 140 und 120 mm.
- **[Case ATX PSU & Fan Duct (ZMASLO)](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct)** — Luftführung und ATX-Netzteil.
- **[ATX PSU case (CatSiewDai)](https://www.thingiverse.com/thing:7269520)** — vollständiges Gehäuse.
- **[OC vRAM Fan Kit (marccyberwiz)](https://www.thingiverse.com/thing:7271946)** — eigener Lüfter für den Grafikspeicher.
- **[Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/)** · **[mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation)** — Anleitungen zur Kühlung.

## Grundlage des Systems

- **[Debian](https://www.debian.org/)** — die zugrunde liegende Distribution (Zweig *sid*).
- **[KDE Plasma](https://kde.org/plasma-desktop/)** — die Arbeitsumgebung.
- **[linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)** — Baurezept für den Kernel.
- **[Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)** — quelloffene Vulkan-Grafiktreiber.
- **[amdgpu-Treiber](https://docs.kernel.org/gpu/amdgpu/)** — Treiber von AMD im Kernel.

## Speicher und Schnappschüsse

- **[Btrfs](https://btrfs.readthedocs.io/)** · **[Snapper](http://snapper.io/)** · **[grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)**

## Arbeitsfläche, Gestaltung und Fernzugriff

- **[Kvantum](https://github.com/tsujan/Kvantum)** · **[Conky](https://github.com/brndnmtthws/conky)** · **[x11vnc](https://github.com/LibVNC/x11vnc)**
- **[PipeWire](https://pipewire.org/)** · **[SDDM](https://github.com/sddm/sddm)** · **[Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/)** · **[NetworkManager](https://networkmanager.dev/)**

## Spiele und Emulation

- **[Steam](https://store.steampowered.com/)** · **[gamescope](https://github.com/ValveSoftware/gamescope)** · **[gamemode](https://github.com/FeralInteractive/gamemode)** · **[MangoHud](https://github.com/flightlessmango/MangoHud)**
- **[Heroic Games Launcher](https://heroicgameslauncher.com/)** · **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** · **[Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)**
- **[EmuDeck](https://www.emudeck.com/)** · **[ES-DE](https://es-de.org/)** · **[RetroArch](https://www.retroarch.com/)**
- **[Waydroid](https://waydro.id/)** · **[Sober](https://sober.vinegarhq.org/)** · **[OptiScaler](https://github.com/optiscaler/OptiScaler)**

## Örtliche KI

- **[Unsloth](https://unsloth.ai/)** · **[llama.cpp](https://github.com/ggml-org/llama.cpp)** · **[Hugging Face](https://huggingface.co/)**

## Werkzeuge und Unterbau

- **[Calamares](https://calamares.io/)** — Installationsprogramm.
- **[balenaEtcher](https://etcher.balena.io/)** · **[Ventoy](https://www.ventoy.net/)** — Schreiben des Abbilds.
- **[reprepro](https://salsa.debian.org/debian/reprepro)** — APT-Paketquelle.
- **[Flatpak](https://flatpak.org/)** — Paketierung von Anwendungen.
- **[vkpeak](https://github.com/nihui/vkpeak)** · **[clpeak](https://github.com/krrishnarraj/clpeak)** · **[sysbench](https://github.com/akopytov/sysbench)** — Messungen.

## Das Projekt

- **Quelltext und Dokumentation** — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS)
- **Netzseite** — [skillfishos.com](https://skillfishos.com)

---

> SkillFishOS steht in keiner Verbindung zu AMD. „AMD“, „Ryzen“, „RDNA“ und die zugehörigen Marken gehören Advanced Micro Devices, Inc. Alle weiteren genannten Marken gehören ihren jeweiligen Inhabern.
