# SkillFishOS 26.06.4 "Aetherium" — media respin

A maintenance respin of the 26.06 "Aetherium" release for the AMD BC-250. Two editions:
**BC-250** (`7.1.7-skillfishos`, znver2) and **Generic** (`7.1.7-skillfishos-generic`,
any x86-64 PC or VM). Boots in English; the language is chosen at install.

This respin started out being about **languages**. It ended up being about an installer
that could not finish on real hardware, and about three guards that were watching the
wrong thing. Both stories are below; the second one matters more if you are on 26.06.3.

## The installer no longer reboots your board

If you tried to install 26.06.3 on a real BC-250 and it failed, this is why — and it was our fault.

`skillfish-core-unlock` unlocks the two disabled CPU cores by writing the SMU core-presence mask and then **rebooting**: that is how the board re-reads how many cores it has, and a cold power-off reverts the mask, so the reboot happens on every cold start. Nothing stopped it from doing this **inside the live session**. The board rebooted a few seconds after start-up and, if that landed while Calamares was copying, the installation died. One cause, both symptoms.

We never caught it because every install test ran in a VM, where the SMU write fails, the script exits and never reboots. The code path that breaks real hardware is exactly the one a virtual machine cannot execute.

**The 8-core unlock is now off by default and opt-in.** SkillFishOS Tuner gained an *8 cores* switch in the CPU section; the tooltip states the cost up front (one extra reboot per cold start). Upgrading does not take the cores away from anyone who was already using them: if the mask is already unlocked, the package keeps it that way.

*Already on 26.06.3 and stuck?* `sudo apt update && sudo apt upgrade` fixes the installed system. To get **past the installer** on the old media, press <kbd>e</kbd> at the boot menu and add `systemd.mask=skillfish-core-unlock.service` to the `linux` line.

## Installing on Btrfs actually works now

26.06.3 could install onto Btrfs and then refuse to boot:

```
error: premature end of file /@/boot/vmlinuz-...
error: you need to load the kernel first.
```

Calamares copies the system with `rsync -aHAXS**S**` — that `S` is `--sparse`, so runs of zeros become holes. Our kernel image ends with 512 zero bytes, so it landed with a hole at the tail; on Btrfs a hole has no extent, the map stops one block short of the declared size, and GRUB stops there. Linux reads the file fine, which is why nothing looked wrong.

We had shipped a repair for this in 26.06.3 — and it repaired nothing. It rewrote the files with `cp --reflink=never` but without `--sparse=never`, and GNU `cp` faithfully reproduces the hole. The check in CI that was meant to catch a regression searched for a string present in the broken version too, so it passed either way. Code, changelog and CI confirmed each other for six days.

Fixed, and the repair now verifies its own work: if a file still occupies fewer sectors than its size requires, it says so.

## Also fixed

- **SSH failed on every fresh install** (`sshd: no hostkeys available`). Host keys are deliberately stripped from the image — otherwise every installation on earth would share the same keys — but the service that regenerates them was not enabled. Five more services were in the same state, including the GPU clock sampler and Wake-on-LAN.
- **A third-party sensor module could abort the whole installation.** `nct6687d` failed to build, `dpkg-reconfigure` returned non-zero, and Calamares gave up — before writing the bootloader. A temperature sensor is not a good reason to refuse to install an operating system.
- **The `nct6687` fan/sensor module now builds.** Its `Kbuild` file was never copied, so `make` walked the directory, found nothing to compile and exited *successfully* while DKMS reported failure.
- **The initrd is compressed with zstd**, not gzip: `zstd` was simply missing from the image.
- **Third-party code without a licence is no longer shipped.** `bc250_memcfg` and `bc250-cu-ref` are out of the image; the memory-split tool is now our own `skillfish-memcfg` (GPL-3.0).

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

## Fixed

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
