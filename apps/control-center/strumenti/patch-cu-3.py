#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #77: a failed routing must not report a CU count as if it went well.

Runs ON the build VM, inside ~/sfx-src, after patch-cu-2.py.

Now that apply_rows and apply_uniform propagate their failures, the callers
have to look. `apply_rows ...; riporta` ran the report whatever happened, which
is the same shape of bug the error propagation was added to remove: the count
printed would be the one still on the card, and the exit status would be the
report's, not the write's.

The `&& riporta` shape is from tom lima's PR #80.
"""
import io
import os
import sys

CU = os.path.expanduser("~/sfx-src/system/usr/local/bin/skillfish-cu")

CAMBI = [
    ('  max|enable-all)   need_root; apply_uniform $FULL;  riporta 40 ;;\n',
     '  max|enable-all)   need_root; apply_uniform $FULL  && riporta 40 ;;\n',
     'max'),
    ('  stock|disable-extra) need_root; apply_uniform $STOCK; riporta 24 ;;\n',
     '  stock|disable-extra) need_root; apply_uniform $STOCK && riporta 24 ;;\n',
     'stock'),
    ('  set)              need_root; apply_uniform "${2:?mask}"; riporta ;;     # 0x07..0x1f, all rows\n',
     '  set)              need_root; apply_uniform "${2:?mask}" && riporta ;;   # 0x01..0x1f, all rows\n',
     'set'),
    ('  set-rows)         need_root; apply_rows "${2:?}" "${3:?}" "${4:?}" "${5:?}"; riporta ;;\n',
     '  set-rows)         need_root; apply_rows "${2:?}" "${3:?}" "${4:?}" "${5:?}" && riporta ;;\n',
     'set-rows'),
]

testo = io.open(CU, encoding="utf-8").read()
esito = 0
for vecchio, nuovo, etichetta in CAMBI:
    n = testo.count(vecchio)
    print("[%s] %s" % ("ok" if n == 1 else "NON TROVATO", etichetta))
    if n != 1:
        esito = 1
        continue
    testo = testo.replace(vecchio, nuovo)
if esito:
    sys.exit("qualcosa non combacia: non ho scritto niente")

# apply_rows returns non-zero on a bad mapping, so cmd_boot must not report
# either; it already calls riporta on its own line, which is fine because it
# only gets there after apply_rows succeeded... check that it does.
if "apply_rows $rows\n    riporta" in testo:
    testo = testo.replace("apply_rows $rows\n    riporta",
                          "apply_rows $rows && riporta")
    print("[ok] anche cmd_boot")

io.open(CU, "w", encoding="utf-8", newline="\n").write(testo)
print("scritto")
