<div align="center">

# SkillFishOS

**A dark, steampunk, gaming-focused Linux distribution that turns the AMD BC-250 compute board into a daily-drivable desktop and games console — tuned and ready out of the box.**

[**skillfishos.com**](https://skillfishos.com) · Based on Debian · KDE Plasma · GPL-3.0

**Release 26.06.4 "Aetherium"** — two editions: **BC-250** and **Generic x86-64** (PCs & VMs) · boots in English, language chosen at install

![SkillFishOS desktop](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/desktop.jpg)

</div>

---

SkillFishOS takes the cheap, abundant **AMD BC-250** compute board — a semi-custom APU from the **AMD Zen 2 + RDNA 2** family (CPU codename *Oberon*, GPU *Cyan Skillfish* / `GFX1013`, 16 GB GDDR6) — and makes it a proper Linux machine: a steampunk KDE Plasma desktop on one side, a Steam Big-Picture / EmuDeck games console on the other, with all of the board's awkward hardware **tamed and tuned for you**.

> It began as a way to get kids to **use and learn Linux while they game** — gaming is the carrot, Btrfs snapshots are the safety net that lets them tinker without fear.

**The whole point: a ready-to-use system, no tinkering required.** Every governor, kernel patch, overclock profile, thermal guard and driver workaround is already configured and tested — you turn it on and it runs at full speed. Everything is documented here so the community can understand it, reproduce it, and make it better.

> **This is a community open-source project and we want it to grow.** Contributions of every kind are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Hardware target

| | |
|---|---|
| Board | AMD BC-250 (*Cyan Skillfish*, `GFX1013`) |
| CPU | AMD Zen 2 (*Oberon*), **8 cores / 16 threads** — the board exposes 6, SkillFishOS unlocks the other two via the SMU (**+20%** measured); **4.0 GHz** all-core validated |
| GPU | RDNA 2, 24 CUs at the driver baseline → **all 40 CUs unlockable** |
| Memory | 16 GB GDDR6 (shared / UMA) |
| Base distro | Debian **sid** |

The BC-250 is fantastic value but a difficult target: non-standard clock control through the SMU, a broken display IRQ/HPD path, an unreliable RDSEED, locked-down compute units, no IOMMU and BIOS ACPI gaps. SkillFishOS papers over all of it. See **[docs/OPTIMIZATIONS.md](docs/OPTIMIZATIONS.md)** for the full list and how each problem is solved.

---

## Highlights

- **All 8 CPU cores, unlocked** — the BC-250 is sold as 6 cores / 12 threads, but the two missing ones are switched off by product configuration, not by defect: the presence mask reads a symmetric `0x77` on virtually every board. SkillFishOS writes that mask through the SMU at boot and comes up as **8 cores / 16 threads**, **+20% measured** on multi-threaded work. No modified BIOS, no soldering. It refuses any mask that is not `0x77` — a different pattern would suggest genuinely harvested cores — and only reboots after confirming the write, so it cannot loop.
- **Custom `linux-tkg` kernel** `7.2.0-skillfishos` — BORE scheduler, GCC `-O3`, 1000 Hz, NTsync + fsync, with BC-250 patches: GPU clock range unlocked **350–2230 MHz**, **40-CU unlock** (opt-in), and the cosmetic *"RDSEED is not reliable…"* boot spam silenced. Built in **three flavours**: **main** (`-march=znver2`, BC-250), **generic** (`-march=x86-64`, PCs/VMs) and **slim** (BC-250-only, lean module set). Prebuilt `.deb` in [**Releases**](../../releases/tag/kernel-7.0.11-skillfishos) or `apt install skillfishos-kernel` — see [docs/BUILD.md](docs/BUILD.md).
- **Real clock control** — the `cyan-skillfish-governor` drives the GPU to its safe-point and idles it at 350 MHz; an SMU **CPU overclock & undervolt** reaches **4.0 GHz** (validated) under an 85 °C thermal guard. **~11,330 GFLOPS** fp32 with the 40-CU unlock (≈1.8× a stock build). The ISO ships the safe **Stock** profile; users opt into more from the Tuner.
- **SkillFishOS Tuner** — a native **PyQt6** app to overclock & undervolt CPU and GPU, control the fan, resize the UMA VRAM split, and manage **Compute Units live** — a grid of CU squares (green = on, red = off, 24/32/40 presets, **no reboot**) with a **CU health test** for the silicon lottery. Four ready presets (Stock · Performance · Turbo · Crazy), *benchmark-and-rollback* testing, and a pop-up **live monitor** (temperature / frequency / voltage / fan charts) during any test. Bilingual **IT/EN**. No terminal needed.
- **Live Compute Units** — boots at the 24-CU driver baseline and routes up to **40 CUs at runtime** (via `umr`, no kernel param), restored at boot by a systemd service. Toggle/test from the Tuner or `skillfish-cu`.
- **Live system HUD** — a translucent overlay with per-core CPU load, clocks, temps, power draw, VRAM/RAM, **active CUs**, fan RPM and Bluetooth controller battery, all from real sensors.
- **Btrfs + Snapper + grub-btrfs** — automatic pre/post-apt snapshots and bootable rollbacks straight from the GRUB menu, with `@home` kept separate so a rollback never touches user data.
- **Gaming, ready** — Steam, Heroic, Proton, gamescope (+ FSR 1), GameMode, MangoHud, plus **EmuDeck** and the **ES-DE** frontend to install and configure emulators in a few clicks. *(SkillFishOS ships the tools, not the games — you bring your own games and ROMs.)*
- **On-device AI** — **Unsloth Studio** accelerated in **Vulkan** on the integrated GPU (**5.1×** faster than CPU, measured), serving both a chat UI and an OpenAI-compatible API, with a one-click panel that frees the GPU when you want to play. Models are GGUF pulled straight from Hugging Face.
- **Native PyQt6 app suite** — grouped under a dedicated **"SkillFishOS"** menu: **Tuner**, **AI Panel**, **Monitor** (live sensor charts with a labelled axis and **per core/thread CPU frequency**), **Kernel Manager** (pick the boot kernel and uninstall old ones), **ISO Mount**, and **Hub** — a Discover-style software centre: browse by category, search, read app pages with screenshots, and install/remove/update across **APT** (incl. the signed [`aetherium`](https://mtsistemi.github.io/SkillFishOS/) repo), **Flatpak** and **Snap**, plus add/remove software sources. Every app ships as an updatable `.deb` — including **`skillfish-base`** (hardware **watchdog** + boot-time **freeze detector**: the board recovers from hard hangs by itself and warns you if your profile is unstable) and **`skillfish-console`** (a SteamOS-style **"SkillFishOS Console (Big Picture)"** session on the login screen).
- **Remote Manager — web control dashboard** — a modular, self-hosted dashboard to drive the board from any browser or phone: **live telemetry** (including per core/thread CPU frequency), a software **KVM** (noVNC) and **web terminal** (ttyd), the **Tuner** on the web (CPU/GPU + live Compute-Unit control), a **full Hub app store** (AppStream + Flatpak + Snap, with the SkillFishOS apps featured), **local AI**, logs, auto-rules, Wake-on-LAN and **ZeroTier** for access from anywhere. PAM login over HTTPS, LAN-first by design; off by default and toggled per-module from the native **Remote Manager** app. `apt install skillfish-dashboard` — see the [remote-control guide](https://skillfishos.com/docs/controllo-remoto/).
- **End-to-end steampunk theme** — GRUB, Plymouth, SDDM, the KDE Plasma desktop, icons, cursors, Kvantum and wallpaper. The theme lives in [`theme/`](theme/).
- Driverless printing (CUPS + IPP Everywhere + Avahi), Bluetooth controllers, broken-HPD display hot-swap, and a fully localized desktop.

---

## Screenshots

| About this system | SkillFishOS Tuner |
|---|---|
| ![About](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/about.jpg) | ![Tuner](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/tuner.jpg) |

| Local AI panel | EmuDeck — easy emulation |
|---|---|
| ![AI panel](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/ai-panel.jpg) | ![EmuDeck](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/emudeck.jpg) |

---

## Performance

> All measured on **our own BC-250** with SkillFishOS at **1080p** (40 CUs unlocked, kernel 7.1.7-skillfishos, Mesa 26.0.8 — 7.0.11 and 7.1.7 measure within ±2% of each other; we ship 7.2.0 today, whose CPU benchmarks match 7.1.7 and whose frame rates we have not re-measured). Full per-benchmark detail — every setting, clock, voltage, temperature and power reading — is on the **[Performance & benchmarks page →](https://skillfishos.com/docs/prestazioni/)**

### Real benchmarks

| Benchmark | Settings | Result |
|---|---|---|
| **Black Myth: Wukong** | 1080p, uncapped (CPU/draw-call bound) | **112 FPS** avg · 128 max · 101 (1% low) |
| **Unigine Superposition** | 1080p **High**, OpenGL | **12 938** · 96.8 FPS avg |
| **Unigine Superposition** | 1080p **Extreme**, OpenGL | **5 513** · 41.3 FPS avg |
| **Unigine Heaven 4.0** | 1080p Ultra, 8× AA, Extreme tess. | **113.7 FPS** · score **2865** |

| Black Myth: Wukong — 112 FPS | Unigine Superposition — 12938 (High) |
|---|---|
| ![Wukong 112 FPS](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/benchmarks/wukong-112fps.jpg) | ![Superposition High 12938](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/benchmarks/superposition-high.jpg) |

| Unigine Superposition — 5513 (Extreme) | Unigine Heaven 4.0 — 113.7 FPS / 2865 |
|---|---|
| ![Superposition Extreme 5513](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/benchmarks/superposition-extreme.jpg) | ![Heaven 113.7 FPS](https://raw.githubusercontent.com/MTSistemi/SkillFishOS/main/screenshots/benchmarks/heaven-113fps.jpg) |

### Synthetic compute — `vkpeak` fp32-scalar (GFLOPS)

| Configuration | GFLOPS | Notes |
|---|---:|---|
| Stock ~2000 MHz, 24 CU | 6141 | baseline |
| tkg + governor, 24 CU | 6868 | +12 % |
| **tkg + governor + 40-CU unlock** | **11329** | **≈1.84× baseline** (≈11.3 TFLOPS) |

Also: FP16 vec4 **22 685**, int8 dot-product **45 495 GIOPS**, memory bandwidth **~350–367 GB/s** (clpeak).

**Same hardware, +34 % just by changing OS** — Superposition 1080p Extreme: SkillFishOS **5513** vs another distro at stock clocks **4102**. In gaming the BC-250 lands in **Radeon RX 6600/6600 XT** territory.

CPU OC validated up to **4.0 GHz** (~1224 mV, 120 s stress, 83 °C peak) on the reference board; under combined CPU+GPU load the APU shares its power budget gracefully, easing CPU clocks to stay within the 85 °C limit. Full methodology and benchmarks: **[skillfishos.com/docs/prestazioni](https://skillfishos.com/docs/prestazioni/)** · [docs/OPTIMIZATIONS.md](docs/OPTIMIZATIONS.md).

---

## Get it

### Prebuilt kernel

Prebuilt kernel `.deb`s (three flavours) are published under [**Releases**](../../releases/tag/kernel-7.2.0-skillfishos):

```sh
# main BC-250 kernel (znver2)
sudo dpkg -i linux-image-7.2.0-skillfishos_7.2.0-1_amd64.deb
# …or generic (PCs/VMs): linux-image-7.2.0-skillfishos-generic_7.2.0-1_amd64.deb
```

Or, from the signed APT repo, simply `sudo apt install skillfishos-kernel` (a thin wrapper that fetches the full kernel `.deb` from the GitHub Release). To build it yourself, see [docs/BUILD.md](docs/BUILD.md) and [`kernel-build/`](kernel-build/).

### Installable ISOs — **26.06.4 "Aetherium"** (two editions)

Each live ISO (~4.6 GB) is captured from the real system with [penguins-eggs](https://github.com/pieroproietti/penguins-eggs): KDE Plasma steampunk desktop, Btrfs + Snapper + grub-btrfs, the native PyQt6 app suite, the signed `aetherium` APT repo, and the **Calamares** installer. They **boot in English** and let you pick your **language and keyboard** at install; the bilingual apps and HUD follow the chosen locale.

| Edition | Kernel | For |
|---|---|---|
| [**BC-250**](https://sourceforge.net/projects/skillfishos/files/26.06.4-Aetherium/SkillFishOS-26.06.4-Aetherium-BC250-amd64.iso/download) | `7.1.7-skillfishos` (znver2) | the AMD BC-250 board |
| [**Generic**](https://sourceforge.net/projects/skillfishos/files/26.06.4-Aetherium/SkillFishOS-26.06.4-Aetherium-Generic-amd64.iso/download) | `7.1.7-skillfishos-generic` | any x86-64 PC / VM |

The **Slim** edition of 26.06 is not part of this release: no Slim image has been rebuilt since, although the slim kernel flavour is still built and published (`7.2.0-skillfishos-slim`, 32 MB).

Downloads are hosted on **SourceForge**: [sourceforge.net/projects/skillfishos/files/26.06.4-Aetherium](https://sourceforge.net/projects/skillfishos/files/26.06.4-Aetherium/) (the project also hosts the code mirror, blog, forum and wiki). The publishing flow (SourceForge Files, the **`aetherium`** APT update repository, and the DistroWatch submission) is documented under [`distribution/`](distribution/).

> The signed **APT repo is live** at <https://mtsistemi.github.io/SkillFishOS/>, mirrored at <https://skillfishos.com/apt>. After install, the **Hub** app (or `apt`) keeps the kernel and every native app up to date from it.

---

## Repository layout

```
README.md          this file
LICENSE            GPL-3.0
CONTRIBUTING.md    how to get involved
docs/              full documentation
  OPTIMIZATIONS.md   kernel patches, governor, OC/UV, 40-CU, VRAM/GTT, audio/display, controllers
  DESKTOP.md         KDE Plasma, steampunk theme, HUD, Tuner, AI panel
  GAMING.md          Steam, EmuDeck, ES-DE, emulators (bring your own games)
  AI.md              the local Unsloth Studio Vulkan engine
  BUILD.md           building the kernel and the ISO
kernel-build/      linux-tkg recipe (customization.cfg + BC-250 userpatches)
apps/              native PyQt6 apps: tuner, ai-panel, iso-mount, kernel-switch, monitor, hub (+ menu)
system/            mirror of the live box config (/usr/local/bin, systemd units, /etc, KDE skel, branding)
theme/             the "SkillFish Steampunk" theme (icons, cursors, Kvantum, wallpapers, palettes)
distribution/      release & publishing: APT repo (suite aetherium), SourceForge, DistroWatch
repo-server/       the services container: reprepro archive, signing keyring, and in bin/
                   the four scripts that publish a release (no credentials in them)
website/           the skillfishos.com site (Astro, four languages)
iso/               live-build configuration for the installable ISO
scripts/           build, publish and repair scripts (ISO, packages, mirrors, site)
tests/             checks run on the built packages and images
screenshots/       images used in this README
```

---

## Documentation

Everything that makes the BC-250 sing is documented:

- **[docs/OPTIMIZATIONS.md](docs/OPTIMIZATIONS.md)** — the heart of the project: the kernel patches, SMU governor, CPU/GPU overclock & undervolt, 40-CU unlock, VRAM/GTT tuning, broken-HPD display fix, audio, Wi-Fi/Bluetooth and controllers.
- **[docs/DESKTOP.md](docs/DESKTOP.md)** — KDE Plasma, the steampunk theme, the live HUD, the Tuner and the AI panel.
- **[docs/GAMING.md](docs/GAMING.md)** — the gaming stack and how EmuDeck / ES-DE are set up.
- **[docs/AI.md](docs/AI.md)** — running LLMs locally on the integrated GPU via Vulkan.
- **[docs/BUILD.md](docs/BUILD.md)** — build the kernel and the ISO from source.

---

## Contributing

We genuinely want this project to take off, and that needs people. Whether you can write kernel patches, package software, improve the theme, test on real hardware, fix typos in the docs, or just file good bug reports — **you're welcome here**. Start with [CONTRIBUTING.md](CONTRIBUTING.md), open an issue, or say hi in a discussion.

---

## Status

Work in progress, dogfooded daily on real BC-250 hardware. An independent community project — **not affiliated with AMD or any other vendor.**

## Contributors & thanks

People who made this better without being asked:

- **Bartek** ([Świat Linuksa](https://www.youtube.com/@SwiatLinuksa)) — reviewed SkillFishOS
  over ten days on real hardware, ran an **independent security audit** of the installed
  system (services, processes, network traffic with tcpdump and nmap) and found no
  unexpected connections. He also reported four bugs on the tracker: the Italian locale on
  a non-Italian install, the missing `docker` group and the local AI falling back to the
  CPU were fixed in 26.06.3; **the btrfs/GRUB install failure was not**, although we said
  it was. The repair we shipped ran, logged success and left the defect byte for byte
  identical. The real cause — `rsync -aHAXS`, where that `S` is `--sparse` — was only
  found for 26.06.4.
- **Cyryl Sochacki** ([cyryllo](https://github.com/cyryllo)) — the Polish translation and a
  polonisation script that carried earlier releases, plus [PR #26](../../pull/26), which
  pointed out that our own boot fix had gone stale without anyone noticing. He was right
  and we told him otherwise. That pull request was then closed by a force-push of ours, not
  by a decision; the reasoning it contained is now in the tree.

## Credits & references

Built on the shoulders of:

- [Frogging-Family/linux-tkg](https://github.com/Frogging-Family/linux-tkg) — the kernel build system
- [Magnap/cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor) — GPU SMU clock control
- [bc250-collective/bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc) · [fanoush/bc250_memcfg](https://github.com/fanoush/bc250_memcfg) · [duggasco/bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [Unsloth](https://unsloth.ai/)
- BC-250 community docs: [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) · [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation)

## License

[GPL-3.0](LICENSE). The bundled artwork/theme is provided for use with SkillFishOS.
