#!/usr/bin/env python3
"""Rewrite scripts/build-debs-ci.sh for the Control Center.

    patch-ci.py <repo>

What changes, and why:
- a new package, skillfish-control-center: the window, its helper, the polkit
  policy, the desktop file, the AppStream card, the icons, the profiles.
- the six old window packages (tuner, fan, monitor, kernel-manager, ai-panel,
  snapshots) keep their daemons and helpers and lose the window: the command
  becomes a launcher that opens the right section, the .desktop and the
  AppStream card go away (one entry in the menu and in the Hub, not seven),
  and each of them depends on skillfish-control-center so an upgrade brings it.
- the checks at the end that looked inside the old windows are replaced by
  checks on the new one.
Idempotent: running it twice changes nothing the second time.
"""
import os
import re
import sys

repo = sys.argv[1]
p = os.path.join(repo, "scripts", "build-debs-ci.sh")
t = open(p, encoding="utf-8").read()
orig = t
if "P=skillfish-control-center" in t:
    print("gia' applicato")
    sys.exit(0)

# ---- 1. the old windows become launchers -----------------------------------
sostituzioni = {
    "put $P 0755 apps/tuner/skillfish-tuner            usr/local/bin/skillfish-tuner":
        "# The window is a section of the Control Center since 26.09: this is the launcher.\nput $P 0755 apps/control-center/lanciatori/skillfish-tuner usr/local/bin/skillfish-tuner",
    "put $P 0755 apps/fan/skillfish-fan               usr/local/bin/skillfish-fan":
        "put $P 0755 apps/control-center/lanciatori/skillfish-fan usr/local/bin/skillfish-fan",
    "put $P 0755 apps/monitor/skillfish-monitor usr/local/bin/skillfish-monitor":
        "put $P 0755 apps/control-center/lanciatori/skillfish-monitor usr/local/bin/skillfish-monitor",
    "put $P 0755 apps/kernel-manager/skillfish-kernel-manager usr/local/bin/skillfish-kernel-manager":
        "put $P 0755 apps/control-center/lanciatori/skillfish-kernel-manager usr/local/bin/skillfish-kernel-manager",
    "put $P 0755 apps/ai-panel/skillfish-ai-panel usr/local/bin/skillfish-ai-panel":
        "put $P 0755 apps/control-center/lanciatori/skillfish-ai-panel usr/local/bin/skillfish-ai-panel",
    "put $P 0755 apps/snapshots/skillfish-snapshots        usr/local/bin/skillfish-snapshots":
        "put $P 0755 apps/control-center/lanciatori/skillfish-snapshots usr/local/bin/skillfish-snapshots",
}
for a, b in sostituzioni.items():
    if a not in t:
        sys.exit("non trovo: " + a)
    t = t.replace(a, b)

# ---- 2. no more .desktop and AppStream card for the old windows --------------
via = [
    "put $P 0644 system/usr/share/applications/os.skillfish.Tuner.desktop usr/share/applications/os.skillfish.Tuner.desktop\n",
    "shot $P apps/tuner/os.skillfish.Tuner.metainfo.xml\n",
    "put $P 0644 system/usr/share/applications/os.skillfish.fan.desktop usr/share/applications/os.skillfish.fan.desktop\n",
    "shot $P apps/fan/os.skillfish.fan.metainfo.xml\n",
    "put $P 0644 system/usr/share/applications/os.skillfish.monitor.desktop usr/share/applications/os.skillfish.monitor.desktop\n",
    "shot $P apps/monitor/os.skillfish.monitor.metainfo.xml\n",
    "put $P 0644 system/usr/share/mime/packages/os.skillfish.monitor.xml usr/share/mime/packages/os.skillfish.monitor.xml\n",
    "put $P 0644 system/usr/share/applications/os.skillfish.kernel.desktop usr/share/applications/os.skillfish.kernel.desktop\n",
    "shot $P apps/kernel-manager/os.skillfish.kernel.metainfo.xml\n",
    "put $P 0644 system/usr/share/applications/os.skillfish.ai.desktop usr/share/applications/os.skillfish.ai.desktop\n",
    "shot $P apps/ai-panel/os.skillfish.ai.metainfo.xml\n",
    "shot $P apps/snapshots/os.skillfish.snapshots.metainfo.xml\n",
    "put $P 0644 system/usr/share/applications/os.skillfish.snapshots.desktop usr/share/applications/os.skillfish.snapshots.desktop\n",
]
for r in via:
    if r not in t:
        sys.exit("non trovo: " + r.strip())
    t = t.replace(r, "")

