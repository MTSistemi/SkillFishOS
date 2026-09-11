# What SkillFishOS takes from the BC-250 community, and what it does not

The BC-250 scene moves fast. This page is the ledger: every community item we
looked at in September 2026, where it comes from, whether it is in the
distribution, and why not when it is not. Dates are when we checked.

## In the distribution

| Item | Source | License | Where it lives | Checked |
|---|---|---|---|---|
| Compute queues (4 ACE) in kernel and RADV | [DryhoppedIPA/bc250-gfx1013-fix](https://github.com/DryhoppedIPA/bc250-gfx1013-fix) | MIT | kernel patches, `skillfish-mesa-gfx1013` | +4.2% Cyberpunk 1080p (05/09) |
| 8-core SMU telemetry layout | community research, own patch | GPL-2.0 | kernel patch 0006 | 8 cores, correct clocks |
| SDMA microcode | Debian's `firmware-amd-graphics` already loads the working 0x34 build | | kernel | `SDMA0 firmware version 0x34` |
| C-states and P-states for all 16 threads | [bc250-collective/bc250-acpi-fix](https://github.com/bc250-collective/bc250-acpi-fix), rebuilt by e-tho | MIT | `/usr/share/skillfish/acpi`, early initrd via GRUB | POLL C1 C2 C3, 8 steps 800–3200 MHz |
| ACPI stubs (APTS, AWAK, AFN7 as no-ops) | [e-tho/bc250-acpi-fix](https://github.com/e-tho/bc250-acpi-fix) | MIT | `SSDT-STUBS` in the same cpio | added 11/09 |
| Unified memory heap in RADV | [Necrosiak/bc250-tweaks](https://github.com/Necrosiak/bc250-tweaks) | | `/usr/share/drirc.d/50-skillfish.conf` | no fps change, fewer OOM |
| Shader cache cap 10 GB | same | | `/etc/environment.d/50-skillfish-mesa.conf` | |
| PipeWire quantum 512 @ 48 kHz | same | | `/etc/pipewire/pipewire.conf.d/50-skillfish-latency.conf` | |
| 8-core unlock before the bootloader | [Hexxeh/bc250-efi-core-unlock](https://github.com/Hexxeh/bc250-efi-core-unlock) | MIT | `/usr/share/skillfish/coreunlock`, `skillfish-coreunlock-efi` | pass-through boot verified 11/09; the unlock path needs a board whose BIOS does not unlock |
| DualSense behind a DS5 bridge | [rpf16rj/bc250-steamos-real-toolkit](https://github.com/rpf16rj/bc250-steamos-real-toolkit) | GPL-2.0 (kernel) | kernel patch 0017 | untested: no bridge here |
| YCbCr 4:4:4 + deep color + HDMI 2.1 FRL on PCON dongles | same | GPL-2.0 (kernel) | kernel patch 0018, off by default (`amdgpu.force_ycbcr444=1 force_min_bpc=10 dcfeaturemask=0x402`) | ported to 7.2, untested: no CH7218 dongle here |
| GE-Proton | GloriousEggroll | | Control Center, Games | |
| Gamepad navigation, CSV export | ideas from [movacx/bc250-control-center](https://github.com/movacx/bc250-control-center) | | Control Center | |

## Tested here, not shipped

| Item | Source | Why not | Result |
|---|---|---|---|
| FSR 4 INT8 lowering for gfx1013 | [dmorazasanchez/bc250-fsr4](https://github.com/dmorazasanchez/bc250-fsr4) | no license in the repository | +12% with FSR 4 on; build it yourself with `compila-mesa-2622.sh` |
| Native mesh shaders on gfx1013 | [lonewolf0622/BC250-Native-Mesh-Shaders-](https://github.com/lonewolf0622/BC250-Native-Mesh-Shaders-) | no license; written for Mesa main, does not apply to 26.2.2 | ported to Mesa main (27 hunks by hand) on top of our compute-queue fix: `meshShader = true`, vkcube fine, but the first `vkCmdDrawMeshTasksEXT` hangs the gfx ring beyond recovery (MODE1 reset fails, board rebooted). Whether the culprit is the patch or its combination with the open compute queues is not yet separated |
| Dolby Digital 5.1 over HDMI/DP (live AC-3 encode) | [MastaG/bc250-dual-audio](https://github.com/MastaG/bc250-dual-audio) | no license in the repository; needs WirePlumber 0.5.17 exactly | sink appears, encoder runs; no display with audio on our boards to hear it |

## Measured, no change needed

- **XeSS instead of FSR 3** (community: XeSS Balanced 78 > FSR2/3 75 > FSR4 73 fps in Cyberpunk with ray tracing). Cyberpunk ships XeSS, so we measured the game's own XeSS on RADV, 1080p, Balanced against Balanced, alternating pairs on the dev board (11/09): FSR 3 97.6 / 97.9 fps, XeSS 97.7 / 97.9 fps. Identical at our settings (the frame time is not in the upscaler at 1080p without RT); the community gain shows with ray tracing, where the base frame rate is far lower. The Games page says so in the FSR 4 card.

## Looked at, nothing to do

- **VCN** ([daveconde/bc250-vcn-enable](https://github.com/daveconde/bc250-vcn-enable)): powered on through the SMU, but the register file reads all ones and the firmware must be signed. Same wall we hit.
- **ROCm** ([akandr/bc250-rocm](https://github.com/akandr/bc250-rocm)): runs, Vulkan stays twice as fast at prompt processing. Unsloth Studio on Vulkan remains our AI engine.
- **llama.cpp Vulkan tuning for gfx1013** ([TechMakesArt/llama.cpp-bc250](https://github.com/TechMakesArt/llama.cpp-bc250)): +48% tokens/s. Parked until we move the AI section off Unsloth.
- **Secondary power limit** above 1850–2200 MHz that locks the board hard: hardware (shunt mod), not software. It is the most likely cause of our hangs at 2230 MHz.
- **`fix-freq` / `fix-metrics` governor options**: our governor reads the clock from the SMN directly.
