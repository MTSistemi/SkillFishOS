---
title: Storage and Btrfs snapshots
description: "SkillFishOS's safety net: automatic snapshots and rollback from boot."
group: System
order: 3
---

One of SkillFishOS's central ideas is being able to **tinker without fear**. This is made possible by the **[Btrfs](https://btrfs.readthedocs.io/)** filesystem with automatic snapshots: every important change is captured, and if something breaks you go back in one click.

## Separate subvolumes

The disk uses two distinct Btrfs subvolumes:

- **`@rootfs`** — the operating system;
- **`@home`** — the user's data.

Keeping them separate is essential: rolling back the system **does not touch personal files**. You can return to a "yesterday" system while keeping today's documents, saves and settings.

## Automatic snapshots with Snapper

SkillFishOS uses **[Snapper](http://snapper.io/)** with a `root` configuration and **pre/post hooks on APT**: every time you install or upgrade packages, a snapshot is created automatically *before* and *after*. So if an update causes problems, the "before" snapshot is already there.

Configuration highlights:

- a cap on the number of retained snapshots so the disk doesn't fill up;
- snapshots kept at important system *milestones*;
- management also via the **Btrfs Assistant** graphical tool.

## Rollback from the boot menu

Thanks to **[grub-btrfs](https://github.com/Antynea/grub-btrfs)** (with the `grub-btrfsd` daemon), snapshots appear directly in the **GRUB** menu, under *"SkillFishOS snapshots"*. In case of a problem:

1. reboot;
2. from the GRUB menu pick a working previous snapshot;
3. boot into that state and, if you want to make the return permanent, complete the rollback.

> This is the "safety net" that lets even the youngest users explore the system without fear of breaking it irreversibly.

## Why Btrfs and not Timeshift

SkillFishOS chose **Btrfs + Snapper + grub-btrfs** over solutions like Timeshift because:

- the APT integration is automatic (a snapshot on every package operation);
- the snapshots are native to the filesystem (instant, *copy-on-write*, cheap);
- rollback is available **from boot**, even if the system no longer starts normally.

## Sources

- [Btrfs documentation](https://btrfs.readthedocs.io/)
- [Snapper](http://snapper.io/)
- [grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)
- [Btrfs Assistant](https://gitlab.com/btrfs-assistant/btrfs-assistant)
