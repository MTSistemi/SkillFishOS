# SkillFishOS — live Compute Unit (CU) manager

Live control of the AMD BC-250 GPU Compute Units (no reboot), by writing the
SPI/CC/RLC WGP masks via **umr**. 1 WGP = 2 CU; 5 WGP per shader array × 4
arrays (2 SE × 2 SH) = 40 CU. Driver floor = WGP0-2 (24 CU) locked at boot.

## Pieces
- `system/usr/local/bin/skillfish-cu` — clean-room helper: `get` (JSON state),
  `max` (40), `stock` (24), `set <0x07..0x1f>`, `set-rows m00 m01 m10 m11`,
  `state`. Writes `/run/skillfish/cu_active` (world-readable) for the HUD.
- `system/etc/systemd/system/skillfish-cu.service` — oneshot at boot that
  routes all WGPs (40 CU), replacing the old `amdgpu.bc250_cc_write_mode=3`
  kernel param (which locked 40 CU and prevented live changes).

## Dependency
`umr` (User Mode Register debugger, freedesktop) — not in Debian; built from
source, see `system/usr/local/share/build_umr.sh`.

## Credits
The register-write **mechanism** (which registers / WGP semantics) was learned
from **WinnieLV/bc250-cu-live-manager** (no license stated). This is a
clean-room reimplementation; no upstream code is bundled or shipped.
