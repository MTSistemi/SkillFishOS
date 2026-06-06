---
title: Useful commands
description: A terminal cheat-sheet to diagnose and tune SkillFishOS.
group: Reference
order: 4
---

SkillFishOS is designed **not** to require the terminal: the [Tuner](/en/docs/app-native) and the graphical apps are enough for normal use. This page is for those who want to **tinker** or diagnose. Privileged commands use `sudo`.

> 🛟 Before risky experiments, remember the safety net: Btrfs snapshots and rollback from the GRUB menu (see [Storage & snapshots](/en/docs/storage-snapshot)).

## System and kernel

```bash
uname -r                      # running kernel (should end with -skillfishos)
cat /proc/cmdline             # active boot parameters
journalctl -b -p err          # errors from the current boot
inxi -Fxxxz                   # full hardware summary
```

## GPU, clocks and temperatures

```bash
# GPU temperature from amdgpu sysfs
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# SMU GPU governor status
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # freq/volt safe-points
# real-time GPU monitoring
nvtop        # or: radeontop
```

> On the BC-250 frequency control does **not** go through standard amdgpu sysfs but through the **SMU governor**. Change the values from the [Tuner](/en/docs/app-native), not by hand.

## CPU — overclock/undervolt

```bash
systemctl status bc250-smu-oc.service   # "inactive" after applying is normal (one-shot)
cat /etc/bc250-smu-oc.conf              # applied clock/voltage
lscpu | grep MHz                        # current core frequencies
sensors                                 # temperatures/voltages (nct6686, k10temp)
```

## Live Compute Units (skillfish-cu)

```bash
skillfish-cu get          # JSON state: active CUs + per-row (SE/SH) mask
sudo skillfish-cu max     # route all CUs (40)
sudo skillfish-cu stock   # back to 24 (driver baseline)
sudo skillfish-cu set 0x1f   # WGP mask for all rows (0x07=24 .. 0x1f=40)
cat /run/skillfish/cu_active # "40/40" (also read by the HUD)
vulkaninfo | grep -i "deviceName\|driverName"   # GPU as seen by Vulkan (RADV)
```

CUs are best managed from the [Tuner](/en/docs/app-native) **grid** (click + presets, with "CU test"). The first 24 are driver-locked and always on.

Quick benchmarks (the same ones the Tuner uses):

```bash
vkpeak                # FP32 throughput (GFLOPS)
clpeak                # memory bandwidth (GB/s)
sysbench cpu run      # CPU stress/benchmark
```

## Unified memory (VRAM/GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'gttsize|ttm'   # GTT/TTM params
glxinfo | grep -i "memory"                                 # memory seen by the driver
free -h                                                     # shared RAM/GDDR6
```

## Gaming

```bash
flatpak list                         # Flatpak apps (Steam, EmuDeck emulators…)
flatpak update                        # update Flatpak apps
gamescope -- %command%               # (set this in Steam launch options)
# Bluetooth controllers
bluetoothctl                         # scan on / pair / connect / trust
```

## Local AI

```bash
# the stack runs in Docker containers (see AI panel)
docker ps                            # running containers (ollama, openwebui, dockge)
docker compose -f <stack> up -d      # start the stack
docker compose -f <stack> down       # stop and free GPU/RAM
ollama list                          # installed models (e.g. qwen3:14b)
```

## Snapshots and rollback (Btrfs)

```bash
sudo snapper list                    # list snapshots
sudo snapper create -d "before X"    # manual snapshot
sudo btrfs subvolume list /          # subvolumes (@rootfs, @home)
# the simplest rollback is from the GRUB menu → "SkillFishOS snapshots"
```

## Updates and repository

```bash
sudo apt update && sudo apt full-upgrade   # update the system
apt-mark showhold                          # held packages (incl. the kernel)
sudo apt install skillfishos-kernel        # install/update the kernel from the repo
apt policy <package>                        # which repo/version a package comes from
```

## Network and remote access

```bash
nmcli device status                  # network interface status
ip a                                 # IP addresses
systemctl status x11vnc              # VNC server for the remote desktop
hostname -I                          # IP to use with the VNC client
```

## Display (DisplayPort HPD)

```bash
systemctl status skillfish-dp-hotswap   # daemon that works around the broken HPD
xrandr                                   # outputs and resolutions (X11 session)
```

## Sources

- [Btrfs wiki](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — reference for many Linux commands
