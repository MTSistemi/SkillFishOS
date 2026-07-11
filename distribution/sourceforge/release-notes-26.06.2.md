# SkillFishOS 26.06.2 "Aetherium" — media respin

A maintenance respin of the 26.06 "Aetherium" release, fixing four community-reported
bugs on the AMD BC-250. Three editions as always: **BC-250** (`7.0.11-skillfishos`,
znver2), **Generic** (`7.0.11-skillfishos-generic`, any x86-64 PC/VM) and **Slim**
(`7.0.11-skillfishos-slim`, ultra-lean). Boots in English; language chosen at install.

## What's fixed
- **Language no longer stuck on Italian.** A hardcoded locale in `/etc/environment`
  overrode the language chosen at install / in KDE, leaving the SkillFishOS apps and
  game launchers in Italian on English (and other) systems. The installed system now
  honours your chosen language. *(GitHub #11)*
- **On-device AI now uses the GPU out of the box.** The AI setup wizard's generated
  `compose.yaml` was missing the GPU flags, so Ollama fell back to slow CPU inference.
  It now sets `OLLAMA_VULKAN=1` + `OLLAMA_IGPU_ENABLE=1` (+ flash-attention). *(#14)*
- **SkillFish AI starts on first try.** The setup wizard now adds your user to the
  `docker` group and runs the first stack start as root, so it no longer fails with a
  Docker permission error before you re-login. *(#13)*
- **Sturdier install/boot.** The installer now also writes the removable EFI fallback
  bootloader (`\EFI\BOOT\BOOTX64.EFI`), which the BC-250's firmware often boots from,
  and uses an explicit GRUB-safe Btrfs subvolume layout. *(hardening for #12 — if you
  hit a GRUB rescue with the automatic Btrfs install, the ext4 option is the safe pick.)*

## Also updated
- Latest **SkillFishOS Remote Manager** web dashboard, **Tuner** (fan curve, named
  CU/WGP profiles, CPU core map, GPU/CPU find-my-max wizards) and the full **Hub** app
  store, all captured in the media.

## Verify your download
```
sha256sum -c SkillFishOS-26.06.2-Aetherium-<edition>-amd64.iso.sha256
```

Thanks to **@SwiatLinuksa** for the precise bug reports. 🐟
