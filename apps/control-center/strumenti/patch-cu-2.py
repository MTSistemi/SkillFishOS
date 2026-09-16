#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #77: the parts of pull request #80 worth keeping.

Runs ON the build VM, inside ~/sfx-src, after patch-cu-1.py.

    python3 patch-cu-2.py [--prova]

PR #80 could not be merged: it removed two verified fixes, deleted vram_get()
while get() still called it, and wired its own boot mapping to nothing. But
three things in it are right and one of them is a defect of ours that nobody
here had spotted.

  1. maxbits was computed by comparing masks as numbers. RLC_PG_ALWAYS_ON gets
     the union of the rows, and 0x18 is numerically larger than 0x07 while
     having fewer bits set, so a row with the low pairs on could be dropped
     from the always-on mask. It is an OR, not a maximum.

  2. umr failures were swallowed. Every write went to /dev/null and nobody
     looked, so a routing that never happened still reported success. The
     failure now travels back.

  3. apply_rows took whatever it was handed. Four arguments in range is worth
     checking before writing them to a register.

Reported and written by tom lima (ZEROAESQUERDA).
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
CU = os.path.expanduser("~/sfx-src/system/usr/local/bin/skillfish-cu")

VECCHIO = '''write_row(){ # se sh mask(decimal)
  local m=$(( $3 & 0x1f ))
  (( m == 0 )) && m=$MIN_WGP
  $UMR -i $INST -w "$ASIC.$CC" 0x0 -b "$1" "$2" 0xffffffff >/dev/null 2>&1
  $UMR -i $INST -w "$ASIC.$SPI" "$(printf '0x%x' $m)" -b "$1" "$2" 0xffffffff >/dev/null 2>&1
}

apply_rows(){ # m00 m01 m10 m11 (decimal/hex)
  local maxbits=0 r se sh idx=1
  $UMR -i $INST -w "$ASIC.$CC" 0x0 >/dev/null 2>&1
  for r in "${ROWS[@]}"; do se=${r%:*}; sh=${r#*:}
    local m=$(( ${!idx} & 0x1f )); (( m == 0 )) && m=$MIN_WGP
    write_row "$se" "$sh" "$m"
    (( m > maxbits )) && maxbits=$m; idx=$((idx+1))
  done
  $UMR -i $INST -w "$ASIC.$RLC" "$(printf '0x%x' $maxbits)" >/dev/null 2>&1
  update_state
}
'''

NUOVO = '''write_row(){ # se sh mask(decimal)
  local m=$(( $3 & 0x1f ))
  (( m == 0 )) && m=$MIN_WGP
  # A write that fails must say so. These calls used to go to /dev/null with
  # nobody looking, so a routing that never happened still reported success.
  # Spotted by tom lima in PR #80.
  $UMR -i $INST -w "$ASIC.$CC" 0x0 -b "$1" "$2" 0xffffffff >/dev/null 2>&1 || return 1
  $UMR -i $INST -w "$ASIC.$SPI" "$(printf '0x%x' $m)" -b "$1" "$2" 0xffffffff >/dev/null 2>&1 || return 1
}

apply_rows(){ # m00 m01 m10 m11 (decimal/hex)
  # Four masks, each one a real one, checked before anything reaches a
  # register. Also from PR #80.
  [ "$#" -eq 4 ] || return 2
  local arg
  for arg in "$@"; do
    [[ "$arg" =~ ^(0x[0-9a-fA-F]{1,2}|[0-9]{1,2})$ ]] || return 2
    (( arg >= 0 && arg <= 31 )) || return 2
  done
  local unione=0 r se sh idx=1
  $UMR -i $INST -w "$ASIC.$CC" 0x0 >/dev/null 2>&1 || return 1
  for r in "${ROWS[@]}"; do se=${r%:*}; sh=${r#*:}
    local m=$(( ${!idx} & 0x1f )); (( m == 0 )) && m=$MIN_WGP
    write_row "$se" "$sh" "$m" || return 1
    # ⚠️ The union of the rows, not the largest number among them. This was
    # `(( m > maxbits )) && maxbits=$m`, which is wrong whenever a row has
    # fewer pairs on but higher ones: 0x18 beats 0x07 as a number while
    # carrying half the WGPs, so the low pairs fell out of the always-on mask.
    # Found by tom lima in PR #80.
    unione=$(( unione | m )); idx=$((idx+1))
  done
  $UMR -i $INST -w "$ASIC.$RLC" "$(printf '0x%x' $unione)" >/dev/null 2>&1 || return 1
  update_state
}
'''

testo = io.open(CU, encoding="utf-8").read()
quante = testo.count(VECCHIO)
print("[%s] i due percorsi di scrittura" % ("ok" if quante == 1 else "NON TROVATO"))
if quante != 1:
    sys.exit("l'ancoraggio non combacia: non ho scritto niente")

testo = testo.replace(VECCHIO, NUOVO)

# ⚠️ The guard looks at code, not at prose: the comment above quotes the old
# line on purpose, so a plain substring search would always trip on itself.
vivo = [r for r in testo.splitlines()
        if "maxbits" in r and not r.lstrip().startswith("#")]
if vivo:
    for r in vivo:
        print("  resta vivo: %s" % r.strip())
    sys.exit("maxbits e' ancora nel codice: non ho scritto niente")

if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

io.open(CU, "w", encoding="utf-8", newline="\n").write(testo)
print("scritto %s" % CU)