# ---- 3. the old packages depend on the Control Center -----------------------
def dipende(nome, extra="skillfish-control-center"):
    global t
    m = re.search(r'ctrl %s "([^"]*)"' % re.escape(nome), t)
    if not m:
        sys.exit("ctrl non trovato per " + nome)
    deps = m.group(1)
    if extra not in deps:
        t = t.replace(m.group(0), 'ctrl %s "%s, %s"' % (nome, deps, extra) if deps else 'ctrl %s "%s"' % (nome, extra))

# the ctrl lines use $P, so resolve them by position: patch the first ctrl after each P=
for pkg in ("skillfish-tuner", "skillfish-fan", "skillfish-monitor", "skillfish-kernel-manager",
            "skillfish-ai-panel", "skillfish-snapshots"):
    i = t.index("P=%s\n" % pkg)
    j = t.index('ctrl $P "', i)
    k = t.index('"', j + 9)
    deps = t[j + 9:k]
    if "skillfish-control-center" not in deps:
        nuovi = (deps + ", skillfish-control-center") if deps else "skillfish-control-center"
        t = t[:j + 9] + nuovi + t[k:]

# ---- 4. the new package, before skillfish-hub ---------------------------------
blocco = r'''P=skillfish-control-center
# One window for every tool. The old ones (tuner, fan, monitor, kernel-manager,
# ai-panel, snapshots) keep their daemons and helpers and depend on this.
put $P 0755 apps/control-center/skillfish-control-center usr/local/bin/skillfish-control-center
# ⚠️ ONE privileged helper for the whole window, superset of the old tuner
# helper (same JSON-per-line protocol, so the Remote Manager keeps working).
put $P 0755 apps/control-center/skillfish-cc-helper usr/local/bin/skillfish-cc-helper
put $P 0644 apps/control-center/os.skillfish.control-center.policy usr/share/polkit-1/actions/os.skillfish.control-center.policy
# the program itself: a Python package under /usr/share/skillfish/control-center
while IFS= read -r f; do
  put $P 0644 "apps/control-center/sfcc/$f" "usr/share/skillfish/control-center/sfcc/$f"
done < <(cd apps/control-center/sfcc && find . -name '*.py' -printf '%P\n')
put $P 0644 apps/control-center/os.skillfish.control-center.desktop usr/share/applications/os.skillfish.control-center.desktop
# the .sfmon recordings of the Monitor open here now
put $P 0644 system/usr/share/mime/packages/os.skillfish.monitor.xml usr/share/mime/packages/os.skillfish.monitor.xml
put $P 0644 apps/control-center/profili.json usr/share/skillfish/profili.json
# the shipped governor curve, for the «Measured» preset: a copy of the
# governor's conffile as it is packaged
put $P 0644 packages/skillfish-vf-governor/etc/skillfish-vf-governor.json usr/share/skillfish/vf-curva-predefinita.json
for n in skillfish-control-center skillfish-giochi skillfish-profili; do
  put $P 0644 system/usr/share/icons/hicolor/scalable/apps/$n.svg usr/share/icons/hicolor/scalable/apps/$n.svg
  for s in 48 128 256; do
    put $P 0644 system/usr/share/icons/hicolor/${s}x${s}/apps/$n.png usr/share/icons/hicolor/${s}x${s}/apps/$n.png
  done
done
shot $P apps/control-center/os.skillfish.control-center.metainfo.xml
ctrl $P "python3, python3-pyqt6, polkitd | policykit-1, skillfish-base, skillfish-vf-governor" "SkillFishOS Control Center - every tool in one window" \
  "Status, Tuner, Fan, Monitor, Games, Profiles, Kernel, Snapshots, AI, Emulators,
Console and ISO in one window. The Tuner is built around the V/F governor
curve, with a trial countdown; Games switches our Mesa and installs GE-Proton."
# the daemons and helpers the sections talk to: recommended, not required, so
# a machine that is not a BC-250 can leave the hardware ones out
sed -i 's/^Depends: .*/&\nRecommends: skillfish-tuner, skillfish-fan, skillfish-monitor, skillfish-kernel-manager, skillfish-snapshots, skillfish-ai-panel, skillfish-emulators, skillfish-console, skillfish-iso-mount, skillfish-scx, skillfish-mesa-gfx1013/' "$OUT/$P/DEBIAN/control"
# the .sfmon mime type moved here from skillfish-monitor: without this dpkg
# refuses to unpack over the old monitor package ("trying to overwrite")
sed -i 's/^Depends: .*/&\nReplaces: skillfish-monitor (<< 26.09)\nBreaks: skillfish-monitor (<< 26.09)/' "$OUT/$P/DEBIAN/control"
printf '#!/bin/sh\nset -e\nupdate-desktop-database -q 2>/dev/null || true\ngtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || true\nupdate-mime-database /usr/share/mime >/dev/null 2>&1 || true\nappstreamcli refresh-cache --force >/dev/null 2>&1 || true\nexit 0\n' > "$OUT/$P/DEBIAN/postinst"
chmod 0755 "$OUT/$P/DEBIAN/postinst"

'''
t = t.replace("P=skillfish-hub\n", blocco + "P=skillfish-hub\n", 1)

