# Release check

Nothing is published before it has run on a real BC-250 and on a real x64
install. `scripts/pubblica-apt.sh` enforces it: it refuses a package whose
exact bytes were not checked, or a version with a failure on any machine.

## Why

Between 11 and 22 September 2026 three bugs reached users in packages that had
passed CI:

- every write to `/sys` from the Control Center failed with EACCES (#93);
- the GPU and CU tests looked for vkpeak only where our development boards
  keep it (#91);
- an update removed the whole desktop (#87).

Each one was a button nobody pressed on a real installation. CI builds and
lints; it cannot press the button that changes the CPU cores of a BC-250.

## How to run it

On the build VM, after `scripts/build-debs-ci.sh <version>`:

```
tests/release/release-check.sh <version> [--long] [extra.deb ...]
```

It installs `/tmp/sfx-debs/out/*_<version>_all.deb`, plus any extra package
given (skillfish-vkpeak, the governor, our Mesa, the encoder), on every
machine in `hosts.conf`. Then it runs `suite/run.py` there as root and brings
the reports back to `~/release-reports/<version>/`. `--long` adds the
benchmarks that take minutes (cu-test, test-gpu, test-cpu, suggest-uv).

Then publish as usual. `pubblica-apt.sh` calls `gate.py` first.

## What it checks

- **The system**: every package at the release version, `dpkg --audit` clean,
  `apt-get check` clean, `dpkg -V` clean apart from conffiles, the desktop
  guard installed and protected, no failed unit, every enabled service
  running, AppStream cards valid, every menu entry pointing at a real
  program, and a full-upgrade that would remove nothing of the desktop.
- **Every executable we ship**: a static check (a Python compile, `bash -n`,
  or no missing shared library for a binary), plus what `suite/coverage.py`
  says: run it and check the output, check its unit, open its window, or
  `manual` with a reason.
- **Every command of skillfish-cc-helper**: reads must answer; writes are a
  round trip. Read, change, read back, put back, read again. Files a write
  touches are saved and restored byte for byte. Cores and SMT go off and on,
  the governor's curve is rewritten and trialled, the scheduler and our Mesa
  are switched and switched back, the CPU benchmark must restore the
  governors, and vkpeak must reach 9000 GFLOPS on a BC-250.
- **Every window** opens offscreen and is still running after 12 seconds,
  with no traceback and no core dump.
- **No CPU is left offline**, before and after.

## The rule that keeps it complete

Coverage is read from the installed system, not from a list. An executable in
our packages, or a command in skillfish-cc-helper, with no entry in
`suite/coverage.py` **fails the check**. A new program cannot ship untested
by accident. It can ship `manual`, with the reason written down and printed
in every report.

## Publishing anyway

```
SKILLFISH_UNTESTED="the reason" scripts/pubblica-apt.sh ...
```

prints the reason in capitals and appends it to
`~/release-reports/<version>/UNTESTED`. It is for the day a test machine is
broken, not for skipping a failure.

## The machines

`hosts.conf`: the BC-250 test board and the x64 test VM, both reached as root
with the build VM's ssh key. They must be test machines: the check switches
real hardware settings off and on.
