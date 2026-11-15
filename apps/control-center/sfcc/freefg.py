# -*- coding: utf-8 -*-
"""FreeFG for the Games page: XeSS frame generation with FSR 4 on the BC-250.

FreeFG (daniel-h-0/freefg, MIT) runs Intel's XeFG runtime with its own faster
shaders and puts FSR 4 next to it through OptiScaler, per game. Measured on
bc250-dev (15/11/2026, Cyberpunk 1080p Quality): 130-133 fps shown against a
bench median of 90.6, 1% lows 30-33. Those are generated frames: the game's own
rate stays near 65 and latency was not measured.

This module is the part without Qt. The page runs it as a separate process
(`skillfish-freefg ...`), so FreeFG's own code never runs inside the Control
Center. Everything happens as the desktop user, in their home.

⚠️ THE VERSION IS PINNED, WITH ITS HASH. A new FreeFG release changes nothing
here until it has been tried on the board and VERSION/SHA256 are moved. The
helper also uses three of FreeFG's own functions (discover, fields, patch) to
read and write the launcher entries; pinning is what keeps them stable.

⚠️ GE-PROTON MUST STAY OUT OF A FREEFG GAME. Our FSR 4 switch sets
PROTON_USE_OPTISCALER=1 and PROTON_FSR4_UPGRADE=1 for the whole launcher (a
flatpak override). GE-Proton then loads its own OptiScaler as dxgi.dll through
WINE_OPTISCALER_NAME, exactly where FreeFG's sits. Before installing, the two
variables are set to 0 in that game's own entry (GE reads them with nonzero(),
so 0 switches it off, and the entry wins over the launcher-wide override); the
values found there are saved and put back on removal.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

VERSION = "1.4.0"
URL = "https://github.com/daniel-h-0/freefg/releases/download/v%s/freefg-%s.zip" % (VERSION, VERSION)
SHA256 = "6fa3a44d27acb331d21169549d9b0bbd5bf283a0f37ef169172d4cb65614ef35"
HOME = Path(os.path.expanduser("~"))
BASE = HOME / ".local/share/skillfish/freefg"
DIR = BASE / ("freefg-" + VERSION)
ORIGINALS = BASE / "entries.json"
GE_VARS = ("PROTON_USE_OPTISCALER", "PROTON_FSR4_UPGRADE")
STATE_DIR = ".bc250-xefg-experimental"
STATE = STATE_DIR + "/state.json"
HEROIC = HOME / ".var/app/com.heroicgameslauncher.hgl/config/heroic"
# What we ask FreeFG for: its BC-250 FSR 4 build (HelixSR's upscalers crash at
# load on our Proton, see helixsr-prova-14-11), the automatic input, and never
# NVIDIA's DLL, which would come with NVIDIA's licence.
INSTALL_ARGS = ["--upscaler", "fsr4", "--dlss-helper", "no", "--no-prepare"]
LAUNCHERS = ("steam", "steamwebhelper", "heroic")


# ---- pure parts (tested in tests/test_cc_freefg.py) ------------------------------
def heroic_neutral(env_options):
    """Heroic enviromentOptions with the GE variables set to 0, the rest kept in order."""
    out = [e for e in (env_options or []) if not (isinstance(e, dict) and e.get("key") in GE_VARS)]
    return out + [{"key": k, "value": "0"} for k in GE_VARS]


def heroic_restored(env_options, original):
    """Undo heroic_neutral on what is there now: drop our zeros, put back the
    GE entries the game had before (in their old order, at the end)."""
    out = [e for e in (env_options or []) if not (isinstance(e, dict) and e.get("key") in GE_VARS)]
    return out + [e for e in (original or []) if isinstance(e, dict) and e.get("key") in GE_VARS]


def steam_neutral(options):
    """Steam LaunchOptions with the GE variables set to 0 in front of %command%.

    Options without %command% are game arguments: Steam appends them, so they go
    after it. Existing assignments of the two variables are replaced."""
    value = (options or "").strip()
    ours = " ".join("%s=0" % k for k in GE_VARS)
    if not value:
        return ours + " %command%"
    if "%command%" not in value:
        return ours + " %command% " + value
    head, tail = value.split("%command%", 1)
    kept = [t for t in head.split() if t.split("=", 1)[0] not in GE_VARS]
    return " ".join(kept + [ours, "%command%"]) + tail


def verdict_short(line):
    """FreeFG's verdict line cut to what fits a list row."""
    line = (line or "").strip()
    for cut in (": ", ". "):
        if line.startswith(("Not supported", "Supported", "Automatic", "Refused", "Verified")) and cut in line:
            return line.split(cut, 1)[0]
    return line[:60]


