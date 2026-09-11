# SkillFishOS apps

Small native apps shipped with SkillFishOS (KDE Plasma), all themed by Kvantum.

- **`control-center/`** — **SkillFishOS Control Center** (PyQt6): every tool in
  one window. Status, Tuner (the V/F governor curve with a trial countdown),
  Fan, Monitor, Games (our Mesa, scx, FSR 4, GE-Proton), Profiles, Kernel,
  Snapshots, AI, Emulators, Console, ISO. `skillfish-control-center` is the
  window; `skillfish-cc-helper` is the privileged daemon (JSON-per-line over a
  single `pkexec`). See [control-center/README.md](control-center/README.md).
- **`tuner/`** — the old **SkillFishOS Tuner**; since 26.09 `skillfish-tuner`
  opens the Tuner section of the Control Center. The package keeps
  `skillfish-tuner-helper`, `skillfish-cu` and the CU boot service.
- **`ai-panel/`** — **SkillFish AI** (PyQt6): one-click on/off for the on-device
  LLM engine (Unsloth Studio, Vulkan), freeing the GPU/RAM for gaming. See [../docs/AI.md](../docs/AI.md).
- **`iso-mount/`** — native KDE ISO mounting via udisks2 (no GNOME). See its README.

The Tuner/AI panels were originally GTK4/libadwaita; they were rewritten in PyQt6
so Kvantum themes them natively with no GTK CSS hacks.

## Install the prebuilt `.deb` packages

The apps are published as Debian packages (architecture `all`) in the
[**`apps-26.06`** release](https://github.com/MTSistemi/SkillFishOS/releases/tag/apps-26.06):

```sh
# download the three .deb from the release, then:
sudo apt install ./skillfish-tuner_26.06_all.deb \
                 ./skillfish-ai-panel_26.06_all.deb \
                 ./skillfish-iso-mount_26.06_all.deb
```

`apt install ./file.deb` resolves the dependencies (`python3-pyqt6`, `udisks2`,
`polkitd`, …) automatically. They are already preinstalled on the SkillFishOS ISO.

To rebuild the packages from the installed files on a SkillFishOS system, run
[`build-debs.sh`](build-debs.sh) (output in `/tmp/debs/out/`).
