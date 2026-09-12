---
title: Juegos y emulación
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android y mandos.
group: Uso
order: 1
---

SkillFishOS nació para jugar. Todo el conjunto para juegos viene instalado y configurado; tú añades **tus** juegos y **tus** ROMs.

## Nuestra Mesa (controlador Vulkan)

La sección **Juegos** del [Control Center](/es/docs/control-center) puede activar nuestra compilación de **Mesa/RADV**, que abre las colas de cómputo que el controlador de serie mantiene cerradas en esta GPU: medido **+4% en Cyberpunk 2077**, **+12% con FSR 4 activado**. Se aplica por lanzador (Steam, Heroic) mediante un override de flatpak, o para **todo el sistema** (escritorio incluido). Necesita el núcleo de SkillFishOS: en otro núcleo esas colas de cómputo cuelgan la GPU y el interruptor de sistema se niega a arrancar. Los programas de 32 bits se quedan con el controlador de Debian.

## Steam y Proton

**Steam** (mediante [Flatpak](https://flatpak.org/)) está integrado con **[gamescope](https://github.com/ValveSoftware/gamescope)** (el microcompositor de Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** y **[MangoHud](https://github.com/flightlessmango/MangoHud)**. Hay una **sesión de consola** propia (gamescope, al estilo Big Picture) que se elige en la pantalla de acceso. Los juegos de Windows funcionan con **Proton**: la sección Juegos del Control Center instala y pone por defecto **GE-Proton 11-6** y **GE-Proton 10-34**, compartidas entre Steam y Heroic.

## Juegos fuera de Steam: Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** gestiona los títulos de **Epic Games** y **GOG**, y los juegos de Windows con **GE-Proton**. Con **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** se instalan a mano otras versiones de Proton y Wine, además de las que ya instala el Control Center. Los juegos de Heroic se pueden añadir a Steam (con sus carátulas).

## Emulación: EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** instala y configura, en unos clics, un conjunto completo de emuladores (Flatpak): **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** y más. La interfaz es **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

En SkillFishOS la carpeta `~/Emulation` puede apuntar a un **NAS** en red (BIOS, ROMs y partidas guardadas compartidas entre máquinas).

> **Aviso:** ES-DE reescribe su archivo de ajustes al salir: edítalo con el programa **cerrado**.
>
> **Aviso:** para **Ryujinx**, el firmware y las claves los importa el usuario: el firmware espera cada NCA como un directorio. **Los juegos, las ROMs, las BIOS y las claves no vienen incluidos** en el sistema — es una decisión legal deliberada: SkillFishOS pone las herramientas, el contenido lo pones tú.

## Android y más

- **[Waydroid](https://waydro.id/)** para aplicaciones y juegos de Android (binder en el núcleo, soporte de iptables y bibliotecas ARM);
- **[Sober](https://sober.vinegarhq.org/)** como reproductor de Roblox — no viene instalado, cógelo de la tienda con `flatpak install flathub org.vinegarhq.Sober`. Es una aplicación de 18 MB que arrastra 1,1 GB de bibliotecas de GNOME: precisamente por dejarla fuera, la ISO se mantiene pequeña.

> Nota: la IA local y Android no conviene usarlos junto con juegos pesados, porque comparten la misma GPU y la misma memoria.

## Mandos

La configuración recomendada y probada:

- **2 DualShock 4 por Bluetooth** — con giroscopio (útil para el control por movimiento en juegos como Mario Kart), conectados al adaptador Realtek integrado;
- **mando por USB** — con un cable **de datos** aparece como un Xbox 360 (controlador `xpad`, XInput), sin giroscopio.

Los controladores `xpad`, `hid_playstation` y `hid_nintendo` van dentro del núcleo. Para volver a emparejar un DS4: mantén *Share + PS* hasta que parpadee y empareja desde la ventana de Bluetooth.

## Escalado

Nuestra Mesa lleva **FSR 4** a través de **[OptiScaler](https://github.com/optiscaler/OptiScaler)** en la ruta DLSS del juego: GE-Proton 11 descarga OptiScaler solo cuando encuentra `PROTON_USE_OPTISCALER=1`, hay que poner el juego en DLSS, y la biblioteca FSR 4 de AMD (`amdxcffx64.dll`, tomada del controlador de Windows de AMD) hay que ponerla junto al juego. Las alternativas siguen siendo el escalado de **gamescope** (FSR1/NIS) y XeSS, donde un juego lo trae incorporado. En títulos que dependen de la *CPU* (por ejemplo *Black Myth: Wukong*) no sirve ni bajar la resolución ni bajar la frecuencia de la GPU — ver [GPU y overclock](/es/docs/gpu-overclock).

## Fuentes

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)
