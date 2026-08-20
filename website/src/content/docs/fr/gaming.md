---
title: Jeu et émulation
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android et manettes.
group: Utilisation
order: 1
---

SkillFishOS est né pour jouer. Tout le nécessaire est préinstallé et configuré ; vous ajoutez **vos** jeux et **vos** ROM.

## Steam et Proton

**Steam** (en [Flatpak](https://flatpak.org/)) est relié à **[gamescope](https://github.com/ValveSoftware/gamescope)** (le micro-compositeur de Valve), **[gamemode](https://github.com/FeralInteractive/gamemode)** et **[MangoHud](https://github.com/flightlessmango/MangoHud)**. Une **session console** dédiée (gamescope, façon Big Picture) se choisit à la connexion. Les jeux Windows passent par **Proton**.

## Les jeux hors Steam : Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** gère les titres **Epic Games** et **GOG**, et les jeux Windows par **GE-Proton**. Avec **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** on installe facilement des versions de Proton ou de Wine. Les jeux d'Heroic peuvent être ajoutés à Steam (avec leurs jaquettes).

## L'émulation : EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** installe et configure, en quelques clics, tout un ensemble d'émulateurs (en Flatpak) : **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** et d'autres. L'interface est **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

Sur SkillFishOS le dossier `~/Emulation` peut pointer vers un **NAS** du réseau (BIOS, ROM et sauvegardes partagés entre plusieurs machines).

> **Attention :** ES-DE réécrit son fichier de réglages en quittant : modifiez-le pendant que le programme est **fermé**.
>
> **Attention :** pour **Ryujinx**, le micrologiciel et les clés doivent être importés par l'utilisateur : le micrologiciel attend chaque NCA sous forme de dossier. **Les jeux, les ROM, les BIOS et les clés ne sont pas fournis** avec le système — c'est un choix légal assumé : SkillFishOS fournit les outils, vous fournissez le contenu.

## Android et le reste

- **[Waydroid](https://waydro.id/)** pour les applications et les jeux Android (binder dans le noyau, prise en charge d'iptables et bibliothèques ARM) ;
- **[Sober](https://sober.vinegarhq.org/)** comme lecteur Roblox — pas préinstallé, prenez-le dans la logithèque avec `flatpak install flathub org.vinegarhq.Sober`. C'est une application de 18 Mo qui traîne derrière elle 1,1 Go d'environnement GNOME : la garder hors de l'image, c'est ce qui garde l'ISO petite.

> À noter : l'IA locale et Android ne s'utilisent pas en même temps que les jeux lourds, puisqu'ils se partagent le même GPU et la même mémoire.

## Les manettes

La configuration conseillée, celle que nous avons essayée :

- **2 DualShock 4 en Bluetooth** — avec le gyroscope (utile pour le *motion* dans des jeux comme Mario Kart), reliées à l'adaptateur Realtek intégré ;
- **une manette en USB** — avec un câble de **données** elle apparaît comme une Xbox 360 (pilote `xpad`, XInput), sans gyroscope.

Les pilotes `xpad`, `hid_playstation` et `hid_nintendo` sont dans le noyau. Pour réappairer une DS4 : maintenez *Share + PS* jusqu'au clignotement, puis appairez depuis l'interface Bluetooth.

## Le rehaussement de définition

**FSR 4 n'est pas disponible** sur la BC-250 (il demande du matériel RDNA 4). Les solutions de rechange sont le rehaussement de **gamescope** (FSR1/NIS) ou **[OptiScaler](https://github.com/optiscaler/OptiScaler)** pour tel ou tel jeu. Pour les titres *limités par le CPU* (par exemple *Black Myth: Wukong*), baisser la définition ou la fréquence du GPU n'y changera rien — voir [GPU et overclock](/fr/docs/gpu-overclock).

## Sources

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)
