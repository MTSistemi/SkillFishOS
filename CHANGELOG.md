# Changelog

All notable changes to SkillFishOS. Dates are ISO-8601.

## [Unreleased]

## [26.06.3 "Aetherium"] — 2026-08-10

Editions: **Generic** (`7.1.7-skillfishos-generic`, any x86-64 PC) and **BC-250** (`7.1.7-skillfishos`). The Slim edition is not part of this release: it was a third kernel flavour of the 7.0.11 series and has not been rebuilt for 7.1.7.

### Added
- **Ukrainian in every native app** — 292 strings across the hub, tuner, monitor, kernel manager, remote manager and AI panel, alongside cyryllo's Polish. The AI panel had an empty Polish dictionary and now has both languages. **The Ukrainian is not a native speaker's work** and wants the same review the Polish received.
- **All 8 CPU cores unlocked** (`skillfish-base`) — the BC-250 ships as 6c/12t because two of its eight Zen 2 cores are switched off by product configuration, not by defect (the presence mask reads a symmetric `0x77` on virtually every board). `skillfish-core-unlock` writes that mask through the SMU at boot and warm-reboots once, bringing the board up as **8c/16t**. No modified BIOS required. It refuses any non-`0x77` mask — a different pattern suggests a real harvest of defective cores — and only reboots after confirming the write, so it can never loop. Verified on hardware: 16 threads, zero MCEs under stress. Credit to [rw-r-r-0644/bc250-core-unlock](https://github.com/rw-r-r-0644/bc250-core-unlock).
- **CPU frequency scaling** (`skillfish-acpi-pstates`, in `skillfish-base`) — the board's firmware exposes no `_PSS` objects, so Linux had no cpufreq interface at all. An SSDT injected through GRUB's early initrd gives `acpi-cpufreq` with 8 P-states (800–3200 MHz), the usual governors including `schedutil`, and working C-states. Idle drops from ~1400 MHz to 800 MHz while the peak is unchanged (~3500 with the SMU overclock — the table's frequency labels don't cap the hardware). Only enables itself on an actual BC-250, and `skillfish-acpi-pstates disable` reverses it.
- **Unsloth Studio as the AI engine** (`scripts/install-unsloth.sh`) — runs GGUF models through llama.cpp's **Vulkan** backend, the only GPU-accelerated path on gfx1013, and serves both a chat UI and an OpenAI-compatible API from one native service. Measured on the board with Qwen3-1.7B Q4_K_M: **210 tok/s** generation and 157 tok/s prompt, against 41 and 9 CPU-only. The dashboard detects the engine and proxies its UI behind the PAM login. The Ollama + Open WebUI stack keeps working where it's already installed.
- **Efficient tuner preset** (1850 MHz @ 950 mV) — with all 40 CUs enabled, asking for 2200 MHz buys ~3% frames for 10 °C and 18 W, and the clock throttles back to ~1859 MHz anyway. 1850 holds, runs 10 °C cooler and is now the first preset offered.
- **Polish and Ukrainian** on the website — full UI translation under `/pl` and `/uk`; the documentation stays in English for now.
- `scripts/install-minecraft.sh` and `scripts/install-minecraft-mods.sh` — official Mojang launcher (the .deb needs repackaging: it declares dependency names that no longer exist on sid) plus Fabric with Sodium, Lithium and FerriteCore.

### Fixed
- **Desktop HUD after the core unlock** — `amdgpu` reports a bogus GPU clock once the cores are unlocked (~100 MHz at idle instead of 350). `skillfish-gpu-freq-sampler` reads the SMU's own getter, which stays correct, and the HUD now shows 16 CPU bars instead of 12. Existing per-user HUD configs are migrated in place, and only when they still match what we shipped.
- **Blank icons** (`skillfish-theme` 26.06.1) — 93 icons in the steampunk theme referenced gradient ids belonging to a *different* icon. Older qtsvg tolerated the dangling reference; since 6.10.2-9 Qt refuses to paint those elements, so they rendered as empty frames. Also, the theme is now a package at all: it used to live only in the ISO filesystem, so fixes could never reach installed systems.
- **Installed systems boot again on btrfs** (#12) — the kernel and initrd written by the installer had an extent map that didn't cover the declared file size: the last extent was missing its `eof` flag, so GRUB read the extent tree, stopped where it ended and gave "premature end of file". Linux read the same file without complaining, which is why it only showed at boot. `skillfish-fix-boot-extents` rewrites them after installation with `cp --reflink=never` — without that flag btrfs reuses the very same broken extents and repairs nothing. `/boot` stays inside btrfs, so snapshots still cover it and rollback still works.
- **No more `grub rescue>` on the first boot** (#20) — with `installEFIFallback` Calamares copies shim and grubx64 into the removable EFI path but not the `grub.cfg` stub that sits beside them, so the GRUB started from there had a prefix that resolved nothing. The installer now runs `grub-install --removable` as well, which writes a self-contained `BOOTX64.EFI`. This is why the bug hit ext4 and btrfs alike.
- **SSH accepts a password again** — a fresh install refused with "allowed types: ['publickey']". eggs strips `PermitRootLogin` and `PasswordAuthentication` from `sshd_config` and appends `PasswordAuthentication no`. A drop-in under `sshd_config.d/`, which is included at the *top* of the file, now wins: OpenSSH keeps the first occurrence of a directive. Root stays key-only, by OpenSSH's own default.
- **The overclock button in the Tuner works on installed systems** — `skillfish-tuner-helper` had `/root/bc250_smu_oc/...` written into it, and eggs excludes `/root` from the image, so those tools existed on the development board and nowhere else: the button failed silently for every user. It now resolves them from `/opt`. Overclocking *at boot* was unaffected, which is why nobody noticed.
- **The AI setup wizard no longer crashes** — its install step filled `self.steps` while the runner read `self._queue`, an attribute nothing created, so pressing "Install" raised `AttributeError`. Invisible on any machine where the engine was already installed.
- **Polish is actually selectable** — the translations have shipped for months, but the image only generated the `en_US` and `it_IT` locales. Without a generated locale KDE doesn't offer the language and SDDM doesn't list it, so Polish was present in the code and unreachable in practice. `skillfish-base` now generates `it_IT`, `en_US`, `pl_PL` and `uk_UA`.
- **The SkillFishOS wallpaper is the actual wallpaper** — the look-and-feel pointed `Image=` at a bare PNG, where Plasma expects a wallpaper *package* (a directory with `metadata.json` and `contents/images/`); handed a file it silently falls back to its own default. It also shipped from nowhere: no package owned it. It is now a proper package inside `skillfish-theme`.
- **The installer shows the right version** — the release string was written by hand in seven places and they had drifted: `os-release` said 26.06.2, `lsb-release` and `/etc/issue` said 26.06, and the two Calamares branding directories disagreed with each other. Calamares selects `branding: eggs`, so the installer was showing 26.06 while the installed system called itself 26.06.2. `scripts/set-release-branding.sh` now sets all of them at once. "Known issues" in the installer also pointed at the penguins-eggs issue tracker rather than ours.
- **The media no longer ships the developer's overclock** — the image is built from the live system, so `/etc/bc250-smu-oc.conf` went in as-is: a profile tuned for one particular chip, applied to every board that installs it. The build script now swaps in the safe 3500 MHz profile for the duration of the build and reads it back out of the finished squashfs to prove it.

### Changed
- **Kernel 7.1.7** — the 7.0 series is end of life. Same tuning; the BC-250 patches apply cleanly. Two flavours were rebuilt, generic and BC-250: the slim one has not been. Performance measured within ±2% of 7.0.11 on both CPU and Vulkan workloads: this is a maintenance move, not a speed one.
- **The image is 4.6 GB, down from 10.2** — and the cause was not what it looked like. Mounting both images and diffing them showed `/var/lib/systemd` had grown by 3.10 GB: five core dumps left by emulator testing, one of them 1.6 GB. systemd's defaults keep dumps up to 10% of the disk with no per-file limit, and the image is built from the live system. A cap now ships in `coredump.conf.d`. The rest: squashfs now uses `-comp xz -Xbcj x86 -b 1M` (measured 13% smaller than plain xz on binaries — and note that eggs picks compression from a `produce` flag, not from `eggs.yaml`), eggs' own exclude list had `var/cache/* var/lib/aide/*` on a single line, which mksquashfs reads as one pattern and never matches, and the LLVM/Rust development toolchain no longer ships.
- **Docker is gone** — it ran exactly one container, dockge, whose stack directory was empty: it had nothing left to manage once the AI moved to native Unsloth. That was a daemon at every boot, a `docker0` bridge, iptables rules and a container-management panel listening on `0.0.0.0:5001`. The Ollama code paths went with it, in both the dashboard and the AI panel.
- **Steam ROM Manager and Sober are no longer preinstalled** — 18 MB of Sober kept 1.1 GB of GNOME runtime alive, and Steam ROM Manager was the last application on the freedesktop 24.08 generation, worth 1.65 GB of runtime by itself. Both are one click away in the software store.

## [26.06.2 "Aetherium" — media respin] — 2026-07-11

A maintenance respin of the 26.06 "Aetherium" media, fixing four community-reported bugs (thanks to **@SwiatLinuksa**). Same three editions and kernel family (`7.0.11-skillfishos` ×3 flavours). Existing installs get the app fixes via `apt full-upgrade` — no reinstall needed; the ISO fixes (locale, installer) only matter for fresh installs.

### Fixed
- **Language no longer stuck on Italian** (#11) — a hardcoded locale in `/etc/environment` overrode the language chosen at install / in KDE, leaving the SkillFishOS apps and game launchers in Italian on English (and other) systems. The installed system now honours the chosen language; the language is set solely by `/etc/default/locale`.
- **On-device AI uses the GPU out of the box** (#14) — the AI setup wizard's generated `compose.yaml` was missing the GPU flags, so Ollama fell back to slow CPU inference. It now sets `OLLAMA_VULKAN=1` + `OLLAMA_IGPU_ENABLE=1` (plus flash-attention and a 30-minute keep-alive). Shipped as `skillfish-ai-panel` 26.06.5.
- **SkillFish AI starts on the first try** (#13) — the setup wizard now adds the user to the `docker` group and runs the first stack start as root (`pkexec`), so it no longer fails with a Docker permission error before the user re-logs in.

### Hardening
- **Sturdier install/boot** (for #12) — the installer now also writes the removable EFI fallback bootloader (`\EFI\BOOT\BOOTX64.EFI`), which the BC-250's firmware often boots from, and uses an explicit GRUB-safe Btrfs subvolume layout (`@`, `@home`, `@cache`, `@log`).

### Also updated
- The media capture the latest **SkillFishOS Remote Manager** web dashboard, the web **Tuner** (temperature→fan% curve editor, named CU/WGP profiles, CPU core map, GPU/CPU "find my max" wizards) and the full web **Hub** app store with a featured "App SkillFishOS" section.

## [26.06.1 "Aetherium" — media respin] — 2026-06-10

### ISOs
Three refreshed installable editions — **BC-250**, **Generic x86-64** and **Slim (BC-250)** — published on SourceForge as `SkillFishOS-26.06.1-Aetherium-<Edition>-amd64.iso` (with SHA-256 checksums). Same kernel family (`7.0.11-skillfishos` ×3 flavours) as 26.06; the respin exists because the original media shipped the old Tuner whose **Turbo/Crazy presets pointed the GPU at 2230 MHz @ 1000 mV**, an undervolted combination that can hard-freeze the board. Out of the box the new media include:
- the **safe GPU presets and multi-point voltage curve** (max 2200 MHz @ 1000 mV) and the safe **Stock CPU profile** (3500 MHz);
- **`skillfish-base`**: the SP5100 **hardware watchdog** (auto-reboot on hard hangs) and the boot-time **freeze detector** with desktop notification;
- **`skillfish-console`**: the SteamOS-style **"SkillFishOS Console (Big Picture)"** login session (and the PATH fix that made the old session bounce back to login);
- the full updated app suite: Tuner 26.06.8 (🎰 find-my-max wizards CPU+GPU, "My silicon" panel), Hub 26.06.9, Monitor 26.06.5 (REC), Kernel Manager 26.06.1, AI 26.06.4 — each with its MetaInfo app page.

Existing 26.06 installations get everything via `apt full-upgrade` — no reinstall needed.

### Added
- **`skillfish-base` 26.06 (new package)** — the safety net: enables the AMD SP5100 **hardware watchdog** (the board reboots itself on a hard hang instead of needing a physical power-cycle) and a boot-time **freeze detector** that logs an unclean previous shutdown and notifies the desktop user that their overclock/undervolt profile may be unstable.
- **`skillfish-console` 26.06 (new package)** — a SteamOS-style **"SkillFishOS Console (Big Picture)"** session on the SDDM login screen: boots straight into Steam's gamepad UI inside gamescope; quitting Steam returns to the login screen. (Also fixes the pre-existing session, which called a bare `gamescope` not on SDDM's PATH and silently bounced back to login.)
- **Tuner 26.06.7/26.06.8** — 🎰 **"Find my max" wizards for CPU and GPU** (stepped benchmark-and-rollback validation that applies the highest stable point for *your* board), a **"My silicon" status panel** (validated profile + freeze counter + one-click sharing), and the **silicon-lottery community database** (prefilled GitHub issue reports, zero backend).
- **Monitor 26.06.5** — **REC** button: record telemetry to CSV (`~/SkillFishOS-benchmarks/`) with min/avg/max stats on stop.
- **Hub 26.06.9** — 24-hour on-disk cache for ODRS ratings (faster launches, stars work offline).
- Infrastructure: a third APT mirror on **SourceForge Project Web**, an **`aetherium-proposed`** staging suite, CI that **builds every package from git and verifies the packaged content**, ruff + shellcheck quality gates, encrypted SFTP deploys, an off-site backup of the repo signing key, and GitHub Discussions.

### Safety
- **Hard-freeze root cause fixed**: the BC-250 hard-froze on **2230 MHz @ 1000 mV** (undervolted — community data says 2230 needs 1000–1060 mV) and on a persistent **4000 MHz @ -36** CPU profile. Presets now cap the GPU at the validated **2200 MHz**, the helper **clamps** any undervolted >2200 request, applying a 4000-class preset warns it is benchmark-only, and CPU tests are **crash-safe** (the on-disk config keeps the last-known-good values while a candidate is benched, so a freeze mid-test can no longer create a reboot loop).
- **SkillFishOS Hub** (`skillfish-hub` 26.06.7) reborn as a Discover-style software centre: sidebar layout (Explore / Categories / Installed / Updates / Sources) with search, category browsing with AppStream icons and descriptions, and install/remove/update across **APT + Flatpak + Snap**. Software sources can be added/removed/enabled (APT deb822 repos with optional signing key; Flatpak remotes), and a single "Update all" applies updates from every backend. Privileged APT/repository actions run via `skillfish-hub-helper` (pkexec).
  - **Discover-style app pages**: a hero (96 px icon, title, developer, summary, star rating, Install / Remove / Open) over a metadata strip (source · version · size · licence · sandbox + website link), a full-width **screenshot carousel** with arrows and dots, then description, "What's new", permissions and ODRS reviews.
  - **Sidebar sub-categories** that expand/collapse under each top category (with a disclosure caret and an "All" entry), matching Discover; clicking the open category collapses it again.
- **In-distro app catalogue (MetaInfo)**: each SkillFishOS app now ships its own `/usr/share/metainfo/*.metainfo.xml` plus local screenshots, so the Hub (and any AppStream client) shows full app pages for **Tuner, AI, Monitor, Kernel Manager and Hub** themselves — bundled into `skillfish-tuner` 26.06.4, `skillfish-ai-panel` 26.06.4, `skillfish-monitor` 26.06.4, `skillfish-kernel-manager` 26.06.1 and `skillfish-hub` 26.06.7.
- **GPU governor "Performance" mode** in the **Tuner** (`skillfish-tuner` 26.06.5): a *Balanced / Performance* toggle in the GPU section. Performance lowers the `cyan-skillfish-governor` load-target so the GPU **holds its top safe-point under any gaming load** (still idling to 350 MHz on the desktop). Measured on the Black Myth: Wukong benchmark (1080p): **100 → 111 FPS average (+11%)**, 92 → 102 FPS on the 5% slowest frames. Default stays Balanced.

### Changed
- **Kernel Switch → Kernel Manager** (`skillfish-kernel-manager`, replaces `skillfish-kernel-switch`): besides choosing the boot kernel (default / boot-once), it now lists every installed kernel with flavour, size and running/default badges, and can **completely uninstall** a kernel (`apt purge` image + headers + modules) so kernels don't pile up. Guardrails: never removes the running kernel or the last remaining one, and moves the GRUB default off a kernel before removing it; a confirmation dialog shows the packages removed and the space freed.

### Fixed
- Hub: clicking a category no longer freezes the window — the sidebar rebuild is deferred so it never deletes the button mid-click.
- Hub: three async view-clobber races fixed with a per-view token — a slow **search**, **updates check** or **snap-category** fetch can no longer overwrite the view after the user has navigated elsewhere (e.g. searching right after opening a category now shows the search results, not the category).
- Hub: starting a search now clears any selected category/sub-category highlight (Discover behaviour), and duplicate Flatpak remotes (system + user) are de-duplicated in Sources.
- Cleared all CodeQL code-scanning alerts (file-not-closed, empty-except, unused-import, a duplicate `closeEvent`, and two overly-permissive `chmod`s) across the native apps.
- **GPU hard-freeze on clock transitions** (BC-250): the default governor voltage curve used a 2-point line topping out at **2230 MHz @ 1000 mV**, which is *undervolted* — abrupt clock transitions there could hard-hang the whole machine. The Tuner now writes a **smooth multi-point curve** (`350/700, 1500/900, 2000/1000, 2200/1000`), caps the GPU max at the validated-stable **2200 MHz @ 1000 mV**, and reloads the governor gently (stop → settle → start) to avoid the abrupt SMU jump.

## [26.06 "Aetherium"] — 2026-06-07

### Kernel
- Updated the custom `linux-tkg` kernel to **`7.0.11-skillfishos`** (BORE, GCC `-O3`, 1000 Hz, NTsync + fsync, BC-250 patches: 350–2230 MHz clock unlock, 40-CU unlock, RDSEED boot-spam silenced).
- Now built in **three flavours**: **main** (`-march=znver2`, BC-250), **generic** (`-march=x86-64`, PCs & VMs) and **slim** (BC-250-only, lean module set).
- Published as GitHub Release `kernel-7.0.11-skillfishos`, and installable from the APT repo via the `skillfishos-kernel` wrapper (postinst fetches the full 152 MB `.deb` out-of-band, sidestepping GitHub Pages' 100 MB limit and the dpkg-in-postinst deadlock).

### ISOs
- Three installable editions for 26.06 "Aetherium" — **BC-250**, **Generic** and **Slim** — each ~6.2 GB, captured with penguins-eggs and verified to boot the matching kernel.
- Calamares installer now shows the release name **"SkillFishOS 26.06 Aetherium"** instead of the build date.
- First-boot service creates the Btrfs `.snapshots` subvolume and configures Snapper + grub-btrfs, so rollbacks appear in GRUB after the first updates.
- Published to **SourceForge Files** under `26.06-Aetherium/`.

### Apps (all shipped as updatable `.deb`s from the `aetherium` repo)
- **New — SkillFishOS Hub**: a native software centre that installs and updates SkillFishOS packages from our signed APT repo.
- **New — SkillFishOS Kernel Switch**: pick the boot kernel (set default / boot once) from a themed GUI.
- **New — SkillFishOS Monitor**: standalone live temperature / frequency / voltage / fan charts (extracted from the Tuner).
- **New — SkillFishOS menu**: a dedicated "SkillFishOS" submenu (via the `X-SkillFishOS` desktop category) that groups every native app.
- **AI Panel**: first-run setup wizard (installs the stack, picks a model from 38 options ≤14B), hardware readout (CPU/GPU/VRAM/RAM) and a shared-memory slider.

### Fixed
- **Apps would not launch from the KDE menu** — two distinct bugs:
  - desktop entries used a relative `Exec=`; KDE's launcher (KIO) has no `/usr/local/bin` on PATH, so it failed with *"Cannot find the program"*. All entries now use the absolute `/usr/local/bin/…` path.
  - `main()` called `Widget().show()` without keeping a Python reference, so the top-level window was garbage-collected immediately and stayed 1×1 / unmapped (invisible). Fixed by holding the reference and raising the window.
- **Monitor crash (SIGSEGV)** — `paintEvent` could leave a `QPainter` active on teardown; rewritten with a `begin()`-checked painter + `try/finally`, sensor sampling moved to a worker thread, and graceful `closeEvent` / SIGTERM shutdown.
- **Branding** — `os-release` no longer reverts to Debian on `apt upgrade` (dpkg-divert); KDE "About this system" shows *SkillFishOS 26.06 Aetherium*.

### Infrastructure
- Signed **`aetherium`** APT repository live at <https://mtsistemi.github.io/SkillFishOS/> (amd64 + i386), end-to-end update flow validated (`apt upgrade` pulls new kernel and app versions).
