#!/usr/bin/env python3
"""Refuse to publish what the release check has not passed.

    gate.py <file.deb> [...]

Called by scripts/pubblica-apt.sh before anything leaves the build VM. For
every package it wants:
  - the report of each machine in hosts.conf for that version, with no failure;
  - the package's sha256 in the list release-check.sh wrote, so the bytes going
    out are the bytes that were tested, not a rebuild made afterwards.

The only way past it is SKILLFISH_UNTESTED="<reason>", which prints the reason
in capitals and appends it to ~/release-reports/<version>/UNTESTED so the
exception is on record.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.expanduser("~/release-reports")


def kinds():
    out = []
    for line in open(os.path.join(HERE, "hosts.conf")):
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line.split()[0])
    return out


def version_of(deb):
    m = re.match(r"[^_]+_([^_]+)_[^_]+\.deb$", os.path.basename(deb))
    return m.group(1) if m else None


def main(debs):
    problems = []
    for deb in debs:
        ver = version_of(deb)
        d = os.path.join(REPORTS, ver or "?")
        tested = {}
        try:
            for line in open(os.path.join(d, "debs.sha256")):
                h, name = line.split()
                tested[name] = h
        except OSError:
            # no fingerprint list: this version was never checked
            pass
        h = hashlib.sha256(open(deb, "rb").read()).hexdigest()
        if tested.get(os.path.basename(deb)) != h:
            # an upstream-versioned package (vkpeak, Mesa...) is tested inside
            # an app release: look for it in any report directory
            found = False
            for other in os.listdir(REPORTS) if os.path.isdir(REPORTS) else []:
                try:
                    lines = open(os.path.join(REPORTS, other, "debs.sha256")).read().split("\n")
                except OSError:
                    continue
                if "%s  %s" % (h, os.path.basename(deb)) in lines:
                    d, found = os.path.join(REPORTS, other), True
                    break
            if not found:
                problems.append("%s: these bytes were never release-checked" % os.path.basename(deb))
                continue
        for k in kinds():
            try:
                r = json.load(open(os.path.join(d, "%s.json" % k)))
            except (OSError, ValueError):
                problems.append("%s: no %s report in %s" % (os.path.basename(deb), k, d))
                continue
            if r.get("counts", {}).get("fail"):
                problems.append("%s: the %s check has %d failures" % (os.path.basename(deb), k, r["counts"]["fail"]))
    problems = sorted(set(problems))
    if not problems:
        print(">>> release check: every package passed on every machine")
        return 0
    reason = os.environ.get("SKILLFISH_UNTESTED", "").strip()
    print("\n".join("    " + p for p in problems), file=sys.stderr)
    if reason:
        print("\n!!! PUBLISHING UNTESTED PACKAGES: %s\n" % reason.upper(), file=sys.stderr)
        for deb in debs:
            d = os.path.join(REPORTS, version_of(deb) or "unknown")
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "UNTESTED"), "a") as f:
                f.write("%s  %s\n" % (os.path.basename(deb), reason))
        return 0
    print("\nNot published. Run tests/release/release-check.sh <version> first "
          "(or set SKILLFISH_UNTESTED=\"<reason>\" to publish anyway, on record).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
