#!/usr/bin/env python3
"""SkillFishOS release check: run on a test machine, as root, after the
packages of the release have been installed on it.

    python3 run.py --kind bc250|x64 --version 26.09.44 [--long] [--report out.json]

WHY THIS EXISTS. Between 11/09 and 22/09/2026 three bugs reached users in
packages that had passed CI: every write to /sys from the Control Center failed
(#93), vkpeak was looked for only where our development boards keep it (#91),
and an update removed the desktop (#87). Each one was a button nobody pressed
on a real installation. This suite presses them.

THE RULE IT ENFORCES. Everything we ship is covered: every executable in our
packages, every command of skillfish-cc-helper and every systemd unit. Coverage
is read from the installed system, not from a list someone must remember to
update: an executable or a helper command with no entry in coverage.py FAILS
the run. An entry may say "manual" with a reason, and the report prints those,
so what was not tested is always stated, never implied.

Writes are tested for real and put back: read the value, change it, read it
back, restore it, read it again. Files a test may touch are saved first and
restored byte for byte whatever happens.
"""
import argparse
import json
import os
import platform
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from common import Skip  # noqa: E402
import checks_system    # noqa: E402
import checks_exec      # noqa: E402
import checks_helper    # noqa: E402
import checks_gui       # noqa: E402

MODULES = (checks_system, checks_exec, checks_helper, checks_gui)


class Ctx:
    def __init__(self, kind, version, long_tests):
        self.kind = kind
        self.version = version
        self.long = long_tests
        self.results = []

    def add(self, name, status, detail=""):
        self.results.append({"name": name, "status": status, "detail": str(detail)[:2000]})
        mark = {"pass": "PASS", "fail": "FAIL", "skip": "skip", "manual": "MANUAL"}[status]
        print("%-6s %s%s" % (mark, name, (" - " + str(detail).splitlines()[0][:160]) if detail else ""),
              flush=True)

    def run(self, name, fn, *args):
        """Run one test function. It returns a detail string on success,
        raises Skip to skip, raises anything else to fail."""
        try:
            detail = fn(*args)
            self.add(name, "pass", detail or "")
        except Skip as s:
            self.add(name, "skip", str(s))
        except Exception as e:
            self.add(name, "fail", "%s: %s\n%s" % (type(e).__name__, e, traceback.format_exc()[-1500:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, choices=("bc250", "x64"))
    ap.add_argument("--version", required=True)
    ap.add_argument("--long", action="store_true", help="also the slow benchmarks (cu-test, test-gpu)")
    ap.add_argument("--report", default="/root/release-check-report.json")
    a = ap.parse_args()
    if os.geteuid() != 0:
        sys.exit("run it as root")
    ctx = Ctx(a.kind, a.version, a.long)
    t0 = time.time()
    for m in MODULES:
        try:
            m.run(ctx)
        except Exception as e:
            # a module that dies must not hide the others
            ctx.add("%s (module)" % m.__name__, "fail", "%s: %s" % (type(e).__name__, e))
    # every test that changes the machine must have put it back
    ctx.run("CPUs: all online after the check", checks_system.t_all_cpus_online, ctx)
    counts = {s: sum(1 for r in ctx.results if r["status"] == s) for s in ("pass", "fail", "skip", "manual")}
    report = {"version": a.version, "kind": a.kind, "host": platform.node(), "kernel": platform.release(),
              "started": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t0)),
              "seconds": int(time.time() - t0), "long": a.long, "counts": counts, "results": ctx.results}
    with open(a.report, "w") as f:
        json.dump(report, f, indent=1)
    print("\n%s on %s (%s): %d passed, %d FAILED, %d skipped, %d manual, %d s"
          % (a.version, report["host"], a.kind, counts["pass"], counts["fail"], counts["skip"],
             counts["manual"], report["seconds"]))
    sys.exit(1 if counts["fail"] else 0)


if __name__ == "__main__":
    main()
