"""The installed system as a whole: packages, dpkg and apt, systemd units,
AppStream cards and menu entries."""
import os
import re

import coverage
from common import Skip, check, files_of, our_packages, read_text, sh

# Packages that carry an upstream version rather than ours (YY.MM.N).
UPSTREAM_VERSIONED = ("skillfish-vkpeak", "skillfish-mesa-gfx1013", "skillfish-vaapi-encoder",
                      "skillfish-vf-governor", "skillfishos-kernel")


def t_versions(ctx):
    pk = our_packages()
    check(pk, "no SkillFishOS package installed")
    ours = {p: v for p, v in pk.items() if not p.startswith(UPSTREAM_VERSIONED)
            and re.fullmatch(r"\d{2}\.\d{2}\.\d+", v)}
    behind = ["%s %s" % (p, v) for p, v in ours.items() if v != ctx.version]
    check(not behind, "not at %s: %s" % (ctx.version, ", ".join(sorted(behind))))
    return "%d packages at %s" % (len(ours), ctx.version)


def t_dpkg_audit(ctx):
    rc, out, err = sh("dpkg --audit", 60)
    check(not out.strip(), "dpkg --audit reports:\n" + out[:1000])
    return "clean"


def t_apt_check(ctx):
    rc, out, err = sh("apt-get check -q", 120)
    check(rc == 0, "apt-get check failed: " + (err or out)[-600:])
    return "ok"


def t_guard(ctx):
    pk = our_packages()
    check("skillfish-desktop-guard" in pk, "skillfish-desktop-guard is not installed (issue #87)")
    rc, out, _ = sh("dpkg-query -W -f='${Protected}' skillfish-desktop-guard", 10)
    check(out.strip() == "yes", "skillfish-desktop-guard is not Protected")
    return "installed and protected"


def t_files_intact(ctx):
    """dpkg -V: a file of ours that differs from the package is either a
    conffile the user may change, or something that should not happen."""
    bad = []
    for p in our_packages():
        rc, out, _ = sh("dpkg -V %s" % p, 120)
        for line in out.splitlines():
            # "??5??????   /usr/..." or "??5?????? c /etc/..." (c = conffile)
            if len(line) > 11 and line[9:12].strip() == "c":
                continue
            if line.strip():
                bad.append("%s: %s" % (p, line.strip()))
    check(not bad, "files that differ from their package:\n" + "\n".join(bad[:40]))
    return "all files match their packages"


def _our_units():
    units = set()
    for p in our_packages():
        for f in files_of(p):
            if re.search(r"/systemd/(system|user)/[^/]+\.(service|timer|path|socket|mount)$", f) \
                    and "/systemd/user/" not in f:
                units.add(os.path.basename(f))
    return sorted(units)


def t_units(ctx):
    """None of our units failed, and every enabled service whose conditions
    hold is running (oneshots count if they exited cleanly)."""
    units = _our_units()
    check(units, "no systemd units found in our packages")
    failed, dead = [], []
    for u in units:
        rc, out, _ = sh("systemctl show %s -p LoadState -p ActiveState -p SubState -p UnitFileState "
                        "-p Type -p ConditionResult -p Result -p RemainAfterExit" % u, 20)
        st = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
        if st.get("LoadState") != "loaded":
            continue
        if st.get("ActiveState") == "failed":
            failed.append("%s (%s)" % (u, st.get("Result")))
            continue
        # A service that chose to exit with success is fine: skillfish-unsloth
        # does exactly that on a machine without Unsloth, on purpose.
        if u.endswith(".service") and st.get("UnitFileState") == "enabled" \
                and st.get("ConditionResult") != "no" and st.get("Type") != "oneshot" \
                and st.get("ActiveState") not in ("active", "activating", "reloading") \
                and st.get("Result") != "success":
            dead.append("%s (%s/%s)" % (u, st.get("ActiveState"), st.get("SubState")))
    check(not failed, "failed units: " + ", ".join(failed))
    check(not dead, "enabled but not running: " + ", ".join(dead))
    return "%d units, none failed" % len(units)


GUARD = re.compile(r"^if \[ -d /run/systemd/system \]")
ENABLE = re.compile(r"\b(systemctl( --global)?|deb-systemd-helper) (--\S+ )*enable\b")


def _enables_outside_guard(script):
    """Unit names a maintainer script enables where a chroot would too.

    Enabling only writes symlinks and works without a running systemd;
    `[ -d /run/systemd/system ]` is false in the ISO chroot, so an enable
    written inside that test never reaches an image (issue #98)."""
    unit = r"[\w@.-]+\.(?:service|timer|path|socket)"
    found, stack, loop = set(), [], []
    for raw in script.replace("\\\n", " ").splitlines():
        s = raw.strip()
        if s.startswith("#"):
            continue
        one_line = s.startswith("if ") and re.search(r"\bfi\s*$", s)
        if s.startswith("if ") and not one_line:
            stack.append(bool(GUARD.match(s)))
        elif s == "fi" or s.startswith("fi "):
            if stack:
                stack.pop()
        if s.startswith("for "):
            # `for u in a.service b.service; do systemctl enable "$u"; done`
            loop = re.findall(unit, s)
        elif s.startswith("done"):
            loop = []
        if ENABLE.search(s) and not any(stack) and not (one_line and GUARD.match(s)):
            found.update(re.findall(unit, s))
            if '"$' in s or " $" in s:
                found.update(loop)
    return found


