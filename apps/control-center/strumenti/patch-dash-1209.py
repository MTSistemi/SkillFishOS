#!/usr/bin/env python3
"""Lab, 2026-09-12: the Remote Manager's AI card follows the Control Center
(rule: an application and its web page move together).

- the first-sign-in password is read from the HOME OF THE USER, not /root;
- /api/ai carries version, update availability, backend, bind and slots;
- new routes: update (start + log), conf (LAN, slots, autostart), setup
  (first sign-in done for the user), keycreate, variants, download, downloads;
- app.js: the card shows all of it.
"""
import os
import sys

R = sys.argv[1] if len(sys.argv) > 1 else "/root/sfx-src"


def patch(rel, coppie):
    p = os.path.join(R, rel)
    s = open(p, encoding="utf-8").read()
    for old, new in coppie:
        if old not in s:
            raise SystemExit("%s: blocco non trovato:\n%s" % (rel, old[:160]))
        s = s.replace(old, new, 1)
    open(p, "w", encoding="utf-8").write(s)
    print("ok", rel)


D = "apps/dashboard/skillfish-dashboardd"

FUNZIONI = r'''

# ---- Unsloth Studio through its own API -----------------------------------------
UNSLOTH_DEFAULT_F = "/etc/default/skillfish-unsloth"
UNSLOTH_UPDATE_BIN = "/usr/local/bin/skillfish-unsloth-update"


def _unsloth_home():
    """The home of the user Unsloth is installed for: the dashboard user, else
    the owner of the graphical session, else the first real user with ~/.unsloth."""
    import pwd
    candidati = [CONFIG.get("user") or ""]
    try:
        out = subprocess.run(["loginctl", "list-sessions", "--no-legend"], capture_output=True,
                             text=True, timeout=5).stdout
        candidati += [ln.split()[2] for ln in out.splitlines() if len(ln.split()) > 2]
    except Exception:
        pass
    candidati += [p.pw_name for p in pwd.getpwall() if 1000 <= p.pw_uid < 65534]
    for u in candidati:
        if not u or u == "root":
            continue
        try:
            h = pwd.getpwnam(u).pw_dir
        except KeyError:
            continue
        if os.path.isdir(os.path.join(h, ".unsloth")):
            return h
    return ""


def _unsloth_bootstrap():
    h = _unsloth_home()
    return os.path.join(h, ".unsloth", "studio", "auth", ".bootstrap_password") if h else UNSLOTH_BOOTSTRAP


def _studio(path, data=None, key=None, t=8, method=None):
    """One call to Studio's API; JSON in, JSON out, None when unreachable."""
    hdr = {"Accept": "application/json"}
    if key:
        hdr["Authorization"] = "Bearer " + key
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        hdr["Content-Type"] = "application/json"
    req = urllib.request.Request("http://127.0.0.1:%d%s" % (UNSLOTH_PORT, path), data=body, headers=hdr,
                                 method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(req, timeout=t) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return {"_error": e.code, **json.loads(e.read().decode())}
        except Exception:
            return {"_error": e.code}
    except Exception:
        return None


_AI_VER = {"t": 0.0, "v": {}}


def _unsloth_version():
    """Version, latest and backend, from Studio when the key allows it; cached
    ten minutes because the update check goes to the network."""
    key = _unsloth_key()
    if not key or not _port_open(UNSLOTH_PORT):
        return {}
    if time.time() - _AI_VER["t"] < 600 and _AI_VER["v"]:
        return _AI_VER["v"]
    agg = _studio("/api/studio/update-status", key=key, t=10) or {}
    be = _studio("/api/llama/backend", key=key, t=6) or {}
    v = {}
    if agg.get("current_version"):
        v = {"version": agg.get("current_version"), "latest": agg.get("latest_version"),
             "update_available": bool(agg.get("update_available")),
             "backend": (be.get("backend") or "") + ((" " + be["installed_tag"]) if be.get("installed_tag") else "")}
        _AI_VER.update(t=time.time(), v=v)
    return v


def _unsloth_conf_read():
    out = {"bind": "127.0.0.1", "parallel": 4}
    try:
        with open(UNSLOTH_DEFAULT_F) as f:
            for line in f:
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
    out["lan"] = out["bind"] not in ("127.0.0.1", "localhost", "::1")
    r = subprocess.run(["systemctl", "is-enabled", UNSLOTH_SVC], capture_output=True, text=True)
    out["autostart"] = r.stdout.strip() == "enabled"
    return out


def ai_conf():
    return {"ok": True, **_unsloth_conf_read()}


def ai_conf_set(d):
    cur = _unsloth_conf_read()
    lan = bool(d.get("lan", cur["lan"]))
    try:
        parallel = max(1, min(64, int(d.get("parallel", cur["parallel"]))))
    except (TypeError, ValueError):
        parallel = cur["parallel"]
    try:
        with open(UNSLOTH_DEFAULT_F, "w") as f:
            f.write("# SkillFishOS: read by skillfish-unsloth.service. Written by the Control Center\n"
                    "# and the Remote Manager; edit by hand if you like, then restart the unit.\n"
                    "UNSLOTH_BIND=%s\nUNSLOTH_PARALLEL=%d\n" % ("0.0.0.0" if lan else "127.0.0.1", parallel))
    except OSError as e:
        return {"ok": False, "error": str(e)}
    if "autostart" in d:
        subprocess.run(["systemctl", "enable" if d["autostart"] else "disable", UNSLOTH_SVC],
                       capture_output=True, text=True, timeout=60)
    if (lan, parallel) != (cur["lan"], cur["parallel"]) and _port_open(UNSLOTH_PORT):
        subprocess.Popen(["systemctl", "restart", UNSLOTH_SVC], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return ai_conf()


_AI_UPD = {"running": False, "log": [], "rc": None, "t": 0.0}


def ai_update_start():
    """skillfish-unsloth-update in a thread; the log is read back by /api/ai/update."""
    if _AI_UPD["running"]:
        return {"ok": True, "running": True}
    if not os.path.exists(UNSLOTH_UPDATE_BIN):
        return {"ok": False, "error": "skillfish-unsloth-update missing"}

    def worker():
        _AI_UPD.update(running=True, log=[], rc=None, t=time.time())
        try:
            p = subprocess.Popen([UNSLOTH_UPDATE_BIN], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, bufsize=1)
            for ln in iter(p.stdout.readline, ""):
                _AI_UPD["log"].append(ln.rstrip()[:300])
                del _AI_UPD["log"][:-400]
            p.wait()
            _AI_UPD["rc"] = p.returncode
        except Exception as e:
            _AI_UPD["log"].append(str(e))
            _AI_UPD["rc"] = 1
        _AI_VER["t"] = 0.0
        _AI_UPD["running"] = False
    threading.Thread(target=worker, daemon=True).start()
    return {"ok": True, "running": True}


def ai_update_state():
    return {"ok": True, "running": _AI_UPD["running"], "rc": _AI_UPD["rc"],
            "log": "\n".join(_AI_UPD["log"][-80:])}


def _unsloth_mint_key(password):
    r = _studio("/api/auth/login", {"username": "unsloth", "password": password})
    if not r or not r.get("access_token"):
        return None, "Studio password not accepted"
    tok = r["access_token"]
    r = _studio("/api/auth/api-keys", {"name": "SkillFishOS Remote Manager"}, key=tok)
    if not r or not r.get("key"):
        return None, "Studio did not issue the key"
    # a request for a model that is not loaded must load it, not fail
    _studio("/api/settings/openai-auto-switch", {"enabled": True}, key=tok, method="PUT")
    return r["key"], ""


def ai_key_create(password):
    if not password:
        return {"ok": False, "error": "password missing"}
    k, err = _unsloth_mint_key(password)
    if not k:
        return {"ok": False, "error": err}
    salva_chiave_unsloth(k)
    _AI_VER["t"] = 0.0
    return {"ok": True, "has_key": True}


def ai_setup(new_password):
    """The first sign-in done for the user: bootstrap password in, their
    password set, a key minted and saved."""
    if not new_password or len(new_password) < 8:
        return {"ok": False, "error": "password too short (8+)"}
    try:
        with open(_unsloth_bootstrap()) as f:
            old = f.read().strip()
    except OSError:
        return {"ok": False, "error": "initial password not found"}
    r = _studio("/api/auth/login", {"username": "unsloth", "password": old})
    if not r or not r.get("access_token"):
        return {"ok": False, "error": "the initial password is no longer valid: sign in to Studio"}
    r2 = _studio("/api/auth/change-password", {"current_password": old, "new_password": new_password},
                 key=r["access_token"])
    if not r2 or r2.get("_error"):
        return {"ok": False, "error": (r2 or {}).get("detail") or "password change refused"}
    return ai_key_create(new_password)


def ai_variants(repo):
    key = _unsloth_key()
    if not key or not repo or "/" not in repo:
        return {"ok": False, "error": "key or repository missing"}
    r = _studio("/api/hub/gguf-variants?repo_id=" + urllib.parse.quote(repo, safe=""), key=key, t=40)
    if not r or r.get("_error"):
        return {"ok": False, "error": (r or {}).get("detail") or "no answer"}
    return {"ok": True, "variants": [{"quant": v.get("quant"), "filename": v.get("filename"),
                                      "size_bytes": v.get("size_bytes"), "downloaded": bool(v.get("downloaded"))}
                                     for v in r.get("variants") or []]}


def ai_download(repo, variant):
    key = _unsloth_key()
    if not key or not repo:
        return {"ok": False, "error": "key or repository missing"}
    r = _studio("/api/hub/download", {"repo_id": repo, "gguf_variant": variant}, key=key, t=40)
    if not r or r.get("_error") or not (r.get("accepted") or r.get("state") == "running"):
        return {"ok": False, "error": (r or {}).get("detail") or "Studio did not accept the download"}
    return {"ok": True, "job": r.get("job_key")}


def ai_downloads():
    key = _unsloth_key()
    if not key or not _port_open(UNSLOTH_PORT):
        return {"ok": True, "downloads": []}
    att = (_studio("/api/hub/active-downloads", key=key, t=6) or {}).get("downloads") or []
    out = []
    for d in att:
        repo = d.get("repo_id") or ""
        prog = _studio("/api/hub/download-progress?repo_id=" + urllib.parse.quote(repo, safe=""), key=key, t=6) or {}
        tot = prog.get("expected_bytes") or prog.get("total_bytes") or 0
        done = prog.get("downloaded_bytes") or 0
        pct = int(100.0 * done / tot) if tot else None
        out.append({"repo_id": repo, "variant": d.get("variant"), "state": d.get("state"),
                    "percent": pct, "downloaded_bytes": done, "total_bytes": tot})
    return {"ok": True, "downloads": out}


def _unsloth_cached():
    key = _unsloth_key()
    if not key or not _port_open(UNSLOTH_PORT):
        return []
    r = _studio("/v1/models", key=key, t=6) or {}
    return [{"id": m.get("id"), "quant": m.get("quant"), "loaded": bool(m.get("loaded"))}
            for m in r.get("data") or [] if m.get("id")]
'''

