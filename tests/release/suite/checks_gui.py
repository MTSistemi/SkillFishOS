"""Every window we ship opens: started offscreen, it must still be running
after a few seconds, with no Python traceback and no core dump.

This does not press buttons. The buttons that change the machine all end in
skillfish-cc-helper, which checks_helper exercises command by command; what
this catches is a window that dies on start (issue #73 was a core dump from an
exception inside a Qt slot).
"""
import os
import time

import coverage
from common import check, sh

SECONDS = 12


def t_window(ctx, path):
    rt = "/tmp/release-check-xdg"
    os.makedirs(rt, mode=0o700, exist_ok=True)
    since = time.strftime("%Y-%m-%d %H:%M:%S")
    rc, out, err = sh("timeout %d %s" % (SECONDS, path), SECONDS + 20,
                      env={"QT_QPA_PLATFORM": "offscreen", "XDG_RUNTIME_DIR": rt,
                           "QT_LOGGING_RULES": "*.debug=false", "SKILLFISH_RELEASE_CHECK": "1"})
    text = out + err
    check("Traceback (most recent call last)" not in text, "Python traceback:\n" + text[-1500:])
    check(rc in (0, 124), "exited with %d before %d s:\n%s" % (rc, SECONDS, text[-800:]))
    rc2, cores, _ = sh("coredumpctl list --no-legend --since '%s' 2>/dev/null" % since, 20)
    check(not cores.strip(), "core dump while it ran:\n" + cores[-600:])
    return "still running after %d s" % SECONDS if rc == 124 else "ran and exited cleanly"


def run(ctx):
    for path, entry in sorted(coverage.EXECUTABLES.items()):
        if entry[0] != "gui":
            continue
        name = "window %s" % os.path.basename(path)
        if not os.path.exists(path):
            ctx.add(name, "skip", "not installed here")
            continue
        ctx.run(name, t_window, ctx, path)
