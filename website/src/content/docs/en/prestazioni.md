---
title: Performance & benchmarks
description: All the real numbers measured on our BC-250 — FP32, memory bandwidth, in-game FPS, profiles and power.
group: Reference
order: 3
---

This page collects the **real performance data**, all **measured on our BC-250**. They are a reference, not a promise: every chip is different (*silicon lottery*) and cooling matters a lot.

> ⚠️ The numbers are obtained with the 40 CUs unlocked and adequate cooling. The stock cooler is marginal: "back-to-back" comparisons without pauses are skewed by *heat-soak* — let the card cool down a few minutes between runs.

## Screenshots from our own hardware

Screen captures taken **during the benchmarks**, on **our own** BC-250 running SkillFishOS — no renders, no mockups.

![Black Myth: Wukong — 112 FPS average at 1080p on the AMD BC-250](/img/benchmarks/wukong-112fps.jpg)
*Black Myth: Wukong — **112 FPS** average at 1080p (max 128, 1% low 101). AMD BC-250 APU, RADV gfx1013 GPU.*

![Unigine Heaven 4.0 — 113.7 FPS, score 2865](/img/benchmarks/heaven-113fps.jpg)
*Unigine Heaven 4.0 — **113.7 FPS**, score **2865** (1080p Ultra, 8× AA, Extreme tessellation). Kernel 7.0.10-skillfishos.*

![Unigine Heaven — scene rendered in real time on the BC-250](/img/benchmarks/heaven-scene.jpg)
*Unigine Heaven — the scene rendered in real time on the BC-250 during the run.*

## GPU — FP32 compute (vkpeak)

| Configuration | FP32 | Notes |
|---|---|---|
| Baseline **24 CU** | ~6141 GFLOPS | locked configuration |
| **40 CU** cold | **11385 GFLOPS** | +85% over baseline |
| **40 CU** under stress (hot) | ~10214 GFLOPS | sustained steady state |

Unlocking the 40 Compute Units (see [kernel](/en/docs/kernel) and [hardware](/en/docs/hardware-bc250)) is the single change with the biggest impact on compute performance.

## GPU — memory bandwidth (clpeak)

| Metric | Value |
|---|---|
| Measured GDDR6 bandwidth | **~350–367 GB/s** |
| `mclk` adjustable | **No** (memory clock is fixed) |

Memory is **unified (UMA)**: the ~16 GB of GDDR6 are shared between CPU and GPU. With the extended GTT, Vulkan sees up to **~13 GiB** of memory — useful for AI models (see [Local AI](/en/docs/ai-locale)).

## Tuner profiles — clocks, voltages, temperatures

| Profile | CPU | CPU voltage | GPU | Peak temp |
|---|---|---|---|---|
| **Stock** *(ISO default)* | 3500 MHz | — | 1500 MHz | the lowest |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | balanced |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (cap) |
| **Crazy** | 4.0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C in 120 s stress |

- **Hard maximum Vid: 1.325 V** (never exceeded).
- **85 °C** thermal cap on all profiles, fan on auto.
- At idle the GPU drops to **350 MHz / 700 mV** (SMU governor).

Profiles above Stock must be **validated by the [Tuner](/en/docs/app-native)** on your card, with automatic test and rollback. Details in [GPU, overclock & undervolt](/en/docs/gpu-overclock).

## In-game FPS — the *Black Myth: Wukong* case

*Black Myth: Wukong* is a **CPU/draw-call bound** title: FPS do **not** scale with resolution or GPU clock.

- Raising the GPU to Turbo does **not** increase FPS: what matters is **CPU overclock** and good cooling.
- **FSR 4 is not available** (it needs RDNA 4 hardware). Use **gamescope** upscaling (FSR1/NIS) or **[OptiScaler](https://github.com/optiscaler/OptiScaler)** per-game.

> General lesson: before "pushing the GPU", figure out whether the game is GPU-bound or CPU-bound. On many light and indie titles the BC-250 has headroom to spare; on heavy, draw-call-bound titles the bottleneck is the CPU.

## CPU↔GPU thermal coupling

CPU and GPU share **the same die** and **the same power budget**. Under mixed load (a game using CPU+GPU together) the APU self-protects and the CPU spontaneously drops to **~3450 MHz** to stay within budget and under 85 °C. **It's not a defect**: the chip gives up the least useful clocks. Undervolting one side leaves more thermal headroom for the other.

## Power and thermals

| Item | Indicative value |
|---|---|
| Available sensor | GPU *edge* only (**no** VRAM sensor) |
| Thermal cap | **85 °C** (SMU + system thermal-guard) |
| Stock cooling | marginal → 2× 120 mm + dedicated VRAM fan recommended |

For cooling, printable 3D cases and recommended fans see [BC-250 hardware](/en/docs/hardware-bc250).

## How they were measured

| Tool | What it measures |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | FP32/FP16 throughput via Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | memory bandwidth and OpenCL throughput |
| [sysbench](https://github.com/akopytov/sysbench) | CPU stress/benchmark (also used by the Tuner) |
| In-game MangoHud | FPS and frametime in real games |

## Sources

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — CU unlock
- [bc250.info](https://bc250.info) — community safe-points and thermal notes
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — per-game upscaling