patch(D, [
    # the bootstrap password lives in the user's home
    ("    try:\n        with open(UNSLOTH_BOOTSTRAP) as f:\n            pw = f.read().strip()",
     "    try:\n        with open(_unsloth_bootstrap()) as f:\n            pw = f.read().strip()"),
    # the new functions, right before ai_status()
    ("\n\ndef ai_status():\n    running = _port_open(UNSLOTH_PORT)",
     FUNZIONI + "\n\ndef ai_status():\n    running = _port_open(UNSLOTH_PORT)"),
    # ai_status carries the extras
    ('''            "has_key": bool(_unsloth_key()),
            "models": _unsloth_models()}''',
     '''            "has_key": bool(_unsloth_key()),
            "models": _unsloth_models(),
            "catalog": _unsloth_cached() if running else [],
            "installed": _unsloth_installed() and bool(_unsloth_home()),
            "conf": _unsloth_conf_read(),
            "update_running": _AI_UPD["running"],
            **(_unsloth_version() if running else {})}'''),
    # GET routes
    ('''            return self._json(200, ai_status())
''',
     '''            return self._json(200, ai_status())
        if path == "/api/ai/update":
            if not self._guard("ai"):
                return
            return self._json(200, ai_update_state())
        if path == "/api/ai/conf":
            if not self._guard("ai"):
                return
            return self._json(200, ai_conf())
        if path == "/api/ai/downloads":
            if not self._guard("ai"):
                return
            return self._json(200, ai_downloads())
        if path == "/api/ai/variants":
            if not self._guard("ai"):
                return
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            return self._json(200, ai_variants((q.get("repo_id") or [""])[0].strip()))
'''),
    # POST routes
    ('''            return self._json(200, ai_chat(data.get("model"), data.get("messages")))
''',
     '''            return self._json(200, ai_chat(data.get("model"), data.get("messages")))
        if path == "/api/ai/update":
            if not self._guard("ai"):
                return
            return self._json(200, ai_update_start())
        if path == "/api/ai/conf":
            if not self._guard("ai"):
                return
            return self._json(200, ai_conf_set(data))
        if path == "/api/ai/setup":
            if not self._guard("ai"):
                return
            return self._json(200, ai_setup(data.get("password") or ""))
        if path == "/api/ai/keycreate":
            if not self._guard("ai"):
                return
            return self._json(200, ai_key_create(data.get("password") or ""))
        if path == "/api/ai/download":
            if not self._guard("ai"):
                return
            return self._json(200, ai_download((data.get("repo_id") or "").strip(), data.get("variant")))
'''),
])

