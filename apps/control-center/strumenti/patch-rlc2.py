#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The two leftovers of dropping the RLC write: a header line that still
promises it, and a variable nobody reads any more."""
import io, os, sys
CU = os.path.expanduser("~/sfx-src/system/usr/local/bin/skillfish-cu")
CAMBI = [
    ("# Routes GPU Compute Units at runtime by writing the SPI/CC/RLC WGP masks via umr.\n",
     "# Routes GPU Compute Units at runtime by writing the CC and SPI WGP masks via umr.\n"
     "# RLC_PG_ALWAYS_ON is deliberately left alone: see apply_rows.\n",
     "l'intestazione non promette piu' RLC"),
    ("RLC=mmRLC_PG_ALWAYS_ON_WGP_MASK\n", "", "via la variabile che nessuno legge"),
]
testo = io.open(CU, encoding="utf-8").read()
esito = 0
for vecchio, nuovo, etichetta in CAMBI:
    n = testo.count(vecchio)
    print("[%s] %s" % ("ok" if n == 1 else "NON TROVATO", etichetta))
    if n != 1:
        esito = 1; continue
    testo = testo.replace(vecchio, nuovo)
if esito:
    sys.exit("non ho scritto niente")
io.open(CU, "w", encoding="utf-8", newline="\n").write(testo)
print("scritto")
