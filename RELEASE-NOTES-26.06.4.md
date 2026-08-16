# SkillFishOS 26.06.4 "Aetherium" — media respin

A maintenance respin of the 26.06 "Aetherium" release for the AMD BC-250. Two editions:
**BC-250** (`7.1.7-skillfishos`, znver2) and **Generic** (`7.1.7-skillfishos-generic`,
any x86-64 PC or VM). Boots in English; the language is chosen at install.

This is the release to use if you are on **26.06.3**. Two earlier candidates were built
and held back: opening them and looking inside — rather than reading the build log —
turned up an installer fix that had reached only half of our build pipeline, and a
handful of files from the build machine that had no business being in a published
image. Both are described below, because they are the most useful things in these notes.

## The installer no longer reboots your board

If you tried to install 26.06.3 on a real BC-250 and it failed, this is why — and it was our fault.

`skillfish-core-unlock` unlocks the two disabled CPU cores by writing the SMU core-presence mask and then **rebooting**: that is how the board re-reads how many cores it has, and a cold power-off reverts the mask, so the reboot happens on every cold start. Nothing stopped it from doing this **inside the live session**. The board rebooted a few seconds after start-up and, if that landed while Calamares was copying, the installation died. One cause, both symptoms.

We never caught it because every install test ran in a VM, where the SMU write fails, the script exits and never reboots. The code path that breaks real hardware is exactly the one a virtual machine cannot execute.

**The 8-core unlock is now off by default and opt-in.** SkillFishOS Tuner gained an *8 cores* switch in the CPU section; the tooltip states the cost up front (one extra reboot per cold start).

Upgrading does not take the cores away from anyone who was already using them — and in the 26.06.4 candidate that promise was **broken**. The package asks the unlock tool for the current core mask and, if the cores are already on, records that you want to keep them. But the tool refused to answer that question on exactly the machines being migrated: the "have you opted in?" guard ran *before* the read-only query, so instead of the mask it printed "unlock not enabled" and the migration never fired. A guard on writing had been placed in front of a read. Fixed, and tested by running the query on a machine with the marker removed.

*Already on 26.06.3 and stuck?* `sudo apt update && sudo apt upgrade` fixes the installed system. To get **past the installer** on the old media, press <kbd>e</kbd> at the boot menu and add `systemd.mask=skillfish-core-unlock.service` to the `linux` line.

## The image no longer carries files from the machine that built it

SkillFishOS images are produced by cloning the development board. That is a practical
way to build a distribution and a very easy way to ship things that belong to one
machine. Checking the 26.06.4 candidates before publishing them, we found several — and
the same files are present in **26.06.3**, so this is worth two minutes of your time if
you installed from it.

Two of them affect **you**, not just us:

- **A ZeroTier identity that is not yours.** `zerotier-one` was installed, enabled, and
  carried a ready-made private identity. Every machine installed from 26.06.3 came up as
  a node of someone else's private network. If you do not use ZeroTier, remove the
  package: `sudo apt purge zerotier-one`. If you do, delete `/var/lib/zerotier-one/identity.*`
  and restart the service so it generates an identity of its own.
- **A shared module-signing key.** `/var/lib/dkms/mok.key` shipped inside the image, so
  every installation had the same private key for signing kernel modules under Secure
  Boot. Delete `mok.key` and `mok.pub` from `/var/lib/dkms/`; DKMS regenerates a pair
  that is yours the next time it builds a module.

The rest were ours to worry about — an API key, Bluetooth pairing records, the build
machine's root password hash, 800 MB of its system logs — and they have been rotated.

The build now moves every per-machine file out of the way before compressing the image
and puts it back afterwards, and it **refuses to produce an image** if any of them is
still in place when the check runs. That check is the part that matters: the previous
mechanism was correct, it was just too short, and nothing was watching it.

## A failing third-party module can no longer abort the installation

`nct6687d`, an out-of-tree sensor module, failed to build; `dpkg-reconfigure` returned non-zero; Calamares gave up — before writing the bootloader. A temperature sensor is not a good reason to refuse to install an operating system, so that step now tolerates the failure and guarantees an initrd either way.

We shipped that fix in the 26.06.4 candidate. It did nothing, because **Calamares is configured from two independent places** in this project — one for the live-build images, one for the eggs images — and the published ISOs come from the second one. The fix had gone into the first. What gave it away was the timestamp on the generated config inside the candidate image: it had been rewritten by the eggs branch, without the fix, during the build.

