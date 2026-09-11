#!/usr/bin/env python3
"""Point the README files at the Control Center. Idempotent.

    patch-readme.py <repo>
"""
import os
import sys

repo = sys.argv[1]


def patch(rel, coppie):
    p = os.path.join(repo, rel)
    t = open(p, encoding="utf-8").read()
    for vecchio, nuovo in coppie:
        if nuovo in t:
            continue
        assert vecchio in t, (rel, vecchio[:60])
        t = t.replace(vecchio, nuovo, 1)
    open(p, "w", encoding="utf-8").write(t)
    print("ok", rel)


patch("apps/README.md", [
    ("- **`tuner/`** — **SkillFishOS Tuner** (PyQt6): GUI to control the BC-250 hardware\n"
     "  with no terminal — CPU OC/UV, GPU governor safe-point, fan, UMA VRAM split,\n"
     "  40-CU toggle, with *apply → benchmark → verify/rollback* tests. `skillfish-tuner`\n"
     "  is the GUI (→ `/usr/local/bin/`); `skillfish-tuner-helper` is the privileged\n"
     "  daemon (JSON-per-line over a single `pkexec`).\n",
     "- **`control-center/`** — **SkillFishOS Control Center** (PyQt6): every tool in\n"
     "  one window. Status, Tuner (the V/F governor curve with a trial countdown),\n"
     "  Fan, Monitor, Games (our Mesa, scx, FSR 4, GE-Proton), Profiles, Kernel,\n"
     "  Snapshots, AI, Emulators, Console, ISO. `skillfish-control-center` is the\n"
     "  window; `skillfish-cc-helper` is the privileged daemon (JSON-per-line over a\n"
     "  single `pkexec`). See [control-center/README.md](control-center/README.md).\n"
     "- **`tuner/`** — the old **SkillFishOS Tuner**; since 26.09 `skillfish-tuner`\n"
     "  opens the Tuner section of the Control Center. The package keeps\n"
     "  `skillfish-tuner-helper`, `skillfish-cu` and the CU boot service.\n"),
])

patch("README.md", [
    ("- **SkillFishOS Tuner** — a native **PyQt6** app to overclock & undervolt CPU and GPU, resize the UMA VRAM split, and manage **Compute Units live**",
     "- **SkillFishOS Control Center** — one native **PyQt6** window for every tool (see [docs/CONTROL-CENTER.md](docs/CONTROL-CENTER.md)): the **Tuner** section draws the V/F governor curve inside the chart and applies it *on trial* with a countdown (the old curve stays on disk until you keep the new one); **Games** switches our Mesa per launcher or system-wide, arms the scx scheduler, FSR 4, and installs GE-Proton; **Profiles** sets ceiling, CPU, fan and scheduler in one click. It also overclocks & undervolts the CPU, resizes the UMA VRAM split, and manages **Compute Units live**"),
    ("  DESKTOP.md         KDE Plasma, steampunk theme, HUD, Tuner, AI panel\n",
     "  DESKTOP.md         KDE Plasma, steampunk theme, HUD, Tuner, AI panel\n"
     "  CONTROL-CENTER.md  the one window: Tuner, Fan, Monitor, Games, Profiles, Kernel, Snapshots...\n"),
    ("apps/              native PyQt6 apps: tuner, ai-panel, iso-mount, kernel-switch, monitor, hub (+ menu)",
     "apps/              native PyQt6 apps: control-center (all tools), hub, dashboard, hud (+ the old per-tool packages)"),
])

patch("apps/control-center/README.md", [
    ("web/                          the same sections for the Remote Manager\n",
     "../dashboard/web/             the same sections for the Remote Manager\n"
     "                              (tuner.html, giochi.html, profili.html)\n"),
])
