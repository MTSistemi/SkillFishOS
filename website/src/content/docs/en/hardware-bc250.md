---
title: The AMD BC-250 hardware
description: The board, the APU, its specs and its known hardware flaws.
group: Introduction
order: 2
---

The **AMD BC-250** is a compact board based on a **semi-custom APU** codenamed *Oberon* for the CPU and *Cyan Skillfish* for the graphics — the same silicon family as AMD's current-generation consoles. It was produced for mining systems (typically mounted several boards per chassis) and today shows up on the second-hand market at low prices.

## Key specifications

| Component | Detail |
|---|---|
| **CPU** | 6 cores / 12 threads **Zen 2** ("Oberon"), up to **3.9 GHz** (Turbo), 4.0 GHz validated |
| **GPU** | **RDNA 2** "Cyan Skillfish" (`gfx1013`), up to **40 Compute Units** unlockable |
| **Memory** | **16 GB GDDR6** shared (UMA) between CPU and GPU |
| **Compute** | ~**11.3 TFLOPS** FP32 at 40 CU / 2000 MHz (measured with vkpeak) |
| **Memory bandwidth** | ~350–367 GB/s (measured with clpeak) |
| **Video output** | 1× DisplayPort |

Memory is **unified**: the GDDR6 is shared between system and graphics. By default about 8 GB is assigned as VRAM, but on Linux the video space can be extended via the **GTT** (Graphics Translation Table), letting Vulkan see ~13 GiB of memory — especially useful for AI models.

## Unlocking the 40 CUs

The GPU has 40 CUs but the driver enables only **24** by default. SkillFishOS **routes them up to 40 live** (no reboot): it boots at the driver baseline and a service brings it to 40 at startup, adjustable from the [Tuner](/en/docs/app-native). The reverse-engineering of the unlock is documented by [bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock); the runtime control via `umr` is inspired by [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager) (clean-room reimplementation).

> With 40 CUs active, SkillFishOS measures **11385 GFLOPS** FP32 (vkpeak) from cold, versus ~6141 for a baseline 24-CU configuration: about **+85%**.

## Hardware flaws to know about

The BC-250 is repurposed "mining" hardware: it has some limitations that SkillFishOS works around in software. Knowing them explains many of the system's choices.

### Broken DisplayPort Hot-Plug Detect (HPD)

The monitor connection detection on the DisplayPort connector **does not work**: the board doesn't "see" when you plug in a screen. SkillFishOS solves this with a dedicated daemon (`skillfish-dp-hotswap`) that forces detection at boot and watches for monitor changes at runtime, plus the `video=DP-1:e` kernel parameter as a fallback. See [Desktop](/en/docs/desktop) and [Troubleshooting](/en/docs/risoluzione-problemi).

### Broken ACPI suspend

Suspend (**s2idle is broken**): the board goes to sleep but **does not wake up** and needs a reset. A suspended machine is also unreachable remotely. For this reason SkillFishOS **permanently disables** all sleep states (see [Desktop](/en/docs/desktop)). It is a mandatory measure.

### IOMMU unusable

The IOMMU on the BC-250 is unstable: it **must never be enabled**. The system always boots without IOMMU.

### Thermal sensors

Only the GPU *edge* temperature sensor is available; **there is no VRAM temperature sensor**. The stock cooling is marginal, so back-to-back benchmark comparisons are invalid (*heat-soak* effect): let the board cool down for a few minutes between runs.

## Cooling, 3D-printable cases and fans

The BC-250 arrives **bare**, designed for mining racks with five 80 mm *screamer* fans driven by the power-distribution connector. Desktop use needs dedicated cooling. **Two things must be cooled**: the APU heatsink **and** the **GDDR6** chips, which run very hot and have no temperature sensor (see [GPU/overclock](/en/docs/gpu-overclock)).

**What works (community advice):**

- **2× 120 mm static-pressure fans** aimed at the heatsink are the most common desktop setup; with no case you can lay them directly on top of the heatsink (zip-ties through the fins).
- A **dedicated VRAM fan** is strongly recommended if you overclock: the GDDR6 modules are the hottest spot.
- The fan connects to the board's **4-pin PWM** header — SkillFishOS drives it via `nct6686` (sensors) and keeps it on **auto**.

**Cases and ducts (free STL, 3D-printable):**

| Model | Author | Notes |
|---|---|---|
| [Console Style Case](https://www.thingiverse.com/thing:7172528) | Arthrimus | "Console" case + PSU bay, shroud for **1× 120 mm** |
| [ASRock BC-250 Shell Case](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case) | onemorecap | Snap-on shell, quick single-fan mount |
| [Yet Another BC-250 Fan Shroud](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud) | ViRazY | **140 mm** intake + **120 mm** exhaust |
| [Case ATX PSU & Fan Duct](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct) | ZMASLO | Uses a standard ATX PSU, duct that won't damage the cooler |
| [Standard ATX PSU case](https://www.thingiverse.com/thing:7269520) | CatSiewDai | Full case for ATX power supplies |
| [OC vRAM Fan Kit (remix)](https://www.thingiverse.com/thing:7271946) | marccyberwiz | Fan kit **dedicated to the VRAM** for overclocking |
| [NexGen3D — DIY Steam Machine (Bazzite)](https://www.printables.com/model/1499974-nexgen3d-diy-steam-machine-powered-by-bazzite) | NexGen3D | Full **Steam Machine**-style case for the BC-250 |
| [NexGen3D — Steam Machine PRO (liquid-cooled)](https://www.printables.com/model/1614131-nexgen3d-diy-steam-machine-pro-liquid-cooled-bc-25/files) | NexGen3D | **Liquid-cooled PRO** (AIO) version — maximum cooling |
| [NexGen3D — AIO mount for BC-250](https://www.printables.com/model/1554003-nexgen3d-aio-mount-for-the-bc-250) | NexGen3D | Bracket to mount an **AIO** (liquid cooler) on the BC-250 |

> Reference cooling guide: [Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/).

## Sources

- [bc250.info](https://bc250.info) — community wiki
- [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) — technical documentation (incl. [cooling](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/))
- [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation) — hardware & cooling notes
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — Compute Unit unlock
- [bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg) — memory configuration
- Linux `amdgpu` kernel driver — [docs.kernel.org/gpu/amdgpu](https://docs.kernel.org/gpu/amdgpu/)
