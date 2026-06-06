---
title: Fonti e riferimenti
description: Tutte le fonti, i progetti upstream e gli strumenti su cui si basa SkillFishOS.
group: Riferimenti
order: 2
---

SkillFishOS è un lavoro di integrazione: mette insieme il lavoro di tante comunità e progetti open source. Questa pagina raccoglie le fonti citate nella documentazione e i progetti su cui il sistema si basa.

## Documentazione hardware BC-250

- **[bc250.info](https://bc250.info)** — wiki comunitaria sulla scheda BC-250.
- **[elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)** — documentazione tecnica dettagliata.

## Progetti specifici per la BC-250

- **[cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor)** — governor SMU per le frequenze GPU.
- **[bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc)** — overclock/undervolt via SMU.
- **[bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)** — sblocco delle 40 Compute Unit.
- **[bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg)** — configurazione della memoria.

## Raffreddamento e case 3D (STL gratuiti)

- **[Console Style Case (Arthrimus)](https://www.thingiverse.com/thing:7172528)** — case + PSU, shroud 120 mm.
- **[ASRock BC-250 Shell Case (onemorecap)](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case)** — guscio snap-on.
- **[Yet Another BC-250 Fan Shroud (ViRazY)](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud)** — 140 + 120 mm.
- **[Case ATX PSU & Fan Duct (ZMASLO)](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct)** — convogliatore + PSU ATX.
- **[Case per PSU ATX (CatSiewDai)](https://www.thingiverse.com/thing:7269520)** — case completo.
- **[OC vRAM Fan Kit (marccyberwiz)](https://www.thingiverse.com/thing:7271946)** — ventola dedicata alla VRAM.
- **[Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/)** · **[mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation)** — guide al raffreddamento.

## Base del sistema

- **[Debian](https://www.debian.org/)** — la distribuzione di base (ramo *sid*).
- **[KDE Plasma](https://kde.org/plasma-desktop/)** — l'ambiente desktop.
- **[linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)** — ricetta di compilazione del kernel.
- **[Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)** — driver grafici Vulkan open source.
- **[Driver amdgpu](https://docs.kernel.org/gpu/amdgpu/)** — driver kernel AMD.

## Storage e snapshot

- **[Btrfs](https://btrfs.readthedocs.io/)** · **[Snapper](http://snapper.io/)** · **[grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)** · **[Btrfs Assistant](https://gitlab.com/btrfs-assistant/btrfs-assistant)**

## Desktop, tema e remoto

- **[Kvantum](https://github.com/tsujan/Kvantum)** · **[Conky](https://github.com/brndnmtthws/conky)** · **[x11vnc](https://github.com/LibVNC/x11vnc)**
- **[PipeWire](https://pipewire.org/)** · **[SDDM](https://github.com/sddm/sddm)** · **[Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/)** · **[NetworkManager](https://networkmanager.dev/)**

## Gaming ed emulazione

- **[Steam](https://store.steampowered.com/)** · **[gamescope](https://github.com/ValveSoftware/gamescope)** · **[gamemode](https://github.com/FeralInteractive/gamemode)** · **[MangoHud](https://github.com/flightlessmango/MangoHud)**
- **[Heroic Games Launcher](https://heroicgameslauncher.com/)** · **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** · **[Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)**
- **[EmuDeck](https://www.emudeck.com/)** · **[ES-DE](https://es-de.org/)** · **[RetroArch](https://www.retroarch.com/)**
- **[Waydroid](https://waydro.id/)** · **[Sober](https://sober.vinegarhq.org/)** · **[OptiScaler](https://github.com/optiscaler/OptiScaler)**

## AI locale

- **[Ollama](https://ollama.com/)** · **[OpenWebUI](https://openwebui.com/)** · **[Dockge](https://github.com/louislam/dockge)**

## Strumenti e infrastruttura

- **[Calamares](https://calamares.io/)** — installer.
- **[balenaEtcher](https://etcher.balena.io/)** · **[Ventoy](https://www.ventoy.net/)** — scrittura ISO.
- **[reprepro](https://salsa.debian.org/debian/reprepro)** — repository APT.
- **[Flatpak](https://flatpak.org/)** — pacchettizzazione applicazioni.
- **[vkpeak](https://github.com/nihui/vkpeak)** · **[clpeak](https://github.com/krrishnarraj/clpeak)** · **[sysbench](https://github.com/akopytov/sysbench)** — benchmark.

## Il progetto

- **Codice e documentazione** — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS)
- **Sito** — [skillfishos.com](https://skillfishos.com)

---

> SkillFishOS non è affiliato ad AMD. "AMD", "Ryzen", "RDNA" e i relativi marchi appartengono ad Advanced Micro Devices, Inc. Tutti gli altri marchi citati appartengono ai rispettivi proprietari.
