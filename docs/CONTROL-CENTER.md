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

## Tuner

The voltage/frequency curve of the governor is the chart: MHz across,
millivolts up, the knots drag, and the same knots sit in a table beside the
chart where every value can be typed. The dashed vertical line is the ceiling;
the blue dot is the GPU right now. Apply runs the candidate on trial for 25
seconds with the old curve kept on disk: unless you press Keep, the old one is
what boots.

The panels open on demand:

- **CPU**: clock, undervolt step (6.25 mV each) and thermal limit, each with a
  slider and a number box (step 1 MHz). "Suggest UV" walks the undervolt down
  two steps at a time with twelve seconds of load per step; "Find my max"
  climbs from 3600 to 4000 MHz; "Test 60 s" loads the current values. Every
  run shows a countdown and a Stop button; the values under test are never
  written to disk, so a hang boots the previous ones.
- **Cores**: which cores are online, SMT, the 8-core unlock and, when the EFI
  program is available, "Before boot (EFI)": the unlock done before GRUB in a
  single boot instead of the extra reboot of the in-system service.
- **CU**: the 40 compute units as 20 cells (pairs), green on, red off, grey
  kept on by the driver. Type the number of CUs you want (24 to 40, in pairs)
  or click the cells; "Test CU" turns the extra pairs on one at a time under
  vkpeak and reports errors.
- **VRAM**: the UMA split in the CMOS, any value from 512 MB, applied at the
  next boot.
- **Advanced**: the governor's own knobs (ascent margin, step, thermal and
  power thresholds, droop).
- **Test**: vkpeak and the helper log.

## Monitor

One chart per quantity, each with its own true scale: temperatures (CPU, GPU,
VRM, system, NVMe), clocks (CPU average, min, max, GPU and its ceiling), load,
power, voltages, fan and memory (RAM, VRAM, GTT), plus one bar per thread.
Click a legend entry to hide a line; hover to read every chart at the same
instant. REC writes a `.sfmon` (CSV) that Open reloads with a scrubber; CSV
exports it for a spreadsheet. The window can be shrunk: below 1150 px the
charts stack in one column, below 1250 px the Tuner moves its readouts above
the curve, and cards everywhere reflow to fewer columns.

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
