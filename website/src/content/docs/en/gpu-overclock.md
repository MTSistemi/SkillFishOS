---
title: GPU, CPU, overclocking and undervolting
description: How SkillFishOS controls the BC-250's clocks, voltages and temperatures — with the real numbers measured on the hardware.
group: System
order: 2
---

On a normal APU you tune clocks through the `amdgpu` sysfs. On the BC-250 **that doesn't work**: control goes through the **SMU** (System Management Unit) and needs dedicated tools. SkillFishOS bundles them all, pre-configured with safe profiles and a thermal-protection system.

> ⚠️ **Silicon lottery.** Every number on this page is **measured on our BC-250**. Each card is different: one may take a deeper undervolt, another less. That's why SkillFishOS **always boots in the Stock profile** and lets you climb using the [Tuner](/docs/app-native), which validates each preset **on your card** with an automatic test and rollback.

## The three profiles

The [Tuner](/docs/app-native) exposes **four presets**. The ISO boots in **Stock**; the others are one click away after the test.

| Profile | CPU | GPU | Notes |
|---|---|---|---|
| **Stock** *(ISO default)* | 3500 MHz | 1500 MHz | Maximum compatibility on any BC-250 |
| **Performance** | 3700 MHz · ~1106 mV | 2000 MHz | Balanced and undervolted |
| **Turbo** | 3900 MHz · ~1199 mV | 2230 MHz | High boost, validated under the 85 °C cap |
| **Crazy** | 4.0 GHz · ~1224 mV | 2230 MHz | Validated maximum (~83 °C under stress) |

All profiles honour the same **85 °C thermal cap** and keep the **fan on auto**.

## The GPU SMU governor

GPU clocks are driven by the **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (written in Rust), a system service configured in `/etc/cyan-skillfish-governor/config.toml`. It defines frequency/voltage *safe-points*: **350 MHz / 700 mV** at idle, and the profile value under load (e.g. 1500/900 in Stock, 2230/1000 in Turbo).

> The standard amdgpu sysfs (`power_dpm_force_performance_level`, `pp_dpm_sclk`) does **not** control the BC-250 — only the SMU governor does. The GPU only ramps to its boost clock under real **graphics saturation**.

## CPU overclocking and undervolting

The CPU (6× Zen 2 "Oberon" cores) is handled by a one-shot service **`bc250-smu-oc.service`** that applies the values from `/etc/bc250-smu-oc.conf` via the [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc) project. It shows as *inactive* after applying — that's normal (it's one-shot).

What we measured pushing **our** card:

- **3700 MHz** (*Performance* preset) undervolted to ~**1106 mV** (`scale −16`);
- **3900 MHz** (*Turbo* preset) at ~**1199 mV** (`scale −24`);
- **4.0 GHz** (*Crazy* preset) validated at ~**1224 mV** (`scale −36`) for 120 s of sustained stress, peaking at **83 °C** — the usable maximum on this sample;
- **Hard Vid ceiling: 1.325 V** (never exceeded).

**Undervolting** isn't about "pushing" — it's about doing the same work with **less heat and less power**: at a given frequency, lowering the voltage until it stays stable drops the temperature and leaves thermal headroom for the rest of the APU.

### CPU↔GPU thermal coupling

CPU and GPU share the **same die** and the **same power budget**. Under **mixed** load (a demanding game: CPU + GPU together) the APU self-protects and the CPU spontaneously drops to ~**3450 MHz** to stay within budget and under 85 °C. **This is not a defect**: it's the chip protecting itself by shedding the least-useful clocks. For the same reason, a CPU undervolt leaves more thermal "room" for the GPU, and vice-versa.

## The 40 Compute Units — live

The BC-250 has **40 CUs** (20 WGP, 1 WGP = 2 CU), but the driver enables **24** by default. SkillFishOS routes them up to 40 **at runtime, no reboot**: the system boots at the driver baseline (24 CU) and a service brings it to 40 at startup; from the [Tuner](/en/docs/app-native) you adjust the count **live** with a grid of squares and 24/32/40 presets. The first 24 CUs are driver-locked and always on.

With all 40 CUs enabled the GPU measures **11385 GFLOPS** FP32 (vkpeak) cold, versus ~**6141** for a 24-CU baseline: **+85%**. Under sustained stress (hot) it settles around **10214 GFLOPS**. Measured memory bandwidth (clpeak) is **~350–367 GB/s**.

> 🔬 **Silicon lottery.** On salvaged/"discard" chips some CUs may be marginal. The [Tuner](/en/docs/app-native) has a **"CU test"** that stresses each pair and flags GPU faults/hangs, so you can confirm your chip sustains all 40 CUs. (Mechanism via `umr`, writing the WGP masks — credit to [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), clean-room reimplementation.)

## Thermal protection — the 85 °C cap

The thermal ceiling is **85 °C**, enforced on two levels:

1. **SMU side**: the `max_temperature` value in the config makes the chip reduce clocks *before* crossing 85 °C (avoiding hard throttling);
2. **system side**: a **thermal-guard** watchdog that, if temperature exceeds the cap, steps clocks down 100 MHz at a time until it's back in range.

Things to know about the stock cooler (see also [BC-250 hardware](/docs/hardware-bc250) for **3D-printable cases and recommended fans**):

- the stock heatsink is **marginal**: "back-to-back" benchmark comparisons are skewed by *heat-soak* — let the card cool for a few minutes between runs;
- only the GPU *edge* sensor exists; there is **no VRAM temperature sensor**;
- memory bandwidth is healthy but `mclk` is **not** adjustable.

## A real case: CPU-bound games

Some titles — like *Black Myth: Wukong* in **gameplay** — are **CPU/draw-call bound**: FPS barely depend on resolution or GPU clock. There, **CPU** overclocking and good cooling help instead. For upscaling, FSR 4 is **not available** (it's RDNA 4 hardware); use gamescope (FSR1/NIS) or per-game [OptiScaler](https://github.com/optiscaler/OptiScaler).

When the workload **is** GPU-bound (e.g. the Wukong benchmark *flythrough*), the clock matters: in the **Tuner** you can switch the **governor to "Performance"**, which holds the GPU at its top safe-point under load (it still idles to 350 MHz). Measured on the Wukong benchmark: **100 → 111 FPS average (+11%)**, 92 → 102 on the slowest frames. For safety the Tuner caps the GPU at **2200 MHz @ 1000 mV** (the stable maximum on stock cooling) with a multi-point voltage curve — pushing 2230 MHz at 1000 mV is undervolted and can hard-freeze the machine.

## All of this, without a terminal

Clocks, undervolt, fan and Compute Units are tuned from the **Tuner** GUI, with the four ready presets and **automatic test + rollback** if your card can't hold a value — see [Native apps](/docs/app-native). It's the recommended way: start at Stock, move to Performance, try Turbo or Crazy, and the Tuner validates everything on **your** BC-250.

## Sources

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — GPU SMU governor
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — CPU overclock/undervolt via SMU
- [bc250.info](https://bc250.info) — community safe-points and thermal notes
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — FP32 and memory-bandwidth benchmarks
