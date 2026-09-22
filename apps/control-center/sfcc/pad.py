"""Gamepad navigation for the Control Center.

A controller is enough to drive the whole window: the D-pad or the left stick
moves the keyboard focus, A activates, B goes back (Escape), LB/RB switch the
section, Start opens the Status page. Everything is turned into the key
presses the widgets already understand, so no page needs to know about pads.

Reads /dev/input through python3-evdev; when the module or the device is
missing the window simply works without it. Hot-plug: the scan is repeated
every few seconds while no pad is attached.
"""
import threading
import time

from PyQt6.QtCore import QEvent, QObject, Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication

try:
    import evdev
    from evdev import ecodes as E
except ImportError:  # the package is only Recommended
    evdev = None
    E = None

# stick: beyond this fraction of the full range it counts as a press
SOGLIA = 0.55
# repeat while held (seconds)
PRIMA_RIPETIZIONE = 0.45
RIPETIZIONE = 0.12


def _e_pad(dev):
    """A gamepad: pad buttons AND sticks or a hat.

    ydotoold's virtual device declares every button there is, BTN_SOUTH
    included, and has no axes. It was taken for a pad on every machine that
    runs ydotool (both test machines do): the window listened to it, and an
    automation typing through ydotool could have moved the focus."""
    if "ydotool" in (dev.name or "").lower():
        return False
    caps = dev.capabilities()
    keys = caps.get(E.EV_KEY, [])
    if E.BTN_SOUTH not in keys and E.BTN_GAMEPAD not in keys:
        return False
    return bool(caps.get(E.EV_ABS))


class Pad(QObject):
    """Emits `tasto(nome)` from a reader thread; the window maps names to keys."""

    tasto = pyqtSignal(str)
    collegato = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._vivo = True
        self._thread = None
        self.nome = ""
        if evdev is not None:
            app = QApplication.instance()
            if app is not None:
                app.aboutToQuit.connect(self.ferma)
            self._thread = threading.Thread(target=self._giro, daemon=True)
            self._thread.start()

    def ferma(self):
        self._vivo = False

    def _emetti(self, segnale, *valori):
        """Emit from the reader thread, unless the window is already gone.

        The thread outlives the Qt object when the window closes: emitting then
        raised "wrapped C/C++ object of type Pad has been deleted", printed as a
        traceback on every exit on a machine with a pad-like input device. The
        release check found it by opening the window offscreen (22/09/2026).
        """
        if not self._vivo:
            return False
        try:
            segnale.emit(*valori)
            return True
        except RuntimeError:
            # the C++ side of this object was deleted: stop reading
            self._vivo = False
            return False

    # ---- reader thread ---------------------------------------------------------
    def _trova(self):
        for p in evdev.list_devices():
            try:
                d = evdev.InputDevice(p)
                if _e_pad(d):
                    return d
                d.close()
            except OSError:
                continue
        return None

    def _giro(self):
        while self._vivo:
            dev = self._trova()
            if dev is None:
                time.sleep(3)
                continue
            self.nome = dev.name
            self._emetti(self.collegato, True)
            try:
                self._leggi(dev)
            except OSError:
                # the pad was unplugged mid-read: the outer loop scans for another one
                pass
            finally:
                try:
                    dev.close()
                except OSError:
                    # already gone: nothing left to close
                    pass
            self.nome = ""
            self._emetti(self.collegato, False)

    def _leggi(self, dev):
        assi = {}
        for code, info in dev.capabilities().get(E.EV_ABS, []):
            assi[code] = (info.min, info.max)
        premuti = {}   # direction name -> time of last emission
        stato = {}     # direction name -> held?

        def direzione(nome, giu):
            if giu and not stato.get(nome):
                stato[nome] = True
                premuti[nome] = time.monotonic() + PRIMA_RIPETIZIONE
                self._emetti(self.tasto, nome)
            elif not giu:
                stato[nome] = False

        def asse(code, val):
            lo, hi = assi.get(code, (-1, 1))
            mid = (lo + hi) / 2.0
            span = (hi - lo) / 2.0 or 1
            f = (val - mid) / span
            return f

        dev.grab = getattr(dev, "grab", None)  # never grab: the desktop keeps it
        while self._vivo:
            ev = dev.read_one()
            if ev is None:
                # key repeat for held directions
                now = time.monotonic()
                for nome, held in stato.items():
                    if held and now >= premuti.get(nome, now):
                        premuti[nome] = now + RIPETIZIONE
                        self._emetti(self.tasto, nome)
                time.sleep(0.02)
                continue
            if ev.type == E.EV_KEY:
                giu = ev.value == 1
                if ev.value == 2:
                    continue
                code = ev.code
                if code in (E.BTN_SOUTH,):
                    giu and self._emetti(self.tasto, "ok")
                elif code in (E.BTN_EAST,):
                    giu and self._emetti(self.tasto, "indietro")
                elif code in (E.BTN_TL,):
                    giu and self._emetti(self.tasto, "sezione-prec")
                elif code in (E.BTN_TR,):
                    giu and self._emetti(self.tasto, "sezione-succ")
                elif code in (E.BTN_START,):
                    giu and self._emetti(self.tasto, "stato")
                elif code in (E.BTN_DPAD_UP,):
                    direzione("su", giu)
                elif code in (E.BTN_DPAD_DOWN,):
                    direzione("giu", giu)
                elif code in (E.BTN_DPAD_LEFT,):
                    direzione("sinistra", giu)
                elif code in (E.BTN_DPAD_RIGHT,):
                    direzione("destra", giu)
            elif ev.type == E.EV_ABS:
                if ev.code == E.ABS_HAT0Y:
                    direzione("su", ev.value < 0)
                    direzione("giu", ev.value > 0)
                elif ev.code == E.ABS_HAT0X:
                    direzione("sinistra", ev.value < 0)
                    direzione("destra", ev.value > 0)
                elif ev.code == E.ABS_Y:
                    f = asse(ev.code, ev.value)
                    direzione("su", f < -SOGLIA)
                    direzione("giu", f > SOGLIA)
                elif ev.code == E.ABS_X:
                    f = asse(ev.code, ev.value)
                    direzione("sinistra", f < -SOGLIA)
                    direzione("destra", f > SOGLIA)


# what each pad action becomes on the keyboard
TASTI = {
    "su": (Qt.Key.Key_Backtab, Qt.KeyboardModifier.ShiftModifier),
    "giu": (Qt.Key.Key_Tab, Qt.KeyboardModifier.NoModifier),
    "sinistra": (Qt.Key.Key_Left, Qt.KeyboardModifier.NoModifier),
    "destra": (Qt.Key.Key_Right, Qt.KeyboardModifier.NoModifier),
    "ok": (Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier),
    "indietro": (Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier),
}


def invia_tasto(nome):
    """Deliver the key press (and release) to the widget that has the focus."""
    w = QApplication.focusWidget()
    if w is None:
        return
    key, mod = TASTI[nome]
    QApplication.postEvent(w, QKeyEvent(QEvent.Type.KeyPress, key, mod))
    QApplication.postEvent(w, QKeyEvent(QEvent.Type.KeyRelease, key, mod))
