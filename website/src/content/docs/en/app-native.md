---
title: Native apps — Tuner and AI
description: SkillFishOS's graphical tools for controlling hardware and AI without a terminal.
group: Usage
order: 3
---

SkillFishOS includes two native applications (written in **PyQt6**, themed with Kvantum) that put hardware and AI-stack control in the user's hands **without touching the terminal**.

## SkillFishOS Tuner

The **Tuner** is the hardware control panel. It lets you adjust:

- **CPU overclock and undervolt**;
- **GPU safe-points** (via the SMU governor, see [GPU and overclock](/en/docs/gpu-overclock));
- the **fan** (PWM control);
- the **UMA VRAM** (requires a reboot);
- the **Compute Units, live** — see below.

### Live Compute Units (grid)

The Tuner shows the GPU's CUs as a **grid of squares** (4 SE/SH rows × 5 WGP): **green = active, red = off**. You toggle them **live, no reboot** — click the pairs (1 WGP = 2 CU) or use the **24 / 32 / 40 CU presets** — then *Apply live*. The first 24 CUs are the driver minimum and stay always on (see [GPU and overclock](/en/docs/gpu-overclock)).

### CU test (silicon lottery)

The **"CU test"** button checks the health of the extra CUs: it enables each pair alone, stresses it with **vkpeak** and watches for **GPU faults/hangs**, plus a final full-40 stress. It's there to catch **defective CUs** on salvaged/"discard" APUs, so you know whether your chip sustains all 40 CUs.

### "Test" flow and live monitor

The **"Test"** flow (CPU, GPU, CU, fan): apply a change → run a benchmark → **verify** stability and, if something is wrong, perform an automatic **rollback**. When any test starts, a **Monitor window** opens with live charts of **temperature, frequency, voltage and fan** (closable at will).

Architecture: a user GUI plus a small **root daemon** that performs the privileged operations. On a personal PC it is configured not to ask for a password on every operation. The desktop HUD also shows the **active CUs** live.

## SkillFishOS AI

The **AI panel** turns the local LLM stack on and off with one click, freeing GPU and RAM for games when not needed. It's the "easy" front-end of the stack described in [On-device AI](/en/docs/ai-locale).

## Why they exist

SkillFishOS's goal is that **anyone** — including the youngest — can use and tune the system without having to learn terminal commands. These apps translate complex operations (SMU governor, kernel parameters, Docker containers) into a few clicks, while keeping the **safeguards** (thermal-guard, test-and-rollback) always active.

## Sources

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Project repository — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)
