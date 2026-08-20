---
title: Storage and Btrfs snapshots
description: "SkillFishOS's safety net: automatic snapshots and rollback from boot."
group: System
order: 3
---

One of SkillFishOS's central ideas is being able to **tinker without fear**. This is made possible by the **[Btrfs](https://btrfs.readthedocs.io/)** filesystem with automatic snapshots: every important change is captured, and if something breaks you go back in one click.

## Separate subvolumes

The disk holds a single Btrfs partition, split into distinct subvolumes:

- **`@`** — the operating system;
- **`@home`** — the user's data;
- **`@cache`** and **`@log`** — caches and logs, kept outside the snapshots so a rollback does not drag yesterday's logs back with it;
- **`@games`** — the games library, which would otherwise make every snapshot enormous;
- **`@swap`** — the swap file.

Keeping them separate is essential: rolling back the system **does not touch personal files**. You can return to a "yesterday" system while keeping today's documents, saves and settings.

## Automatic snapshots with Snapper

SkillFishOS uses **[Snapper](http://snapper.io/)** with a `root` configuration and **pre/post hooks on APT**: every time you install or upgrade packages, a snapshot is created automatically *before* and *after*. So if an update causes problems, the "before" snapshot is already there.

Configuration highlights:

- a cap on the number of retained snapshots so the disk doesn't fill up;
- snapshots kept at important system *milestones*;
- management also via the **Btrfs Assistant** graphical tool.

## How many are kept

**Five**, by default: three ordinary ones (the pre/post pair around each `apt`
operation) and two "important" ones — the upgrades that touch the kernel or
systemd, which are the ones you are most likely to want back. On top of those
sits the *"SkillFishOS - clean install"* point, which never expires: the way
back to the system as it came out of the box.

The hourly timeline is **off**. On a home console it only eats disk without
anyone ever looking at those snapshots. Snapshots you create **by hand** are not
counted among the five and are never deleted automatically: if you made one on
purpose, it stays until you remove it.

## Rollback from the boot menu

Thanks to **[grub-btrfs](https://github.com/Antynea/grub-btrfs)**, snapshots
appear directly in the **GRUB** menu, under *"SkillFishOS snapshots"*. Reboot,
pick the snapshot from before the trouble, and you are inside it.

Two things worth knowing before you rely on it:

- **What you boot is read-only.** It is a rescue environment: look around, check
  whether the older state really was fine, copy out the files you need. A few
  services will report a failure at startup — they simply cannot write. That is
  expected, not a fault.
- **The boot menu is refreshed after every `apt` transaction**, so the snapshot
  taken *before* an upgrade is in the list exactly when you need it.

## Making the return permanent

Booting a snapshot does not change anything by itself, and `snapper rollback`
does not help here: it swaps the default subvolume, while our GRUB entry pins
`subvol=@` and wins. The command that does the job is:

```bash
sudo skillfish-rollback --list    # which snapshots are available
sudo skillfish-rollback 12        # snapshot 12 becomes the system, from the next boot
```

It moves the current system aside — it is not deleted, it becomes
`@-rotto-<date>` — and builds a new, writable `@` from the snapshot you chose,
carrying the whole snapshot history across with it. If the older state turns out
not to be the answer either, `sudo skillfish-rollback --undo` puts everything
back, and `--clean` frees the space when you are sure.

It works from the normal system and from inside a snapshot booted read-only,
which is the case that matters when the machine no longer starts.

> **Your home directory is never touched.** `@home` is a separate subvolume: the
> system travels back in time, your files stay as they are. Handy to know, and
> worth remembering before you count on a rollback to bring back a document you
> deleted — it will not.

> This is the safety net that lets even the youngest users explore the system
> without fear of breaking it irreversibly.

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
