#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skillfish-cu stops writing RLC_PG_ALWAYS_ON_WGP_MASK.

Runs ON the build VM, inside ~/sfx-src.

    python3 patch-rlc.py [--prova]

⚠️ WHY. We changed kernels to stop writing this register and then wrote it from
userspace anyway. The patch set we ship, userpatches-350, replaced the old CU
unlock with Ariel's 0114-ariel-16-cu-unlock-cc-spi-safe-no-rlc, whose whole
point is the register this tool was still writing at every boot:

    Writing RLC_PG_ALWAYS_ON_WGP_MASK with RLC firmware running causes the
    RLC's per-WGP bring-up state machine to activate for WGPs 3-4. These WGPs
    have been harvest-disabled since VBIOS POST; their handshake registers are
    uninitialised. The RLC stalls indefinitely waiting for a WGP-ready ACK that
    never arrives, causing a system hang on first rocBLAS / HSA launch. On
    BC-250, ppfeaturemask already disables global power gating, making the
    always-on mask redundant.

From userspace the firmware is certainly running, which is the worse of the two
cases the patch describes.

⚠️ AND THIS RETIRES tom lima's maxbits fix, which was right. The union of the
rows existed only to feed that write; with the write gone there is nothing to
compute. His other two changes, the error propagation and the argument
validation, stay where they are.

⚠️ NOT A SOURCE-ONLY CHANGE. Whether the routing still works without it has to
be measured: yesterday's linear scaling was all recorded with RLC forced to
0x1f. See prova-rlc.sh.
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
CU = os.path.expanduser("~/sfx-src/system/usr/local/bin/skillfish-cu")

CAMBI = []


def cambia(vecchio, nuovo, etichetta):
    CAMBI.append((vecchio, nuovo, etichetta))


cambia('''  local unione=0 r se sh idx=1
''', '''  local r se sh idx=1
''', "via la variabile dell'unione")

cambia('''    write_row "$se" "$sh" "$m" || return 1
    # ⚠️ The union of the rows, not the largest number among them. This was
    # `(( m > maxbits )) && maxbits=$m`, which is wrong whenever a row has
    # fewer pairs on but higher ones: 0x18 beats 0x07 as a number while
    # carrying half the WGPs, so the low pairs fell out of the always-on mask.
    # Found by tom lima in PR #80.
    unione=$(( unione | m )); idx=$((idx+1))
  done
  $UMR -i $INST -w "$ASIC.$RLC" "$(printf '0x%x' $unione)" >/dev/null 2>&1 || return 1
  update_state
''', '''    write_row "$se" "$sh" "$m" || return 1
    idx=$((idx+1))
  done
  # ⚠️ RLC_PG_ALWAYS_ON_WGP_MASK IS DELIBERATELY NOT WRITTEN HERE.
  #
  # It used to be, with the union of the rows. We then changed kernels to stop
  # the driver writing it: userpatches-350 carries Ariel's CU unlock, the one
  # whose subject line ends "no RLC_PG write", because writing it while the RLC
  # firmware is running makes the RLC wait forever for a ready ACK from WGPs
  # that VBIOS harvested off, and the board hangs on the first ROCm/HSA launch.
  # Doing it from here is that same write, at a worse moment. The always-on
  # mask is redundant anyway: our ppfeaturemask already keeps global power
  # gating off, and the kernel disables GFXOFF for gfx1013 outright.
  #
  # This is also why the union is gone. It existed only to feed this write, and
  # computing it as a numeric maximum instead of an OR was a real bug that tom
  # lima found in PR #80. The fix was right; the code it fixed is no longer
  # needed.
  update_state
''', "via la scrittura di RLC, con il perche'")

testo = io.open(CU, encoding="utf-8").read()
esito = 0
for vecchio, nuovo, etichetta in CAMBI:
    n = testo.count(vecchio)
    stato = "ok" if n == 1 else "NON TROVATO" if n == 0 else "%d VOLTE" % n
    print("[%-11s] %s" % (stato, etichetta))
    if n != 1:
        esito = 1
        continue
    testo = testo.replace(vecchio, nuovo)

if esito:
    sys.exit("\nqualche ancoraggio non combacia: non ho scritto niente")

vivi = [r for r in testo.splitlines()
        if ("$RLC" in r or "unione" in r) and not r.lstrip().startswith("#")]
if vivi:
    for r in vivi:
        print("  resta vivo: %s" % r.strip())
    sys.exit("RLC o unione sono ancora nel codice: non ho scritto niente")
print("[ok         ] nel codice non resta ne' RLC ne' l'unione")

if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

io.open(CU, "w", encoding="utf-8", newline="\n").write(testo)
print("scritto %s" % CU)
