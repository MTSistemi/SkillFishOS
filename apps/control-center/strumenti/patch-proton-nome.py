#!/usr/bin/env python3
"""Steam calls a compatibility tool by the name written INSIDE it, not by the
name of its folder. GE-Proton11-6 unpacks into a folder called GE-Proton11-6
and declares itself as "GE-Proton11-6-x86_64".

We wrote the folder name into CompatToolMapping, so Steam looked for a tool
that does not exist, found none, and ran the .exe with no Proton at all: the
game appeared for a moment in the log and was gone. Black Myth Wukong on both
boards, and every Steam game for anyone who pressed "Default" since 26.09.1.

    patch-proton-nome.py <repo>

Both the window and the Remote Manager read the internal name from
compatibilitytool.vdf now, and both accept either name when they say which one
is the default, so a configuration written before this still reads right.
"""
import os
import re
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."

# ---------------------------------------------------------------- the window
p = os.path.join(repo, "apps", "control-center", "sfcc", "pagine", "giochi.py")
s = open(p, encoding="utf-8").read()

if "def nome_interno" not in s:
    NUOVA = '''def nome_interno(cartella, n):
    """The name Steam knows a compatibility tool by.

    ⚠️ It is NOT the name of the folder. GE-Proton11-6 sits in a folder called
    GE-Proton11-6 and declares itself "GE-Proton11-6-x86_64"; writing the
    folder name into config.vdf makes Steam find no tool and start the game's
    .exe with no Proton, which dies instantly and looks like a broken game.
    """
    try:
        with open(os.path.join(cartella, n, "compatibilitytool.vdf"), encoding="utf-8", errors="replace") as f:
            t = f.read()
        m = re.search(r'"compat_tools"\\s*\\{\\s*"([^"]+)"', t)
        if m:
            return m.group(1)
    except OSError:
        pass
    return n


def proton_installati():'''
    s = s.replace("def proton_installati():", NUOVA, 1)

# the default is written with the internal name
s = s.replace('''            if not self._steam_default(n):''',
              '''            if not self._steam_default(nome_interno(STEAM_TOOLS, n)):''', 1)

# and recognised under either name
s = s.replace('''                dove.append("Steam" + (" ★" if n == ds else ""))''',
              '''                dove.append("Steam" + (" ★" if ds in (n, nome_interno(STEAM_TOOLS, n)) else ""))''', 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok apps/control-center/sfcc/pagine/giochi.py")

# ------------------------------------------------------- the Remote Manager
p = os.path.join(repo, "apps", "dashboard", "skillfish-dashboardd")
s = open(p, encoding="utf-8").read()

if "def _cc_proton_nome_interno" not in s:
    NUOVA = '''def _cc_proton_nome_interno(dove, n):
    """The name Steam knows the tool by, read from compatibilitytool.vdf.

    ⚠️ Not the folder name: GE-Proton11-6 declares itself GE-Proton11-6-x86_64,
    and a name Steam does not know means the game starts with no Proton at all.
    """
    import re as _re
    try:
        with open(os.path.join(_cc_proton_dir(dove), n, "compatibilitytool.vdf"),
                  encoding="utf-8", errors="replace") as f:
            m = _re.search(r'"compat_tools"\\s*\\{\\s*"([^"]+)"', f.read())
        if m:
            return m.group(1)
    except OSError:
        pass
    return n


def cc_proton():'''
    s = s.replace("def cc_proton():", NUOVA, 1)
    # the listing says which one is the default: accept either name
    s = s.replace('''    out["default_steam"] = ""''',
                  '''    out["default_steam"] = ""
    out["nomi_interni"] = {d: _cc_proton_nome_interno("steam", d) for d in out.get("steam", [])}''', 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok apps/dashboard/skillfish-dashboardd")

# the writer of the default, in the dashboard: the Steam branch is what comes
# after the Heroic one returns, so the name is translated right before it
s = open(p, encoding="utf-8").read()
ANCORA = '''    try:
        aperto = "com.valvesoftware.Steam" in subprocess.run(["flatpak", "ps", "--columns=application"], capture_output=True, text=True, timeout=10).stdout'''
if ANCORA in s and "_cc_proton_nome_interno(\"steam\", nome)" not in s:
    s = s.replace(ANCORA,
                  '    # from here down it is Steam, which wants the name declared inside the tool\n'
                  '    nome = _cc_proton_nome_interno("steam", nome)\n' + ANCORA, 1)
    open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("ok cc_proton_default")
else:
    print("cc_proton_default: gia' a posto o ancora non trovata")
