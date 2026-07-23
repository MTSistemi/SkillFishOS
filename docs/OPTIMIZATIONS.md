# System optimizations

This is the heart of SkillFishOS: the work that turns a raw **AMD BC‑250** compute board into a fast, stable, daily‑drivable machine. Everything here is **pre‑configured and tested** — you don't need to apply any of it by hand. It's documented so the community can understand, reproduce and improve it.

The BC‑250 is a semi‑custom APU from the **AMD Zen 2 + RDNA 2** family: CPU codename *Oberon*, GPU *Cyan Skillfish* (`GFX1013`), 16 GB of shared GDDR6. It's great value but a hostile Linux target. Here's each problem and how it's solved.

---

## 1. Custom kernel — `linux-tkg` 7.0.10‑skillfishos

Built from [Frogging‑Family/linux‑tkg](https://github.com/Frogging-Family/linux-tkg) with:

- **BORE** scheduler, GCC `-O3`, `-march=znver2`, **1000 Hz**, NTsync + fsync — for gaming responsiveness.
- **BC‑250 userpatches:**
  - **GPU frequency unlock** — exposes the SMU clock range **350–2230 MHz** (stock firmware otherwise pins it).
  - **40‑CU unlock** (opt‑in) — enables all 40 compute units instead of the default 24.
  - **RDSEED‑quiet** — the BC‑250 silicon has an unreliable `RDSEED`; mainline correctly disables it but prints `RDSEED is not reliable on this platform; disabling.` twelve times at boot (once per CPU, at EMERG priority, before any graphical console). The patch removes **only** the cosmetic `pr_emerg()` line while keeping `clear_cpu_cap()` + the MSR bit clear, so RDSEED stays correctly disabled — silently.

> ⚠️ **Never enable IOMMU on the BC‑250** — it's broken on this hardware. Avoid kernels 6.15.0–6.15.6 and 6.17.8–6.17.10.

Recipe and patches: [`kernel-build/`](../kernel-build/). Build instructions: [BUILD.md](BUILD.md). Prebuilt `.deb`: [Releases](../../../releases/tag/kernel-7.0.10-skillfishos).

---

## 2. GPU clock control — the governor

⚠️ The standard amdgpu sysfs (`power_dpm_force_performance_level`) **does not control the BC‑250** — only the SMU does, through the OD voltage curve. SkillFishOS uses the [`cyan-skillfish-governor`](https://github.com/Magnap/cyan-skillfish-governor) (Rust), installed as a systemd service with safe‑points in `/etc/cyan-skillfish-governor/config.toml`.

It is **load‑based**: it settles on the *lowest* frequency that keeps GPU utilisation inside the `[load-target]` band, idling to **350 MHz** when the GPU is unused. Two profiles, switchable from the **SkillFishOS Tuner** (GPU → *Governor mode*):

- **Balanced** (default, band `0.70–0.95`): raises the clock only as much as the workload needs — cooler and quieter.
- **Performance** (band `0.08–0.20` + snappier ramp): holds the **top safe‑point under any gaming load**, for the best FPS in GPU‑bound titles. Still idles to 350 MHz on the desktop.

**Measured (Black Myth: Wukong Benchmark Tool, 1080p):** Balanced ≈ **100 FPS** avg / 92 FPS 5%‑low; Performance ≈ **111 FPS** avg / 102 FPS 5%‑low — **+11%**. (An earlier note claimed 2000 ≈ 2230 MHz gave identical FPS; that held for *gameplay*, which is more CPU/draw‑call bound. The benchmark **flythrough** is heavier and *is* GPU‑bound, so holding a high clock clearly helps there.)

⚠️ **The voltage curve must be a smooth multi‑point ladder — `350/700, 1500/900, 2000/1000, 2200/1000`.** On the BC‑250, **1000 mV is the practical stable ceiling at ~2150–2200 MHz**; **2230 MHz @ 1000 mV is undervolted**, and an abrupt clock transition there can **hard‑freeze the whole machine** (reproduced: a 2‑point `350/700 → 2230/1000` curve hung the box on the load→idle transition, with nothing in the logs). The Tuner therefore caps the max at **2200 MHz** and inserts the mid‑points so transitions are gentle; governor reloads stop → settle → start to avoid the abrupt SMU jump. 2230 needs 1000–1060 mV and the silicon lottery.

Memory bandwidth was *measured* (clpeak/OpenCL) at **~350–367 GB/s** — healthy, not a bottleneck. The `Memory Clock 450 MHz` the driver reports is a reporting convention, not a 1/4 clock. Memory clock is **not** adjustable on the BC‑250.

---

## 3. CPU overclock & undervolt — 3.7 GHz

A persistent SMU overclock via [`bc250_smu_oc`](https://github.com/bc250-collective/bc250_smu_oc), applied at boot by a one‑shot systemd service from `/etc/bc250-smu-oc.conf`:

- **3700 MHz** with **Vid ≤ 1.325 V**, 6 cores active, **85 °C** thermal cap.
- 3700 is this chip's verified‑stable maximum under an 85 °C cap; 3800 throttles back to 3700 reproducibly.
- **APU power sharing:** under a combined CPU+GPU load the APU eases the CPU to ~3450 MHz to stay in budget — by design, no instability. Under CPU‑only load it holds 3700 MHz pinned right at the 85 °C guard.
- A **thermal guard** watchdog steps the clock down if temperature exceeds the cap.

⚠️ **SMU contention:** the governor and the OC tool both talk to the SMU. The OC service ordering (`After=`) and a lock prevent them from clashing during apply/detect.

---

## 4. 40‑CU unlock

Adds `amdgpu.bc250_cc_write_mode=3` to the kernel cmdline → `active_cu_number` goes from **24 → 40** at GPU init. Result: fp32 jumps from ~6.9 to **~11.3 TFLOPS** (vkpeak `11329` GFLOPS). It's a boot‑time setting (no runtime toggle); the **Tuner** flips it for you and reboots.

| Configuration | vkpeak fp32 (GFLOPS) |
|---|---:|
| Stock ~2000 MHz, 24 CU (baseline) | 6141 |
| tkg + governor, 24 CU | 6868 |
| **tkg + governor + 40 CU** | **11329** |

---

## 5. Memory split — VRAM (UMA) & GTT

All memory is shared GDDR6, so the split can be managed from the OS:

- **UMA VRAM** is set in the BIOS CMOS via [`bc250_memcfg`](https://github.com/fanoush/bc250_memcfg) (persistent, battery‑backed; needs a reboot). The Tuner exposes this.
- **GTT** is raised with `amdgpu.gttsize=` on the cmdline so the GPU can address far more than the UMA VRAM.
- **TTM** page limits are raised (`ttm.pages_limit` / `ttm.page_pool_size`) so Vulkan can see the full pool — essential for running large LLMs on the GPU. See [AI.md](AI.md).

---

## 6. Display — broken HPD / DisplayPort

The BC‑250's hotplug‑detect (HPD) line is non‑functional: the GPU never reads the monitor's EDID, so connectors report `disconnected` and audio/video fail or fall back to VESA.

- **Generic fix:** `video=DP-1:e` on the cmdline force‑enables the connector *without* hardcoding a resolution — the monitor's EDID is then read and the **monitor decides the resolution**. This also makes the DisplayPort audio sink appear.
- **Hot‑swap daemon** (`skillfish-dp-hotswap`): the kernel still updates the sysfs `edid` file passively on plug/unplug, so the daemon polls it silently and triggers a re‑detect **only** when the EDID changes — giving monitor hot‑swap with automatic resolution change and (almost) no flicker.

⚠️ Active DP→HDMI adapters break audio on the BC‑250 — use a native DP monitor, a passive adapter, or a USB DAC.

---

## 7. Audio

The full **PipeWire** stack (pipewire‑pulse, WirePlumber, ALSA/BT) with user services enabled. Output works over DisplayPort (once the display fix above validates the ELD), USB DAC, or **Bluetooth** speakers — WirePlumber creates the sink automatically.

---

## 8. Wi‑Fi & Bluetooth

Common combo adapters (e.g. Realtek **RTL8851BU**, Wi‑Fi 6 + BT) ship in **CD‑ROM installer mode**. `usb-modeswitch` + `usb-modeswitch-data` flip them to the real device, persistently via udev — without them there is **no Wi‑Fi and no Bluetooth** on these adapters.

---

## 9. Game controllers

The kernel ships `xpad`, `hid_playstation`, `hid_nintendo`, `hid_sony`, `hid_steam`, etc. Verified working:

- **DualShock 4** over Bluetooth (with gyro/motion) — trusted auto‑reconnect.
- Generic "Pro Controller" clones: most reliable **over USB**, where they enumerate as an Xbox 360 pad (`xpad`, XInput mode).

Controller battery levels (via UPower) are surfaced in the desktop HUD.

---

## 10. Storage — Btrfs + Snapper + grub‑btrfs

- Subvolumes `@rootfs` and a **separate `@home`** — rollbacks never touch user data.
- **Snapper** with timeline + automatic **pre/post‑apt** snapshots.
- **grub‑btrfs** (built from source — not in Debian) puts bootable snapshots directly in the GRUB menu. The "safety net for tinkering" is real and one reboot away.

> ⚠️ `desktop-base` can re‑inject the Debian GRUB theme via `/etc/grub.d/05_debian_theme`; SkillFishOS disables it (`chmod -x`) so the steampunk GRUB theme stays.

---

## 11. Always‑on (no suspend)

The BC‑250's ACPI suspend is broken (it enters `s2idle` and never wakes → reset). SkillFishOS **masks** `sleep.target suspend.target hibernate.target hybrid-sleep.target` and sets logind/KDE to never idle‑suspend or lock — so the box stays reachable (important for remote access) and a child or a remote session is never locked out. **This mask is mandatory on any desktop environment.**

---

## Further reading

- [DESKTOP.md](DESKTOP.md) — desktop, theme, HUD, Tuner, AI panel
- [GAMING.md](GAMING.md) — the gaming & emulation stack
- [AI.md](AI.md) — local LLMs on the GPU
- [BUILD.md](BUILD.md) — build the kernel and ISO