def t_units_enabled_by_package(ctx):
    """Every unit we ship with an [Install] section is enabled by its package
    in a way that also works when the ISO is built, or coverage.py says who
    turns it on. The live check (systemctl is-enabled) could not catch #98:
    on both test machines the CU unit had been enabled by hand long ago."""
    bad, n = [], 0
    for p in sorted(our_packages()):
        script = ""
        for name in (p, p + ":amd64"):
            f = "/var/lib/dpkg/info/%s.postinst" % name
            if os.path.exists(f):
                script = read_text(f)
        enabled = _enables_outside_guard(script)
        for f in files_of(p):
            if not re.search(r"/systemd/system/[^/]+\.(service|timer|path|socket)$", f) or not os.path.isfile(f):
                continue
            if not re.search(r"^\[Install\]", read_text(f), re.M):
                continue
            u = os.path.basename(f)
            n += 1
            if u in coverage.UNITS_ON_DEMAND or u in enabled:
                continue
            bad.append("%s (%s)" % (u, p))
    check(not bad, "shipped with [Install] but not enabled by the package outside "
                   "`if [ -d /run/systemd/system ]` (an ISO would ship them off), and not "
                   "listed in coverage.UNITS_ON_DEMAND:\n  " + "\n  ".join(bad))
    return "%d units: each enabled by its package, or on demand for a stated reason" % n


def t_metainfo(ctx):
    if not os.path.exists("/usr/bin/appstreamcli"):
        raise Skip("appstreamcli not installed")
    bad, n = [], 0
    for p in our_packages():
        for f in files_of(p):
            if f.endswith(".metainfo.xml") and os.path.isfile(f):
                n += 1
                rc, out, err = sh("appstreamcli validate --no-net --pedantic=no %s" % f, 60)
                if rc != 0:
                    bad.append("%s: %s" % (f, (out + err).strip()[-300:]))
    check(not bad, "\n".join(bad))
    return "%d AppStream cards valid" % n


def t_desktop_entries(ctx):
    """Every menu entry we ship points at a program that exists."""
    bad, n = [], 0
    for p in our_packages():
        for f in files_of(p):
            if f.endswith(".desktop") and os.path.isfile(f):
                n += 1
                for line in read_text(f).splitlines():
                    if line.startswith(("Exec=", "TryExec=")):
                        prog = line.split("=", 1)[1].strip().split()[0] if line.split("=", 1)[1].strip() else ""
                        prog = prog.strip('"')
                        if prog.startswith("/"):
                            if not os.path.exists(prog):
                                bad.append("%s: %s" % (f, prog))
                        elif prog and sh("command -v %s" % prog, 10)[0] != 0:
                            bad.append("%s: %s not in PATH" % (f, prog))
    check(not bad, "menu entries pointing nowhere:\n" + "\n".join(bad))
    return "%d menu entries point at real programs" % n


def t_update_removes_nothing(ctx):
    """What the Hub would do next must not remove the desktop (issue #87)."""
    rc, out, err = sh("apt-get -s -o Debug::NoLocking=1 full-upgrade", 300)
    removed = re.findall(r"^Remv (\S+)", out, re.M)
    desk = [p for p in removed if re.match(r"(plasma-|kwin|sddm|dolphin|konsole|systemsettings|skillfish-)", p)]
    check(not desk, "a full-upgrade now would remove: " + ", ".join(desk))
    return "a full-upgrade would remove %d packages, none of the desktop or ours" % len(removed)


def t_all_cpus_online(ctx):
    """Nothing left switched off: by the user before the check, or by a test
    that did not put it back (a core stayed off on the x64 VM after the #93
    tests of 21/09, and every later count was off by one)."""
    rc, on, _ = sh("nproc", 10)
    rc, total, _ = sh("nproc --all", 10)
    check(on.strip() == total.strip(), "%s of %s CPUs online" % (on.strip(), total.strip()))
    return "%s of %s CPUs online" % (on.strip(), total.strip())


def run(ctx):
    ctx.run("CPUs: all online before the check", t_all_cpus_online, ctx)
    ctx.run("packages: all at the release version", t_versions, ctx)
    ctx.run("dpkg: audit clean", t_dpkg_audit, ctx)
    ctx.run("apt: dependencies consistent", t_apt_check, ctx)
    ctx.run("desktop guard installed and protected", t_guard, ctx)
    ctx.run("packages: files intact (dpkg -V)", t_files_intact, ctx)
    ctx.run("systemd: our units healthy", t_units, ctx)
    ctx.run("systemd: units enabled by their package, ISO included", t_units_enabled_by_package, ctx)
    ctx.run("AppStream cards valid", t_metainfo, ctx)
    ctx.run("menu entries point at real programs", t_desktop_entries, ctx)
    ctx.run("next update removes nothing of the desktop", t_update_removes_nothing, ctx)
