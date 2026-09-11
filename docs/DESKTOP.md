# Desktop & theme

SkillFishOS runs **KDE Plasma 6** with a complete **SkillFish Steampunk** theme. It's mature, fully GUI‑configurable (network, Bluetooth, displays, wallpaper, right‑click menus — all native), and Qt‑native so the Kvantum theme applies cleanly.

## Sessions

SDDM (auto‑login, themed) offers:

- **KDE Plasma (X11)** — the default, because remote access (x11vnc) is trivial on X11.
- **KDE Plasma (Wayland)** — selectable.
- **Gaming (gamescope)** — a Steam Big‑Picture console session, independent of the desktop. See [GAMING.md](GAMING.md).

> Earlier builds used Wayfire and Hyprland; both were removed in favour of KDE, which solves the rough edges (empty network/BT panels, no wallpaper GUI, no desktop context menu) natively. The full brass theme was ported to KDE.

## The SkillFish Steampunk theme

A coherent brass/steampunk look across the entire boot‑to‑desktop chain — accent `#d8a849` on dark brown:

- **GRUB** theme, **Plymouth** boot splash, **SDDM** login (custom QML), and a fish‑themed wallpaper.
- **Plasma**: a global look‑and‑feel package (`org.skillfish.steampunk`), color scheme, desktop theme, **Kvantum** Qt style, **SkillFishSteampunk** icon theme (with symbolic icons that recolor to the scheme), **SkillFish‑Steampunk‑Cursors**, and a brass Konsole palette.
- The **Kickoff** application menu uses the brass fish logo.

The theme is shipped in this repo under [`theme/`](../theme/) — see [theme/README.md](../theme/README.md) for install notes (including the cursor‑symlink gotcha).

> **Warning:** The icon theme must provide `inode-directory` (not just `folder`) or KDE shows generic folders in the base theme's blue — SkillFishOS copies `folder.svg` → `inode-directory.svg` to fix this.

## Live system HUD

A translucent, always‑on overlay (top‑right) built with **Conky** on the X11 session, styled to match the brass theme. It shows:

- Per‑core CPU mini‑bars, average CPU clock & temperature, package power draw.
- GPU clock, temperature, VRAM usage.
- RAM and disk usage, fan RPM.
- **Connected Bluetooth controllers grouped by category** (Gamepad / Audio / …) with **battery %** read from UPower.

Sensor reads go through a small helper that locates hwmon devices **by name** (k10temp / amdgpu / nct6686), so it survives the hwmon index shuffling across boots.

## Mounting ISO images

Disc images mount the **KDE‑native** way through **udisks2** (no `gnome-disk-image-mounter`):
**double‑click** an `.iso` in Dolphin to mount it, or **right‑click → Mount / Unmount ISO image**.
Mounts are read‑only, single, and idempotent (re‑opening reuses the loop device).

Shipped in this repo under [`apps/iso-mount/`](../apps/iso-mount/) — wrapper, Dolphin
service menu, double‑click handler and a polkit rule, with the install notes and gotchas.

## SkillFishOS Control Center

Since September 2026 (26.09.x) every tool that used to be its own app lives
in one native PyQt6 window, themed automatically by Kvantum with native KWin
window controls, no terminal needed. Open it from the SkillFishOS menu or
with `skillfish-control-center`.

Its sections: Status (one number per card: GPU clock and ceiling, CPU,
compute units, fan), Tuner (the V/F governor curve, CPU overclock and
undervolt, cores, compute units, the UMA VRAM split, advanced governor
knobs), Fan (curve, sensors, lead, PWM test), Monitor (one chart per
reading, plus a bar per CPU thread — this board reports per-core P-states
that a single "CPU MHz" number hides, see
[OPTIMIZATIONS.md](OPTIMIZATIONS.md#11-telemetry--what-this-apu-will-and-wont-tell-you)),
Games, Profiles, Kernel, Snapshots, AI, Emulators, Console and ISO. The old
per-tool commands (`skillfish-tuner`, `skillfish-monitor`, `skillfish-fan`,
`skillfish-kernel-manager`, `skillfish-snapshots`, `skillfish-ai-panel`)
still work — each opens the matching section.

A polkit policy lets the active local user run the privileged helper,
`skillfish-cc-helper` (a personal machine — no password prompts for the
kids).

Full detail: [docs/CONTROL-CENTER.md](CONTROL-CENTER.md) and
[skillfishos.com/en/docs/control-center](https://skillfishos.com/en/docs/control-center/).

## Other niceties

- Driverless printing (CUPS + IPP Everywhere + cups‑browsed + Avahi); the user is in `lpadmin`.
- Fully localized desktop (ships IT/EN).
- A "Software" store (Discover with deb + flatpak backends).
