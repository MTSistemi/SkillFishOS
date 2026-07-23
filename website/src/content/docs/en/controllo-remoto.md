---
title: Remote control — Remote Manager
description: SkillFishOS's web dashboard to control the BC-250 from a browser or phone — telemetry, KVM, terminal, Tuner, app store and AI.
group: Usage
order: 4
---

**SkillFishOS Remote Manager** is a modular web dashboard that lets you control the BC-250 **from another PC or your phone**, on the same LAN or — through ZeroTier — from anywhere in the world. You sign in with your system credentials, everything over HTTPS.

## Install

```bash
sudo apt update
sudo apt install skillfish-dashboard
```

The package installs the daemon, the native **Remote Manager** app (to turn the dashboard on/off and pick the modules) and all the web pages. The optional dependencies (KVM, terminal, Wake-on-LAN) are *Recommends* and are pulled in automatically when available.

## Enable

Open **SkillFishOS Remote Manager** from the application menu:

- **Master switch** — starts the service (persistent, via systemd).
- **Module checkboxes** — choose what to expose (telemetry, Tuner, Hub, KVM, terminal, AI…).
- Shows the **URL, a QR code and the credentials** to connect.

Or from a terminal: `sudo systemctl enable --now skillfish-dashboard`.

> For safety the dashboard **does not start on its own** after install — you enable it when you want.

## Access

Open **`https://<board-ip>:8443`** in your browser (or `https://BC-250.local:8443`). Since the certificate is self-signed the browser will warn you the first time — that's expected, proceed.

Sign in with your **system username and password** (the same as the SkillFishOS login): authentication uses PAM.

## The modules

The dashboard composes itself from the modules you enabled:

- **Telemetry** — live charts of temperatures, frequencies, Watts and CPU/GPU load.
- **System status** — host, IP, kernel, uptime, RAM, disk, active CUs, detected freezes.
- **Controls (Tuner)** — quick presets plus the **full Tuner** on the web: CPU (frequency/undervolt/temperature), GPU (frequency/voltage/governor), **live Compute-Unit control** (WGP grid, no reboot), fan, VRAM, *Test* and the **"Find my max"** wizards.
- **Apps & packages (Hub)** — a real **app store** (AppStream + Flatpak + Snap): browse by category, search, install/remove, update. The **SkillFishOS apps** are featured at the top.
- **Desktop (KVM)** — see and control the board's real desktop from the browser (noVNC), no extra hardware.
- **Terminal** — a web shell (ttyd) inside the dashboard.
- **AI / OpenWebUI** — engine status, installed models and a chat with the local LLM, running on the BC-250 GPU.
- **AI-Ops** — the local LLM reads logs and telemetry and diagnoses problems for you.
- **Logs**, **automatic rules** (auto-throttle above a °C threshold), **Wake-on-LAN** and scheduled power on/off.
- **ZeroTier** — to reach the dashboard **from anywhere** (see below).

The **Reboot** and **Shut down** buttons are always available in the top bar. You can **close, reopen and drag** the cards and **save the layout**.

## Remote access (ZeroTier)

The dashboard is meant for the **local network**. To use it from outside, enable the **ZeroTier** module: join one of your networks, authorise the board on [my.zerotier.com](https://my.zerotier.com), then reach the dashboard at the board's ZeroTier address — with no router ports to open.

## Security

- **HTTPS** with a self-signed certificate (TLS 1.2+), generated on first start.
- **PAM login** with your user credentials, **signed sessions** (HMAC) and **rate-limiting** on attempts.
- Designed for the **LAN**; for remote access use ZeroTier rather than exposing it directly on the internet.
