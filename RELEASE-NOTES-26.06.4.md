# SkillFishOS 26.06.4 "Aetherium" — media respin

A maintenance respin of the 26.06 "Aetherium" release for the AMD BC-250. Two editions:
**BC-250** (`7.1.7-skillfishos`, znver2) and **Generic** (`7.1.7-skillfishos-generic`,
any x86-64 PC or VM). Boots in English; the language is chosen at install.

This respin is mostly about **languages** and about **things that were quietly broken
outside Italian and English** — including a few we only found because we went looking.

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
