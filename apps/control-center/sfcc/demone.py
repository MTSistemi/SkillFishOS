# -*- coding: utf-8 -*-
"""The privileged helper, started once and talked to over JSON lines.

Pages that only READ (status, monitor, fan readings) never start it: the
password is asked the first time something has to be WRITTEN as root, and
then kept for the session by polkit (auth_admin_keep). One helper for every
section instead of one per app, which is the point of a single window.
"""
import json
import subprocess
import threading

from PyQt6.QtCore import QThread, pyqtSignal

from .comune import HELPER, L


class Demone:
    def __init__(self):
        self.p = None
        self.lock = threading.Lock()
        self.rifiutato = False

    def attivo(self):
        return self.p is not None and self.p.poll() is None

    def avvia(self):
        """Start the helper through pkexec. False if the user cancelled."""
        if self.attivo():
            return True
        if self.rifiutato:
            return False
        try:
            self.p = subprocess.Popen(["pkexec", HELPER], stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                      text=True, bufsize=1)
            riga = self.p.stdout.readline()
            if not riga:
                self.p = None
                self.rifiutato = True
                return False
            return json.loads(riga).get("ready", False)
        except Exception:
            self.p = None
            self.rifiutato = True
            return False

    def cmd(self, timeout=None, **kw):
        """Send one command and wait for its reply. Never raises."""
        if not self.avvia():
            return {"ok": False, "err": L("autenticazione annullata", "authentication cancelled"),
                    "annullato": True}
        with self.lock:
            try:
                self.p.stdin.write(json.dumps(kw) + "\n")
                self.p.stdin.flush()
                riga = self.p.stdout.readline()
                if not riga:
                    self.p = None
                    return {"ok": False, "err": L("helper terminato", "helper exited")}
                return json.loads(riga)
            except Exception as e:
                self.p = None
                return {"ok": False, "err": str(e)}

    def chiudi(self):
        if self.attivo():
            try:
                self.p.stdin.write('{"cmd":"quit"}\n')
                self.p.stdin.flush()
                self.p.wait(timeout=3)
            except Exception:
                try:
                    self.p.kill()
                except Exception:
                    # already dead: nothing left to kill
                    pass
        self.p = None


class Lavoro(QThread):
    """Run a function off the GUI thread and hand its result back."""
    finito = pyqtSignal(object)

    def __init__(self, fn, parent=None):
        super().__init__(parent)
        self.fn = fn

    def run(self):
        try:
            r = self.fn()
        except Exception as e:
            r = {"ok": False, "err": str(e)}
        self.finito.emit(r)


_lavori = []


def in_sfondo(fn, poi, padre=None):
    """Start fn in a thread; call poi(result) on the GUI thread when done."""
    t = Lavoro(fn, padre)
    _lavori.append(t)

    def _fine(r):
        try:
            poi(r)
        finally:
            if t in _lavori:
                _lavori.remove(t)
    t.finito.connect(_fine)
    t.start()
    return t