def installed(exe):
    """FreeFG is in this game: its state file is there and does not say restored."""
    try:
        with open(Path(exe).parent / STATE) as f:
            return json.load(f).get("status") != "restored"
    except (OSError, ValueError):
        return False


# ---- download ---------------------------------------------------------------------
def downloaded():
    return (DIR / "install.py").is_file()


def download(progress=print):
    """Fetch the pinned release, check its hash, unpack it with bsdtar (which
    keeps the executable bits that Python's zipfile drops)."""
    if downloaded():
        return str(DIR)
    if not shutil.which("bsdtar"):
        raise RuntimeError("bsdtar is missing (package libarchive-tools)")
    BASE.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="freefg-", dir=BASE))
    try:
        zip_path = work / ("freefg-%s.zip" % VERSION)
        req = urllib.request.Request(URL, headers={"User-Agent": "SkillFishOS-Control-Center"})
        h = hashlib.sha256()
        with urllib.request.urlopen(req, timeout=60) as r, open(zip_path, "wb") as out:
            total = int(r.headers.get("Content-Length") or 0)
            done = 0
            for block in iter(lambda: r.read(1 << 20), b""):
                out.write(block)
                h.update(block)
                done += len(block)
                if total:
                    progress("download %d%%" % (done * 100 // total))
        if h.hexdigest() != SHA256:
            raise RuntimeError("wrong sha256: the download is corrupt")
        unpack = work / "x"
        unpack.mkdir()
        subprocess.run(["bsdtar", "-xf", str(zip_path), "-C", str(unpack)], check=True)
        top = unpack / ("freefg-" + VERSION)
        if not (top / "install.py").is_file():
            raise RuntimeError("unexpected archive layout")
        os.replace(top, DIR)
        return str(DIR)
    finally:
        shutil.rmtree(work, ignore_errors=True)


# ---- FreeFG's own modules, in this process only --------------------------------------
def _freefg():
    if not downloaded():
        raise RuntimeError("FreeFG is not downloaded")
    if str(DIR) not in sys.path:
        sys.path.insert(0, str(DIR))
    import launcher_config  # noqa: E402  (FreeFG's)
    return launcher_config


def _heroic_sideload():
    """Heroic's sideloaded games, which FreeFG's scan does not list."""
    try:
        with open(HEROIC / "sideload_apps/library.json") as f:
            games = json.load(f).get("games", [])
    except (OSError, ValueError):
        return []
    out = []
    for g in games:
        exe = (g.get("install") or {}).get("executable")
        if exe and exe.lower().endswith(".exe") and os.path.isfile(exe):
            out.append({"nome": g.get("title") or g.get("app_name"), "store": "heroic", "id": g.get("app_name"), "exe": exe})
    return out


def games():
    """Every Steam and Heroic game with FreeFG's verdict and whether it is in."""
    _freefg()
    import gamescan  # noqa: E402  (FreeFG's)
    import compat  # noqa: E402  (FreeFG's)
    import install as ffg  # noqa: E402  (FreeFG's install.py; main() only runs as a script)
    rm = ffg.recipes_module()
    recipes = DIR / "recipes/recipes.json"
    data = rm.load(recipes) if recipes.is_file() else None
    found = []
    for game in gamescan.installed_games(None):
        try:
            scan = gamescan.scan_folder(game)
        except Exception:  # noqa: BLE001 - one unreadable game must not hide the others
            continue
        exe = (scan.get("exe") or {}).get("selected") or ""
        if exe and game.get("path"):
            exe = str((Path(game["path"]) / exe).resolve())
        found.append(({"nome": game.get("name"), "store": game.get("store"), "id": str(game.get("id")), "exe": exe}, scan, game))
    known = {g["exe"] for g, _, _ in found}
    for g in _heroic_sideload():
        if g["exe"] not in known:
            try:
                found.append((g, gamescan.scan_exe(Path(g["exe"])), None))
            except Exception:  # noqa: BLE001
                continue
    out = []
    for g, scan, game in found:
        ids = dict(exe=Path(g["exe"]).name.lower(), steam=set(), gog=set(), epic=set(),
                   titles={rm.norm(g["nome"] or "")}, folders={rm.norm(p) for p in Path(g["exe"]).parts[:-1]} - {""})
        if g["store"] in ("steam", "gog", "epic"):
            ids[g["store"]].add(g["id"])
        try:
            v = compat.decide(scan, data, ids)
            g["verdetto"] = v["line"]
            g["blocca"] = v["blocking"][0]["code"] if v["blocking"] else None
        except Exception as e:  # noqa: BLE001
            g["verdetto"], g["blocca"] = "not checked (%s)" % type(e).__name__, "error"
        g["breve"] = verdict_short(g["verdetto"])
        g["dentro"] = installed(g["exe"]) if g["exe"] else False
        out.append(g)
    return sorted(out, key=lambda g: (not g["dentro"], g["blocca"] is not None, (g["nome"] or "").lower()))


# ---- the launcher entries: GE-Proton out while FreeFG is in ----------------------------
def _load_originals():
    try:
        with open(ORIGINALS) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_originals(d):
    BASE.mkdir(parents=True, exist_ok=True)
    tmp = ORIGINALS.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(d, f, indent=1)
    os.replace(tmp, ORIGINALS)


def _key(t):
    return "%s|%s|%s" % (t["launcher"], t["path"], t["id"])


def neutralize(exe):
    """Set the GE variables to 0 in every Steam/Heroic entry of this game,
    remembering what was there. Returns the entries changed."""
    lc = _freefg()
    lc.require_stopped(LAUNCHERS)
    originals = _load_originals()
    changed = []
    for t in lc.discover(Path(exe)):
        if t["launcher"] not in ("steam", "heroic"):
            continue
        p = Path(t["path"])
        data = p.read_bytes()
        cur = lc.fields(t, data)
        if t["launcher"] == "heroic":
            field, old = "enviromentOptions", cur.get("enviromentOptions")
            new = heroic_neutral(old)
        else:
            field, old = "LaunchOptions", cur.get("LaunchOptions")
            new = steam_neutral(old)
        if new == old:
            continue
        values = {k: v for k, v in cur.items()}
        values[field] = new
        p.write_bytes(lc.patch(t, data, values))
        originals.setdefault(_key(t), {"campo": field, "originale": old, "scritto": new})
        changed.append(_key(t))
    _save_originals(originals)
    return changed


def restore_entries(exe):
    """Put back what neutralize() found, after FreeFG has restored its own."""
    lc = _freefg()
    lc.require_stopped(LAUNCHERS)
    originals = _load_originals()
    done = []
    for t in lc.discover(Path(exe)):
        rec = originals.get(_key(t))
        if not rec:
            continue
        p = Path(t["path"])
        data = p.read_bytes()
        cur = lc.fields(t, data)
        now = cur.get(rec["campo"])
        if now == rec["scritto"]:
            back = rec["originale"]
        elif t["launcher"] == "heroic":
            back = heroic_restored(now, rec["originale"])
        else:
            # Someone changed the options since: only take our two zeros out.
            back = " ".join(x for x in (now or "").split() if x not in ("%s=0" % k for k in GE_VARS)) or None
        values = dict(cur)
        values[rec["campo"]] = back
        p.write_bytes(lc.patch(t, data, values))
        originals.pop(_key(t))
        done.append(_key(t))
    _save_originals(originals)
    return done


def _install_py(*args, timeout=1800):
    r = subprocess.run([sys.executable, "-I", "install.py", *args], cwd=str(DIR),
                       capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def install(exe):
    neutralize(exe)
    rc, out = _install_py("install", exe, *INSTALL_ARGS)
    if rc != 0 or not installed(exe):
        # Nothing of FreeFG went in: the entries go back as they were.
        try:
            restore_entries(exe)
        except Exception:  # noqa: BLE001 - the install error is the one to report
            pass
        raise RuntimeError(out or "install failed")
    return out


# The copies of FreeFG's state folder a reinstall sets aside (install.py renames the
# previous restored record to STATE_DIR-restored-<12 hex>).
ARCHIVE = re.compile(r"^" + re.escape(STATE_DIR) + r"-restored-[0-9a-f]{12}$")


def archive_done_with(record):
    """An archived record that holds nothing a later install could need: its Restore
    put everything back. A record that left files installed, kept files the user
    changed, or left game settings in place still holds the true originals (FreeFG's
    previous_settings() and left_installed() read them), so it stays."""
    if not isinstance(record, dict) or record.get("status") != "restored":
        return False
    if record.get("left_installed") or record.get("kept_changed"):
        return False
    return all(isinstance(i, dict) and i.get("status") == "restored"
               for i in record.get("game_settings") or [])


def prune_archives(exe):
    """Delete the records earlier reinstalls set aside in the game folder, when they
    are done with. The current STATE_DIR folder is never touched: it holds this
    installation's backups and the settings a reinstall carries over.
    Returns (deleted, kept) folder names."""
    root = Path(exe).parent.resolve()
    deleted, kept = [], []
    for d in sorted(root.iterdir()):
        if not ARCHIVE.match(d.name) or d.is_symlink() or not d.is_dir():
            continue
        try:
            with open(d / "state.json", encoding="utf-8") as f:
                record = json.load(f)
        except (OSError, ValueError):
            record = None
        if archive_done_with(record):
            shutil.rmtree(d)
            deleted.append(d.name)
        else:
            kept.append(d.name)
    return deleted, kept


def remove(exe):
    rc, out = _install_py("restore", exe)
    if rc != 0:
        raise RuntimeError(out or "restore failed")
    restore_entries(exe)
    try:
        deleted, kept = prune_archives(exe)
    except OSError as e:  # the game is out already; a leftover folder is not a failure
        return out + "\nEarlier records not cleaned: %s" % e
    if deleted:
        out += "\nDeleted %d earlier record(s) set aside by reinstalls." % len(deleted)
    if kept:
        out += "\nKept, they still hold originals: " + ", ".join(kept)
    return out


# ---- command line: what the page runs ---------------------------------------------
def main(argv):
    cmd = argv[1] if len(argv) > 1 else "stato"
    try:
        if cmd == "stato":
            print(json.dumps({"versione": VERSION, "scaricato": downloaded(), "dir": str(DIR),
                              "bsdtar": bool(shutil.which("bsdtar"))}))
        elif cmd == "scarica":
            print(json.dumps({"ok": True, "dir": download(lambda s: print(s, file=sys.stderr, flush=True))}))
        elif cmd == "giochi":
            print(json.dumps({"ok": True, "giochi": games()}))
        elif cmd in ("installa", "togli") and len(argv) > 2:
            out = (install if cmd == "installa" else remove)(argv[2])
            print(json.dumps({"ok": True, "testo": out}))
        else:
            print("usage: skillfish-freefg stato | scarica | giochi | installa EXE | togli EXE", file=sys.stderr)
            return 2
    except Exception as e:  # noqa: BLE001 - the page shows the message as it is
        print(json.dumps({"ok": False, "errore": str(e)}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
