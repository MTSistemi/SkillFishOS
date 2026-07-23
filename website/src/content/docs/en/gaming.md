---
title: Gaming and emulation
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android and controllers.
group: Usage
order: 1
---

SkillFishOS was born to play. The whole gaming stack is preinstalled and configured; you add **your** games and **your** ROMs.

## Steam and Proton

**Steam** (via [Flatpak](https://flatpak.org/)) is integrated with **[gamescope](https://github.com/ValveSoftware/gamescope)** (Valve's micro-compositor), **[gamemode](https://github.com/FeralInteractive/gamemode)** and **[MangoHud](https://github.com/flightlessmango/MangoHud)**. A dedicated **console session** (gamescope, Big Picture style) is selectable at login. Windows games run through **Proton**.

## Non-Steam games: Heroic

**[Heroic Games Launcher](https://heroicgameslauncher.com/)** manages **Epic Games** and **GOG** titles, and Windows games via **GE-Proton**. With **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** you can easily install Proton/Wine versions. Heroic games can be added to Steam (with their cover art).

## Emulation: EmuDeck + ES-DE

**[EmuDeck](https://www.emudeck.com/)** installs and configures, in a few clicks, a complete set of emulators (Flatpak): **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** and more. The frontend is **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

On SkillFishOS the `~/Emulation` folder can point to a network **NAS** (BIOS, ROMs and saves shared across machines).

> ⚠️ ES-DE rewrites its settings file on exit: edit them while the program is **closed**.
>
> ⚠️ For **Ryujinx**, firmware and keys must be imported by the user: the firmware expects each NCA as a directory. **Games, ROMs, BIOS and keys are not included** in the system — a deliberate legal choice: SkillFishOS provides the tools, you supply the content.

## Android and more

- **[Waydroid](https://waydro.id/)** for Android apps/games (binder in the kernel, iptables support and ARM libraries);
- **[Sober](https://sober.vinegarhq.org/)** as a Roblox player.

> Note: local AI and Android should not be used together with heavy games, because they share the same GPU and memory.

## Controllers

The recommended, tested configuration:

- **2× DualShock 4 over Bluetooth** — with gyroscope (useful for *motion* in games like Mario Kart), connected to the integrated Realtek adapter;
- **controller over USB** — a **data** cable makes it appear as an Xbox 360 (`xpad` driver, XInput), without a gyroscope.

The `xpad`, `hid_playstation` and `hid_nintendo` drivers are included in the kernel. To re-pair a DS4: hold *Share + PS* until it blinks, then pair from the Bluetooth GUI.

## Upscaling

**FSR 4 is not available** on the BC-250 (it requires RDNA 4 hardware). The alternatives are **gamescope** upscaling (FSR1/NIS) or **[OptiScaler](https://github.com/optiscaler/OptiScaler)** for individual games. For *CPU-bound* titles (e.g. *Black Myth: Wukong*), lowering resolution or GPU clock won't help — see [GPU and overclock](/en/docs/gpu-overclock).

## Sources

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)
