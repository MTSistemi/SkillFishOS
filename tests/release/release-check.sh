#!/bin/bash
# Install a release on the test machines and run the release check on them.
#
#     tests/release/release-check.sh <version> [--long] [--only bc250|x64] [extra.deb ...]
#
# Takes /tmp/sfx-debs/out/*_<version>_all.deb (what scripts/build-debs-ci.sh
# just built) plus any extra .deb given on the command line (skillfish-vkpeak,
# the governor, our Mesa...), installs them on every machine in hosts.conf,
# runs suite/run.py there as root and brings the reports back to
# ~/release-reports/<version>/. It also records the sha256 of every package it
# tested: scripts/pubblica-apt.sh refuses to publish a package whose bytes are
# not in that list, or a version whose reports are missing or have a failure.
#
# The machines are reached as root with the build VM's ssh key. They must be
# test machines: the check switches cores, SMT, the governor, the scheduler and
# our Mesa off and on, and puts each one back.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
VER="${1:?usage: $0 <version> [--long] [--only kind] [extra.deb ...]}"
shift
LONG=""
ONLY=""
EXTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    --long) LONG="--long" ;;
    --only) ONLY="$2"; shift ;;
    *.deb) EXTRA+=("$1") ;;
    *) echo "unknown argument $1" >&2; exit 2 ;;
  esac
  shift
done

DEBS=( /tmp/sfx-debs/out/*_"${VER}"_all.deb "${EXTRA[@]}" )
[ -f "${DEBS[0]}" ] || { echo "no packages for $VER in /tmp/sfx-debs/out: build them first" >&2; exit 1; }
OUT="$HOME/release-reports/$VER"
mkdir -p "$OUT"
sha256sum "${DEBS[@]}" | sed 's|  .*/|  |' | sort -k2 > "$OUT/debs.sha256"
echo ">>> ${#DEBS[@]} packages, fingerprints in $OUT/debs.sha256"

SSH=(ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new)
fail=0
while read -r kind target <&3; do
  case "$kind" in ''|\#*) continue ;; esac
  [ -n "$ONLY" ] && [ "$ONLY" != "$kind" ] && continue
  echo
  echo "================ $kind  $target ================"
  if ! "${SSH[@]}" "$target" true 2>/dev/null; then
    echo "cannot reach $target as root with the build key" >&2
    printf '{"version":"%s","kind":"%s","counts":{"fail":1},"results":[{"name":"reach the machine","status":"fail","detail":"ssh %s failed"}]}\n' \
      "$VER" "$kind" "$target" > "$OUT/$kind.json"
    fail=1; continue
  fi
  "${SSH[@]}" "$target" "rm -rf /root/release-check && mkdir -p /root/release-check/debs"
  scp -q -o BatchMode=yes "${DEBS[@]}" "$target:/root/release-check/debs/" || { fail=1; continue; }
  scp -q -o BatchMode=yes -r "$HERE/suite" "$target:/root/release-check/" || { fail=1; continue; }
  echo ">>> installing"
  # A machine that is not a BC-250 still gets every package: they are meant
  # to install anywhere and switch themselves off where they don't apply.
  if ! "${SSH[@]}" "$target" "cd /root/release-check/debs && DEBIAN_FRONTEND=noninteractive \
        apt-get install -y -q --allow-downgrades -o Dpkg::Options::=--force-confold ./*.deb" \
        > "$OUT/$kind-install.log" 2>&1; then
    tail -20 "$OUT/$kind-install.log"
    printf '{"version":"%s","kind":"%s","counts":{"fail":1},"results":[{"name":"install the packages","status":"fail","detail":"see %s-install.log"}]}\n' \
      "$VER" "$kind" "$kind" > "$OUT/$kind.json"
    fail=1; continue
  fi
  grep -E "^[0-9]+ upgraded" "$OUT/$kind-install.log"
  echo ">>> checking"
  "${SSH[@]}" "$target" "python3 /root/release-check/suite/run.py --kind $kind --version $VER $LONG \
        --report /root/release-check/report.json" | tee "$OUT/$kind.log" | grep -E "^(FAIL|MANUAL)|passed,"
  scp -q -o BatchMode=yes "$target:/root/release-check/report.json" "$OUT/$kind.json" || fail=1
  python3 -c "import json,sys; r=json.load(open(sys.argv[1])); sys.exit(1 if r['counts'].get('fail') else 0)" \
    "$OUT/$kind.json" || fail=1
done 3< "$HERE/hosts.conf"
# ⚠️ The machine list is read on fd 3, not stdin: ssh inside the loop reads
# stdin and swallowed the rest of hosts.conf, so the first run of 26.09.45
# checked the BC-250 only and then said "passed on every machine".

# Every machine in hosts.conf must have left a report for this version.
while read -r kind target <&4; do
  case "$kind" in ''|\#*) continue ;; esac
  [ -n "$ONLY" ] && [ "$ONLY" != "$kind" ] && continue
  [ -f "$OUT/$kind.json" ] && [ "$OUT/$kind.json" -nt "$OUT/debs.sha256" ]     || { echo "no fresh report from $kind ($target)" >&2; fail=1; }
done 4< "$HERE/hosts.conf"

echo
if [ "$fail" = 0 ]; then
  echo ">>> $VER: release check passed on every machine. Reports in $OUT"
else
  echo ">>> $VER: release check FAILED. Reports in $OUT" >&2
fi
exit "$fail"
