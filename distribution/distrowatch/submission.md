# DistroWatch — new distribution submission (draft)

Submit via the DistroWatch "Submit a distribution" page once the ISO is publicly
downloadable (SourceForge). DistroWatch only lists distros with a public release and
a working download, and reviews submissions manually — so do SourceForge first.

## Form fields

| Field | Value |
|---|---|
| **Distribution name** | SkillFishOS |
| **Home page** | https://skillfishos.com |
| **Download (ISO)** | https://skillfishos.com/dl/SkillFishOS-26.06-Aetherium-BC250-amd64.iso (5.6 GB, 302 → direct download) |
| **Based on** | Debian (unstable / sid) |
| **Origin** | Italy |
| **Architecture** | x86_64 (amd64) — current release targets the AMD BC-250 board |
| **Desktop** | KDE Plasma 6 |
| **Category** | Desktop, Gaming, Live Medium |
| **Release model** | Fixed releases on a rolling (sid) base, with a curated/tested update repository |
| **Status** | Active |
| **Installer** | Calamares |
| **Package management** | APT / dpkg (+ Flatpak) |
| **Init** | systemd |
| **License** | Open source (GPL-compatible; Debian-based) |
| **Source code** | https://github.com/MTSistemi/SkillFishOS |

## Description (≈ 100 words)

SkillFishOS is a steampunk-themed gaming Linux distribution built specifically for the
AMD BC-250 — a salvaged, low-cost mining board carrying a semi-custom Zen 2 + RDNA 2 APU
(16 GB GDDR6). Based on Debian sid with KDE Plasma 6, it ships a custom linux-tkg kernel
that unlocks all 40 Compute Units, a dedicated SMU governor, CPU/GPU overclock and undervolt
profiles with thermal protection, Btrfs snapshots with one-click rollback, a full gaming and
emulation stack (Steam, EmuDeck, ES-DE, Heroic) and an on-device Vulkan AI stack. The system
boots in English with language selection at install. Open source; a generic x86-64 version is
planned.

## Notes for the editor
- Release: **26.06 "Aetherium"** (BC-250 specific).
- The project is not affiliated with AMD or any console manufacturer.
- Screenshots available at https://skillfishos.com/gallery
