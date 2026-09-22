"""skillfish-cc-helper, command by command, the way the Control Center and the
Remote Manager talk to it: one JSON request per line on stdin, one answer per
line on stdout.

Every write is a round trip: read the value, change it, read it back, put it
back, read it again. The files a write touches are saved first and restored
byte for byte whatever happens (common.preserved).

Issue #93 is the reason this module exists: every write to /sys from this
helper failed for eleven days, and nothing in CI or on our boards pressed the
button that would have shown it.
"""
import glob
import json
import os
import re
import select
import subprocess
import time

import coverage
from common import Skip, check, preserved, read_json, read_text, sh

HELPER = "/usr/local/bin/skillfish-cc-helper"


class Helper:
    def __init__(self):
        self.p = subprocess.Popen([HELPER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, bufsize=1)
        # ⚠️ it greets before reading: {"ok": true, "ready": true}. A probe that
        # does not consume the greeting reads every answer one request late.
        hello = self._line(30)
        check(hello.get("ready"), "no greeting from the helper: %s" % hello)

    def _line(self, timeout):
        r, _, _ = select.select([self.p.stdout], [], [], timeout)
        if not r:
            raise AssertionError("no answer within %d s" % timeout)
        line = self.p.stdout.readline()
        check(line, "the helper closed its output (crashed?)")
        return json.loads(line)

    def __call__(self, cmd, timeout=120, **args):
        req = dict(args, cmd=cmd)
        self.p.stdin.write(json.dumps(req) + "\n")
        self.p.stdin.flush()
        return self._line(timeout)

    def close(self):
        try:
            self.p.stdin.close()
            self.p.wait(10)
        except Exception:
            self.p.kill()


def _const(name):
    """A path constant from the installed helper, so the tests follow it."""
    src = read_text(HELPER)
    m = re.search(r'^%s\s*=\s*"([^"]+)"' % name, src, re.M)
    return m.group(1) if m else None


def _ok(r, what):
    check(isinstance(r, dict) and r.get("ok") is not False, "%s answered: %s" % (what, json.dumps(r)[:600]))
    return r


def _bc(ctx):
    if ctx.kind != "bc250":
        raise Skip("BC-250 only")


# ---- coverage of the command list --------------------------------------------
def t_command_coverage(ctx):
    src = read_text(HELPER)
    cmds = sorted(set(re.findall(r'^\s+if c == "([a-z0-9-]+)":', src, re.M)))
    check(cmds, "no commands found in %s" % HELPER)
    missing = [c for c in cmds if c not in coverage.CC_COMMANDS]
    check(not missing, "commands with no entry in coverage.CC_COMMANDS: " + ", ".join(missing))
    return "%d commands, all classified" % len(cmds)


# ---- reads -----------------------------------------------------------------
READ_ARGS = {"cluster": {"azione": "stato"}, "ai-mode": {"azione": "stato"}}


def t_read(ctx, h, cmd):
    r = h(cmd, **READ_ARGS.get(cmd, {}))
    _ok(r, cmd)
    return "ok"


# ---- writes ----------------------------------------------------------------
def _nproc():
    """Online threads, as nproc counts them."""
    return int(sh("nproc", 10)[1].strip())


def t_cores(ctx, h):
    cores = _ok(h("cpu-cores"), "cpu-cores")["cores"]
    cand = [c for c in cores if c["online"] and all(x["removable"] and x["online"] for x in c["cpus"])]
    if not cand:
        raise Skip("no core that can be switched off")
    c = cand[-1]
    n0 = _nproc()
    try:
        _ok(h("cpu-cores-set", cores=[{"core": c["core"], "online": False}]), "cpu-cores-set off")
        n1 = _nproc()
        check(n1 == n0 - len(c["cpus"]), "core %d off: %d threads, expected %d" % (c["core"], n1, n0 - len(c["cpus"])))
    finally:
        _ok(h("cpu-cores-set", cores=[{"core": c["core"], "online": True}]), "cpu-cores-set on")
    n2 = _nproc()
    check(n2 == n0, "core %d back on: %d threads, expected %d" % (c["core"], n2, n0))
    return "core %d off and on: %d, %d, %d threads" % (c["core"], n0, n1, n2)


def t_smt(ctx, h):
    _bc(ctx)
    p = "/sys/devices/system/cpu/smt/control"
    if not os.path.exists(p) or read_text(p).strip() != "on":
        raise Skip("SMT not on or not controllable")
    n0 = _nproc()
    try:
        _ok(h("cpu-smt", on=False), "cpu-smt off")
        check(read_text(p).strip() == "off", "smt/control is not off")
        n1 = _nproc()
        check(n1 == n0 // 2, "SMT off: %d threads, expected %d" % (n1, n0 // 2))
    finally:
        _ok(h("cpu-smt", on=True), "cpu-smt on")
    check(read_text(p).strip() == "on", "smt/control did not come back on")
    check(_nproc() == n0, "threads after SMT back on: %d, expected %d" % (_nproc(), n0))
    return "SMT off and on: %d, %d, %d threads" % (n0, n1, _nproc())


def t_thermal(ctx, h):
    g = _ok(h("thermal-guard-get"), "thermal-guard-get")
    lim = g.get("limite")
    if lim is None:
        raise Skip("no limit configured")
    other = lim - 1 if lim > 60 else lim + 1
    with preserved("/etc/skillfish/thermal-guard.conf"):
        try:
            _ok(h("thermal-guard", limit=other), "thermal-guard set")
            check(h("thermal-guard-get").get("limite") == other, "the limit did not change to %d" % other)
        finally:
            _ok(h("thermal-guard", limit=lim), "thermal-guard restore")
    check(h("thermal-guard-get").get("limite") == lim, "the limit did not come back to %d" % lim)
    return "limit %d -> %d -> %d" % (lim, other, lim)


def _gov_conf_file():
    return _const("GOV_CONF") or "/etc/skillfish-vf-governor.json"


def _gov(ctx, h):
    _bc(ctx)
    g = _ok(h("gov-get"), "gov-get")
    if not g.get("installato"):
        raise Skip("skillfish-vf-governor not installed")
    if g.get("prova"):
        raise Skip("a curve trial is already in progress")
    return g


def t_gov_set(ctx, h):
    g = _gov(ctx, h)
    conf = g["conf"]
    with preserved(_gov_conf_file()):
        _ok(h("gov-set", conf=conf, timeout=90), "gov-set")
        g2 = _ok(h("gov-get"), "gov-get")
        check(g2["conf"].get("curva") == conf.get("curva") and g2["conf"].get("freq_max") == conf.get("freq_max"),
              "the curve read back differs from the one written")
        check(g2.get("attivo") is True, "governor not active after gov-set: %s" % g2.get("attivo"))
    return "curve rewritten unchanged, governor active"


def t_gov_trial(ctx, h, finish):
    g = _gov(ctx, h)
    conf = g["conf"]
    with preserved(_gov_conf_file()):
        _ok(h("gov-prova", conf=conf, timeout=90), "gov-prova")
        check(h("gov-get").get("prova"), "no trial recorded after gov-prova")
        _ok(h(finish, timeout=90), finish)
        g2 = _ok(h("gov-get"), "gov-get")
        check(not g2.get("prova"), "trial still recorded after %s" % finish)
        check(g2["conf"].get("curva") == conf.get("curva"), "curve changed after %s" % finish)
        check(g2.get("attivo") is True, "governor not active after %s" % finish)
    return "trial then %s: curve unchanged, governor active" % finish


def t_apply_gpu(ctx, h):
    _gov(ctx, h)
    gpu = _ok(h("get"), "get")["data"]["gpu"]
    before = h("gov-get")["conf"]
    with preserved(_gov_conf_file()):
        _ok(h("apply-gpu", minmhz=gpu["min_mhz"], minmv=gpu["min_mv"], maxmhz=gpu["max_mhz"],
              maxmv=gpu["max_mv"], timeout=90), "apply-gpu")
        after = h("gov-get")["conf"]
        check(after.get("freq_max") == before.get("freq_max"), "ceiling changed: %s -> %s"
              % (before.get("freq_max"), after.get("freq_max")))
    return "old two-point call with the current values: ceiling %s kept" % before.get("freq_max")


def t_gov_toggle(ctx, h):
    g = _gov(ctx, h)
    if g.get("attivo") is not True:
        raise Skip("governor not running before the test")
    try:
        r = _ok(h("gov-attiva", on=False, timeout=90), "gov-attiva off")
        check(r.get("attivo") is not True, "still active after gov-attiva off")
    finally:
        r = _ok(h("gov-attiva", on=True, timeout=90), "gov-attiva on")
    check(r.get("attivo") is True, "not active after gov-attiva on: %s" % r.get("attivo"))
    check(r.get("abilitato") is True, "not enabled after gov-attiva on: %s" % r.get("abilitato"))
    return "governor off and on again, enabled"


def _cpu_now(h):
    return _ok(h("get"), "get")["data"]["cpu"]


def t_cpu(ctx, h, cmd):
    _bc(ctx)
    c = _cpu_now(h)
    oc = _const("OC_CONF")
    paths = [p for p in (oc,) if p]
    with preserved(*paths):
        _ok(h(cmd, mhz=c["frequency"], scale=c["scale"], temp=c["max_temperature"], timeout=120), cmd)
        c2 = _cpu_now(h)
        check(c2 == c, "CPU setting changed: %s -> %s" % (c, c2))
    return "%s with the current values %s: accepted, unchanged" % (cmd, c)


def _cu_rows(j):
    rows = j.get("rows")
    if isinstance(rows, dict):
        return [rows[k] for k in ("0.0", "0.1", "1.0", "1.1")]
    return rows


def t_cu_apply(ctx, h):
    _bc(ctx)
    j = _ok(h("cu-get", timeout=60), "cu-get")
    rows = _cu_rows(j)
    check(rows and len(rows) == 4, "cu-get gave no rows: %s" % j)
    _ok(h("cu-apply", rows=rows, timeout=120), "cu-apply")
    j2 = _ok(h("cu-get", timeout=60), "cu-get")
    check(_cu_rows(j2) == rows and j2.get("active_cu") == j.get("active_cu"),
          "CU mapping changed: %s -> %s" % (rows, _cu_rows(j2)))
    return "%s CU, masks %s re-applied unchanged" % (j.get("active_cu"), rows)


def t_cu_keep_boot(ctx, h):
    _bc(ctx)
    j = _ok(h("cu-get", timeout=60), "cu-get")
    keep, rows = bool(j.get("keep_boot")), j.get("boot_rows") or _cu_rows(j)
    _ok(h("cu-keep-boot", on=keep, rows=rows, timeout=60), "cu-keep-boot")
    j2 = _ok(h("cu-get", timeout=60), "cu-get")
    check(bool(j2.get("keep_boot")) == keep, "keep_boot changed: %s -> %s" % (keep, j2.get("keep_boot")))
    return "keep at boot rewritten unchanged (%s)" % keep


def t_scx(ctx, h):
    s = _ok(h("scx"), "scx")
    if not s.get("supportato"):
        raise Skip("sched_ext not supported here")
    # _unit() in the helper answers True/False, not the systemctl word
    was = bool(s.get("abilitato"))
    try:
        r = _ok(h("scx-set", on=not was, timeout=60), "scx-set")
        check(bool(r.get("abilitato")) == (not was), "scx-set did not change it: %s" % r.get("abilitato"))
    finally:
        r = _ok(h("scx-set", on=was, timeout=60), "scx-set restore")
    check(bool(r.get("abilitato")) == was, "scx not back to %s" % was)
    return "scheduler switch %s -> %s -> %s" % (was, not was, was)


def t_scx_reset(ctx, h):
    s = _ok(h("scx"), "scx")
    if not s.get("installato"):
        raise Skip("skillfish-scx not installed")
    conta = _const("SCX_CONTA")
    with preserved(*([conta] if conta else [])):
        r = _ok(h("scx-azzera"), "scx-azzera")
        check(r.get("espulsioni") == 0, "counter not zero: %s" % r.get("espulsioni"))
    return "counter reset (and put back)"


def _graphical_session():
    """A user's desktop or game session running on the machine, or ''.

    Class=user only: the login screen is a graphical session of class
    "greeter" with its own kwin_wayland, and nothing of a user starts there.
    """
    rc, out, _ = sh("loginctl list-sessions --no-legend", 10)
    for line in out.splitlines():
        sid = line.split()[0] if line.split() else ""
        rc, st, _ = sh("loginctl show-session %s -p Type -p State -p Name -p Class" % sid, 10)
        d = dict(l.split("=", 1) for l in st.splitlines() if "=" in l)
        if d.get("Type") in ("x11", "wayland") and d.get("Class") == "user" \
                and d.get("State") in ("active", "online"):
            return "%s (%s)" % (d.get("Name"), d.get("Type"))
    return ""


def t_mesa(ctx, h):
    _bc(ctx)
    # While the switch is off, anything that STARTS gets Debian's Mesa, which
    # is the driver gfx1013 must not run on. A live Plasma starts things by
    # itself (portals, notifications, Dolphin previews), and the failure would
    # show up half an hour later in an app nobody links to this test.
    live = _graphical_session()
    if live:
        raise Skip("graphical session of %s is live: switch the system Mesa with the screen off" % live)
    m = _ok(h("mesa-sistema", timeout=60), "mesa-sistema")
    if not m.get("installata"):
        raise Skip("our Mesa not installed")
    was = bool(m.get("attivo"))
    try:
        r = _ok(h("mesa-sistema-set", on=not was, timeout=180), "mesa-sistema-set")
        check(bool(r.get("attivo")) == (not was), "Mesa switch did not move: %s" % r.get("attivo"))
    finally:
        r = _ok(h("mesa-sistema-set", on=was, timeout=180), "mesa-sistema-set restore")
    check(bool(r.get("attivo")) == was, "Mesa switch not back to %s" % was)
    return "system Mesa %s -> %s -> %s" % (was, not was, was)


def t_unsloth_conf(ctx, h):
    c = _ok(h("unsloth-conf"), "unsloth-conf")
    with preserved("/etc/default/skillfish-unsloth"):
        r = _ok(h("unsloth-conf-set", lan=c["bind"] == "0.0.0.0", parallel=c["parallel"], timeout=180),
                "unsloth-conf-set")
        check(r["bind"] == c["bind"] and r["parallel"] == c["parallel"], "AI engine settings changed: %s -> %s"
              % ({k: c[k] for k in ("bind", "parallel")}, {k: r[k] for k in ("bind", "parallel")}))
    return "bind %s, %d slots rewritten unchanged" % (c["bind"], c["parallel"])


def t_gddr6(ctx, h):
    _bc(ctx)
    if not os.path.exists("/usr/local/bin/skillfish-gddr6-helper"):
        raise Skip("skillfish-gddr6 not installed")
    a = h("gddr6", azione="avvia", timeout=60)
    time.sleep(4)
    f = h("gddr6", azione="ferma", timeout=60)
    check(a.get("ok") is not False, "gddr6 avvia: %s" % a)
    check(f.get("ok") is not False, "gddr6 ferma: %s" % f)
    return "memory temperature reading started and stopped"


def t_service(ctx, h):
    unit = "skillfish-fand.service"
    if sh("systemctl is-active %s" % unit, 10)[1].strip() != "active":
        raise Skip("%s not running" % unit)
    r = _ok(h("servizio", azione="restart", unit=unit, timeout=120), "servizio restart")
    check(r.get("attivo") is True, "%s not active after restart: %s" % (unit, r.get("attivo")))
    r = h("servizio", azione="restart", unit="ssh.service")
    check(r.get("ok") is False, "a unit outside the allow-list was accepted")
    return "%s restarted; a unit outside the list refused" % unit


def _govs():
    out = {}
    for p in glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"):
        try:
            out[p] = read_text(p).strip()
        except OSError:
            # this CPU went offline between the glob and the read: skip it
            pass
    return out


def t_cpu_gov(ctx, h):
    """The CPU governor (issue #95): switch every thread to another one, check
    it is kept, check a core that comes back online gets it too (the udev
    rule), switch back. The kept-choice file goes back byte for byte."""
    st = _ok(h("cpu-gov"), "cpu-gov")
    av = st.get("available") or []
    if not av:
        raise Skip("no cpufreq here (driver %s)" % st.get("driver"))
    cur = st.get("current") or []
    if len(cur) != 1:
        raise Skip("threads already on different governors: %s" % cur)
    orig = cur[0]
    other = next((g for g in ("schedutil", "ondemand", "powersave", "performance") if g in av and g != orig), None)
    if other is None:
        raise Skip("only one governor available")
    detail = ""
    with preserved("/etc/skillfish/cpu-governor.conf"):
        try:
            _ok(h("cpu-gov-set", gov=other, timeout=90), "cpu-gov-set")
            check(set(_govs().values()) == {other}, "not every thread on %s: %s" % (other, sorted(set(_govs().values()))))
            check(h("cpu-gov").get("saved") == other, "the choice was not kept")
            cores = _ok(h("cpu-cores"), "cpu-cores")["cores"]
            cand = [c for c in cores if c["online"] and all(x["removable"] and x["online"] for x in c["cpus"])]
            if cand:
                c = cand[-1]
                try:
                    _ok(h("cpu-cores-set", cores=[{"core": c["core"], "online": False}]), "core off")
                finally:
                    _ok(h("cpu-cores-set", cores=[{"core": c["core"], "online": True}]), "core on")
                time.sleep(2)   # the udev rule runs asynchronously
                back = {read_text("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_governor" % x["cpu"]).strip()
                        for x in c["cpus"]}
                check(back == {other}, "core %d came back on %s, not %s: the udev rule did not apply it"
                      % (c["core"], sorted(back), other))
                detail = "; core %d off and on came back on %s" % (c["core"], other)
        finally:
            _ok(h("cpu-gov-set", gov=orig, timeout=90), "cpu-gov-set restore")
    check(set(_govs().values()) == {orig}, "not back on %s: %s" % (orig, sorted(set(_govs().values()))))
    bad = h("cpu-gov-set", gov="nonsense")
    check(bad.get("ok") is False, "an unknown governor was accepted")
    return "%s -> %s -> %s on every thread%s; unknown name refused" % (orig, other, orig, detail)


def t_bench_cpu(ctx, h):
    if not sh("command -v sysbench", 10)[1].strip():
        raise Skip("sysbench not installed")
    before = _govs()
    r = _ok(h("bench-cpu", secs=10, timeout=90), "bench-cpu")
    after = _govs()
    check(after == before, "CPU governors not restored after the benchmark")
    return "score %s, governors restored" % r.get("score", r.get("events", "?"))


def t_bench_gpu(ctx, h):
    r = _ok(h("bench-gpu", timeout=200), "bench-gpu")
    score = float(r.get("score") or 0)
    if ctx.kind == "bc250":
        check(score >= coverage.VKPEAK_MIN_BC250, "GPU %.0f GFLOPS, below %.0f" % (score, coverage.VKPEAK_MIN_BC250))
    return "%.2f %s" % (score, r.get("unit", ""))


def t_snapshot(ctx, h):
    """Create a snapshot through the helper, see it, delete it, see it gone."""
    if not os.path.exists("/usr/local/bin/skillfish-snapshots-helper") or not os.path.isdir("/.snapshots"):
        raise Skip("no snapper setup here")
    r = _ok(h("snapshot", args=["crea", "release check"], attesa=300, timeout=320), "snapshot crea")
    m = re.search(r"OK creato (\d+)", r.get("out", ""))
    check(m, "no snapshot number in: %s" % r.get("out"))
    n = m.group(1)
    try:
        check(os.path.isdir("/.snapshots/%s/snapshot" % n), "snapshot %s not on disk" % n)
    finally:
        d = _ok(h("snapshot", args=["cancella", n], attesa=300, timeout=320), "snapshot cancella")
    check("OK cancellato %s" % n in d.get("out", ""), "no deletion confirmed: %s" % d.get("out"))
    check(not os.path.exists("/.snapshots/%s" % n), "snapshot %s still on disk" % n)
    bad = h("snapshot", args=["cancella", "0"])
    check(bad.get("ok") is False, "deleting snapshot 0 (the running system) was accepted")
    return "snapshot %s created and deleted; snapshot 0 refused" % n


def _same_where_both(a, b, path=""):
    """Differences between two JSON trees, ignoring keys only one side has
    (the fan helper may add defaults) and int/float spelling."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in set(a) & set(b):
            out += _same_where_both(a[k], b[k], "%s.%s" % (path, k))
        return out
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return [] if abs(a - b) < 1e-9 else ["%s: %s -> %s" % (path, a, b)]
    return [] if a == b else ["%s: %s -> %s" % (path, a, b)]


def t_fan(ctx, h, azione, path):
    """Write the current fan configuration (or sensor labels) back through the
    helper: accepted, and nothing the user set comes back different."""
    if not os.path.exists(path):
        raise Skip("%s does not exist here" % path)
    before = read_json(path)
    fand_on = sh("systemctl is-active skillfish-fand.service", 10)[1].strip() == "active"
    with preserved(path):
        _ok(h("ventola", azione=azione, dati=before, timeout=240), "ventola %s" % azione)
        after = read_json(path)
        diff = _same_where_both(before, after)
        check(not diff, "values changed on the way through the helper:\n" + "\n".join(diff[:20]))
    # the daemon read the rewritten file: give it the original bytes back
    if fand_on:
        sh("systemctl restart skillfish-fand.service", 60)
        check(sh("systemctl is-active skillfish-fand.service", 10)[1].strip() == "active",
              "skillfish-fand not running after the test")
    return "%s rewritten through the helper, values unchanged" % os.path.basename(path)


# ---- long ones -------------------------------------------------------------
def t_cu_test(ctx, h):
    _bc(ctx)
    r = _ok(h("cu-test", timeout=900), "cu-test")
    return "CU test: %s" % json.dumps(r)[:200]


def t_test_gpu(ctx, h):
    g = _gov(ctx, h)
    gpu = _ok(h("get"), "get")["data"]["gpu"]
    with preserved(_gov_conf_file()):
        r = _ok(h("test-gpu", maxmhz=gpu["max_mhz"], maxmv=gpu["max_mv"], timeout=400), "test-gpu")
        check(h("gov-get")["conf"].get("freq_max") == g["conf"].get("freq_max"), "ceiling changed")
    return "current ceiling trialled and kept: %s" % json.dumps(r.get("bench", {}))[:160]


def t_test_cpu(ctx, h):
    _bc(ctx)
    c = _cpu_now(h)
    with preserved(*[p for p in (_const("OC_CONF"),) if p]):
        r = _ok(h("test-cpu", mhz=c["frequency"], scale=c["scale"], temp=c["max_temperature"], timeout=300),
                "test-cpu")
        check(_cpu_now(h) == c, "CPU setting changed by test-cpu")
    return "current CPU setting tested: %s" % json.dumps(r)[:160]


def t_suggest_uv(ctx, h):
    _bc(ctx)
    c = _cpu_now(h)
    with preserved(*[p for p in (_const("OC_CONF"),) if p]):
        r = _ok(h("suggest-uv", mhz=c["frequency"], timeout=900), "suggest-uv")
        check(_cpu_now(h) == c, "CPU setting not restored after suggest-uv")
    return "suggested scale %s at %s MHz, setting restored" % (r.get("suggested_scale"), c["frequency"])


WRITE_TESTS = {
    "cpu-cores-set": t_cores, "cpu-smt": t_smt, "thermal-guard": t_thermal,
    "gov-set": t_gov_set, "gov-prova": lambda ctx, h: t_gov_trial(ctx, h, "gov-annulla"),
    "gov-annulla": lambda ctx, h: t_gov_trial(ctx, h, "gov-annulla"),
    "gov-conferma": lambda ctx, h: t_gov_trial(ctx, h, "gov-conferma"),
    "apply-gpu": t_apply_gpu, "gov-attiva": t_gov_toggle,
    "apply-cpu": lambda ctx, h: t_cpu(ctx, h, "apply-cpu"),
    "persist-cpu": lambda ctx, h: t_cpu(ctx, h, "persist-cpu"),
    "cpu-volatile": lambda ctx, h: t_cpu(ctx, h, "cpu-volatile"),
    "cu-apply": t_cu_apply, "cu-keep-boot": t_cu_keep_boot, "scx-set": t_scx, "scx-azzera": t_scx_reset,
    "mesa-sistema-set": t_mesa, "unsloth-conf-set": t_unsloth_conf, "gddr6": t_gddr6,
    "servizio": t_service, "bench-cpu": t_bench_cpu, "bench-gpu": t_bench_gpu,
    "snapshot": t_snapshot,
    "cpu-gov-set": t_cpu_gov,
    "ventola": lambda ctx, h: "%s; %s" % (t_fan(ctx, h, "scrivi", "/etc/skillfish/ventola.json"),
                                           t_fan(ctx, h, "etichette", "/etc/skillfish/sensori.json")),
}
LONG_TESTS = {"cu-test": t_cu_test, "test-gpu": t_test_gpu, "test-cpu": t_test_cpu, "suggest-uv": t_suggest_uv}


def run(ctx):
    if not os.path.exists(HELPER):
        ctx.add("cc-helper installed", "fail", "%s missing" % HELPER)
        return
    ctx.run("cc-helper: every command classified", t_command_coverage, ctx)
    h = Helper()
    try:
        for cmd, kind in coverage.CC_COMMANDS.items():
            name = "cc-helper %s" % cmd
            if kind == "read":
                ctx.run(name, t_read, ctx, h, cmd)
            elif kind == "write":
                fn = WRITE_TESTS.get(cmd)
                if fn is None:
                    ctx.add(name, "fail", "classified as write but no test in checks_helper.WRITE_TESTS")
                else:
                    ctx.run(name, fn, ctx, h)
            elif kind == "long":
                if ctx.long:
                    ctx.run(name, LONG_TESTS[cmd], ctx, h)
                else:
                    ctx.add(name, "skip", "slow: runs with --long")
            else:
                ctx.add(name, "manual", kind[1])
            if h.p.poll() is not None:
                # the helper died: say so once and start a new one for the rest
                ctx.add("cc-helper survived %s" % cmd, "fail", "exit %s" % h.p.returncode)
                h = Helper()
    finally:
        h.close()
