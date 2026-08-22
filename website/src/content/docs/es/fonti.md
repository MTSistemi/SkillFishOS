---
title: Fuentes y referencias
description: Todas las fuentes, proyectos originales y herramientas sobre los que se apoya SkillFishOS.
group: Referencia
order: 6
---

SkillFishOS es un trabajo de integración: reúne el esfuerzo de muchas comunidades y proyectos de código abierto. Esta página recoge las fuentes citadas en la documentación y los proyectos sobre los que se levanta el sistema.

## Documentación del hardware BC-250

- **[bc250.info](https://bc250.info)** — wiki comunitaria sobre la placa BC-250.
- **[elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)** — documentación técnica detallada.

## Proyectos específicos de la BC-250

- **[cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor)** — gobernador SMU para las frecuencias de la GPU.
- **[bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc)** — overclock y undervolt por la SMU.
- **[bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock)** — desbloqueo de los 8 núcleos de la CPU.
- **[bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)** — desbloqueo de las 40 unidades de cómputo.
- **[bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg)** — configuración de la memoria.

## Refrigeración y cajas imprimibles en 3D (STL gratuitos)

- **[Console Style Case (Arthrimus)](https://www.thingiverse.com/thing:7172528)** — caja con fuente y carenado de 120 mm.
- **[ASRock BC-250 Shell Case (onemorecap)](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case)** — carcasa a presión.
- **[Yet Another BC-250 Fan Shroud (ViRazY)](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud)** — de 140 y 120 mm.
- **[Case ATX PSU & Fan Duct (ZMASLO)](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct)** — conducto y fuente ATX.
- **[ATX PSU case (CatSiewDai)](https://www.thingiverse.com/thing:7269520)** — caja completa.
- **[OC vRAM Fan Kit (marccyberwiz)](https://www.thingiverse.com/thing:7271946)** — ventilador dedicado a la VRAM.
- **[Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/)** · **[mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation)** — guías de refrigeración.

## Base del sistema

- **[Debian](https://www.debian.org/)** — la distribución base (rama *sid*).
- **[KDE Plasma](https://kde.org/plasma-desktop/)** — el entorno de escritorio.
- **[linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)** — receta de compilación del núcleo.
- **[Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)** — controladores gráficos Vulkan de código abierto.
- **[controlador amdgpu](https://docs.kernel.org/gpu/amdgpu/)** — controlador de AMD en el núcleo.

## Almacenamiento e instantáneas

- **[Btrfs](https://btrfs.readthedocs.io/)** · **[Snapper](http://snapper.io/)** · **[grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)**

## Escritorio, tema y acceso remoto

- **[Kvantum](https://github.com/tsujan/Kvantum)** · **[Conky](https://github.com/brndnmtthws/conky)** · **[x11vnc](https://github.com/LibVNC/x11vnc)**
- **[PipeWire](https://pipewire.org/)** · **[SDDM](https://github.com/sddm/sddm)** · **[Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/)** · **[NetworkManager](https://networkmanager.dev/)**

## Juegos y emulación

- **[Steam](https://store.steampowered.com/)** · **[gamescope](https://github.com/ValveSoftware/gamescope)** · **[gamemode](https://github.com/FeralInteractive/gamemode)** · **[MangoHud](https://github.com/flightlessmango/MangoHud)**
- **[Heroic Games Launcher](https://heroicgameslauncher.com/)** · **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** · **[Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)**
- **[EmuDeck](https://www.emudeck.com/)** · **[ES-DE](https://es-de.org/)** · **[RetroArch](https://www.retroarch.com/)**
- **[Waydroid](https://waydro.id/)** · **[Sober](https://sober.vinegarhq.org/)** · **[OptiScaler](https://github.com/optiscaler/OptiScaler)**

## IA local

- **[Unsloth](https://unsloth.ai/)** · **[llama.cpp](https://github.com/ggml-org/llama.cpp)** · **[Hugging Face](https://huggingface.co/)**

## Herramientas e infraestructura

- **[Calamares](https://calamares.io/)** — instalador.
- **[balenaEtcher](https://etcher.balena.io/)** · **[Ventoy](https://www.ventoy.net/)** — escritura de la ISO.
- **[reprepro](https://salsa.debian.org/debian/reprepro)** — repositorio APT.
- **[Flatpak](https://flatpak.org/)** — empaquetado de aplicaciones.
- **[vkpeak](https://github.com/nihui/vkpeak)** · **[clpeak](https://github.com/krrishnarraj/clpeak)** · **[sysbench](https://github.com/akopytov/sysbench)** — pruebas de rendimiento.

## El proyecto

- **Código y documentación** — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS)
- **Sitio web** — [skillfishos.com](https://skillfishos.com)

---

> SkillFishOS no está afiliado a AMD. «AMD», «Ryzen», «RDNA» y las marcas relacionadas pertenecen a Advanced Micro Devices, Inc. Las demás marcas citadas pertenecen a sus respectivos dueños.
