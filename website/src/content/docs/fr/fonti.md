---
title: Sources et références
description: Toutes les sources, les projets d'origine et les outils sur lesquels SkillFishOS s'appuie.
group: Référence
order: 6
---

SkillFishOS est un travail d'assemblage : il réunit l'effort de nombreuses communautés et de nombreux projets libres. Cette page rassemble les sources citées dans la documentation et les projets sur lesquels le système repose.

## La documentation du matériel BC-250

- **[bc250.info](https://bc250.info)** — le wiki communautaire sur la carte BC-250.
- **[elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)** — une documentation technique détaillée.

## Les projets propres à la BC-250

- **[cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor)** — le gouverneur SMU pour les fréquences du GPU.
- **[bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc)** — overclock et undervolt par la SMU.
- **[bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock)** — le déverrouillage des 8 cœurs du CPU.
- **[bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)** — le déverrouillage des 40 unités de calcul.
- **[bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg)** — la configuration de la mémoire.

## Refroidissement et boîtiers imprimables en 3D (STL gratuits)

- **[Console Style Case (Arthrimus)](https://www.thingiverse.com/thing:7172528)** — boîtier avec alimentation et capot de 120 mm.
- **[ASRock BC-250 Shell Case (onemorecap)](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case)** — une coque à clipser.
- **[Yet Another BC-250 Fan Shroud (ViRazY)](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud)** — en 140 et 120 mm.
- **[Case ATX PSU & Fan Duct (ZMASLO)](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct)** — conduit et alimentation ATX.
- **[ATX PSU case (CatSiewDai)](https://www.thingiverse.com/thing:7269520)** — un boîtier complet.
- **[OC vRAM Fan Kit (marccyberwiz)](https://www.thingiverse.com/thing:7271946)** — un ventilateur dédié à la mémoire graphique.
- **[Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/)** · **[mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation)** — des guides de refroidissement.

## La base du système

- **[Debian](https://www.debian.org/)** — la distribution de base (branche *sid*).
- **[KDE Plasma](https://kde.org/plasma-desktop/)** — l'environnement de bureau.
- **[linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)** — la recette de compilation du noyau.
- **[Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)** — les pilotes graphiques Vulkan libres.
- **[le pilote amdgpu](https://docs.kernel.org/gpu/amdgpu/)** — le pilote d'AMD dans le noyau.

## Stockage et instantanés

- **[Btrfs](https://btrfs.readthedocs.io/)** · **[Snapper](http://snapper.io/)** · **[grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)** · **[Btrfs Assistant](https://gitlab.com/btrfs-assistant/btrfs-assistant)**

## Bureau, thème et accès à distance

- **[Kvantum](https://github.com/tsujan/Kvantum)** · **[Conky](https://github.com/brndnmtthws/conky)** · **[x11vnc](https://github.com/LibVNC/x11vnc)**
- **[PipeWire](https://pipewire.org/)** · **[SDDM](https://github.com/sddm/sddm)** · **[Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/)** · **[NetworkManager](https://networkmanager.dev/)**

## Jeu et émulation

- **[Steam](https://store.steampowered.com/)** · **[gamescope](https://github.com/ValveSoftware/gamescope)** · **[gamemode](https://github.com/FeralInteractive/gamemode)** · **[MangoHud](https://github.com/flightlessmango/MangoHud)**
- **[Heroic Games Launcher](https://heroicgameslauncher.com/)** · **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** · **[Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)**
- **[EmuDeck](https://www.emudeck.com/)** · **[ES-DE](https://es-de.org/)** · **[RetroArch](https://www.retroarch.com/)**
- **[Waydroid](https://waydro.id/)** · **[Sober](https://sober.vinegarhq.org/)** · **[OptiScaler](https://github.com/optiscaler/OptiScaler)**

## IA locale

- **[Unsloth](https://unsloth.ai/)** · **[llama.cpp](https://github.com/ggml-org/llama.cpp)** · **[Hugging Face](https://huggingface.co/)**

## Outils et infrastructure

- **[Calamares](https://calamares.io/)** — l'installateur.
- **[balenaEtcher](https://etcher.balena.io/)** · **[Ventoy](https://www.ventoy.net/)** — l'écriture de l'image.
- **[reprepro](https://salsa.debian.org/debian/reprepro)** — le dépôt APT.
- **[Flatpak](https://flatpak.org/)** — l'empaquetage des applications.
- **[vkpeak](https://github.com/nihui/vkpeak)** · **[clpeak](https://github.com/krrishnarraj/clpeak)** · **[sysbench](https://github.com/akopytov/sysbench)** — les mesures.

## Le projet

- **Code et documentation** — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS)
- **Site web** — [skillfishos.com](https://skillfishos.com)

---

> SkillFishOS n'est pas affilié à AMD. « AMD », « Ryzen », « RDNA » et les marques associées appartiennent à Advanced Micro Devices, Inc. Toutes les autres marques citées appartiennent à leurs propriétaires respectifs.