# ---- 5. the build loop ----------------------------------------------------------
t = t.replace("for P in skillfish-tuner skillfish-fan skillfish-hub", "for P in skillfish-control-center skillfish-tuner skillfish-fan skillfish-hub", 1)

# ---- 6. the checks: drop the ones that read the old windows, add ours ------------
righe = t.split("\n")
out = []
via_check = ("./usr/local/bin/skillfish-tuner ", "./usr/local/bin/skillfish-tuner\t", "./usr/local/bin/skillfish-tuner  ",
             "./usr/local/bin/skillfish-ai-panel ", "./usr/local/bin/skillfish-ai-panel\t",
             "./usr/local/bin/skillfish-kernel-manager ", "./usr/local/bin/skillfish-monitor ",
             "./usr/local/bin/skillfish-snapshots ", "./usr/local/bin/skillfish-snapshots\t",
             "os.skillfish.fan.desktop", "os.skillfish.Tuner.desktop", "os.skillfish.monitor.desktop",
             "os.skillfish.kernel.desktop", "os.skillfish.ai.desktop", "os.skillfish.snapshots.desktop")
for r in righe:
    if r.startswith(("check ", "notcheck ")) and any(v in r for v in via_check):
        continue
    out.append(r)
t = "\n".join(out)
nuovi = '''
# THE CONTROL CENTER. The helper must ask for the password like the Tuner did,
# the trial must exist (a curve applied without one hangs boards), and the
# divert of the system Mesa must go somewhere ldconfig does not look.
check skillfish-control-center_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.control-center.policy '<allow_active>auth_admin_keep</allow_active>'
notcheck skillfish-control-center_${VER}_all.deb ./usr/share/polkit-1/actions/os.skillfish.control-center.policy '<allow_any>yes</allow_any>'
check skillfish-control-center_${VER}_all.deb ./usr/local/bin/skillfish-cc-helper 'gov-prova'
check skillfish-control-center_${VER}_all.deb ./usr/local/bin/skillfish-cc-helper 'reset-failed'
check skillfish-control-center_${VER}_all.deb ./usr/local/bin/skillfish-cc-helper '/var/lib/skillfish/mesa-distrib'
check skillfish-control-center_${VER}_all.deb ./usr/share/skillfish/control-center/sfcc/pagine/tuner.py 'ProvaCurva'
check skillfish-control-center_${VER}_all.deb ./usr/share/applications/os.skillfish.control-center.desktop 'StartupWMClass=os.skillfish.control-center'
check skillfish-control-center_${VER}_all.deb ./usr/share/icons/hicolor/scalable/apps/skillfish-control-center.svg '<svg'
# the old commands still work: they open the right section
check skillfish-tuner_${VER}_all.deb ./usr/local/bin/skillfish-tuner 'pagina tuner'
check skillfish-fan_${VER}_all.deb ./usr/local/bin/skillfish-fan 'pagina ventola'
check skillfish-monitor_${VER}_all.deb ./usr/local/bin/skillfish-monitor 'pagina monitor'
check skillfish-kernel-manager_${VER}_all.deb ./usr/local/bin/skillfish-kernel-manager 'pagina kernel'
check skillfish-snapshots_${VER}_all.deb ./usr/local/bin/skillfish-snapshots 'pagina snapshots'
check skillfish-ai-panel_${VER}_all.deb ./usr/local/bin/skillfish-ai-panel 'pagina ai'
'''
t = t.replace('\necho "\nALL DEBS VERIFIED"', nuovi + '\necho "\nALL DEBS VERIFIED"', 1)
open(p, "w", encoding="utf-8").write(t)
print("patch applicata: %+d righe" % (t.count("\n") - orig.count("\n")))
