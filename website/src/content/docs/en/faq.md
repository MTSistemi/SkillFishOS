---
title: Frequently asked questions (FAQ)
description: The most common questions about SkillFishOS and the BC-250, with short answers.
group: Reference
order: 2
---

Quick answers to the most common questions. For depth, each answer links to the right page.

## General

**What is SkillFishOS?**
A Linux distribution (Debian + KDE Plasma 6) designed and tuned for the **AMD BC-250** board: gaming, emulation, local AI and desktop use, all preconfigured. See [Introduction](/en/docs/introduzione).

**What hardware does it run on?**
Only on the **AMD BC-250** (Zen 2 + RDNA 2 "gfx1013" APU, 16 GB GDDR6). It's a system built around *that* board, not a generic distro. See [BC-250 hardware](/en/docs/hardware-bc250).

**How much does it cost? Is it open source?**
It's **free**. It integrates open-source software from many communities; the project's code is on [GitHub](https://github.com/MTSistemi/SkillFishOS). See [Sources](/en/docs/fonti).

**Does it include games, ROMs or BIOS?**
No. SkillFishOS provides the **tools** (Steam, EmuDeck, emulators, frontends); you add the content yourself, legally. See [Gaming](/en/docs/gaming).

## Installation

**How do I install it?**
Write the ISO to a USB stick and boot the **Calamares** graphical installer. All with the mouse. See [Installation](/en/docs/installazione).

**Can I try it without installing?**
Yes: the ISO is **live**, you can explore the desktop before installing.

**Does it erase my disk?**
The automatic install ("Erase disk") does. To keep existing data, use manual partitioning. SkillFishOS uses **Btrfs** with separate `@rootfs` and `@home` subvolumes.

**Do I need an internet connection?**
Not to install; you'll need one afterwards for Steam, updates and AI.

## Performance and overclock

**Why does it start "slow" / in Stock?**
For safety: every BC-250 is different (*silicon lottery*). You move up profiles from the **[Tuner](/en/docs/app-native)**, which validates everything on your card. See [GPU & overclock](/en/docs/gpu-overclock).

**Is overclocking dangerous?**
The Tuner applies a profile, **tests** it and **rolls back** if the card can't handle it; the 85 °C cap and the thermal-guard are always on. It's designed to be safe.

**How many FPS in game X?**
It depends: some games are **CPU-bound** (e.g. *Black Myth: Wukong*) and don't scale with the GPU. See [Performance & benchmarks](/en/docs/prestazioni).

**Can I use FSR 4?**
No, it requires RDNA 4 hardware. Use gamescope (FSR1/NIS) or OptiScaler. See [Gaming](/en/docs/gaming).

## Daily use

**Why is the screen sometimes black?**
The **DisplayPort HPD is broken** on the BC-250: SkillFishOS works around it with a dedicated daemon. Use a DP monitor or a **passive** adapter. See [Troubleshooting](/en/docs/risoluzione-problemi).

**Why is there no audio from the TV?**
Often it's an **active** DP→HDMI adapter: use a passive one, a DP monitor, a USB DAC or Bluetooth audio.

**Can I put the PC to sleep?**
No. **Suspend is broken** at the hardware level and the board won't wake up: SkillFishOS disables it on purpose. **Don't re-enable it.** See [Desktop](/en/docs/desktop).

**Can I use it from another computer?**
Yes: the default session is X11 and **x11vnc** runs, so you can control the desktop over VNC on the LAN. See [Desktop](/en/docs/desktop).

## Local AI

**Which AI model can I use?**
The practical reference is **`qwen3:14b`**, which runs fully on the GPU. The stack is Ollama + OpenWebUI in **Vulkan** (not ROCm, unsupported on gfx1013). See [Local AI](/en/docs/ai-locale).

**Can I game while the AI is on?**
No: AI and heavy games share GPU and memory. Shut down the AI stack before playing.

## Updates

**How do I update the system?**
`sudo apt update && sudo apt full-upgrade` or the **Discover** app. A snapshot is taken automatically before/after every update. See [Updates](/en/docs/aggiornamenti).

**An update broke something — what now?**
Reboot and pick a snapshot from **GRUB → "SkillFishOS snapshots"**. See [Storage & snapshots](/en/docs/storage-snapshot).

**Does Debian update the kernel?**
No: the SkillFishOS kernel is **held** (`apt-mark hold`) and updated only from our tested repo. See [Kernel](/en/docs/kernel).

## Project

**Can I contribute or report a bug?**
Yes, via **Issues** on [GitHub](https://github.com/MTSistemi/SkillFishOS/issues).

**Where do I download the ISO?**
From the [Download](/en/download) page (hosted on SourceForge).
