#!/usr/bin/env python3
"""Teach the Remote Manager the Control Center sections: Games, Profiles, the
governor curve. Same rule as always: the web page mirrors the window.

    patch-dashboardd.py <repo>

Edits apps/dashboard/skillfish-dashboardd (backend + routes + module list),
apps/dashboard/web/app.js (two cards) and scripts/build-debs-ci.sh (the two
new pages). Idempotent.
"""
import os
import sys

repo = sys.argv[1]
D = os.path.join(repo, "apps", "dashboard", "skillfish-dashboardd")
A = os.path.join(repo, "apps", "dashboard", "web", "app.js")
CI = os.path.join(repo, "scripts", "build-debs-ci.sh")

with open(D, encoding="utf-8") as f:
    t = f.read()
if "def cc_giochi" in t:
    print("dashboardd: gia' applicato")
else:
    # 1. the helper: the Control Center one when it is there (superset)
    a = 'TUNER_HELPER = "/usr/local/bin/skillfish-tuner-helper"'
    assert a in t
    t = t.replace(a, '# ⚠️ The Control Center helper is a superset of the Tuner one (same protocol):\n'
                     '# it is preferred when installed, because only it knows the V/F governor.\n'
                     'TUNER_HELPER = ("/usr/local/bin/skillfish-cc-helper" if os.path.exists("/usr/local/bin/skillfish-cc-helper")\n'
                     '                else "/usr/local/bin/skillfish-tuner-helper")')
    # 2. the modules
    t = t.replace('    "snapshots": True,\n', '    "snapshots": True,\n    "giochi": True,\n    "profili": True,\n', 1)
    t = t.replace('    "snapshots":  {"icon": "🕒", "name": "Snapshot",       "name_en": "Snapshots"},\n',
                  '    "snapshots":  {"icon": "🕒", "name": "Snapshot",       "name_en": "Snapshots"},\n'
                  '    "giochi":     {"icon": "🎮", "name": "Giochi",         "name_en": "Games"},\n'
                  '    "profili":    {"icon": "🎚️", "name": "Profili",        "name_en": "Profiles"},\n', 1)
    # 3. the backend
    backend = r'''
# ======================= Control Center: games, profiles, governor =======================
# The window does these things on the machine; here they are done for the
# desktop user from the web. Overrides are FILES in that user's home, so they
# are written as root and handed back to the user.
CC_MESA_ICD = "/opt/skillfish-gfx1013/share/vulkan/icd.d/radeon_icd.x86_64.json"
CC_MESA_LIBS = "/opt/skillfish-gfx1013/lib/x86_64-linux-gnu"
CC_MESA_NOSTRE = ("VK_DRIVER_FILES", "LD_LIBRARY_PATH")
CC_APP = {"steam": "com.valvesoftware.Steam", "heroic": "com.heroicgameslauncher.hgl"}
CC_FSR4 = ("PROTON_USE_OPTISCALER", "PROTON_FSR4_UPGRADE")
CC_PROFILI_SISTEMA = "/usr/share/skillfish/profili.json"
CC_CURVA_PREDEFINITA = "/usr/share/skillfish/vf-curva-predefinita.json"
CC_PRESET_VENTOLA = {
    "silenzioso": [[45, 20], [60, 30], [70, 45], [80, 70], [88, 100]],
    "equilibrato": [[40, 30], [55, 40], [65, 60], [75, 85], [85, 100]],
    "prestazioni": [[35, 40], [50, 60], [60, 80], [70, 100], [85, 100]],
    "massimo": [[0, 100], [100, 100]],
}


def _cc_utente():
    import pwd
    u = CONFIG.get("user", "skillfish")
    try:
        p = pwd.getpwnam(u)
        return p.pw_uid, p.pw_gid, p.pw_dir
    except Exception:
        return None, None, "/home/" + u


def _cc_override(app):
    import configparser
    c = configparser.RawConfigParser()
    c.optionxform = str
    c.read(os.path.join(user_home(), ".local/share/flatpak/overrides", CC_APP[app]))
    for s in ("Context", "Environment"):
        if not c.has_section(s):
            c.add_section(s)
    return c


def _cc_override_scrivi(app, c):
    uid, gid, casa = _cc_utente()
    cartella = os.path.join(casa, ".local/share/flatpak/overrides")
    os.makedirs(cartella, exist_ok=True)
    percorso = os.path.join(cartella, CC_APP[app])
    with open(percorso, "w", encoding="utf-8", newline="\n") as fh:
        c.write(fh, space_around_delimiters=False)
    if uid is not None:
        try:
            os.chown(percorso, uid, gid)
            os.chown(cartella, uid, gid)
        except OSError:
            pass


def _cc_pulisci_unset(c, nomi):
    v = c.get("Context", "unset-environment", fallback="")
    resto = [x for x in v.split(";") if x and x not in nomi]
    if resto:
        c.set("Context", "unset-environment", ";".join(resto) + ";")
    elif c.has_option("Context", "unset-environment"):
        c.remove_option("Context", "unset-environment")


def cc_mesa_stato(app):
    c = _cc_override(app)
    return (c.get("Environment", "VK_DRIVER_FILES", fallback=None) == CC_MESA_ICD
            and "VK_DRIVER_FILES" not in c.get("Context", "unset-environment", fallback=""))


def cc_mesa_set(app, on):
    if app not in CC_APP:
        return {"ok": False, "err": "app sconosciuta"}
    if on and not os.path.exists(CC_MESA_ICD):
        return {"ok": False, "err": "la nostra Mesa non e' installata"}
    c = _cc_override(app)
    _cc_pulisci_unset(c, CC_MESA_NOSTRE)
    if on:
        v = c.get("Context", "filesystems", fallback="")
        voci = [x for x in v.split(";") if x]
        if "/opt/skillfish-gfx1013:ro" not in voci:
            voci.append("/opt/skillfish-gfx1013:ro")
        c.set("Context", "filesystems", ";".join(voci) + ";")
        c.set("Environment", "VK_DRIVER_FILES", CC_MESA_ICD)
        c.set("Environment", "LD_LIBRARY_PATH", CC_MESA_LIBS)
    else:
        for n in CC_MESA_NOSTRE:
            if c.has_option("Environment", n):
                c.remove_option("Environment", n)
    _cc_override_scrivi(app, c)
    return {"ok": True, "on": bool(on)}


def cc_fsr4_stato(app):
    c = _cc_override(app)
    return all(c.get("Environment", k, fallback="") == "1" for k in CC_FSR4)


def cc_fsr4_set(app, on):
    if app not in CC_APP:
        return {"ok": False, "err": "app sconosciuta"}
    c = _cc_override(app)
    _cc_pulisci_unset(c, CC_FSR4)
    for k in CC_FSR4:
        if on:
            c.set("Environment", k, "1")
        elif c.has_option("Environment", k):
            c.remove_option("Environment", k)
    _cc_override_scrivi(app, c)
    return {"ok": True, "on": bool(on)}


def _cc_proton_dir(dove):
    casa = user_home()
    return (os.path.join(casa, ".var/app/com.valvesoftware.Steam/data/Steam/compatibilitytools.d") if dove == "steam"
            else os.path.join(casa, ".var/app/com.heroicgameslauncher.hgl/config/heroic/tools/proton"))


def cc_proton():
    import re as _re
    out = {}
    for dove in ("steam", "heroic"):
        try:
            out[dove] = sorted(d for d in os.listdir(_cc_proton_dir(dove)) if os.path.isdir(os.path.join(_cc_proton_dir(dove), d)))
        except OSError:
            out[dove] = []
    out["default_heroic"] = ""
    try:
        with open(os.path.join(user_home(), ".var/app/com.heroicgameslauncher.hgl/config/heroic/config.json")) as f:
            out["default_heroic"] = (json.load(f).get("defaultSettings", {}).get("wineVersion") or {}).get("name", "")
    except Exception:
        pass
    out["default_steam"] = ""
    try:
        with open(os.path.join(user_home(), ".var/app/com.valvesoftware.Steam/data/Steam/config/config.vdf"), encoding="utf-8", errors="replace") as f:
            m = _re.search(r'"CompatToolMapping"\s*\{(.*?)\n\t{4}\}', f.read(), _re.S)
        if m:
            z = _re.search(r'"0"\s*\{[^}]*?"name"\s*"([^"]*)"', m.group(1), _re.S)
            if z:
                out["default_steam"] = z.group(1)
    except Exception:
        pass
    return out


def cc_proton_default(dove, nome):
    import re as _re
    import shutil as _sh
    nome = (nome or "").strip()
    if dove not in ("steam", "heroic") or not _re.match(r"^[A-Za-z0-9._-]+$", nome):
        return {"ok": False, "err": "richiesta non valida"}
    if nome not in cc_proton().get(dove, []):
        return {"ok": False, "err": "non installata in %s" % dove}
    uid, gid, casa = _cc_utente()
    if dove == "heroic":
        p = os.path.join(casa, ".var/app/com.heroicgameslauncher.hgl/config/heroic/config.json")
        try:
            with open(p) as f:
                d = json.load(f)
            d.setdefault("defaultSettings", {})["wineVersion"] = {
                "bin": os.path.join(_cc_proton_dir("heroic"), nome, "proton"), "name": nome, "type": "proton"}
            with open(p, "w") as f:
                json.dump(d, f, indent=2)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "err": str(e)}
    try:
        aperto = "com.valvesoftware.Steam" in subprocess.run(["flatpak", "ps", "--columns=application"], capture_output=True, text=True, timeout=10).stdout
    except Exception:
        aperto = False
    if aperto:
        return {"ok": False, "err": "chiudi Steam prima: riscrive la configurazione all'uscita"}
    p = os.path.join(casa, ".var/app/com.valvesoftware.Steam/data/Steam/config/config.vdf")
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            t = f.read()
    except OSError:
        return {"ok": False, "err": "config.vdf non trovato"}
    voce = '"0"\n\t\t\t\t\t{\n\t\t\t\t\t\t"name"\t\t"%s"\n\t\t\t\t\t\t"config"\t\t""\n\t\t\t\t\t\t"priority"\t\t"75"\n\t\t\t\t\t}' % nome
    m = _re.search(r'"CompatToolMapping"\s*\{', t)
    if m:
        z = _re.search(r'"0"\s*\{[^}]*\}', t[m.end():], _re.S)
        if z and z.start() < 400:
            t = t[:m.end() + z.start()] + voce + t[m.end() + z.end():]
        else:
            t = t[:m.end()] + "\n\t\t\t\t\t" + voce + t[m.end():]
    else:
        s = _re.search(r'"Steam"\s*\{', t)
        if not s:
            return {"ok": False, "err": "config.vdf senza blocco Steam"}
        t = t[:s.end()] + '\n\t\t\t\t"CompatToolMapping"\n\t\t\t\t{\n\t\t\t\t\t' + voce + "\n\t\t\t\t}" + t[s.end():]
    _sh.copy2(p, p + ".skillfish.bak")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    return {"ok": True}


def cc_giochi():
    return {"ok": True,
            "mesa": {a: cc_mesa_stato(a) for a in CC_APP},
            "mesa_sistema": tuner_cmd([{"cmd": "mesa-sistema"}]),
            "scx": tuner_cmd([{"cmd": "scx"}]),
            "fsr4": {a: cc_fsr4_stato(a) for a in CC_APP},
            "proton": cc_proton()}


def cc_gov():
    r = tuner_cmd([{"cmd": "gov-get"}])
    try:
        for h in os.listdir("/sys/class/hwmon"):
            p = "/sys/class/hwmon/" + h
            if open(p + "/name").read().strip() == "amdgpu":
                r["mv"] = int(open(p + "/in0_input").read().strip())
                break
    except Exception:
        pass
    try:
        with open(CC_CURVA_PREDEFINITA) as f:
            r["predefinita"] = json.load(f)
    except Exception:
        r["predefinita"] = {}
    return r


def cc_gov_post(data):
    az = data.get("azione")
    if az == "attiva":
        return tuner_cmd([{"cmd": "gov-attiva", "on": bool(data.get("on", True))}], timeout=90)
    if az in ("set", "prova"):
        return tuner_cmd([{"cmd": "gov-" + az, "conf": data.get("conf") or {}}], timeout=90)
    if az in ("conferma", "annulla"):
        return tuner_cmd([{"cmd": "gov-" + az}], timeout=90)
    return {"ok": False, "err": "azione sconosciuta"}


def _cc_conf_governor():
    try:
        with open("/etc/skillfish-vf-governor.json") as f:
            return json.load(f)
    except Exception:
        return {}


def cc_profili():
    import re as _re
    profili = {}
    for p in (CC_PROFILI_SISTEMA, os.path.join(user_home(), ".config/skillfish/profili.json")):
        try:
            with open(p) as f:
                d = json.load(f)
            if isinstance(d, dict):
                profili.update(d)
        except Exception:
            pass
    g = _cc_conf_governor()
    fan = ventola_conf() or {}
    m = None
    try:
        m = _re.search(r"frequency\s*=\s*(\d+)", open("/etc/bc250-smu-oc.conf").read())
    except Exception:
        pass
    scx_on = subprocess.run(["systemctl", "is-enabled", "skillfish-scx.path"], capture_output=True, text=True).stdout.strip() == "enabled"
    stato = {"tetto": int(g.get("freq_max", 0) or 0), "cpu": int(m.group(1)) if m else 0,
             "ventola": fan.get("preset", ""), "scx": scx_on}
    attivo = None
    for k, p in profili.items():
        if (stato["tetto"] == p.get("tetto") and stato["ventola"] == p.get("ventola")
                and stato["scx"] == bool(p.get("scx")) and (not p.get("cpu") or stato["cpu"] == p.get("cpu"))):
            attivo = k
    return {"ok": True, "profili": profili, "stato": stato, "attivo": attivo}


def cc_profilo_applica(chiave):
    import re as _re
    p = cc_profili()["profili"].get(chiave)
    if not p:
        return {"ok": False, "err": "profilo sconosciuto"}
    errori = []
    g = _cc_conf_governor()
    pts = g.get("curva") or []
    if pts and p.get("tetto"):
        g["freq_max"] = max(pts[0][0], min(pts[-1][0], int(p["tetto"])))
        r = tuner_cmd([{"cmd": "gov-set", "conf": g}], timeout=90)
        if not r.get("ok"):
            errori.append("GPU: " + str(r.get("err", "?")))
    if p.get("cpu"):
        try:
            t = open("/etc/bc250-smu-oc.conf").read()
        except Exception:
            t = ""
        sc = _re.search(r"scale\s*=\s*(-?\d+)", t)
        tp = _re.search(r"max_temperature\s*=\s*(\d+)", t)
        r = tuner_cmd([{"cmd": "apply-cpu", "mhz": int(p["cpu"]), "scale": int(sc.group(1)) if sc else 0,
                        "temp": int(tp.group(1)) if tp else 85}], timeout=90)
        if not r.get("ok"):
            errori.append("CPU: " + str(r.get("err", "?")))
    if p.get("ventola") in CC_PRESET_VENTOLA:
        c = ventola_conf() or {}
        if c.get("pwm") and c.get("sorgente"):
            c["curva"] = CC_PRESET_VENTOLA[p["ventola"]]
            c["preset"] = p["ventola"]
            c["attivo"] = True
            r = ventola_scrivi(c)
            if not r.get("ok"):
                errori.append("ventola: " + str(r.get("error", r.get("err", "?"))))
        else:
            errori.append("ventola: configurala prima una volta dalla sua pagina")
    if "scx" in p:
        r = tuner_cmd([{"cmd": "scx-set", "on": bool(p["scx"])}], timeout=60)
        if not r.get("ok") and bool(p["scx"]):
            errori.append("scx: " + str(r.get("err", "?")))
    return {"ok": not errori, "err": "; ".join(errori), "profilo": chiave}


'''
    a = "def launch_app(cmd):"
    assert a in t
    t = t.replace(a, backend + a, 1)
    # 4. GET routes
    get_routes = '''        if path == "/api/tuner/gov":
            if not self._guard("tuner"):
                return
            return self._json(200, cc_gov())
        if path == "/api/giochi":
            if not self._guard("giochi"):
                return
            return self._json(200, cc_giochi())
        if path == "/api/profili":
            if not self._guard("profili"):
                return
            return self._json(200, cc_profili())
'''
    a = '        if path == "/api/snapshots":\n            if not self._guard("snapshots"):\n                return\n            return self._json(200, snapshots_leggi())'
    assert a in t
    t = t.replace(a, get_routes + a, 1)
    # 5. POST routes
    post_routes = '''        if path == "/api/tuner/gov":
            if not self._guard("tuner"):
                return
            return self._json(200, cc_gov_post(data))
        if path == "/api/giochi/mesa":
            if not self._guard("giochi"):
                return
            return self._json(200, cc_mesa_set(data.get("app"), bool(data.get("on"))))
        if path == "/api/giochi/mesa-sistema":
            if not self._guard("giochi"):
                return
            return self._json(200, tuner_cmd([{"cmd": "mesa-sistema-set", "on": bool(data.get("on"))}], timeout=60))
        if path == "/api/giochi/scx-azzera":
            if not self._guard("giochi"):
                return
            return self._json(200, tuner_cmd([{"cmd": "scx-azzera"}]))
        if path == "/api/giochi/fsr4":
            if not self._guard("giochi"):
                return
            return self._json(200, cc_fsr4_set(data.get("app"), bool(data.get("on"))))
        if path == "/api/giochi/proton-default":
            if not self._guard("giochi"):
                return
            return self._json(200, cc_proton_default(data.get("dove"), data.get("nome")))
        if path == "/api/profili":
            if not self._guard("profili"):
                return
            return self._json(200, cc_profilo_applica(data.get("chiave")))
'''
    a = '        if path == "/api/hub/op":'
    assert a in t
    t = t.replace(a, post_routes + a, 1)
    with open(D, "w", encoding="utf-8") as f:
        f.write(t)
    print("dashboardd: patch applicata")