# ---- app.js: the card ---------------------------------------------------------------
J = os.path.join(R, "apps/dashboard/web/app.js")
s = open(J, encoding="utf-8").read()
i = s.index("  ai(card) {\n")
j = s.index("\n  },\n", i) + len("\n  },\n")

CARD = r'''  ai(card) {
    const it = LANG === "it";
    card.innerHTML = "<h3>🧠 " + (T("x_localai")) + "</h3><div id=\"ai\">…</div>";
    let dlTimer = null;
    const pollDl = async () => {
      const box = $("#aidl", card); if (!box) { clearInterval(dlTimer); dlTimer = null; return; }
      let d; try { d = await (await api("/api/ai/downloads")).json(); } catch (e) { return; }
      const ds = d.downloads || [];
      if (!ds.length) { clearInterval(dlTimer); dlTimer = null; box.textContent = T("ai_dl_done"); setTimeout(refresh, 1500); return; }
      box.textContent = ds.map(x => x.repo_id + (x.variant ? " · " + x.variant : "") + (x.percent != null ? "  " + x.percent + "%" : "")).join("\n");
    };
    const refresh = async () => { let s; try { s = await (await api("/api/ai")).json(); } catch (e) { return; }
      const fl = s.first_login || {};
      const conf = s.conf || {};
      const cat = s.catalog || [];
      const models = cat.length
        ? cat.map(m => `<span class="pill" style="display:inline-block;margin:2px">${m.id}${m.quant ? " · " + m.quant : ""}${m.loaded ? " · " + T("ai_loaded") : ""}</span>`).join(" ")
        : `<span class="stub">${T("ai_none")}</span>`;
      const ver = s.version ? (s.version + (s.update_available && s.latest ? " → " + s.latest + " " + T("ai_avail") : "")) : (s.has_key ? "—" : T("ai_needkey"));
      $("#ai", card).innerHTML =
        '<div class="rows">' +
        '<div class="r"><span>' + T("x_engine") + ' (Unsloth Studio)</span><span>' + (s.running ? T("ai_on") : (s.installed ? T("ai_off") : T("ai_notinst"))) + '</span></div>' +
        '<div class="r"><span>' + T("ai_version") + '</span><span>' + ver + '</span></div>' +
        '<div class="r"><span>' + T("ai_backend") + '</span><span>' + (s.backend || "llama.cpp · Vulkan") + '</span></div>' +
        '<div class="r"><span>' + T("x_accel") + '</span><span>Vulkan · GPU</span></div></div>' +
        // Unsloth generates a random password at install, announces it once in
        // a log and shuts itself down after an hour if it is not changed. The
        // form does the first sign-in for the user and mints the API key.
        (s.running && fl.must_change && fl.password
          ? '<div class="gl" style="margin-top:12px">' + T("ai_first") + '</div>' +
            '<div style="font-size:12px;opacity:.75;margin:4px 0 6px">' + T("ai_first_hint") + '</div>' +
            '<div class="brow"><input id="aipw1" type="password" class="dsel" placeholder="' + T("ai_newpw") + '" style="flex:1"/>' +
            '<input id="aipw2" type="password" class="dsel" placeholder="' + T("ai_repeat") + '" style="flex:1"/>' +
            '<button class="dbtn" id="aisetup">' + T("ai_setup") + '</button></div>'
          : "") +
        (s.running && !s.has_key && !fl.must_change
          ? '<div class="gl" style="margin-top:12px">' + T("x_apikey") + '</div>' +
            '<div class="brow"><input id="aispw" type="password" class="dsel" placeholder="' + T("ai_pwph") + '" style="flex:1"/>' +
            '<button class="dbtn" id="aikeymk">' + T("ai_createkey") + '</button></div>' +
            '<div class="brow" style="margin-top:6px"><input id="aikey" class="dsel" placeholder="sk-unsloth-…" style="flex:1"/>' +
            '<button class="dbtn" id="aikeysave">' + T("x_save") + '</button></div>'
          : "") +
        '<div class="brow" style="margin-top:10px">' +
        (s.running ? '<button class="dbtn danger" id="aistop">' + T("ai_stop") + '</button>' : '<button class="dbtn" id="aistart"' + (s.installed ? "" : " disabled") + '>' + T("ai_start") + '</button>') +
        '<button class="dbtn" id="aichat"' + (s.running && s.has_key ? "" : " disabled") + '>💬 ' + T("x_chat") + '</button>' +
        '<button class="dbtn" id="aiweb"' + (s.webui ? "" : " disabled") + '>' + T("x_open") + 'Unsloth Studio ↗</button>' +
        '<button class="dbtn" id="aiupd"' + (s.update_running ? " disabled" : "") + '>' + (s.installed ? T("ai_update") : T("ai_install")) + '</button></div>' +
        '<pre id="aiupdlog" class="stub" style="display:none;white-space:pre-wrap;max-height:160px;overflow:auto;margin-top:6px"></pre>' +
        '<div class="brow" style="margin-top:10px;flex-wrap:wrap;gap:10px">' +
        '<label><input type="checkbox" id="aiauto"' + (conf.autostart ? " checked" : "") + '/> ' + T("ai_autostart") + '</label>' +
        '<label><input type="checkbox" id="ailan"' + (conf.lan ? " checked" : "") + '/> ' + T("ai_lan") + '</label>' +
        '<label>' + T("ai_slots") + ' <input type="number" id="aislots" min="1" max="16" value="' + (conf.parallel || 4) + '" style="width:60px"/></label>' +
        '<button class="dbtn" id="aiconf">' + T("ai_apply") + '</button></div>' +
        (conf.lan ? '<div class="stub" style="margin-top:4px">http://' + location.hostname + ':' + (s.port || 8888) + ' — ' + T("ai_lan_hint") + '</div>' : "") +
        '<div class="gl" style="margin-top:12px">' + T("ai_models") + '</div><div style="margin-top:4px">' + models + '</div>' +
        '<div class="brow" style="margin-top:8px"><input id="airepo" class="dsel" list="airepos" placeholder="' + T("ai_repo") + '" style="flex:1"/>' +
        '<datalist id="airepos"><option value="unsloth/Qwen3-1.7B-GGUF"/><option value="unsloth/Qwen3-4B-GGUF"/><option value="unsloth/Qwen3-8B-GGUF"/><option value="unsloth/gemma-3-4b-it-GGUF"/><option value="unsloth/Qwen2.5-Coder-7B-Instruct-GGUF"/></datalist>' +
        '<button class="dbtn" id="ailook"' + (s.running && s.has_key ? "" : " disabled") + '>' + T("ai_lookup") + '</button></div>' +
        '<div class="brow" style="margin-top:6px"><select id="aivar" class="dsel" style="flex:1" disabled></select>' +
        '<button class="dbtn" id="aidlgo" disabled>' + T("ai_download") + '</button>' +
        '<button class="dbtn" id="aihub"' + (s.webui ? "" : " disabled") + '>' + T("ai_openhub") + ' ↗</button></div>' +
        '<pre id="aidl" class="stub" style="white-space:pre-wrap;margin-top:4px"></pre>' +
        '<div class="brow" style="margin-top:10px"><button class="dbtn" id="aitunebtn" style="border-color:var(--gold)">⚡ ' + T("x_optai") + '</button></div><div id="aitune"></div>' +
        '<div class="stub" style="margin-top:8px">' + (it ? "Gira sulla GPU: spegnilo quando giochi. La chat completa, con file e ricerca, e' dentro Studio."
                                                          : "It runs on the GPU: turn it off when gaming. The full chat, with files and search, is inside Studio.") + "</div>";
      const studioUrl = "http://" + location.hostname + ":" + (s.port || 8888);
      if ($("#aistart", card)) $("#aistart", card).onclick = async () => { await action("/api/ai/start", {}, T("ai_starting")); setTimeout(refresh, 4000); };
      if ($("#aistop", card)) $("#aistop", card).onclick = async () => { await action("/api/ai/stop", {}, T("ai_stopping")); setTimeout(refresh, 2000); };
      if ($("#aisetup", card)) $("#aisetup", card).onclick = async () => {
        const a = $("#aipw1", card).value, b = $("#aipw2", card).value;
        if (a.length < 8) return toast(T("ai_short"));
        if (a !== b) return toast(T("ai_mismatch"));
        const j = await (await post("/api/ai/setup", { password: a })).json().catch(() => ({}));
        toast(j.ok ? T("x_keysaved") : (T("err") + (j.error || ""))); setTimeout(refresh, 800);
      };
      if ($("#aikeymk", card)) $("#aikeymk", card).onclick = async () => {
        const p = $("#aispw", card).value; if (!p) return;
        const j = await (await post("/api/ai/keycreate", { password: p })).json().catch(() => ({}));
        toast(j.ok ? T("x_keysaved") : (T("err") + (j.error || ""))); setTimeout(refresh, 800);
      };
      if ($("#aikeysave", card)) $("#aikeysave", card).onclick = async () => {
        const v = $("#aikey", card).value.trim(); if (!v) return;
        await action("/api/ai/key", { key: v }, T("x_keysaved")); setTimeout(refresh, 800);
      };
      if ($("#aichat", card)) $("#aichat", card).onclick = () => openFrame("SkillFishOS AI", "/static/aichat.html");
      // Studio is opened DIRECTLY, not through the dashboard proxy: its pages ask
      // for their assets with absolute paths (/assets/...). It has its own login.
      if ($("#aiweb", card)) $("#aiweb", card).onclick = () => window.open(studioUrl, "_blank");
      if ($("#aihub", card)) $("#aihub", card).onclick = () => window.open(studioUrl + "/hub", "_blank");
      if ($("#aiupd", card)) $("#aiupd", card).onclick = async () => {
        if (s.installed && !confirm(T("ai_update_q"))) return;
        const j = await (await post("/api/ai/update", {})).json().catch(() => ({}));
        if (!j.ok) return toast(T("err") + (j.error || ""));
        const box = $("#aiupdlog", card); box.style.display = "block"; box.textContent = T("ai_updating");
        const iv = setInterval(async () => { let u; try { u = await (await api("/api/ai/update")).json(); } catch (e) { return; }
          box.textContent = u.log || T("ai_updating"); box.scrollTop = box.scrollHeight;
          if (!u.running) { clearInterval(iv); setTimeout(refresh, 1500); } }, 2000);
      };
      if ($("#aiconf", card)) $("#aiconf", card).onclick = async () => {
        await action("/api/ai/conf", { autostart: $("#aiauto", card).checked, lan: $("#ailan", card).checked, parallel: +$("#aislots", card).value || 4 }, T("x_updated"));
        setTimeout(refresh, 1500);
      };
      if ($("#ailook", card)) $("#ailook", card).onclick = async () => {
        const repo = $("#airepo", card).value.trim(); if (!repo.includes("/")) return toast(T("ai_repo"));
        const sel = $("#aivar", card); sel.innerHTML = "<option>…</option>"; sel.disabled = true; $("#aidlgo", card).disabled = true;
        const j = await (await api("/api/ai/variants?repo_id=" + encodeURIComponent(repo))).json().catch(() => ({}));
        sel.innerHTML = "";
        if (!j.ok || !(j.variants || []).length) { sel.innerHTML = "<option>" + (j.error || T("ai_none")) + "</option>"; return; }
        j.variants.forEach(v => { const o = document.createElement("option"); o.value = v.quant || ""; o.textContent = (v.quant || v.filename) + "  ·  " + (v.size_bytes ? (v.size_bytes / 1e9).toFixed(1) + " GB" : "?") + (v.downloaded ? "  ·  ✓" : ""); sel.appendChild(o); });
        const pref = j.variants.findIndex(v => /^(UD-Q4|Q4_K_M)/i.test(v.quant || "")); if (pref >= 0) sel.selectedIndex = pref;
        sel.disabled = false; $("#aidlgo", card).disabled = false;
      };
      if ($("#aidlgo", card)) $("#aidlgo", card).onclick = async () => {
        const repo = $("#airepo", card).value.trim(), variant = $("#aivar", card).value;
        const j = await (await post("/api/ai/download", { repo_id: repo, variant })).json().catch(() => ({}));
        if (!j.ok) return toast(T("err") + (j.error || ""));
        $("#aidl", card).textContent = T("ai_dl_running"); $("#aidlgo", card).disabled = true;
        if (!dlTimer) dlTimer = setInterval(pollDl, 2000);
      };
      if ($("#aitunebtn", card)) $("#aitunebtn", card).onclick = () => aiTune(card, it);
      if (dlTimer) pollDl();
    };
    refresh(); card._iv = setInterval(refresh, 8000);
  },
'''
s = s[:i] + CARD + s[j:]

