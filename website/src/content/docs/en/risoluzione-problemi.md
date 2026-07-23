---
title: Troubleshooting
description: The most common BC-250 problems and how SkillFishOS handles them.
group: Reference
order: 1
---

Many of the BC-250's "problems" are actually known hardware flaws that SkillFishOS works around automatically. Here are the most common ones.

## The screen stays black / the monitor isn't detected

The DisplayPort **Hot-Plug Detect (HPD) is broken**: the board doesn't detect when you connect a monitor. SkillFishOS handles this with the `skillfish-dp-hotswap` daemon (which forces detection at boot and on monitor changes) and the `video=DP-1:e` kernel parameter.

What to check:

- use a **DisplayPort monitor** or a **passive** DP→HDMI adapter;
- avoid **active** DP→HDMI adapters: besides detection issues, they **break the audio** (see below);
- if the monitor changed, wait a few seconds: detection is automatic but not instant.

## The board won't wake from standby

Suspend is **broken at the hardware level**. SkillFishOS disables it completely for this very reason (see [Desktop](/en/docs/desktop)). If the board appears "dead" after being idle and power management had been changed, the only way out is a **physical reset**. Do not re-enable sleep states.

## No audio from the monitor/TV

DisplayPort audio works, but:

- **active DP→HDMI adapters** break the audio: use passive adapters, a native DP monitor, a **USB DAC** or **Bluetooth** audio;
- the audio stack is **PipeWire**: the default sink is set from KDE's audio settings.

## The controllers don't work

- **DualShock 4** controllers go over **Bluetooth** (with gyroscope). To pair: hold *Share + PS* until they blink, then pair from the Bluetooth GUI.
- A controller **over USB** must be connected with a **data** cable (not just charging): it's recognized as an Xbox 360.
- Clone controllers may not share the Bluetooth adapter well with the DS4s: in that case use them **over USB**.

## The GPU seems slow / temperatures are high

- Check in the [Tuner](/en/docs/app-native) that the **40 CUs** and the SMU governor are active.
- Remember the cooling is marginal: after prolonged load the **thermal-guard** (85 °C) kicks in. For valid benchmarks, let the board cool between runs (see [GPU](/en/docs/gpu-overclock)).
- For **CPU-bound** games, lowering the resolution won't raise the FPS.

## The board froze (hard freeze)

The BC-250 can hit a **hard freeze** (total lock-up), often tied to **too-aggressive undervolt**: the instability mostly shows up at **low load**, so a freeze can even strike at idle. SkillFishOS tackles it on two fronts:

- **Hardware watchdog** — the chipset's **SP5100 TCO** timer is active (`RuntimeWatchdogSec=2min`): if the system locks up completely, the board **reboots itself** within two minutes, no need to pull the power.
- **Freeze detector** — at boot a service notices whether the previous shutdown was abnormal (no clean-shutdown marker) and **logs it** to `/var/log/skillfish-freeze.log`, with a desktop notification. The counter also shows up in the Tuner's **"My silicon"** panel.

If freezes recur, **drop one preset** (e.g. from Crazy/Turbo to Performance) in the Tuner: the less aggressive value is almost always the fix. All presets are **crash-safe** — a freeze mid-test never leaves the board on an unstable profile at reboot. If they persist even in Stock, suspect the **power supply**.

## An update broke something

Reboot and from the **GRUB → "SkillFishOS snapshots"** menu pick a working previous snapshot. See [Storage and snapshots](/en/docs/storage-snapshot). Pre/post-update snapshots are automatic.

## The AI won't start or gives strange output

- The AI runs on Vulkan (not ROCm) and **shouldn't be used together with games** (same GPU/RAM).
- If the output is corrupted, make sure you're using the KV cache in **f16** (`q4_0` corrupts the output on RADV). See [On-device AI](/en/docs/ai-locale).

## Sources

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — troubleshooting](https://docs.pipewire.org/)