# ---- app.js: the two cards ----------------------------------------------------
with open(A, encoding="utf-8") as f:
    j = f.read()
if "async giochi(card)" in j:
    print("app.js: gia' applicato")
else:
    cards = r'''  async giochi(card) {
    // Giochi: driver, schedulatore, Proton. La scheda mostra lo stato e apre
    // la pagina vera, come fanno Ventola e Snapshot.
    const it = LANG === "it";
    card.innerHTML = "<h3>🎮 " + (it ? "Giochi" : "Games") + '</h3><div id="gk">…</div>';
    let d = {};
    try { d = await (await api("/api/giochi")).json(); } catch (e) {}
    const m = d.mesa || {}, ms = d.mesa_sistema || {}, x = d.scx || {};
    const dove = [m.steam && "Steam", m.heroic && "Heroic", ms.attivo && (it ? "sistema" : "system")].filter(Boolean);
    const row = (a, b) => `<div class="r"><span>${a}</span><span>${b || "–"}</span></div>`;
    $("#gk", card).innerHTML = '<div class="rows">' +
      row(it ? "Driver nostro" : "Our driver", dove.length ? dove.join(", ") : (it ? "di serie" : "stock")) +
      row(it ? "Schedulatore" : "Scheduler", x.caricato ? (it ? "caricato" : "loaded") : (x.abilitato ? (it ? "armato" : "armed") : (it ? "spento" : "off"))) +
      row("Proton", ((d.proton || {}).default_heroic || "–")) + "</div>" +
      '<div class="brow"><button class="dbtn" id="opengiochi" style="border-color:var(--gold)">🎮 ' + (it ? "Apri" : "Open") + "</button></div>";
    $("#opengiochi", card).onclick = () => openFrame("SkillFishOS " + (it ? "Giochi" : "Games"), "/static/giochi.html");
  },
  async profili(card) {
    // Profili: un bottone per profilo, come nella finestra.
    const it = LANG === "it";
    card.innerHTML = "<h3>🎚️ " + (it ? "Profili" : "Profiles") + '</h3><div id="pk">…</div>';
    let d = {};
    try { d = await (await api("/api/profili")).json(); } catch (e) {}
    const btns = Object.entries(d.profili || {}).map(([k, p]) => `<button class="dbtn" data-prof="${k}" ${d.attivo === k ? 'style="border-color:var(--gold)"' : ""}>${(it ? p.nome_it : p.nome_en) || k}</button>`).join("");
    $("#pk", card).innerHTML = '<div class="brow">' + btns + '</div>' +
      '<div class="brow" style="margin-top:8px"><button class="dbtn" id="openprofili">' + (it ? "Apri" : "Open") + "</button></div>";
    card.querySelectorAll("[data-prof]").forEach(b => b.onclick = async () => { await action("/api/profili", { chiave: b.dataset.prof }, (it ? "Profilo applicato: " : "Profile applied: ") + b.textContent); });
    $("#openprofili", card).onclick = () => openFrame("SkillFishOS " + (it ? "Profili" : "Profiles"), "/static/profili.html");
  },
'''
    a = "  async ventola(card) {"
    assert a in j
    j = j.replace(a, cards + a, 1)
    with open(A, "w", encoding="utf-8") as f:
        f.write(j)
    print("app.js: patch applicata")

# ---- the CI script: the two pages ------------------------------------------------
with open(CI, encoding="utf-8") as f:
    c = f.read()
if "web/giochi.html" in c:
    print("ci: gia' applicato")
else:
    a = "put $P 0644 apps/dashboard/web/tuner.html  usr/share/skillfish/dashboard/tuner.html\n"
    assert a in c
    c = c.replace(a, a + "# the Control Center sections, mirrored on the web\nput $P 0644 apps/dashboard/web/giochi.html usr/share/skillfish/dashboard/giochi.html\nput $P 0644 apps/dashboard/web/profili.html usr/share/skillfish/dashboard/profili.html\n", 1)
    with open(CI, "w", encoding="utf-8") as f:
        f.write(c)
    print("ci: patch applicata")
