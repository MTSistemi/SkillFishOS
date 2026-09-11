# SkillFishOS Control Center

Since September 2026 every SkillFishOS tool lives in one window. Open it from
the menu (SkillFishOS → Control Center) or with `skillfish-control-center`.

| Section | What it does |
|---|---|
| **Status** | One number per card: GPU clock and ceiling, CPU, compute units, fan; the kernel, the governor, the Vulkan driver in use, whether the last boot followed a clean shutdown. Nothing to set. |
| **Tuner** | The V/F governor curve, drawn inside the chart: drag a knot, double-click to add one, right-click to remove it. The ceiling, three presets, and Apply with a trial countdown (the old curve stays on disk until you press Keep). Panels for CPU, cores, compute units, VRAM, the advanced governor knobs and a quick vkpeak. |
| **Fan** | The fan curve, the source sensors, the lead, the safety limits and the PWM test. The controller runs with or without the window. |
| **Monitor** | Every reading in one chart plus the per-thread bars. REC writes a `.sfmon` you can reopen and scrub. |
| **Games** | Our Mesa per launcher (Steam, Heroic) or for the whole system; the scx_bpfland scheduler armed through GameMode; FSR 4 through OptiScaler; GE-Proton 11 install and default for Steam and Heroic. |
| **Profiles** | Quiet / Balanced / Performance: ceiling, CPU, fan preset and scheduler in one click. Save the current state as your own. |
| **Kernel** | The installed kernels, the default, boot once, uninstall. |
| **Snapshots** | The system snapshots and the btrfs maintenance schedule. |
| **AI** | Unsloth Studio on Vulkan: on/off, hardware, the GTT limit. |
| **Emulators** | EmuDeck, or the emulators one by one from Flathub. |
| **Console** | Steam Big Picture inside gamescope, now or from the login screen. |
| **ISO** | Disk images mounted through udisks. |

The Remote Manager mirrors the same sections on the web: Tuner (with the
curve), Games and Profiles are there too.

A controller drives the window as well: D-pad or left stick move the focus, A
confirms, B goes back, LB and RB switch section, Start opens Status. It needs
`python3-evdev`; without it the window simply ignores the pad. The Monitor's
CSV button exports the open recording (or the last one made) for a
spreadsheet.

## Our Mesa as the system driver

The Games section can make our RADV build the Vulkan driver of the whole
system, desktop included. It needs the SkillFishOS kernel: the build opens
compute queues that wedge the GPU on a kernel without the compute-queue
patches, and the switch refuses to start on another kernel. 32-bit programs
keep Debian's driver.

## Measured after the change (BC-250 dev board, kernel 7.2.4, governor 26.09.12)

Three rounds each, same settings as before the Control Center existed:

| Benchmark | Rounds | Before |
|---|---|---|
| Cyberpunk 2077 (FSR 3 Balanced, median fps) | 98.1 / 98.4 / 98.9 | 98.4 |
| Black Myth: Wukong (no FG, avg fps) | 48 / 50 / 51 | 50 |
| GravityMark (Vulkan, score) | 26881 / 26902 / 27002 | 26868–27140 |
| Unigine Superposition (1080p High) | 12555 / 12580 / 12547 | see release notes |

Nothing moved, which is the point: the window changes how things are set, not
what the hardware does.
