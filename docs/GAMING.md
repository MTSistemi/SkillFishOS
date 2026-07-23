# Gaming & emulation

Gaming is the carrot that makes the whole project worthwhile. SkillFishOS ships a complete, pre‑configured gaming stack — **the tools, not the games.**

> ⚖️ **SkillFishOS does not include any games, ROMs, BIOS files or copyrighted emulator content.** It ships the open‑source tooling to install and run them. **You bring your own games.** Please respect the law and only use content you own.

## PC gaming

- **Steam** (Flatpak) with **Proton** / **GE‑Proton**, plus **gamescope**, **GameMode** and **MangoHud** preinstalled.
- **Heroic Games Launcher** for Epic / GOG / sideloaded titles.
- A dedicated **gamescope console session** (Steam Big Picture) selectable at login — turn the box into a couch console.
- **Upscaling that works on RDNA 2:** gamescope **FSR 1 / NIS** (`-F fsr` / `-F nis`) is the universal, zero‑cost baseline. (FSR 4 is RDNA 4‑only and **not** possible on this hardware; OptiScaler/lsfg‑vk are options per‑game.)

## Emulation — EmuDeck + ES‑DE

**EmuDeck** installs and configures a full set of emulators (RetroArch and standalone cores) and the **ES‑DE** frontend in a few clicks — no manual setup. It's the easy on‑ramp for retro gaming.

- EmuDeck's library folder can point at network storage (e.g. an NFS share) so a whole ROM/BIOS collection lives off‑box.
- **ES‑DE** is the couch‑friendly frontend: per‑system game lists, favorites/collections, and artwork scraping (e.g. ScreenScraper) for nice box art.
- Arcade/Bluetooth controllers are detected out of the box.

Again: **EmuDeck and the emulators are installable tooling; the games and BIOS files are yours to provide.**

## Controllers

See [OPTIMIZATIONS.md §9](OPTIMIZATIONS.md#9-game-controllers). In short: DualShock 4 over Bluetooth (with gyro) works great; generic "Pro Controller" clones are most reliable over USB (XInput mode). Battery levels show in the desktop HUD.

## Performance notes

The 40‑CU unlock and the governor give the GPU plenty of headroom; in practice many modern titles are **CPU/draw‑call bound** on this APU, so the CPU OC (3.7 GHz) and in‑game CPU‑side settings (draw distance, crowd/vegetation density, shadows) matter more than GPU clock or resolution. Full benchmark methodology in [OPTIMIZATIONS.md](OPTIMIZATIONS.md).
