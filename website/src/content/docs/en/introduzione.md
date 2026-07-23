---
title: Introduction
description: What SkillFishOS is, why it exists and who it is for.
group: Introduction
order: 1
---

**SkillFishOS** is a Linux distribution designed and tuned for one specific, unusual board: the **AMD BC-250**. It is a ready-to-use *console-PC* system — gaming, emulation, on-device AI and everyday desktop use — built on [Debian](https://www.debian.org/) and [KDE Plasma 6](https://kde.org/plasma-desktop/), with a consistent steampunk look from boot all the way to the desktop.

## The philosophy

The BC-250 was born as a cryptocurrency mining board and ended up on the second-hand market at very low prices. Under the heatsink, though, sits a **semi-custom AMD APU** from the same silicon family as the current-generation consoles: a Zen 2 CPU, RDNA 2 graphics and 16 GB of GDDR6. With the right software it becomes a surprisingly capable little console-PC.

The problem is that getting it to run well on Linux requires kernel patches, a dedicated frequency governor, overclocking, thermal profiles and a long list of hardware workarounds. SkillFishOS exists to **do all of that work once** and deliver a system that *"powers on and runs at its best"*, without the user needing to touch the terminal.

> SkillFishOS does not distribute games or ROMs: it provides the **tools** (Steam, EmuDeck, emulators, frontends). You add the content yourself, legally.

## Who it is for

The project was born from a concrete, personal need: to **let kids use and learn Linux while they play**. Gaming is the "carrot" that draws them in, and Btrfs's **automatic snapshots** are the safety net that lets them tinker without fear of breaking the system — if something goes wrong, you roll back in one click from the boot menu.

So SkillFishOS is a good fit for:

- anyone who owns a **BC-250** and wants to play without becoming a Linux kernel expert;
- **families** who want a cheap console that is also an educational PC;
- **tinkerers** who want to start from an already-tuned base instead of rebuilding everything from scratch.

## What's inside, in short

- A **tailored kernel** ([linux-tkg](https://github.com/Frogging-Family/linux-tkg)) with the BC-250 patches: 40 Compute Units unlocked, unlocked frequencies, a dedicated SMU governor.
- A **KDE Plasma 6 desktop** with a steampunk theme (icons, cursors, wallpaper, system HUD).
- **Gaming ready**: Steam, [gamescope](https://github.com/ValveSoftware/gamescope), [EmuDeck](https://www.emudeck.com/), [ES-DE](https://es-de.org/), [Heroic](https://heroicgameslauncher.com/), Proton.
- **On-device AI**: an [Ollama](https://ollama.com/) + [OpenWebUI](https://openwebui.com/) stack accelerated in Vulkan on the integrated GPU.
- **Btrfs snapshots** with [Snapper](http://snapper.io/) and rollback from the GRUB menu.
- **Native apps**: the *Tuner* (hardware control without a terminal) and the *AI* panel.
- **Dedicated, tested updates** from our own APT repository, so Debian updates can't surprise you.

The following pages cover each component in detail.

## Sources

- BC-250 community documentation — [bc250.info](https://bc250.info)
- AMD BC-250 docs (elektricm) — [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- Debian — [debian.org](https://www.debian.org/)
- KDE Plasma — [kde.org/plasma-desktop](https://kde.org/plasma-desktop/)
