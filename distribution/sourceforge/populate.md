# SourceForge — populate everything (paste-ready content)

Project: **skillfishos** · all tools (Code, Files, Forum/Discussion, Wiki, Blog) are enabled.
Below is ready-to-paste content for each tool. (I can't log in to your account — these are for
you to paste, or I can drive your browser if you're already logged in.)

---

## 1. Code — import from GitHub

Admin → Tools → **Import** (or the Code tool's "Import from GitHub"):
- Source: `https://github.com/MTSistemi/SkillFishOS`
- This mirrors the repo (kernel recipe, theme, docs, distribution/) into SourceForge Code.
> The `gh-pages` branch (APT repo) and large release assets stay on GitHub; SF Code is a mirror.

---

## 2. Project summary & description

**Summary (one line):**
> Steampunk gaming Linux for the AMD BC-250 — Debian sid + KDE Plasma 6, pre-tuned.

**Description (project home):**

SkillFishOS turns the cheap, salvaged **AMD BC-250** mining board — a semi-custom
**Zen 2 + RDNA 2** APU ("Oberon" CPU / "Cyan Skillfish" gfx1013 GPU, 16 GB GDDR6) — into a
ready-to-use console-PC for gaming, emulation, local AI and everyday desktop use.

Everything is pre-tuned: a custom **linux-tkg 7.0.10** kernel with the **40 Compute Unit**
unlock, a dedicated **SMU governor**, CPU/GPU overclock + undervolt profiles with an 85 °C
thermal-guard, a consistent **steampunk** theme from boot to desktop, Btrfs snapshots with
one-click rollback, Steam + EmuDeck + ES-DE + Heroic, and an on-device Vulkan AI stack.

The **26.06 "Aetherium"** release is specific to the AMD BC-250; a generic x86-64 PC version
will follow. Open source. Not affiliated with AMD or any console manufacturer.

- Website: https://skillfishos.com · Docs: https://skillfishos.com/docs
- Source: https://github.com/MTSistemi/SkillFishOS

**Categories:** Operating System Distribution · Games/Entertainment · Desktop Environment (KDE)
**License:** GPL-compatible (open source) · **Audience:** End Users/Desktop · Advanced End Users
**External links:** Homepage → skillfishos.com · Git → github.com/MTSistemi/SkillFishOS

---

## 3. Files — the ISO

See [`UPLOAD.md`](UPLOAD.md): create folder `26.06-Aetherium/`, upload the 5.6 GB ISO + `.sha256`,
set it as the default download for Linux. That URL is what DistroWatch needs.

---

## 4. Blog / News — release announcement (paste as the first post)

**Title:** SkillFishOS 26.06 "Aetherium" — first release for the AMD BC-250

We're thrilled to launch **SkillFishOS 26.06 "Aetherium"**, a steampunk gaming Linux distro
built and dogfooded directly on the real **AMD BC-250** — the cheap, salvaged mining board with
a console-class Zen 2 + RDNA 2 APU.

**What's inside**
- 🐧 Custom **linux-tkg 7.0.10** kernel with the **40 Compute Unit unlock** (+85% FP32:
  11,385 vs 6,141 GFLOPS measured) and BC-250 quirk fixes (DisplayPort hot-swap, suspend, IOMMU).
- ⚡ **SMU governor** + CPU/GPU **overclock & undervolt** with four Tuner presets
  (Stock → Crazy, up to 4.0 GHz CPU / 2230 MHz GPU) and an 85 °C thermal-guard.
- 🎨 End-to-end **steampunk** KDE Plasma 6 desktop, live system HUD (bilingual IT/EN).
- 📸 **Btrfs** snapshots with one-click rollback from GRUB.
- 🎮 Steam, EmuDeck, ES-DE, Heroic, Proton-GE · 🧠 on-device Vulkan AI (Ollama + OpenWebUI).

**Get it:** boots in English, pick your language at install. Download on the Files page.
**Updates:** signed APT repo (`aetherium`) — `apt install skillfishos-kernel`.

Benchmarks show the ~€50 board matching a **Radeon RX 6600** in gaming. Open source, community-driven.
Join the discussion on the Forum and at https://github.com/MTSistemi/SkillFishOS/discussions.

---

## 5. Forum / Discussion — welcome post

**Title:** Welcome to the SkillFishOS community

Welcome! This is the place to ask questions, share your BC-250 builds (cases, fans, cooling),
report issues and suggest features for **SkillFishOS**.

- 📖 Docs: https://skillfishos.com/docs
- 🐛 Bugs: https://github.com/MTSistemi/SkillFishOS/issues
- 💬 Also on GitHub Discussions: https://github.com/MTSistemi/SkillFishOS/discussions
- 🔧 Hardware help (3D-printable cases, recommended fans): see the Hardware doc.

Tell us about your setup: which BC-250, your cooling solution, and what you're playing. 🎮

---

## 6. Wiki — Home page

```
# SkillFishOS Wiki

**SkillFishOS** is a steampunk gaming Linux distribution for the **AMD BC-250**
(Debian sid + KDE Plasma 6), pre-tuned out of the box.

## Start here
- [Download & install](https://skillfishos.com/docs/installazione)
- [The BC-250 hardware](https://skillfishos.com/docs/hardware-bc250) — incl. 3D cases & fans
- [GPU/CPU overclock & undervolt](https://skillfishos.com/docs/gpu-overclock)
- [Updates & the APT repo](https://skillfishos.com/docs/aggiornamenti)
- [Gaming & emulation](https://skillfishos.com/docs/gaming) · [On-device AI](https://skillfishos.com/docs/ai-locale)

## Links
- Website: https://skillfishos.com
- Source & releases: https://github.com/MTSistemi/SkillFishOS
- APT repo: https://mtsistemi.github.io/SkillFishOS/ (suite `aetherium`)

The full documentation lives on the website; this wiki points to it to avoid duplication.
```

---

> Wiki & Blog on SourceForge are **git-backed**. If you add an SSH key to your SF account, the
> content above can be pushed via `git clone ssh://<user>@git.code.sf.net/p/skillfishos/wiki`
> — but adding the key requires logging in once (which you do, not me).
