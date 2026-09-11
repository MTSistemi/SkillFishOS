#!/usr/bin/env python3
"""Lab, 2026-09-12: the AI section grows up and the VRAM panel loses a false
ban. Run inside the repository on the board.

- helper: enable/disable without --now, unsloth-conf / unsloth-conf-set /
  unsloth-key-set;
- Tuner: VRAM presets 512 MB and 1 GB (window and web);
- skillfish-memcfg: 2048 MB is a valid split, not a known fault;
- skillfish-unsloth: --parallel from /etc/default/skillfish-unsloth;
- unit: EnvironmentFile;
- skillfish-unsloth-update: current installer URL, run from the user's home
  (uv reads uv.toml from the working directory, and /root is not readable),
  pkexec caller as the user;
- install-unsloth.sh: a thin wrapper over skillfish-unsloth-update.
"""
import os
import sys

R = sys.argv[1] if len(sys.argv) > 1 else "/root/sfx-src"


def patch(rel, coppie, tutto=False):
    p = os.path.join(R, rel)
    s = open(p, encoding="utf-8").read()
    for old, new in coppie:
        if old not in s:
            raise SystemExit("%s: blocco non trovato:\n%s" % (rel, old[:120]))
        s = s.replace(old, new) if tutto else s.replace(old, new, 1)
    open(p, "w", encoding="utf-8").write(s)
    print("ok", rel)


# ---- helper -------------------------------------------------------------------
patch("apps/control-center/skillfish-cc-helper", [
    ('    if unit not in permessi or azione not in ("enable --now", "disable --now", "start", "stop", "restart"):',
     '    if unit not in permessi or azione not in ("enable --now", "disable --now", "enable", "disable", "start", "stop", "restart"):'),
    ('''def gtt(mb):
    """The GTT limit of the AI panel goes through skillfish-gtt."""''',
     '''UNSLOTH_DEFAULT = "/etc/default/skillfish-unsloth"
UNSLOTH_KEY_DASH = "/etc/skillfish/unsloth.key"


def unsloth_conf():
    """Bind address and parallel slots of the engine, from its environment file."""
    out = {"ok": True, "bind": "127.0.0.1", "parallel": 4}
    try:
        for line in _rd(UNSLOTH_DEFAULT).splitlines():
            line = line.strip()
            if line.startswith("UNSLOTH_BIND="):
                out["bind"] = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("UNSLOTH_PARALLEL="):
                try:
                    out["parallel"] = int(line.split("=", 1)[1].strip().strip('"'))
                except ValueError:
                    pass
    except OSError:
        pass
    out["attivo"] = _unit("is-active", "skillfish-unsloth.service")
    out["abilitato"] = _unit("is-enabled", "skillfish-unsloth.service")
    return out


def unsloth_conf_set(lan, parallel):
    """Write the environment file the unit reads, restart the engine if it runs."""
    try:
        parallel = max(1, min(64, int(parallel)))
    except (TypeError, ValueError):
        parallel = 4
    bind = "0.0.0.0" if lan else "127.0.0.1"
    testo = ("# SkillFishOS: read by skillfish-unsloth.service. Written by the Control Center\\n"
             "# and the Remote Manager; edit by hand if you like, then restart the unit.\\n"
             "UNSLOTH_BIND=%s\\nUNSLOTH_PARALLEL=%d\\n" % (bind, parallel))
    try:
        with open(UNSLOTH_DEFAULT, "w") as f:
            f.write(testo)
    except OSError as e:
        return {"ok": False, "err": str(e)}
    _log("unsloth: bind %s, parallel %d" % (bind, parallel))
    if _unit("is-active", "skillfish-unsloth.service") == "active":
        sh("systemctl restart skillfish-unsloth.service", 120)
    return unsloth_conf()


def unsloth_key_set(key):
    """The copy of the API key the Remote Manager reads (root, 0600)."""
    key = (key or "").strip()
    try:
        if not key:
            if os.path.exists(UNSLOTH_KEY_DASH):
                os.remove(UNSLOTH_KEY_DASH)
            return {"ok": True}
        if not re.match(r"^sk-[A-Za-z0-9._-]{8,200}$", key):
            return {"ok": False, "err": "chiave non valida"}
        os.makedirs(os.path.dirname(UNSLOTH_KEY_DASH), exist_ok=True)
        fd = os.open(UNSLOTH_KEY_DASH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(key + "\\n")
        return {"ok": True}
    except OSError as e:
        return {"ok": False, "err": str(e)}


def gtt(mb):
    """The GTT limit of the AI panel goes through skillfish-gtt."""'''),
    ('''    if c == "gtt":
        return gtt(req.get("mb", 0))''',
     '''    if c == "gtt":
        return gtt(req.get("mb", 0))
    if c == "unsloth-conf":
        return unsloth_conf()
    if c == "unsloth-conf-set":
        return unsloth_conf_set(bool(req.get("lan")), req.get("parallel", 4))
    if c == "unsloth-key-set":
        return unsloth_key_set(req.get("key", ""))'''),
])

