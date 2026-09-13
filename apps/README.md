# SkillFishOS apps

Small native apps shipped with SkillFishOS (KDE Plasma), all themed by Kvantum.

- **`control-center/`** — **SkillFishOS Control Center** (PyQt6): every tool in
  one window. Status, Tuner (the V/F governor curve with a trial countdown),
  Fan, Monitor, Games (our Mesa, scx, FSR 4, GE-Proton), Profiles, Kernel,
  Snapshots, AI, Emulators, Console, ISO. `skillfish-control-center` is the
  window; `skillfish-cc-helper` is the privileged daemon (JSON-per-line over a
  single `pkexec`). See [control-center/README.md](control-center/README.md).
- **`tuner/`, `monitor/`, `fan/`, `kernel-manager/`, `snapshots/`, `ai-panel/`,
  `emulators/`, `console/`, `iso-mount/`** — the old per-tool packages. Since
  26.09 their commands (`skillfish-tuner`, `skillfish-monitor`,
  `skillfish-fan`, `skillfish-kernel-manager`, `skillfish-snapshots`,
  `skillfish-ai-panel`) open the matching Control Center section instead of a
  standalone window. The packages stay because they carry the daemons and
  helpers the Control Center relies on: the fan daemon, the tuner helper
  (`skillfish-tuner-helper`), `skillfish-cu` and the CU boot service, and the
  Unsloth launcher (`skillfish-unsloth`) and updater
  (`skillfish-unsloth-update`). The Tuner and AI panel were originally
  GTK4/libadwaita; both were rewritten in PyQt6 (and then folded into the
  Control Center) so Kvantum themes them natively with no GTK CSS hacks.
- **`hub/`** — **SkillFishOS Hub** (PyQt6): the Discover-style software
  centre. A separate app.
- **`hud/`** — the live system HUD: a translucent Conky overlay (BC-250
  only). A separate app.
- **`dashboard/`** — **SkillFishOS Remote Manager**: the web dashboard
  (`https://<board>:8443`, PAM login). A separate app; it mirrors Tuner,
  Games, Profiles, Fan, Monitor and AI on the web. See
  [../docs/AI.md](../docs/AI.md) for the AI side.

## Install the prebuilt `.deb` packages

The packages come from the signed APT repository:

```
deb https://mtsistemi.github.io/SkillFishOS aetherium main
```

(mirrored at [deb.skillfishos.com](https://deb.skillfishos.com) too). They
are already preinstalled on the SkillFishOS ISO; on an existing Debian-based
system, once the repository and its key are added:

```sh
sudo apt install skillfish-control-center
```

`apt` resolves the dependencies (`python3-pyqt6`, `udisks2`, `polkitd`, …)
automatically.

To rebuild the packages from the installed files on a SkillFishOS system, run
[`build-debs.sh`](build-debs.sh) (output in `/tmp/debs/out/`).
