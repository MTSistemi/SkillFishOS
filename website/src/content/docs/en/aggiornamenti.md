---
title: Updates and repository
description: How SkillFishOS updates safely, without being broken by Debian sid.
group: Usage
order: 4
---

SkillFishOS is based on **Debian sid** (*unstable*), Debian's development branch: always up to date, but by nature subject to occasional regressions. On "exotic" hardware like the BC-250, a bad update (of Mesa, firmware or the kernel) can break the system. SkillFishOS addresses this with two tools.

## 1. Our own components, from a dedicated repository

The most critical parts are built and distributed by **us**, from our **own, signed APT repository**:

- the optimized **[kernel](/en/docs/kernel)** (image + headers);
- the **SMU governor** and the overclock tools;
- the [Tuner and AI](/en/docs/app-native) **native apps**;
- the **steampunk theme** and the **branding**;
- the system configuration.

Publishing a component from our own repo means we can **test it first** on the real hardware and update it **only when it brings benefits** — not whenever upstream happens to change.

## 2. "Pinning" the fragile packages

For the packages that come from Debian but are delicate on this hardware, SkillFishOS uses **APT pinning**: it keeps them at a **verified** version until we test a newer one. The main pinning candidates are:

- **Mesa / Vulkan drivers (RADV)** — an update can regress `gfx1013`;
- **AMD firmware / `linux-firmware`** — GPU microcode;
- **the Debian stock kernel** — to block the known-problematic versions (see [kernel](/en/docs/kernel));
- **KDE Plasma** — to avoid unstable releases.

This way "normal" updates (most of the system) keep arriving regularly, while the handful of packages that could break everything stay frozen at versions we know work.

## How to update

Like any Debian system, from the terminal:

```bash
sudo apt update && sudo apt full-upgrade
```

…or from the **Discover** graphical app, or from the **SkillFishOS Hub** — our Discover-style software centre that installs, removes and updates in one place across **APT, Flatpak and Snap**, with category browsing, app pages with a screenshot carousel and a one-click "Update all". Thanks to the [Snapper](/en/docs/storage-snapshot) hooks, a Btrfs snapshot is created **before and after** every update: if something goes wrong, the rollback from the GRUB menu restores the previous state.

> In short: **we** give you a tested kernel, apps and themes; **Debian** gives you the rest of the updated software; **pinning** prevents surprises; **Btrfs** is the safety net. Three layers of protection, so updating isn't scary.

## The official repository

The SkillFishOS APT repo is **live**, GPG-signed and hosted on **GitHub Pages** (suite `aetherium`):

```bash
# 1. import the signing key
sudo curl -fsSL https://mtsistemi.github.io/SkillFishOS/skillfishos-archive-keyring.gpg \
  -o /usr/share/keyrings/skillfishos-archive-keyring.gpg
# 2. add the repo
echo "deb [signed-by=/usr/share/keyrings/skillfishos-archive-keyring.gpg] \
https://mtsistemi.github.io/SkillFishOS aetherium main" \
  | sudo tee /etc/apt/sources.list.d/skillfishos.list
# 3. install/update the kernel via apt
sudo apt update && sudo apt install skillfishos-kernel
```

Recent SkillFishOS builds ship it **pre-configured**; otherwise the commands above set it up. The [kernel](/docs/kernel)
(152 MB image) is published as a GitHub *release asset*: the tiny `skillfishos-kernel`
package downloads and installs it automatically, so the update still goes through `apt`. The
repo is managed with **[reprepro](https://salsa.debian.org/debian/reprepro)** and the client
verifies the signature via the dedicated *keyring*.

## Sources

- [Debian unstable (sid)](https://wiki.debian.org/DebianUnstable)
- [APT pinning — Debian manual](https://wiki.debian.org/AptConfiguration)
- [reprepro](https://salsa.debian.org/debian/reprepro) — APT repository management
- [Snapper](http://snapper.io/) — pre/post APT snapshots