STR_NUOVE = r'''const STR = {
  ai_version: { it: "Versione", en: "Version", pl: "Wersja", uk: "Версія", ru: "Версия", es: "Versión", pt: "Versão", de: "Version", fr: "Version" },
  ai_backend: { it: "Backend", en: "Backend", pl: "Backend", uk: "Бекенд", ru: "Бэкенд", es: "Backend", pt: "Backend", de: "Backend", fr: "Backend" },
  ai_avail: { it: "disponibile", en: "available", pl: "dostępna", uk: "доступна", ru: "доступна", es: "disponible", pt: "disponível", de: "verfügbar", fr: "disponible" },
  ai_needkey: { it: "serve la chiave", en: "needs the key", pl: "potrzebny klucz", uk: "потрібен ключ", ru: "нужен ключ", es: "hace falta la clave", pt: "precisa da chave", de: "Schlüssel nötig", fr: "clé requise" },
  ai_notinst: { it: "non installato", en: "not installed", pl: "nie zainstalowany", uk: "не встановлено", ru: "не установлен", es: "no instalado", pt: "não instalado", de: "nicht installiert", fr: "non installé" },
  ai_update: { it: "Aggiorna", en: "Update", pl: "Aktualizuj", uk: "Оновити", ru: "Обновить", es: "Actualizar", pt: "Atualizar", de: "Aktualisieren", fr: "Mettre à jour" },
  ai_install: { it: "Installa", en: "Install", pl: "Zainstaluj", uk: "Встановити", ru: "Установить", es: "Instalar", pt: "Instalar", de: "Installieren", fr: "Installer" },
  ai_update_q: { it: "Rilancio l'installatore ufficiale di Unsloth (qualche GB, il motore si riavvia)?", en: "Rerun the official Unsloth installer (a few GB, the engine restarts)?", pl: "Uruchomić ponownie oficjalny instalator Unsloth (kilka GB, silnik się zrestartuje)?", uk: "Запустити офіційний інсталятор Unsloth знову (кілька ГБ, рушій перезапуститься)?", ru: "Запустить официальный установщик Unsloth заново (несколько ГБ, движок перезапустится)?", es: "¿Volver a ejecutar el instalador oficial de Unsloth (varios GB, el motor se reinicia)?", pt: "Executar de novo o instalador oficial do Unsloth (alguns GB, o motor reinicia)?", de: "Den offiziellen Unsloth-Installer erneut ausführen (einige GB, der Motor startet neu)?", fr: "Relancer l'installateur officiel d'Unsloth (quelques Go, le moteur redémarre) ?" },
  ai_updating: { it: "Aggiornamento in corso…", en: "Updating…", pl: "Aktualizacja…", uk: "Оновлення…", ru: "Обновление…", es: "Actualizando…", pt: "A atualizar…", de: "Aktualisiere…", fr: "Mise à jour…" },
  ai_autostart: { it: "All'avvio", en: "At boot", pl: "Przy starcie", uk: "При запуску", ru: "При запуске", es: "Al arrancar", pt: "No arranque", de: "Beim Start", fr: "Au démarrage" },
  ai_lan: { it: "Raggiungibile dalla rete locale", en: "Reachable from the local network", pl: "Dostępny w sieci lokalnej", uk: "Доступний з локальної мережі", ru: "Доступен из локальной сети", es: "Accesible desde la red local", pt: "Acessível na rede local", de: "Im lokalen Netz erreichbar", fr: "Joignable depuis le réseau local" },
  ai_lan_hint: { it: "Studio chiede il suo utente e la sua password.", en: "Studio asks for its own user and password.", pl: "Studio pyta o własnego użytkownika i hasło.", uk: "Studio запитує власного користувача і пароль.", ru: "Studio спрашивает своего пользователя и пароль.", es: "Studio pide su propio usuario y contraseña.", pt: "O Studio pede o seu próprio utilizador e senha.", de: "Studio fragt nach eigenem Benutzer und Passwort.", fr: "Studio demande son propre utilisateur et mot de passe." },
  ai_slots: { it: "Chat in parallelo", en: "Parallel chats", pl: "Równoległe czaty", uk: "Паралельні чати", ru: "Параллельные чаты", es: "Chats en paralelo", pt: "Chats em paralelo", de: "Parallele Chats", fr: "Chats en parallèle" },
  ai_apply: { it: "Applica", en: "Apply", pl: "Zastosuj", uk: "Застосувати", ru: "Применить", es: "Aplicar", pt: "Aplicar", de: "Anwenden", fr: "Appliquer" },
  ai_first: { it: "Primo accesso", en: "First sign-in", pl: "Pierwsze logowanie", uk: "Перший вхід", ru: "Первый вход", es: "Primer acceso", pt: "Primeiro acesso", de: "Erste Anmeldung", fr: "Première connexion" },
  ai_first_hint: { it: "Scegli la password di Studio. La chiave API viene creata insieme.", en: "Choose the Studio password. The API key is created with it.", pl: "Wybierz hasło do Studio. Klucz API powstaje razem z nim.", uk: "Виберіть пароль Studio. Ключ API створюється разом із ним.", ru: "Выберите пароль Studio. Ключ API создаётся вместе с ним.", es: "Elige la contraseña de Studio. La clave API se crea a la vez.", pt: "Escolhe a senha do Studio. A chave API é criada com ela.", de: "Wähle das Studio-Passwort. Der API-Schlüssel entsteht dabei.", fr: "Choisis le mot de passe de Studio. La clé API est créée en même temps." },
  ai_newpw: { it: "nuova password", en: "new password", pl: "nowe hasło", uk: "новий пароль", ru: "новый пароль", es: "nueva contraseña", pt: "nova senha", de: "neues Passwort", fr: "nouveau mot de passe" },
  ai_repeat: { it: "ripeti", en: "repeat", pl: "powtórz", uk: "повторіть", ru: "повторите", es: "repite", pt: "repete", de: "wiederholen", fr: "répéter" },
  ai_setup: { it: "Imposta e crea la chiave", en: "Set and create the key", pl: "Ustaw i utwórz klucz", uk: "Задати і створити ключ", ru: "Задать и создать ключ", es: "Fijar y crear la clave", pt: "Definir e criar a chave", de: "Setzen und Schlüssel erzeugen", fr: "Définir et créer la clé" },
  ai_short: { it: "Almeno 8 caratteri.", en: "At least 8 characters.", pl: "Co najmniej 8 znaków.", uk: "Щонайменше 8 символів.", ru: "Не меньше 8 символов.", es: "Al menos 8 caracteres.", pt: "Pelo menos 8 caracteres.", de: "Mindestens 8 Zeichen.", fr: "Au moins 8 caractères." },
  ai_mismatch: { it: "Le due password non coincidono.", en: "The two passwords do not match.", pl: "Hasła się różnią.", uk: "Паролі не збігаються.", ru: "Пароли не совпадают.", es: "Las dos contraseñas no coinciden.", pt: "As duas senhas não coincidem.", de: "Die Passwörter stimmen nicht überein.", fr: "Les deux mots de passe ne correspondent pas." },
  ai_createkey: { it: "Crea la chiave", en: "Create the key", pl: "Utwórz klucz", uk: "Створити ключ", ru: "Создать ключ", es: "Crear la clave", pt: "Criar a chave", de: "Schlüssel erzeugen", fr: "Créer la clé" },
  ai_pwph: { it: "password di Studio", en: "Studio password", pl: "hasło Studio", uk: "пароль Studio", ru: "пароль Studio", es: "contraseña de Studio", pt: "senha do Studio", de: "Studio-Passwort", fr: "mot de passe Studio" },
  ai_models: { it: "Modelli", en: "Models", pl: "Modele", uk: "Моделі", ru: "Модели", es: "Modelos", pt: "Modelos", de: "Modelle", fr: "Modèles" },
  ai_none: { it: "nessun modello scaricato", en: "no model downloaded", pl: "brak pobranych modeli", uk: "жодної моделі не завантажено", ru: "модели не скачаны", es: "ningún modelo descargado", pt: "nenhum modelo transferido", de: "kein Modell geladen", fr: "aucun modèle téléchargé" },
  ai_loaded: { it: "in memoria", en: "loaded", pl: "w pamięci", uk: "у пам'яті", ru: "в памяти", es: "en memoria", pt: "em memória", de: "geladen", fr: "chargé" },
  ai_repo: { it: "repository Hugging Face, es. unsloth/Qwen3-4B-GGUF", en: "Hugging Face repository, e.g. unsloth/Qwen3-4B-GGUF", pl: "repozytorium Hugging Face, np. unsloth/Qwen3-4B-GGUF", uk: "репозиторій Hugging Face, напр. unsloth/Qwen3-4B-GGUF", ru: "репозиторий Hugging Face, напр. unsloth/Qwen3-4B-GGUF", es: "repositorio de Hugging Face, p. ej. unsloth/Qwen3-4B-GGUF", pt: "repositório Hugging Face, p. ex. unsloth/Qwen3-4B-GGUF", de: "Hugging-Face-Repository, z. B. unsloth/Qwen3-4B-GGUF", fr: "dépôt Hugging Face, ex. unsloth/Qwen3-4B-GGUF" },
  ai_lookup: { it: "Cerca", en: "Look up", pl: "Szukaj", uk: "Знайти", ru: "Найти", es: "Buscar", pt: "Procurar", de: "Suchen", fr: "Chercher" },
  ai_download: { it: "Scarica", en: "Download", pl: "Pobierz", uk: "Завантажити", ru: "Скачать", es: "Descargar", pt: "Transferir", de: "Herunterladen", fr: "Télécharger" },
  ai_dl_running: { it: "Download avviato…", en: "Download started…", pl: "Pobieranie rozpoczęte…", uk: "Завантаження почалося…", ru: "Загрузка началась…", es: "Descarga iniciada…", pt: "Transferência iniciada…", de: "Download gestartet…", fr: "Téléchargement lancé…" },
  ai_dl_done: { it: "Download finito.", en: "Download finished.", pl: "Pobieranie zakończone.", uk: "Завантаження завершено.", ru: "Загрузка завершена.", es: "Descarga terminada.", pt: "Transferência concluída.", de: "Download abgeschlossen.", fr: "Téléchargement terminé." },
  ai_openhub: { it: "Apri l'Hub", en: "Open the Hub", pl: "Otwórz Hub", uk: "Відкрити Hub", ru: "Открыть Hub", es: "Abrir el Hub", pt: "Abrir o Hub", de: "Hub öffnen", fr: "Ouvrir le Hub" },
'''
assert "const STR = {\n" in s
s = s.replace("const STR = {\n", STR_NUOVE, 1)
open(J, "w", encoding="utf-8").write(s)
print("ok apps/dashboard/web/app.js")
