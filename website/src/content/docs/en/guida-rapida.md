---
title: Quick start
description: Your first 10 minutes with SkillFishOS — from first boot to first game.
group: Introduction
order: 3
---

You've installed SkillFishOS (see [Installation](/en/docs/installazione)) and you're at first boot. This page is a **quick checklist** to get going right away: everything else is already configured and working.

## In one line

> Power on → you're already at the tuned desktop → connect a controller → add your games → play. No terminal, no setup.

## 1. First boot (it's all ready)

On first boot you get a **KDE Plasma 6** desktop with a steampunk theme, an optimized kernel, the SMU governor, the **Stock** profile, the gaming stack and snapshots **already active**. Top-right, the **HUD** shows CPU, GPU, temperatures, RAM, fan and connected Bluetooth devices in real time.

You don't need to install drivers, set frequencies or enable anything: the system boots "at maximum compatibility".

## 2. Connect to the network

Ethernet is managed by NetworkManager and ready to go. For Wi-Fi/Bluetooth use the network icon in the panel. A connection is needed for Steam, updates and the local AI.

## 3. Connect a controller

| Controller | How |
|---|---|
| **DualShock 4** | Bluetooth: hold **Share + PS** until it flashes, then pair from the Bluetooth icon. It has the **gyro**. |
| **Generic controller** | Over **USB** with a **data** cable (not charge-only): seen as an Xbox 360 pad. |

Details and troubleshooting → [Gaming](/en/docs/gaming) and [Troubleshooting](/en/docs/risoluzione-problemi).

## 4. Add your games

- **Steam** is already installed and integrated with gamescope/MangoHud. Sign in and install your games: Windows titles run via **Proton**.
- **Epic / GOG** → [Heroic](/en/docs/gaming).
- **Emulation** → launch **EmuDeck**, pick your emulators, then play from the **ES-DE** frontend. ROMs, BIOS and keys are added by you (see the legal note in [Gaming](/en/docs/gaming)).

## 5. (Optional) Push the hardware

SkillFishOS boots in the **Stock** profile to be safe on any board. When you want more performance open the **[Tuner](/en/docs/app-native)** and move up a profile:

**Stock → Performance → Turbo → Crazy**

The Tuner **tests each profile on your own BC-250** and automatically **rolls back** if the card can't handle it. It's the safe way to find your chip's limit (see [GPU & overclock](/en/docs/gpu-overclock)).

## 6. (Optional) Turn on local AI

When you need an offline AI assistant, open the **AI panel** and start the [Ollama + OpenWebUI](/en/docs/ai-locale) stack. Remember: AI and heavy games should **not** be used together (same GPU and memory). With the stack off, the GPU goes back fully to gaming.

## Things to know right away

- **Do not re-enable suspend**: on the BC-250 it's broken and the board won't wake up (see [Desktop](/en/docs/desktop)).
- Use a **DisplayPort monitor** or a **passive** adapter; **active** DP→HDMI adapters break audio.
- You have a **safety net**: a Btrfs snapshot is taken before and after every update; if things go wrong, roll back from the GRUB menu → *SkillFishOS snapshots* (see [Storage & snapshots](/en/docs/storage-snapshot)).

## What next?

- Want to understand **what** you're using? → [BC-250 hardware](/en/docs/hardware-bc250)
- Want the real performance **numbers**? → [Performance & benchmarks](/en/docs/prestazioni)
- Have a quick **question**? → [FAQ](/en/docs/faq)
- A **term** you don't know? → [Glossary](/en/docs/glossario)
