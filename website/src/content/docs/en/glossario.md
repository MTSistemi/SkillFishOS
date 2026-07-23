---
title: Glossary
description: The technical terms of SkillFishOS and the BC-250, briefly explained.
group: Reference
order: 5
---

The terms that recur throughout the documentation, each explained in one line. In alphabetical order.

## Hardware and APU

**APU** — *Accelerated Processing Unit*: a chip that integrates CPU and GPU on the same die. The BC-250 carries a semi-custom AMD one.

**BC-250** — the board SkillFishOS runs on: Zen 2 + RDNA 2 APU, 16 GB GDDR6, originally made for mining.

**Cyan Skillfish** — the code name of the **graphics** part (GPU) of the BC-250's APU. Hence the name "SkillFish".

**Oberon** — the code name of the **CPU** part (Zen 2) of the APU.

**Compute Unit (CU)** — the GPU's compute blocks. The BC-250 has 40, but exposes fewer by default: SkillFishOS **unlocks them all** (see [kernel](/en/docs/kernel)).

**gfx1013** — the identifier of the BC-250's GPU architecture (RDNA 2 family). It matters because **ROCm doesn't support it** → Vulkan is used instead.

**RDNA 2** — the AMD graphics architecture of the GPU (same family as the current consoles).

**Zen 2** — the AMD CPU architecture of the APU (6 cores / 12 threads).

**GDDR6** — the board's memory type: fast, here **shared** between CPU and GPU.

**UMA** — *Unified Memory Architecture*: CPU and GPU use the **same** memory pool (the ~16 GB of GDDR6).

**GTT** — *Graphics Translation Table*: a mechanism that lets the GPU use system memory beyond dedicated VRAM. SkillFishOS extends it so Vulkan sees ~13 GiB (useful for AI).

## Clocks, voltages, thermals

**SMU** — *System Management Unit*: the micro-controller inside the APU that manages clocks and voltages. On the BC-250 control goes **only** through it, not through standard amdgpu sysfs.

**SMU governor** — the service (`cyan-skillfish-governor`) that sets the GPU's frequency/voltage *safe-points*.

**sclk / mclk** — GPU **core** clock (sclk) and **memory** clock (mclk). On the BC-250 the mclk is **not** adjustable.

**Undervolt** — lowering voltage at the same frequency: same work, **less heat and power**. See [GPU & overclock](/en/docs/gpu-overclock).

**Overclock (OC)** — raising clocks above default for more performance.

**Vid** — the voltage the chip requests at a given frequency. On the BC-250 the hard maximum is **1.325 V**.

**Thermal-guard** — the system watchdog that lowers clocks if 85 °C is exceeded.

**Heat-soak** — heat build-up that skews "back-to-back" benchmarks: let the card cool between runs.

**Silicon lottery** — the fact that each chip tolerates different OC/undervolt: that's why SkillFishOS validates profiles **on your** card.

## System software

**Debian sid** — Debian's *unstable* branch, always up to date but prone to regressions: the base of SkillFishOS (see [Updates](/en/docs/aggiornamenti)).

**KDE Plasma 6** — the desktop environment used, dressed in a steampunk theme.

**linux-tkg** — the kernel build recipe (Frogging-Family) the tailored SkillFishOS kernel is based on.

**Mesa / RADV** — the open-source graphics drivers; **RADV** is the **Vulkan** driver used by the BC-250's GPU.

**ROCm** — AMD's "official" compute stack: it does **not** support gfx1013, so it isn't used.

**Vulkan** — the graphics/compute API used for both gaming and **AI** (Ollama) on the BC-250.

**Btrfs** — the copy-on-write filesystem with snapshots that provides the "safety net" (see [Storage & snapshots](/en/docs/storage-snapshot)).

**Snapper** — the tool that creates automatic Btrfs snapshots before/after updates.

**grub-btrfs** — makes snapshots appear in the GRUB menu for boot-time rollback.

**APT pinning** — holding a package at a verified version, for components that are fragile on this hardware.

**reprepro** — the tool that manages SkillFishOS's signed APT repository.

**HPD** — *Hot-Plug Detect*: monitor connection detection. On the BC-250 it's **broken** → the `skillfish-dp-hotswap` daemon.

**s2idle / suspend** — the ACPI sleep states: **broken** on the BC-250, therefore disabled.

**IOMMU** — I/O virtualization memory management unit: unstable on the BC-250, **never** enabled.

## Gaming and AI

**Proton** — Valve's compatibility layer that runs Windows games on Linux via Steam.

**gamescope** — Valve's micro-compositor for gaming ("console" session, FSR1/NIS upscaling).

**EmuDeck / ES-DE** — emulator installer and frontend for emulation.

**FSR / OptiScaler** — **upscaling** technologies. FSR 4 is unavailable (needs RDNA 4); FSR1/NIS or OptiScaler are used.

**Ollama / OpenWebUI** — backend and interface of the local AI.

**qwen3:14b** — the reference AI model, running entirely on the GPU.

**Tuner** — SkillFishOS's native app to tune the hardware with test-and-rollback (see [Native apps](/en/docs/app-native)).

## Sources

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [amdgpu documentation](https://docs.kernel.org/gpu/amdgpu/) · [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)
