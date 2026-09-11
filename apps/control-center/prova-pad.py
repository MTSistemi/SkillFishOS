#!/usr/bin/env python3
"""Lab only: a virtual gamepad through uinput, to drive the Control Center
without a real controller.

    prova-pad.py <sequenza>      e.g.  "giu giu ok pausa2 rb rb sinistra b"

Names: su giu sinistra destra (D-pad), a b (south/east), lb rb, start,
levetta-giu/levetta-su (left stick), pausaN (N seconds).
"""
import sys
import time

from evdev import AbsInfo, UInput, ecodes as E

cap = {
    E.EV_KEY: [E.BTN_SOUTH, E.BTN_EAST, E.BTN_NORTH, E.BTN_WEST, E.BTN_TL, E.BTN_TR,
               E.BTN_START, E.BTN_SELECT, E.BTN_DPAD_UP, E.BTN_DPAD_DOWN,
               E.BTN_DPAD_LEFT, E.BTN_DPAD_RIGHT, E.BTN_GAMEPAD],
    E.EV_ABS: [
        (E.ABS_X, AbsInfo(0, -32768, 32767, 16, 128, 0)),
        (E.ABS_Y, AbsInfo(0, -32768, 32767, 16, 128, 0)),
        (E.ABS_HAT0X, AbsInfo(0, -1, 1, 0, 0, 0)),
        (E.ABS_HAT0Y, AbsInfo(0, -1, 1, 0, 0, 0)),
    ],
}
ui = UInput(cap, name="SkillFishOS prova pad", vendor=0x045e, product=0x028e, version=1)
time.sleep(1.5)  # let the window find it

TASTI = {"a": E.BTN_SOUTH, "b": E.BTN_EAST, "lb": E.BTN_TL, "rb": E.BTN_TR, "start": E.BTN_START}
HAT = {"su": (E.ABS_HAT0Y, -1), "giu": (E.ABS_HAT0Y, 1), "sinistra": (E.ABS_HAT0X, -1), "destra": (E.ABS_HAT0X, 1)}


def premi(code):
    ui.write(E.EV_KEY, code, 1); ui.syn(); time.sleep(0.08)
    ui.write(E.EV_KEY, code, 0); ui.syn()


def hat(code, val):
    ui.write(E.EV_ABS, code, val); ui.syn(); time.sleep(0.08)
    ui.write(E.EV_ABS, code, 0); ui.syn()


for tok in sys.argv[1:]:
    if tok.startswith("pausa"):
        time.sleep(float(tok[5:] or 1))
    elif tok in TASTI:
        premi(TASTI[tok])
    elif tok in HAT:
        hat(*HAT[tok])
    elif tok == "levetta-giu":
        ui.write(E.EV_ABS, E.ABS_Y, 30000); ui.syn(); time.sleep(0.1)
        ui.write(E.EV_ABS, E.ABS_Y, 0); ui.syn()
    elif tok == "levetta-su":
        ui.write(E.EV_ABS, E.ABS_Y, -30000); ui.syn(); time.sleep(0.1)
        ui.write(E.EV_ABS, E.ABS_Y, 0); ui.syn()
    else:
        print("ignoro", tok)
    time.sleep(0.35)
time.sleep(1)
ui.close()
