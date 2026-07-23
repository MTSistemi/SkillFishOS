---
title: Performance & benchmarks
description: Every real BC-250 benchmark on SkillFishOS — screenshots, full settings, clocks, voltages, temperatures and power.
group: Reference
order: 3
---

This is the **complete benchmark section**: every run was done on **our own BC-250** with SkillFishOS, with real screenshots, **all the settings used**, and the telemetry of **clocks, voltages, temperatures, power and fan** recorded during the run.

> ⚠️ **Silicon lottery + cooling.** The numbers hold for *this* chip with adequate cooling. The stock cooler is marginal: "back-to-back" comparisons without pauses are skewed by *heat-soak* — let the card cool a few minutes between runs.

## Test conditions (test rig)

Apply to **all** benchmarks below unless stated otherwise.

| Item | Value |
|---|---|
| Board | **AMD BC-250** — Zen 2 "Oberon" + RDNA 2 "Cyan Skillfish" APU (`gfx1013`) |
| Memory | **16 GB GDDR6** unified (UMA) |
| Compute Units | **40 / 40 active** (routed live, see [GPU](/en/docs/gpu-overclock)) |
| Kernel | **7.0.10-skillfishos** (linux-tkg) |
| Driver | **Mesa 26.0.8** — RADV (Vulkan) / radeonsi (OpenGL), ACO |
| GPU governor | cyan-skillfish — idle **350 MHz / 700 mV**, load **2230 MHz / ~1000 mV** |
| OC profile | **Turbo/Crazy** (GPU cap 2230 MHz, CPU 3.9–4.0 GHz) |
| Thermal cap | **85 °C** (SMU + thermal-guard), fan on **auto** |
| Resolution | **1920×1080** |

> Architecture reminder: CPU and GPU share **the same die** and **the same power budget**. Under mixed load the CPU spontaneously gives up clock (≈3.4–3.5 GHz) to stay within budget and under 85 °C — not a defect, the chip self-protecting.

---

## 🎮 Black Myth: Wukong — 112 FPS (1080p)

![Black Myth: Wukong — 112 FPS average at 1080p on the AMD BC-250](/img/benchmarks/wukong-112fps.jpg)

| Setting | Value |
|---|---|
| Resolution | 1920×1080 |
| FPS cap | none (uncapped) |
| Load type | **CPU / draw-call bound** |
| Upscaling | FSR 4 unavailable (RDNA 4) → gamescope FSR1/NIS or OptiScaler |

**Result:** average **112 FPS** · max **128** · min **92** · 1% low **101**.

**Telemetry during the run** (~4 min):

| Metric | Measured value |
|---|---|
| GPU clock | ~1.4–1.6 GHz (*not saturated*: the game is CPU-bound) |
| GPU edge | 83–86 °C |
| GPU power | ~90–140 W |
| GPU mV | ~970–987 mV |
| CPU clock | ~3.5 GHz (dropped from 3.9 due to the shared budget) |
| CPU temp | 85 °C (at the cap) |
| VRAM | ~1.9 GB (menu) → ~4.4 GB (in game) |
| Fan | ~2950–3140 RPM |

> Lesson: in *gameplay* on a draw-call bound title like Wukong, what matters most is **CPU stability** under load and good cooling.

### Governor Balanced vs Performance (benchmark tool)

The benchmark tool's *flythrough* is **GPU-bound**, so there the clock matters. Switching the governor to **Performance** in the Tuner (it holds the GPU at its top safe-point under load, idling to 350 MHz):

| Governor mode | Average | 5%-low |
|---|---|---|
| **Balanced** (default) | 100 FPS | 92 FPS |
| **Performance** | **111 FPS** | **102 FPS** |

**+11%** on the average and on the slowest frames, just from holding the clock high. For safety the Tuner caps the GPU at **2200 MHz @ 1000 mV** with a multi-point voltage curve: 2230 MHz at 1000 mV is undervolted and can hard-freeze the machine.

---

## 🧪 Unigine Superposition — 1080p HIGH: 12938

![Unigine Superposition 1080p High — score 12938 on the BC-250](/img/benchmarks/superposition-high.jpg)

| Setting | Value |
|---|---|
| Version | 1.1 |
| Graphics API | **OpenGL** |
| Resolution | 1920×1080, fullscreen |
| Shaders | **High** |
| Textures | High |
| DOF | enabled |
| Motion Blur | enabled |

**Result:** score **12,938** · FPS min **75.59** · avg **96.77** · max **127.16**.
**Config read by the tool:** CPU AMD BC-250 **@ 3894 MHz**, RAM 7 GB, GPU AMD BC-250 8 GB (Cyan Skillfish), kernel 7.0.10-skillfishos.

---

## 🧪 Unigine Superposition — 1080p EXTREME: 5513

![Unigine Superposition 1080p Extreme — score 5513 on the BC-250](/img/benchmarks/superposition-extreme.jpg)

| Setting | Value |
|---|---|
| Version | 1.1 |
| Graphics API | **OpenGL** |
| Resolution | 1920×1080, fullscreen |
| Shaders | **Extreme** |
| Textures | High |
| DOF | enabled |
| Motion Blur | enabled |