# ---- VRAM presets ---------------------------------------------------------------
patch("apps/control-center/sfcc/pagine/tuner.py", [
    ('''        for mb in (2048, 4096, 6144, 8192):
            b = QPushButton("%d GB" % (mb // 1024))''',
     '''        for mb, testo in ((512, "512 MB"), (1024, "1 GB"), (2048, "2 GB"), (4096, "4 GB"), (6144, "6 GB"), (8192, "8 GB")):
            b = QPushButton(testo)'''),
])
patch("apps/dashboard/web/tuner.html", [
    ('    <button class="btn sec mini" data-vram="2048">2 GB</button>',
     '    <button class="btn sec mini" data-vram="512">512 MB</button><button class="btn sec mini" data-vram="1024">1 GB</button>\n    <button class="btn sec mini" data-vram="2048">2 GB</button>'),
])
patch("system/usr/local/bin/skillfish-memcfg", [
    ("  elenca anche i valori ammessi e avverte che 2048 MB impedisce l'avvio.",
     "  elenca anche i valori ammessi."),
    ("UMA_CONFERMATI = (256, 512, 1024, 3072, 4096, 6144, 8192, 10240, 12288)\n"
     'UMA_VIETATI = {2048: "con 2048 MB il sistema non si avvia (guasto noto e documentato)"}',
     "UMA_CONFERMATI = (256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 10240, 12288)\n"
     "# 2048 MB was listed here as a known fault; it boots fine (checked on our boards).\n"
     "UMA_VIETATI = {}"),
])

# ---- the engine's launcher, unit, updater, installer -----------------------------
patch("system/usr/local/bin/skillfish-unsloth", [
    ('    "$BIN" studio -p "$PORTA" -H "$ASCOLTO" --no-cloudflare',
     '    "$BIN" studio -p "$PORTA" -H "$ASCOLTO" --parallel "${UNSLOTH_PARALLEL:-4}" --no-cloudflare'),
    ('PORTA="${UNSLOTH_PORT:-8888}"\nASCOLTO="${UNSLOTH_BIND:-127.0.0.1}"',
     '# UNSLOTH_BIND, UNSLOTH_PORT and UNSLOTH_PARALLEL come from /etc/default/skillfish-unsloth\n'
     '# (EnvironmentFile of the unit); the Control Center writes that file.\n'
     'PORTA="${UNSLOTH_PORT:-8888}"\nASCOLTO="${UNSLOTH_BIND:-127.0.0.1}"'),
])
patch("system/etc/systemd/system/skillfish-unsloth.service", [
    ("ExecStart=/usr/local/bin/skillfish-unsloth",
     "EnvironmentFile=-/etc/default/skillfish-unsloth\nExecStart=/usr/local/bin/skillfish-unsloth"),
])
patch("system/usr/local/bin/skillfish-unsloth-update", [
    ("    if [ -n \"${SUDO_USER:-}\" ] && [ \"$SUDO_USER\" != root ]; then echo \"$SUDO_USER\"; return; fi\n",
     "    if [ -n \"${SUDO_USER:-}\" ] && [ \"$SUDO_USER\" != root ]; then echo \"$SUDO_USER\"; return; fi\n"
     "    # launched through pkexec from the Control Center: the caller is the user\n"
     "    if [ -n \"${PKEXEC_UID:-}\" ] && [ \"$PKEXEC_UID\" != 0 ]; then id -un \"$PKEXEC_UID\"; return; fi\n"),
    ("sudo -u \"$U\" HOME=\"$CASA\" UNSLOTH_FORCE_VULKAN=1 \\\n    sh -c 'curl -fsSL https://install.unsloth.ai | sh' || {",
     "# ⚠️ Two things learned on 2026-09-12: install.unsloth.ai answers 404 now, the\n"
     "# installer lives at unsloth.ai/install.sh; and uv reads a uv.toml from the\n"
     "# working directory upwards, so started from /root it dies on a file it may\n"
     "# not read. The command runs from the user's home.\n"
     "sudo -u \"$U\" HOME=\"$CASA\" UNSLOTH_FORCE_VULKAN=1 \\\n    sh -c 'cd \"$HOME\" && curl -fsSL https://unsloth.ai/install.sh | sh' || {"),
])

INSTALLER = '''#!/bin/bash
# install-unsloth.sh — Unsloth Studio as the SkillFishOS on-device AI engine.
#
# Kept for the callers that still know this path (older panels, the docs). The
# work is done by skillfish-unsloth-update, which installs in the HOME OF THE
# USER (an image never ships /root), forces the Vulkan bundle of llama.cpp (the
# only GPU path on gfx1013), removes the desktop icon the installer drops and
# restarts the service so the new version really runs.
set -u
if [ -x /usr/local/bin/skillfish-unsloth-update ]; then
    exec /usr/local/bin/skillfish-unsloth-update "$@"
fi
echo "install-unsloth.sh: skillfish-unsloth-update is missing; install skillfish-ai-panel first." >&2
exit 1
'''
with open(os.path.join(R, "scripts/install-unsloth.sh"), "w", encoding="utf-8") as f:
    f.write(INSTALLER)
print("ok scripts/install-unsloth.sh")