Both branches now carry it, and the check that is supposed to notice looks for the actual lines instead of three strings that were present either way. A check that cannot fail is not a check.

## Installing on Btrfs actually works now

26.06.3 could install onto Btrfs and then refuse to boot:

```
error: premature end of file /@/boot/vmlinuz-...
error: you need to load the kernel first.
```

Calamares copies the system with `rsync -aHAX**S**` — that `S` is `--sparse`, so runs of zeros become holes. Our kernel image ends with 512 zero bytes, so it landed with a hole at the tail; on Btrfs a hole has no extent, the map stops one block short of the declared size, and GRUB stops there. Linux reads the file fine, which is why nothing looked wrong.

We had shipped a repair for this in 26.06.3 — and it repaired nothing. It rewrote the files with `cp --reflink=never` but without `--sparse=never`, and GNU `cp` faithfully reproduces the hole. The check in CI that was meant to catch a regression searched for a string present in the broken version too, so it passed either way. Code, changelog and CI confirmed each other for six days.

Fixed, and the repair now verifies its own work: if a file still occupies fewer sectors than its size requires, it says so.

## The snapshot boot menu stops erroring on every boot

On an installed 26.06.3, `grub-btrfsd` logged

```
grub-btrfsd: [!] Error during grub menu creation (grub/ grub-btrfs error)
```

at every boot, and the pre-upgrade snapshot did not appear in the menu — missing exactly when you need it. We generate that menu ourselves from an apt hook, which works, so the daemon is masked.

That masking was already written, and it never reached anyone: it sat *after* an early exit in the first-boot script, so any machine that had already completed its first boot — that is, every installed 26.06.3 — skipped it. It now runs before the guard, on every boot, and `grub-btrfs.path` is masked too, since that is what wakes the daemon up.

## Also fixed

- **SSH failed on every fresh install** (`sshd: no hostkeys available`). Host keys are deliberately stripped from the image — otherwise every installation on earth would share the same keys — but the service that regenerates them was not enabled. Five more services were in the same state, including the GPU clock sampler and Wake-on-LAN.
- **The `nct6687` fan/sensor module now builds.** Its `Kbuild` file was never copied, so `make` walked the directory, found nothing to compile and exited *successfully* while DKMS reported failure.
- **The initrd is compressed with zstd**, not gzip: `zstd` was simply missing from the image.
- **The GPU's share of memory is set with one knob again.** The kernel deprecated `amdgpu.gttsize` and, when both it and `ttm.pages_limit` were set, obeyed the first while warning about the mismatch at every boot — which is why raising the TTM limit had never given the GPU a single extra byte. The command line now sets only `ttm.pages_limit` (counted in 4 KiB pages: 1572864 = 6 GiB, exactly what the board had before), and the AI panel, the dashboard and the GTT helper all read and write that one knob.
- **A private TLS key was being shipped.** The Remote Manager's key, certificate and session secret were cloned from the build machine into every published 26.06.x image. They are now moved aside before the image is made, along with the development environment.

- **The installer no longer under-estimates the disk it needs.** It asked for 10 GiB and
  the system it unpacks occupies 15, so an install onto a small disk was allowed to start
  and then failed part-way. It now asks for 24 GiB.
- **The BC-250 edition boots its own kernel.** `GRUB_DEFAULT` was shipped pinned to the
  build machine's disk UUID; on your disk that entry does not exist, GRUB fell back to
  the first entry, and the ordering put the *generic* kernel first — so the BC-250
  edition installed and then ran the generic kernel.
- **Safe Mode and Text Mode in the boot menu do something.** They were byte-for-byte
  copies of the normal entry. Safe Mode now disables kernel mode-setting and the splash;
  Text Mode stops at a text console.
- **The boot menu is in English.** The first screen, before any language is chosen, said
  *"gioca e impara Linux"* and carried a stray Spanish label. (The attribution to the
  Quirinux theme it derives from stays where it belongs, in the comments.)
- **The live session now runs with the same kernel parameters as the installed system**
  (`mitigations=off`, `split_lock_detect=off`), and the BIOS and UEFI boot paths no
  longer behave differently from each other.
- **Btrfs keeps its compression after installation.** The system was installed with
  `zstd` and then remounted with the defaults.
- **Waydroid, the snapshot timeline timer and the LXC services** are no longer enabled in
  a fresh install: the first failed at every boot, the second contradicted what we say
  about snapshots, and the third belongs to our build infrastructure.

