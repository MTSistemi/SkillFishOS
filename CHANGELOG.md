# Changelog

All notable changes to SkillFishOS. Dates are ISO-8601.

## [Unreleased]

### Added
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
