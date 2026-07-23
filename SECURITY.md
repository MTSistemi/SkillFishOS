# Security Policy

SkillFishOS is a Debian-sid–based gaming distribution for the AMD **BC-250**. This policy covers
the parts **we** ship and maintain — the custom kernel patches, the native apps, the APT
repository, the ISO/installer configuration and the website. It does **not** cover upstream
software we merely repackage (the Linux kernel itself, Debian, Mesa, KDE Plasma, Ollama, …);
report those to their respective projects.

## Supported versions

| Component | Version | Supported |
|---|---|---|
| SkillFishOS release | **26.06 "Aetherium"** | ✅ security fixes |
| SkillFishOS release | < 26.06 (pre-release) | ❌ |
| Kernel | `7.0.11-skillfishos` (+ `-generic` / `-slim`) | ✅ |
| Kernel | `7.0.10-skillfishos` | ✅ (previous, best-effort) |
| Apps | `skillfish-*` `26.06` | ✅ |

Fixes are delivered through the signed APT repository
(<https://mtsistemi.github.io/SkillFishOS>) — `sudo apt update && sudo apt upgrade`.

## Reporting a vulnerability

**Please report privately — do not open a public issue for security problems.**

1. Preferred: **GitHub → this repo → Security → "Report a vulnerability"** (private vulnerability
   reporting is enabled). This keeps the report confidential until a fix ships.
2. Alternative: email **security@skillfishos.com** (or `apt@skillfishos.com`). PGP: the same
   ed25519 key that signs the APT repository
   ([`skillfishos-archive-keyring`](https://mtsistemi.github.io/SkillFishOS/skillfishos-archive-keyring.asc)).

Please include: affected component + version, a description, reproduction steps or a PoC, and the
impact you foresee.

**Our targets**

| Severity | First response | Fix target |
|---|---|---|
| Critical (RCE, privilege escalation, repo/key compromise) | 48 h | 7 days |
| High | 4 days | 30 days |
| Medium / Low | 7 days | best effort |

We credit reporters in the advisory and the release changelog unless you prefer to stay
anonymous. We follow coordinated disclosure (typically 90 days, or sooner once a fix is out).

## Scope

**In scope**
- Kernel patches in [`kernel-build/`](kernel-build/) (GPU clock unlock, 40-CU unlock, RDSEED quiet).
- Native apps in [`apps/`](apps/): `skillfish-tuner` (+ helper), `skillfish-ai-panel`
  (+ `skillfish-gtt`), `skillfish-iso-mount`, and the system scripts/services in
  [`system/`](system/) (`skillfish-cu`, governor, thermal guard, first-boot, …).
- The **APT repository** and the `skillfishos-kernel` wrapper (signing, the download-and-install
  `postinst`).
- ISO / **Calamares** installer configuration and the live medium.
- The website ([`website/`](website/)) and the deploy tooling.

**Out of scope**
- Upstream Linux, Debian sid packages, Mesa, KDE, Ollama, open-webui, Docker, penguins-eggs.
- Issues that require the attacker to already be root, or physical access plus a willing operator.
- The intentional, documented trade-offs listed below (open a discussion if you disagree).

## Security design notes & deliberate trade-offs

SkillFishOS targets a **single-user gaming console / desktop on trusted hardware**. Some defaults
favour performance or convenience; they are listed here honestly so you can make an informed
choice and re-harden if your threat model differs.

- **`mitigations=off`** in the kernel command line. CPU speculative-execution mitigations
  (Spectre/Meltdown/etc.) are **disabled** for performance on the single-user BC-250. On a
  multi-user or untrusted-workload machine, remove `mitigations=off` from `GRUB_CMDLINE_LINUX_DEFAULT`
  and `update-grub`.
- **RDSEED is disabled** on the BC-250 (the Cyan Skillfish hardware RNG is unreliable; the kernel
  clears the CPU capability). This is a correctness fix, not a weakening — other entropy sources
  (jitter, interrupts, `random_trust_cpu`) remain. Our patch only silences the boot message.
- **IOMMU is left off** (broken on this board) — no DMA isolation for peripherals.
- **Privileged helpers via polkit/pkexec.** `skillfish-tuner-helper`, `skillfish-gtt` and the
  CU/governor scripts run as root through a single `pkexec`/polkit authentication. They validate
  their inputs (e.g. `skillfish-gtt` bounds the GTT size and only edits known GRUB keys). Report
  any unsanitised path that lets a normal user run arbitrary code as root.
- **`skillfish-iso-mount` polkit rule** lets members of the `sudo` group loop-mount/unmount disk
  images via `udisks2` **without a password prompt**. This is a deliberate convenience for the
  admin user; it does not grant mounting to non-admin accounts.
- **SSH is disabled by default** on installed systems: no host keys are shipped and `ssh.service`
  is not enabled. Enable it yourself (`sudo systemctl enable --now ssh`) and set keys if you want
  remote access.
- **Live ISO credentials** are well-known (`live` / `evolution`, `root` / `evolution`) and apply
  **only to the live session**. A real, password-protected user is created at install time. Do not
  run the live medium unattended on an untrusted network.
- **On-device AI stack.** Ollama runs locally in Docker with telemetry off
  (`ANONYMIZED_TELEMETRY=false`). The compose binds the Ollama API (`:11434`) and open-webui
  (`:8080`) with `OLLAMA_HOST=0.0.0.0`, so **the LLM API is reachable from your LAN**. If that is
  not what you want, firewall those ports or set `OLLAMA_HOST=127.0.0.1` in
  `/opt/stacks/skillfish-ai/compose.yaml`.
- **APT repository integrity.** The `aetherium` repo is **GPG-signed** (ed25519). Because the
  kernel `.deb` exceeds GitHub Pages' 100 MB limit, the tiny `skillfishos-kernel` wrapper's
  `postinst` downloads the kernel image over **HTTPS from a pinned GitHub Releases URL**. Integrity
  there relies on TLS + GitHub; a future hardening step is to verify a published SHA-256 in the
  `postinst`.

## Hardening checklist (optional, for stricter setups)
- Remove `mitigations=off` from GRUB and `update-grub`.
- Set `OLLAMA_HOST=127.0.0.1` (or firewall 11434/8080) if you don't use the AI API over LAN.
- Change the installed user's password; never expose the live medium to untrusted networks.
- Keep `apt upgrade` current so signed fixes from the `aetherium` repo land promptly.

## Supply-chain & repository security
- This repository has **private vulnerability reporting**, **secret scanning** (+ push
  protection), **Dependabot** alerts/updates and **CodeQL** code scanning (the
  `security-and-quality` query suite) enabled — see the **Security** tab.
- Releases and the APT metadata are signed; never install SkillFishOS packages from an unsigned
  mirror.
