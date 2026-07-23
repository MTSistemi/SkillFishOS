# DistroWatch — new distribution submission

**DistroWatch submission is by EMAIL, not a web form.** Per
<https://distrowatch.com/dwres.php?resource=submit>: *"you should e-mail us"* with the four
items below. The contact is **Jesse Smith** (DistroWatch) — use the contact link at the bottom
of that page (distro@distrowatch.com). A copy-paste-ready email is at the end of this file.

> Status: the **ISO is live on SourceForge** and is set as the **default download** —
> `sourceforge.net/projects/skillfishos/files/latest/download` redirects to it. This satisfies
> DistroWatch's "no cloud-storage downloads" rule. Ready to send.

## ⚠️ Read this first — alignment with DistroWatch's rules

DistroWatch only needs **four** things in the submission: project name, website URL, a short
description (incl. the base distro), and **a link to the installation media (ISO)**. But two
of its stated rules affect us directly:

1. **No cloud-storage downloads.** ✅ **Resolved.** DistroWatch rejects Google Drive / MEGA /
   "other cloud storage" downloads. We now host the ISO on **SourceForge** (a proper, accepted
   mirror) — submit the SourceForge URL, **not** the Dropbox-masked `skillfishos.com/dl/…`
   (which is fine for the website only).

2. **Waiting list + maturity.** New distros go on a waiting list — *"be prepared for a
   year-long wait"* — and are expected to have *"proper infrastructure, including forums,
   mailing lists, documentation, bug tracking databases, etc."*
   → We now have: **documentation** (skillfishos.com/docs), **bug tracking**
   (GitHub issues), and a **forum** (GitHub Discussions:
   <https://github.com/MTSistemi/SkillFishOS/discussions>). A mailing list is still missing
   (optional) — a contact form exists at skillfishos.com/contact.

(There's also a paid fast-track: buy ≥100,000 ad impressions / $250 for immediate evaluation —
*no guarantee* of inclusion. Only if you want to skip the queue.)

## The 4 required fields

| Field | Value |
|---|---|
| **Project / distribution name** | SkillFishOS |
| **Website URL** | https://skillfishos.com |
| **Description (with base)** | Steampunk gaming Linux for the AMD BC-250, based on **Debian sid** + KDE Plasma 6 (see 100-word version below) |
| **ISO download link** | ✅ **LIVE** — `https://sourceforge.net/projects/skillfishos/files/26.06-Aetherium/SkillFishOS-26.06-Aetherium-BC250-amd64.iso/download` (6.0 GB, default download for Linux) |

## Useful extra context (DistroWatch fills the DB entry themselves)

- Origin: Italy · Architecture: x86_64 (amd64), BC-250-specific · Desktop: KDE Plasma 6
- Base: Debian unstable (sid) · Installer: Calamares · Packaging: APT/dpkg + Flatpak · Init: systemd
- Category: Desktop, Gaming, Live Medium · Release: 26.06 "Aetherium" · Status: Active
- License: open source (GPL-compatible) · Source: https://github.com/MTSistemi/SkillFishOS
- Screenshots: https://skillfishos.com/gallery

## Description (≈ 100 words)

SkillFishOS is a steampunk-themed gaming Linux distribution built specifically for the
AMD BC-250 — a salvaged, low-cost mining board carrying a semi-custom Zen 2 + RDNA 2 APU
(16 GB GDDR6). Based on Debian sid with KDE Plasma 6, it ships a custom linux-tkg kernel
that unlocks all 40 Compute Units, a dedicated SMU governor, CPU/GPU overclock and undervolt
profiles with thermal protection, Btrfs snapshots with one-click rollback, a full gaming and
emulation stack (Steam, EmuDeck, ES-DE, Heroic) and an on-device Vulkan AI stack. The system
boots in English with language selection at install. Open source; a generic x86-64 version is
planned. Not affiliated with AMD or any console manufacturer.

---

## ✉️ Ready-to-send email

> **To:** distro@distrowatch.com (Jesse Smith / DistroWatch)
> **Subject:** New distribution submission — SkillFishOS

Hello,

I'd like to submit a new Linux distribution for listing on DistroWatch.

- **Name:** SkillFishOS
- **Website:** https://skillfishos.com
- **Based on:** Debian (unstable / sid), KDE Plasma 6
- **Installation media (ISO):** https://sourceforge.net/projects/skillfishos/files/26.06-Aetherium/SkillFishOS-26.06-Aetherium-BC250-amd64.iso/download

**Description:** SkillFishOS is a steampunk-themed gaming Linux distribution built specifically
for the AMD BC-250 — a low-cost, salvaged mining board with a semi-custom Zen 2 + RDNA 2 APU
(16 GB GDDR6). Based on Debian sid with KDE Plasma 6, it ships a custom linux-tkg kernel that
unlocks all 40 Compute Units, a dedicated SMU governor, CPU/GPU overclock & undervolt profiles
with thermal protection, Btrfs snapshots with one-click rollback, a full gaming/emulation stack
(Steam, EmuDeck, ES-DE, Heroic) and an on-device Vulkan AI stack. It boots in English with
language selection at install. Open source; a generic x86-64 build is planned.

Infrastructure: docs at https://skillfishos.com/docs, source/issues at
https://github.com/MTSistemi/SkillFishOS, forum/discussions at
https://github.com/MTSistemi/SkillFishOS/discussions, and a SourceForge project at
https://sourceforge.net/projects/skillfishos/.

Thanks for your consideration.
Mattia — SkillFishOS