**Result:** score **5,513** · FPS avg **41.25** (min ~32.8 · max ~49).

![Unigine Superposition — scene rendered in real time](/img/benchmarks/superposition-scene.jpg)
*A Superposition scene rendered in real time on the BC-250.*

---

## 🏔️ Unigine Heaven 4.0 — 113.7 FPS · score 2865

![Unigine Heaven 4.0 — 113.7 FPS, score 2865 on the BC-250](/img/benchmarks/heaven-113fps.jpg)

| Setting | Value |
|---|---|
| Graphics API | **OpenGL** |
| Resolution | 1920×1080, windowed |
| Anti-aliasing | **8×** |
| Quality | **Ultra** |
| Tessellation | **Extreme** |

**Result:** **113.7 FPS** · score **2865** · min **54.8** · max **219.5**.
**Platform read by the tool:** Linux 7.0.10-skillfishos x86_64 · CPU AMD BC-250 ×12 · GPU gfx1013.

![Unigine Heaven — scene rendered in real time](/img/benchmarks/heaven-scene.jpg)
*The Heaven scene rendered in real time on the BC-250 during the run.*

---

## ⚙️ GPU compute — vkpeak (synthetic)

Vulkan compute throughput on the **same** board, before and after unlocking the 40 CUs.

| Metric | Baseline 24 CU | SkillFishOS 40 CU |
|---|---|---|
| **FP32** scalar | 6141 GFLOPS | **11,329** GFLOPS *(11,385 cold)* |
| FP16 vec4 | 12,260 | **22,685** |
| int8 dot-product | 24,550 GIOPS | **45,495** GIOPS |
| FP64 scalar | 385 | ~640 |
| copy d2d (internal bandwidth) | — | 191 GBPS |

With the 40 CUs active: **+85%** FP32 over baseline (≈**11.3 TFLOPS**). When hot, under sustained stress, it settles around **10,214 GFLOPS**. At idle the governor drops to 350 MHz, edge ~54 °C after the load.

## 📦 Memory bandwidth — clpeak

| Metric | Value |
|---|---|
| Measured GDDR6 bandwidth | **~350–367 GB/s** |
| `mclk` adjustable | **No** (fixed memory clock) |
| Memory seen by Vulkan | ~13 GiB (with extended GTT) |

---

## 🔧 Tuner profiles — clocks, voltages, temperatures

| Profile | CPU | CPU voltage | GPU | Peak temp |
|---|---|---|---|---|
| **Stock** *(ISO default)* | 3500 MHz | — | 1500 MHz | the lowest |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | balanced |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (cap) |
| **Crazy** | 4.0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C in 120 s stress |

- **Hard maximum Vid: 1.325 V** (never exceeded).
- 85 °C thermal cap on all profiles; fan on auto; at idle the GPU sits at **350 MHz / 700 mV**.

## 🌡️ Thermal validation (stress test)

Data recorded during the Tuner's automatic validation (test-and-rollback).

| Phase | Clock | Temperature | Notes |
|---|---|---|---|
| Idle | CPU ~2.5 GHz · GPU 350 MHz | k10 46 °C · GPU 45 °C | at rest |
| **CPU stress** (12 threads, 120 s) | CPU **3.68–3.69 GHz** | k10 **85 °C** (at the cap) | GPU stays at 350 MHz/56 °C |
| **GPU stress** (vkpeak loop, 120 s) | GPU **2000 MHz** | edge up to **86 °C** | at 86 °C the governor drops to 1819–1900 MHz (thermal-guard); the CPU falls to ~2.2–2.4 GHz due to the shared budget |

---

## 📊 Comparisons

**Same hardware, just changing the OS** — Superposition 1080p Extreme on the **same** BC-250:

| System | Score |
|---|---|
| **SkillFishOS** (GPU 2230 · CPU 3900, 40 CU) | **5513** |
| Other distro (Bazzite, stock clocks) | 4102 |

→ **+34% real performance** from the very same chip, thanks to 40 unlocked CUs, a governor pushing 2230 MHz and CPU OC+undervolt.

**Versus desktop Radeons** (Superposition 1080p High): the BC-250 with SkillFishOS (**12,938**) matches an **RX 6600 / 6600 XT** costing €200+, with raw compute of an **RX 6700** (~11.3 TFLOPS) — on a ~€50 board.

---

## 🛠️ Tools and method

| Tool | What it measures |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | FP32/FP16/int8 throughput via Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | memory bandwidth and OpenCL throughput |
| [sysbench](https://github.com/akopytov/sysbench) | CPU stress/benchmark (also used by the Tuner) |
| [Unigine Superposition / Heaven](https://benchmark.unigine.com/) | OpenGL graphics benchmarks |
| In-game MangoHud | FPS and frametime in real games |
| custom telemetry | clock/temp/power/fan via `amdgpu` sysfs, `k10temp`, `nct6686` |

## Sources

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench) · [Unigine](https://benchmark.unigine.com/)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — CU unlock
- [bc250.info](https://bc250.info) — community safe-points and thermal notes
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — per-game upscaling
