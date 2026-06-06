---
title: Installation
description: How to write the ISO, boot the installer and finish the setup.
group: Installation
order: 1
---

SkillFishOS installs from a **live ISO** that contains the [Calamares](https://calamares.io/) graphical installer. The whole process is done with the mouse, no terminal required.

> ✅ The **26.06 «Aetherium»** ISO is available — download it from the [Download](/en/download) page. It boots in **English** to stay universal and lets you pick your language and keyboard during installation.

## Requirements

- an **AMD BC-250** board (see [hardware](/en/docs/hardware-bc250));
- an **SSD/NVMe** to install onto;
- a monitor connected via **DisplayPort** (a *passive* DP→HDMI adapter can work, but see the display/audio notes in [Troubleshooting](/en/docs/risoluzione-problemi));
- a **USB stick of at least 8 GB** for the installer;
- a keyboard and mouse for the installation.

## 1. Write the ISO to USB

Download the ISO from the [Download](/en/download) page and write it to a stick with one of these tools:

- **[balenaEtcher](https://etcher.balena.io/)** (Windows/macOS/Linux, graphical, recommended);
- **[Ventoy](https://www.ventoy.net/)** (lets you keep several ISOs on the same stick);
- from a Linux terminal with `dd`:

```bash
sudo dd if=SkillFishOS_amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

> Replace `/dev/sdX` with the correct device for your stick. **Warning**: `dd` writes without asking and erases everything on the target device.

## 2. Boot the BC-250 from USB

Insert the stick, power on the board and enter the boot/UEFI menu to select the USB as the boot device. The SkillFishOS **live** environment (KDE Plasma) will start: you can explore the system before installing it.

## 3. Install with Calamares

From the live desktop launch the installer (*Install SkillFishOS* icon). Calamares guides you step by step:

1. **Language and timezone.**
2. **Keyboard.**
3. **Partitioning.** SkillFishOS uses **Btrfs** with separate `@rootfs` (system) and `@home` (user data) subvolumes: this lets you *roll back* the system without touching your files. A small **EFI** partition and a **swap** partition complete the layout. For most users the automatic install option ("Erase disk") is fine.
4. **User.** Create your account (it will be in the right groups for gaming, audio, render, etc.).
5. **Summary and install.**

When installation finishes, reboot and remove the stick.

## 4. First boot

On first boot **everything is already configured**: optimized kernel, governor, overclock, theme, gaming and snapshots are active. No manual tuning needed.

From here you can:

- pair your [controllers](/en/docs/gaming) (DualShock 4 over Bluetooth or a USB controller);
- add your games to [Steam/EmuDeck](/en/docs/gaming);
- enable the [local AI](/en/docs/ai-locale) stack when you need it;
- tune the hardware with the [Tuner](/en/docs/app-native) if you wish.

## Disk layout

| Partition | Filesystem | Content |
|---|---|---|
| `nvme0n1p1` | FAT32 (EFI) | GRUB bootloader |
| `nvme0n1p2` | **Btrfs** | `@rootfs` (system) + `@home` (data) |
| `nvme0n1p3` | swap | swap space |

## Sources

- [Calamares](https://calamares.io/) — the universal installer
- [balenaEtcher](https://etcher.balena.io/) · [Ventoy](https://www.ventoy.net/)
- [Btrfs wiki](https://btrfs.readthedocs.io/) — subvolumes and snapshots
