"""Every executable we ship: a static check for all of them, and the
functional probe coverage.py gives each one."""
import os
import re
import stat

import coverage
from common import Skip, check, files_of, our_packages, sh


def shipped_executables():
    """(package, path) for every executable regular file in our packages,
    documentation and maintainer scripts aside."""
    out = []
    for p in sorted(our_packages()):
        for f in files_of(p):
            if "/share/doc/" in f or "/__pycache__/" in f:
                continue
            try:
                st = os.lstat(f)
            except OSError:
                continue
            if stat.S_ISREG(st.st_mode) and st.st_mode & 0o111:
                out.append((p, f))
    return out


def static_check(path):
    with open(path, "rb") as fh:
        head = fh.read(256)
    if head.startswith(b"\x7fELF"):
        # A library under /opt finds its siblings through ld.so.conf.d or the
        # launcher's LD_LIBRARY_PATH (our Mesa does both): look where it looks.
        libdirs = ""
        if path.startswith("/opt/"):
            m = re.match(r"(/opt/[^/]+/lib(?:/[^/]+-linux-gnu)?)", path)
            if m:
                libdirs = "LD_LIBRARY_PATH=%s " % m.group(1)
        rc, out, err = sh("%sldd %s" % (libdirs, path), 30)
        missing = [l.strip() for l in out.splitlines() if "not found" in l]
        check(not missing, "missing libraries: " + ", ".join(missing))
        return "binary, libraries resolve"
    first = head.split(b"\n", 1)[0]
    if b"python" in first:
        src = open(path, encoding="utf-8", errors="replace").read()
        compile(src, path, "exec")
        return "python compiles"
    if first.startswith(b"#!") and (b"sh" in first):
        shell = "bash" if b"bash" in first else "sh"
        rc, out, err = sh("%s -n %s" % (shell, path), 30)
        check(rc == 0, "%s -n: %s" % (shell, err.strip()[-400:]))
        return "%s syntax ok" % shell
    return "not a script or binary we know how to check"


def probe(ctx, path, entry):
    kind = entry[0]
    if kind == "run":
        cmd, exp = entry[1], entry[2]
        if ctx.kind not in exp.get("kinds", coverage.ANY):
            raise Skip("only on %s" % ", ".join(exp["kinds"]))
        rc, out, err = sh(cmd, exp.get("timeout", 120))
        ok_rc = exp.get("rc_by_kind", {}).get(ctx.kind, exp.get("rc", [0]))
        check(rc in ok_rc, "exit %d (expected %s): %s" % (rc, ok_rc, (err or out).strip()[-400:]))
        want = exp.get("out_by_kind", {}).get(ctx.kind, exp.get("out"))
        if want:
            check(re.search(want, out + err), "output does not match /%s/: %s"
                  % (want, (out + err).strip()[-400:]))
        if ctx.kind in exp.get("empty_by_kind", ()):
            check(not out.strip(), "expected no output here, got: %s" % out.strip()[-300:])
        if path.endswith("/vkpeak"):
            m = re.search(r"fp32-scalar\s*=\s*([0-9.]+)", out)
            val = float(m.group(1)) if m else 0.0
            if ctx.kind == "bc250":
                check(val >= coverage.VKPEAK_MIN_BC250, "fp32-scalar %.0f GFLOPS, below %.0f"
                      % (val, coverage.VKPEAK_MIN_BC250))
            return "fp32-scalar %.2f GFLOPS" % val
        return "`%s` -> exit %d" % (cmd, rc)
    if kind == "unit":
        rc, out, _ = sh("systemctl show %s -p LoadState -p ActiveState -p ConditionResult" % entry[1], 20)
        st = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
        if st.get("LoadState") != "loaded":
            raise AssertionError("unit %s is not loaded (%s)" % (entry[1], st.get("LoadState")))
        return "unit %s %s" % (entry[1], st.get("ActiveState"))
    return None


def run(ctx):
    exes = shipped_executables()
    check_names = set()
    for pkg, path in exes:
        name = "exec %s" % path
        # Shared libraries carry the exec bit by convention; they are not
        # programs. Each one must still find every library it links against.
        if re.search(r"\.so(\.\d+)*$", path):
            ctx.run("library %s [static]" % path, static_check, path)
            continue
        entry = coverage.EXECUTABLES.get(path)
        if entry is None:
            ctx.add(name, "fail", "shipped by %s but has no entry in coverage.py: say how it is tested" % pkg)
            continue
        check_names.add(path)
        ctx.run(name + " [static]", static_check, path)
        if entry[0] in ("run", "unit"):
            ctx.run(name, probe, ctx, path, entry)
        elif entry[0] == "manual":
            ctx.add(name, "manual", entry[1])
        # gui and helper entries are exercised by their own modules
    # entries for things no longer shipped are harmless, but say so once
    stale = sorted(set(coverage.EXECUTABLES) - {p for _, p in exes})
    if stale:
        ctx.add("coverage.py entries for files not installed here", "skip", ", ".join(stale)[:1500])
