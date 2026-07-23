# SkillFishOS 26.06 "Aetherium" — BC-250 release

First public release, built and dogfooded directly on real AMD BC-250 hardware.

## Highlights
- **Custom kernel** linux-tkg **7.0.10-skillfishos** with the **40 CU unlock** (≈ +85 % FP32,
  measured 11385 GFLOPS vkpeak vs 6141 baseline), RDSEED log spam removed, BC-250 quirks patched.
- **SMU GPU governor** + **CPU overclock/undervolt** with an **85 °C** thermal-guard. Ships in
  the safe **Stock** profile; **Performance**, **Turbo** and **Crazy** (up to 4.0 GHz CPU /
  2230 MHz GPU) are one click away in the **Tuner**, validated per-card with test + rollback.
- **KDE Plasma 6** with a full **steampunk** theme (boot → SDDM → desktop), live system **HUD**
  (bilingual IT/EN), Btrfs snapshots with **one-click rollback** from GRUB.
- **Gaming & emulation**: Steam, EmuDeck, ES-DE, Heroic, Proton-GE, gamescope/gamemode/MangoHud.
- **On-device AI**: Ollama + OpenWebUI accelerated in Vulkan.
- BC-250 hardware fixes: DisplayPort HPD hot-swap daemon, suspend disabled, IOMMU off, audio via EDID force.

## Install
- Boots in **English**; choose your **language and keyboard** in the Calamares installer.
- Native bilingual **IT/EN** apps (Tuner, AI Panel) and HUD that follow the system locale.
- Write the ISO to USB (Etcher/Ventoy/dd), boot the BC-250, follow the graphical installer.

## Notes
- Release **specific to the AMD BC-250**; a generic x86-64 PC version will follow.
- **Open source.** Not affiliated with AMD or any console manufacturer.
- SHA-256: `8eea73d9dd23a1d8aa8fda3d8cc7639712b6391e2802282518c141145e1fce8c`
