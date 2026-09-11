---
title: "Control Center"
description: "Every SkillFishOS tool in one window: Tuner, Fan, Monitor, Games, Profiles, Kernel, Snapshots, AI, Emulators, Console, ISO."
group: Usage
order: 4
---

Every SkillFishOS tool lives in one window. Open it from the menu (SkillFishOS → Control Center) or with `skillfish-control-center`. A controller drives it too: D-pad or stick to move, A confirms, B goes back, LB and RB switch section.

## The sections

- **Status**: one number per card: GPU clock and ceiling, CPU, compute units, fan, kernel, governor, Vulkan driver, whether the last boot followed a clean shutdown. Nothing to set.
- **Tuner**: the voltage/frequency curve of the GPU governor, the CPU, the cores, the compute units, the VRAM split.
- **Fan**: the fan curve with its lead, the source sensors, the safety limits, the PWM test.
- **Monitor**: every reading in one chart per unit, plus the per-thread clock bars. REC records, CSV exports.
- **Games**: our Mesa per launcher or system-wide, the scx_bpfland scheduler, FSR 4, GE-Proton install and default.
- **Profiles**: ceiling, CPU, fan and scheduler in one click; save your own.
- **Kernel**: the installed kernels, the default one, boot once, uninstall.
- **Snapshots**: system snapshots and the btrfs maintenance schedule.
- **AI**: Unsloth Studio on Vulkan: on/off, hardware, the GTT limit.
- **Emulators**: EmuDeck, or the emulators one by one from Flathub.
- **Console**: Steam Big Picture inside gamescope, now or from the login screen.
- **ISO**: disk images mounted through udisks.

## Tuner

The curve is the chart: MHz across, millivolts up. Drag a knot, double-click to add one, right-click to remove it, or type the numbers in the table beside the chart (+ and − add and remove knots). The dashed vertical line is the ceiling, the blue dot is the GPU right now. Three presets: **Cautious 1850** (the sweet spot with the stock heatsink, nearly the same frames and ten degrees less), **Balanced 2000**, **Performance 2100** (the fifteen-point curve measured on the development board, the one we ship).

**Apply is a trial.** A curve that asks too little voltage hangs the board, and on the BC-250 a hang means pulling the plug. So Apply starts the candidate with the previous curve still on disk and counts down 25 seconds: press Keep and the candidate is written for good; do nothing, or let the board die and come back, and the previous curve is what boots.

The panels open on demand:

- **CPU**: clock, undervolt step (6.25 mV each) and thermal limit, each with a slider and a number box at step 1. *Suggest UV* walks the undervolt down two steps at a time with twelve seconds of load per step; *Find my max* climbs from 3600 to 4000 MHz; *Test 60 s* loads the current values. Every run shows a countdown and a Stop button; the values under test are never written to disk, so a hang boots the previous ones. Above 3500 MHz with eight cores the gain is nil: heat is in charge.
- **Cores**: which cores are online, SMT, the 8-core unlock (6c/12t becomes 8c/16t, +20% measured) and *Before boot (EFI)*: the unlock done before GRUB in a single boot, instead of the extra reboot of the in-system service.
- **CU**: the 40 compute units as 20 cells (pairs): green on, red off, grey kept on by the driver. Type the number of CUs you want (24 to 40, in pairs) or click the cells; *Test CU* turns the extra pairs on one at a time under vkpeak and reports errors, for the silicon lottery.
- **VRAM**: the UMA split in the CMOS, applied at the next boot. With the 512 MB dynamic split some games pick low textures: if they look blurry, try 4 or 6 GB fixed.
- **Advanced**: the governor's own knobs: ascent margin, step, descent confirmations, thermal and power thresholds, droop.
- **Test**: vkpeak and the helper log.

## Monitor

One chart per quantity, each with its own true scale: temperatures (CPU, GPU, VRM, system, NVMe), clocks (CPU average, min, max, GPU and its ceiling), load, power, voltages, fan and memory (RAM, VRAM, GTT), plus one bar per thread. Click a legend entry to hide a line; hover to read every chart at the same instant. REC writes a `.sfmon` file (CSV) that Open reloads with a scrubber; CSV exports it for a spreadsheet.

## Games

- **Vulkan driver**: our Mesa opens the compute queues the stock driver keeps closed on this GPU: +4% in Cyberpunk 2077, +12% with FSR 4 on. Per launcher (Steam, Heroic) through a flatpak override, or for the whole system. It needs the SkillFishOS kernel: on another kernel those queues wedge the GPU, and the system-wide switch refuses to start there. The card shows the kernel that is running.
- **Scheduler**: scx_bpfland, loaded only while a game runs (GameMode raises it at launch and drops it at exit): +1.5-2% in Cyberpunk and steadier frames. If the kernel ejects it twice the service stops until you reset the counter: that is the "Ejected by the kernel" row.
- **FSR 4**: through OptiScaler on the game's DLSS path. GE-Proton 11 downloads OptiScaler by itself when it finds `PROTON_USE_OPTISCALER=1`, the game must be set to DLSS, and AMD's FSR 4 library (`amdxcffx64.dll`, from AMD's Windows driver) goes next to the game. XeSS, where a game has it built in, costs the same as FSR 3 at 1080p.
- **Proton**: the GE-Proton 11 releases; Install downloads one (about 500 MB) into the Steam and Heroic folders, Default picks it. Steam must be closed for its default to be written.

## Fan, profiles and the rest

The **Fan** page draws the curve inside the chart of the sensors: at this temperature the fan turns like this, with a lead so the speed rises before the temperature does. **Profiles** move the ceiling within the curve that is already there and set CPU, fan preset and scheduler together. **Snapshots** are pictures of the system, your files are not touched. **AI** holds GPU memory while on: turn it off before gaming. **Console** starts Steam Big Picture inside gamescope on top of the desktop, or as a session from the login screen. The **Remote Manager** mirrors the Tuner, Games and Profiles pages in a browser.
