---
title: GPU, CPU, overclocking and undervolting
description: How SkillFishOS controls the BC-250's clocks, voltages and temperatures — with the real numbers measured on the hardware.
group: System
order: 2
---

On a normal APU you tune clocks through the `amdgpu` sysfs. On the BC-250 **that doesn't work**: control goes through the **SMU** (System Management Unit) and needs dedicated tools. SkillFishOS bundles them all, pre-configured with safe profiles and a thermal-protection system.

> ⚠️ **Silicon lottery.** Every number on this page is **measured on our BC-250**. Each card is different: one may take a deeper undervolt, another less. That's why SkillFishOS **always boots in the Stock profile** and lets you climb using the [Tuner](/docs/app-native), which validates each preset **on your card** with an automatic test and rollback.

## The three profiles

The [Tuner](/docs/app-native) exposes three presets. The ISO boots in **Stock**; the other two are one click away after the test.

| Profile | CPU | GPU | Notes |
|---|---|---|---|
| **Stock** *(ISO default)* | 3500 MHz | 1500 MHz | Maximum compatibility on any BC-250 |
| **Performance** | 3700 MHz | 2000 MHz | Good performance/heat balance |
| **Turbo** | 3900 MHz | 2230 MHz | Peak performance, validated under the 85 °C cap |

All profiles honour the same **85 °C thermal cap** and keep the **fan on auto**.

## The GPU SMU governor

GPU clocks are driven by the **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (written in Rust), a system service configured in `/etc/cyan-skillfish-governor/config.toml`. It defines frequency/voltage *safe-points*: **350 MHz / 700 mV** at idle, and the profile value under load (e.g. 1500/900 in Stock, 2230/1000 in Turbo).

> The standard amdgpu sysfs (`power_dpm_force_performance_level`, `pp_dpm_sclk`) does **not** control the BC-250 — only the SMU governor does. The GPU only ramps to its boost clock under real **graphics saturation**.

## CPU overclocking and undervolting

The CPU (6× Zen 2 "Oberon" cores) is handled by a one-shot service **`bc250-smu-oc.service`** that applies the values from `/etc/bc250-smu-oc.conf` via the [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc) project. It shows as *inactive* after applying — that's normal (it's one-shot).

What we measured pushing **our** card:

- **3700 MHz** stable at a real voltage (Vid) of ~**1.23 V**, under 85 °C;
- **3900 MHz** (Turbo) validated with a curve undervolt (`scale −24`);
- **4.0 GHz** reached and validated at ~**1206 mV** for 120 s of sustained stress, peaking at **83 °C** — the usable ceiling before instability on this sample;
- **Hard Vid ceiling: 1.325 V** (never exceeded).

**Undervolting** isn't about "pushing" — it's about doing the same work with **less heat and less power**: at a given frequency, lowering the voltage until it stays stable drops the temperature and leaves thermal headroom for the rest of the APU.

### CPU↔GPU thermal coupling

CPU and GPU share the **same die** and the **same power budget**. Under **mixed** load (a demanding game: CPU + GPU together) the APU self-protects and the CPU spontaneously drops to ~**3450 MHz** to stay within budget and under 85 °C. **This is not a defect**: it's the chip protecting itself by shedding the least-useful clocks. For the same reason, a CPU undervolt leaves more thermal "room" for the GPU, and vice-versa.

## The 40 Compute Units

With all 40 CUs enabled (see [kernel](/docs/kernel)) the GPU measures **11385 GFLOPS** FP32 (vkpeak) cold, versus ~**6141** for a 24-CU baseline: **+85%**. Under sustained stress (hot) it settles around **10214 GFLOPS**. Measured memory bandwidth (clpeak) is **~350–367 GB/s**.

## Thermal protection — the 85 °C cap

The thermal ceiling is **85 °C**, enforced on two levels:

1. **SMU side**: the `max_temperature` value in the config makes the chip reduce clocks *before* crossing 85 °C (avoiding hard throttling);
2. **system side**: a **thermal-guard** watchdog that, if temperature exceeds the cap, steps clocks down 100 MHz at a time until it's back in range.

Things to know about the stock cooler (see also [BC-250 hardware](/docs/hardware-bc250) for **3D-printable cases and recommended fans**):

- the stock heatsink is **marginal**: "back-to-back" benchmark comparisons are skewed by *heat-soak* — let the card cool for a few minutes between runs;
- only the GPU *edge* sensor exists; there is **no VRAM temperature sensor**;
- memory bandwidth is healthy but `mclk` is **not** adjustable.

## A real case: CPU-bound games

Some titles — like *Black Myth: Wukong* — are **CPU/draw-call bound**: FPS do **not** depend on resolution or GPU clock. In those cases you don't need GPU Turbo: **CPU** overclocking and good cooling help instead. For upscaling, FSR 4 is **not available** (it's RDNA 4 hardware); use gamescope (FSR1/NIS) or per-game [OptiScaler](https://github.com/optiscaler/OptiScaler).

## All of this, without a terminal

Clocks, undervolt, fan and Compute Units are tuned from the **Tuner** GUI, with the three ready presets and **automatic test + rollback** if your card can't hold a value — see [Native apps](/docs/app-native). It's the recommended way: start at Stock, move to Performance, try Turbo, and the Tuner validates everything on **your** BC-250.

## Sources

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — GPU SMU governor
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — CPU overclock/undervolt via SMU
- [bc250.info](https://bc250.info) — community safe-points and thermal notes
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — FP32 and memory-bandwidth benchmarks
