# SkillFishOS apps

Small native apps shipped with SkillFishOS (KDE Plasma), all themed by Kvantum.

- **`tuner/`** — **SkillFishOS Tuner** (PyQt6): GUI to control the BC-250 hardware
  with no terminal — CPU OC/UV, GPU governor safe-point, fan, UMA VRAM split,
  40-CU toggle, with *apply → benchmark → verify/rollback* tests. `skillfish-tuner`
  is the GUI (→ `/usr/local/bin/`); `skillfish-tuner-helper` is the privileged
  daemon (JSON-per-line over a single `pkexec`).
- **`ai-panel/`** — **SkillFish AI** (PyQt6): one-click on/off for the on-device
  LLM stack (Ollama + Vulkan), freeing the GPU/RAM for gaming. See [../docs/AI.md](../docs/AI.md).
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