## Now genuinely in four languages

SkillFishOS has claimed Italian, English, Polish and Ukrainian for a while. In practice
a lot of text could not be translated *at all*, for a reason that is invisible from the
outside: strings were being assembled **before** reaching the translation function, so
the lookup key contained a model name or a number and never matched anything. It fell
back to English every time, whatever language you picked.

- **Native apps** — 46 such strings across Tuner, Hub, AI panel, Kernel Manager and
  Monitor were rewritten so the placeholder stays inside the translated text. All keys
  now exist in Polish and Ukrainian, with the placeholders verified to match across
  languages.
- **Remote Manager web dashboard** — the same defect in three different shapes: a
  dictionary that only had Italian and English, 52 strings hardcoded in inline
  conditionals, and about 50 more written straight into the HTML of the Tuner, Hub and
  chat pages. That last group was not "missing Polish": it was **fixed Italian**, shown
  to English users too. The dashboard now carries 160 + 59 translated strings and a
  language switcher with all four options.
- **Login screen (SDDM)** — said *"Accedi"* to Polish and Ukrainian users. It is the
  very first thing you see of the system, and it spoke the wrong language.
- **Menu entries, the SkillFishOS menu category and the Tuner presets** now use English
  as the base with Italian, Polish and Ukrainian alongside it — including the Polish
  diacritics that had been dropped.
- **Calamares slideshow** — the five install slides were hardcoded Italian. They are now
  written per language; the English fallback is used when a language is missing.

**The rule we settled on:** the fallback is always English, never Italian. If a
translation is missing, or the script that applies it fails, you get English — the
language most people in the world can read.

## Also fixed (desktop)

- **The Hub could not install any Flatpak.** With Flathub configured both system-wide
  and per-user, the install command did not say which scope to use and Flatpak refused
  to guess. Every Flatpak install from the software centre failed.
- **BC-250-only services had no hardware guard.** The code meant to add it never ran —
  an unescaped newline inside a `sed` made it a no-op that failed silently. On a normal
  PC those services restart every five seconds forever. This is exactly what the guard
  was written to prevent.
- **The desktop theme wiped its own icons.** Its post-install step regenerated an icon
  cache that Qt cannot read, leaving every launcher in the panel as a blank sheet — on
  every machine, at every package update.
- **The HUD never started at login.** KDE turns autostart entries into systemd services,
  and in that conversion `$HOME` stayed literal, so conky could not find its
  configuration. It is now launched by a small script. On non-BC-250 hardware the HUD
  does not start at all: its layout is built for this board and collapses to an
  invisible 15×15 window anywhere else.

## New

- **The Hub replaces Discover in the panel**, with the steampunk shopping bag from our
  own icon theme.
- **Emulator installers.** Emulators cannot ship in the image — EmuDeck installs
  everything into the user's home, which the installer does not copy. Two entries now
  appear under *Games*: one that runs EmuDeck, one that installs individual emulators
  from Flathub and tells you which ones actually perform well on this hardware.
- **Every package now ships a changelog and a copyright file**, which Debian policy
  requires and which we had never included. The changelog is generated from the commits
  that touch that package, not written by hand.

## Third-party tools, and an honest note about licensing

`bc250_memcfg` is **included** in these images. It has no licence, and we have asked its
author for one. We are shipping it anyway because today it is the only working way to
change the VRAM/GTT split on this board — that is, to give more memory to local AI. Our
own replacement, `skillfish-memcfg` (GPL-3.0), writes the CMOS block correctly but has
not yet been proven to make the firmware act on it, and removing something that works in
favour of something that does not is a regression with a good excuse. `bc250-cu-ref` is
**not** included: there our own `skillfish-cu` does the job.

## Known limitations

- The install slideshow is shown in **English** for Polish and Ukrainian installs. The
  language Calamares uses for its own interface is not exposed to the slideshow the way
  we assumed; the proper fix uses Qt translation catalogues and is coming.
- **Ukrainian has not been reviewed by a native speaker.** Polish was reviewed by
  Cyryl Sochacki; Ukrainian is our own work and corrections are very welcome.
- Game streaming (Sunshine) is still listed as a module without a panel.

## Verify your download

```
sha256sum -c SkillFishOS-26.06.4-Aetherium-<edition>-amd64.iso.sha256
```

Already running SkillFishOS? You do not need the ISO — `sudo apt update && sudo apt
upgrade` brings the same applications to your installed system.
