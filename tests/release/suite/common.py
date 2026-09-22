"""Small shared pieces of the release check."""
import contextlib
import os
import subprocess


class Skip(Exception):
    """A test that does not apply on this machine."""


def sh(cmd, timeout=60, env=None, input_text=None):
    """Run a shell command, return (rc, stdout, stderr). Never raises on a
    non-zero exit: the caller decides what counts as a failure."""
    e = dict(os.environ)
    if env:
        e.update(env)
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout,
                           env=e, input=input_text)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as t:
        out = t.stdout.decode() if isinstance(t.stdout, bytes) else (t.stdout or "")
        err = t.stderr.decode() if isinstance(t.stderr, bytes) else (t.stderr or "")
        return 124, out, err


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def our_packages():
    """Installed packages that are ours: skillfish-*, skillfishos-*."""
    rc, out, _ = sh("dpkg-query -W -f='${db:Status-Abbrev} ${Package} ${Version}\\n'", 30)
    pk = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0].startswith("ii") and parts[1].startswith(("skillfish-", "skillfishos-")):
            pk[parts[1]] = parts[2]
    return pk


def files_of(pkg):
    rc, out, _ = sh("dpkg -L %s" % pkg, 30)
    return [l for l in out.splitlines() if l.startswith("/")]


@contextlib.contextmanager
def preserved(*paths):
    """Save files byte for byte and put them back whatever happens inside.
    A file that did not exist before is removed afterwards."""
    saved = {}
    for p in paths:
        try:
            with open(p, "rb") as f:
                saved[p] = f.read()
        except FileNotFoundError:
            saved[p] = None
    try:
        yield
    finally:
        for p, data in saved.items():
            try:
                if data is None:
                    if os.path.exists(p):
                        os.unlink(p)
                else:
                    with open(p, "wb") as f:
                        f.write(data)
            except OSError:
                # the report will show the test that was running; nothing else to do here
                pass
