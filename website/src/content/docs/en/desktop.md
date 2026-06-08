---
title: Desktop, theme and remote access
description: KDE Plasma 6, the steampunk theme, the system HUD, anti-suspend and remote access.
group: System
order: 4
---

SkillFishOS uses **[KDE Plasma 6](https://kde.org/plasma-desktop/)** as its desktop environment, dressed in a consistent steampunk theme and a set of tweaks specific to the BC-250.

## Sessions

At login (handled by **SDDM**, with autologin) several sessions are available:

- **KDE Plasma X11** — *default*. Choosing X11 makes remote access trivial (see below);
- **KDE Plasma Wayland** — selectable;
- **Gaming** — a [gamescope](https://github.com/ValveSoftware/gamescope) session in Big Picture style (see [Gaming](/en/docs/gaming)).

## ⚠️ Anti-suspend (critical)

The BC-250 has **broken ACPI suspend**: if it sleeps, it **won't wake up** and needs a reset (see [hardware](/en/docs/hardware-bc250)). For this reason SkillFishOS **permanently disables** all sleep states:

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

To this it adds a `logind` rule (`IdleAction=ignore`), automatic screen locking disabled and power management with "infinite" idle. It is a **mandatory** measure: a suspended machine is also unreachable remotely.

## "SkillFish Steampunk" theme

The look is a coordinated brass/copper palette (accent **`#d8a849`**, dark surfaces) and consistent from **boot to desktop**: GRUB theme, Plymouth splash, SDDM greeter, fish-themed wallpaper. The theme package includes:

- **icons** (`SkillFishSteampunk`, with `breeze-dark` as a fallback) and dedicated **cursors**;
- a **Kvantum** style for Qt applications and a KDE **color scheme**;
- a **plasma theme**, a **Konsole** theme, window buttons and a global **look-and-feel** (`org.skillfish.steampunk`);
- themed user avatars and a selectable gallery.

> The default **Breeze** themes stay installed as a load-bearing fallback (in particular they provide the logout/shutdown dialog). They must not be removed.

## System HUD (Conky)

In the top-right corner there's a brass-styled **HUD** built with **[Conky](https://github.com/brndnmtthws/conky)** showing in real time: per-core CPU bars with MHz/°C/W, GPU MHz/temperature/VRAM, RAM, disk, fan and the **connected Bluetooth devices** with their battery level (gamepads, audio…). The values come from dedicated helpers that read the hardware sensors directly.

## Remote access (x11vnc)

Because the default session is X11, remote access is simple: SkillFishOS starts **[x11vnc](https://github.com/LibVNC/x11vnc)** on the active display, sharing the real screen. On the LAN any VNC client can connect. This allows support and configuration from another PC without a physical keyboard/mouse on the board.

## Network, audio and applications

- **Network**: ethernet is managed by **NetworkManager**, so it's visible and configurable from the Plasma GUI.
- **Audio**: a full **[PipeWire](https://pipewire.org/)** stack (with Bluetooth support). Note: *active* DP→HDMI adapters can break the audio — see [Troubleshooting](/en/docs/risoluzione-problemi).
- **Base apps**: Dolphin file manager, Konsole terminal, Okular PDF viewer, Gwenview image viewer, Ark archiver, Spectacle screenshots, Discover store (with flatpak), **Google Chrome** browser, **OnlyOffice**.
- **Native SkillFishOS apps** (grouped under the **"SkillFishOS"** menu, each installable/updatable as a `.deb` from the signed repo): **Tuner** (BC-250 overclock/undervolt/fan/CU control), **AI** (on-demand local LLM on the integrated GPU), **Monitor** (live temperature/frequency/voltage/fan charts), **Kernel Manager** (pick the boot kernel and uninstall old ones), **ISO Mount** and **Hub** — the Discover-style software centre (APT + Flatpak + Snap) with app pages, a screenshot carousel and software-source management.
- **Display**: a daemon (`skillfish-dp-hotswap`) handles monitor detection, needed because the DisplayPort HPD is broken.

## Sources

- [KDE Plasma](https://kde.org/plasma-desktop/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [Conky](https://github.com/brndnmtthws/conky) · [x11vnc](https://github.com/LibVNC/x11vnc)
- [PipeWire](https://pipewire.org/) · [SDDM](https://github.com/sddm/sddm)
- [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/) · [NetworkManager](https://networkmanager.dev/)
