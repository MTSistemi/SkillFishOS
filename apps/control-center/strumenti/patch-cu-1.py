#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #77, first half: skillfish-cu stops forcing WGP0-2 on, and learns to
put a chosen mapping back at boot.

Runs ON the build VM, inside ~/sfx-src.

    python3 patch-cu-1.py [--prova]

⚠️ WHY THE BOOT BEHAVIOUR IS KEPT AS THE DEFAULT. 40 CU at boot is the point
of this distribution, so `skillfish-cu boot` still turns everything on unless
someone has deliberately saved a mapping. Nothing changes for anyone who does
not ask for it.

⚠️ WHY A MINIMUM OF ONE AND NOT THREE. The old floor of three was an assumption
that measurement did not support (see the header rewritten below). One pair per
row is a real limit: a row with no WGP at all has nothing to run on.

The user-facing echoes stay Italian because every message already in this file
is Italian; the comments are English, as the project wants.
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
RADICE = os.path.expanduser("~/sfx-src")
CU = os.path.join(RADICE, "system/usr/local/bin/skillfish-cu")
UNITA = os.path.join(RADICE, "system/etc/systemd/system/skillfish-cu.service")

CAMBI = []


def cambia(percorso, vecchio, nuovo, etichetta):
    CAMBI.append((percorso, vecchio, nuovo, etichetta))


# ---------------------------------------------------- the claim that was wrong
cambia(CU, """# Driver floor = WGP0-2 (24 CU) are locked on at boot and always kept.
# Implementazione nostra. I fatti su cui si regge — nomi e campi dei registri,
# la regola che 1 WGP vale 2 CU, il pavimento di WGP0-2 imposto dal driver —
# stanno negli header AMD (licenza MIT) e in gfx_v10_0.c del kernel Linux.
""", """# No WGP is forced on. Any pair can be switched off, down to one per row.
# Our own implementation. The facts it rests on, the register names and fields
# and the rule that 1 WGP is 2 CU, come from the AMD headers (MIT licence) and
# from gfx_v10_0.c in the Linux kernel.
#
# There used to be a third "fact" here: that the driver locks WGP0-2 on and
# they can never be disabled. It is not true, and it cost a user with a
# defective CU in that range any way of switching it off. Measured on the dev
# board on 16/09/2026 by writing the masks through umr directly:
#
#   a row set to 0x1b keeps WGP2 off with WGP3 on, through a GPU load and
#   fifteen seconds, with nothing putting the bit back, and with
#   RLC_PG_ALWAYS_ON_WGP_MASK still at 0x1f
#
#   0x18 leaves only WGP3 and WGP4, so WGP0, WGP1 and WGP2 go off together
#
#   the silicon honours it rather than just reading it back: vkpeak fp32 gives
#   10156 GFLOPS at 40 CU, 8145 at 32, 4091 at 16, linear within a fifth of a
#   percent, and returns to 10158 when everything is switched back on
#
# See issue #77. Reported by tom lima.
""", "l'intestazione dice la verita'")

# -------------------------------------------------------------- the constants
cambia(CU, """FLOOR=0x07            # WGP0,1,2 — driver-locked, never disabled
FULL=0x1f            # all 5 WGP
RUN=/run/skillfish
STATE=$RUN/cu_active
""", """MIN_WGP=0x01          # a row with no WGP has nothing to run on: keep one
FULL=0x1f            # all 5 WGP
STOCK=0x07           # WGP0-2: the mapping the driver comes up with on its own
RUN=/run/skillfish
STATE=$RUN/cu_active
BOOTCONF=/etc/skillfish/cu-boot.conf
""", "MIN_WGP al posto di FLOOR")

# ------------------------------------------------------------- the write paths
cambia(CU, """write_row(){ # se sh mask(decimal)
  local m=$(( ($3 | FLOOR) & 0x1f ))
""", """write_row(){ # se sh mask(decimal)
  local m=$(( $3 & 0x1f ))
  (( m == 0 )) && m=$MIN_WGP
""", "write_row non forza piu' niente")

cambia(CU, """    local m=$(( (${!idx} | FLOOR) & 0x1f )); write_row "$se" "$sh" "$m"
""", """    local m=$(( ${!idx} & 0x1f )); (( m == 0 )) && m=$MIN_WGP
    write_row "$se" "$sh" "$m"
""", "apply_rows non forza piu' niente")

# ------------------------------------------------------------------- reporting
cambia(CU, """  printf '{"active_cu":%s,"max_cu":40,"floor":%d,"rows":{%s}}\\n' "$(read_total)" $((FLOOR)) "$(IFS=,; echo "${parts[*]}")"
""", """  # "floor" stays in the JSON because the Control Center reads it, and it is
  # now what it always should have been: nothing is forced on.
  printf '{"active_cu":%s,"max_cu":40,"floor":0,"min_wgp":%d,"rows":{%s}}\\n' "$(read_total)" $((MIN_WGP)) "$(IFS=,; echo "${parts[*]}")"
""", "il JSON dichiara floor 0 e il minimo vero")

# -------------------------------------------------------- keeping it at boot
cambia(CU, """need_root(){ [ "$(id -u)" = 0 ] || { echo "skillfish-cu: needs root" >&2; exit 1; }; }
""", """need_root(){ [ "$(id -u)" = 0 ] || { echo "skillfish-cu: needs root" >&2; exit 1; }; }

righe_salvate(){ # the saved mapping, or nothing
  [ -r "$BOOTCONF" ] || return 0
  sed -n 's/^rows=//p' "$BOOTCONF" | head -1
}

cmd_boot_get(){
  local rows; rows=$(righe_salvate)
  if [ -n "$rows" ] && [ "$(echo $rows | wc -w)" = 4 ]; then
    printf '{"keep":true,"rows":[%s]}\\n' "$(echo $rows | tr ' ' ',')"
  else
    printf '{"keep":false,"rows":[]}\\n'
  fi
}

cmd_boot_save(){ # m00 m01 m10 m11
  mkdir -p "$(dirname "$BOOTCONF")" 2>/dev/null
  printf '# scritto da skillfish-cu: la mappatura da rimettere all%s avvio\\nrows=%d %d %d %d\\n' \\
    "'" $(( $1 & 0x1f )) $(( $2 & 0x1f )) $(( $3 & 0x1f )) $(( $4 & 0x1f )) > "$BOOTCONF"
  chmod 644 "$BOOTCONF" 2>/dev/null
  echo "tenuta per il prossimo avvio: $1 $2 $3 $4"
}

cmd_boot(){ # what the unit runs
  # ⚠️ All 40 CU stay the default. A saved mapping is used only when somebody
  # asked for one, and only when it is four fields: a truncated or hand-edited
  # file must not leave the board with fewer CU than its owner expects.
  local rows; rows=$(righe_salvate)
  if [ -n "$rows" ] && [ "$(echo $rows | wc -w)" = 4 ]; then
    apply_rows $rows
    riporta
  else
    apply_uniform $FULL
    riporta 40
  fi
}
""", "boot, boot-save, boot-get")

# ------------------------------------------------------------ the command line
cambia(CU, """  max|enable-all)   need_root; apply_uniform $FULL;  riporta 40 ;;
  stock|disable-extra) need_root; apply_uniform $FLOOR; riporta 24 ;;
""", """  max|enable-all)   need_root; apply_uniform $FULL;  riporta 40 ;;
  stock|disable-extra) need_root; apply_uniform $STOCK; riporta 24 ;;
  boot)             need_root; cmd_boot ;;
  boot-save)        need_root; cmd_boot_save "${2:?}" "${3:?}" "${4:?}" "${5:?}" ;;
  boot-clear)       need_root; rm -f "$BOOTCONF"; echo "all'avvio tornano tutte accese" ;;
  boot-get)         cmd_boot_get ;;
""", "le voci nuove del comando")

cambia(CU, """  *) echo "usage: skillfish-cu {get|max|stock|set <0x07..0x1f>|set-rows m00 m01 m10 m11|state}"; exit 1 ;;
""", """  *) echo "usage: skillfish-cu {get|max|stock|set <0x01..0x1f>|set-rows m00 m01 m10 m11|state|boot|boot-save m00 m01 m10 m11|boot-clear|boot-get}"; exit 1 ;;
""", "la riga di aiuto")

# -------------------------------------------------------------------- the unit
cambia(UNITA, """Description=SkillFishOS — route all BC-250 Compute Units (40 CU) at boot
""", """Description=SkillFishOS — route the BC-250 Compute Units at boot
""", "descrizione dell'unita'")

cambia(UNITA, """ExecStart=/usr/local/bin/skillfish-cu max
""", """# `boot` and not `max`: all 40 CU are still what happens unless somebody has
# saved a mapping with "keep at boot", which is how a defective CU gets to stay
# switched off. See issue #77.
ExecStart=/usr/local/bin/skillfish-cu boot
""", "l'unita' chiama boot")

# ------------------------------------------------------------------- applica
testi = {}
for percorso, _, _, _ in CAMBI:
    testi.setdefault(percorso, io.open(percorso, encoding="utf-8").read())

esito = 0
for percorso, vecchio, nuovo, etichetta in CAMBI:
    quante = testi[percorso].count(vecchio)
    stato = "ok" if quante == 1 else "NON TROVATO" if quante == 0 else "%d VOLTE" % quante
    print("[%-11s] %-44s %s" % (stato, etichetta, os.path.basename(percorso)))
    if quante != 1:
        esito = 1
        continue
    testi[percorso] = testi[percorso].replace(vecchio, nuovo)

if esito:
    sys.exit("\nqualche ancoraggio non combacia: non ho scritto niente")

# nothing may mention the old floor any more
resto = [r for r in testi[CU].splitlines() if "FLOOR" in r]
if resto:
    print("\n⚠️ restano riferimenti a FLOOR:")
    for r in resto:
        print("   %s" % r.strip())
    sys.exit("non ho scritto niente")

if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

for percorso, testo in testi.items():
    io.open(percorso, "w", encoding="utf-8", newline="\n").write(testo)
    print("scritto %s" % percorso)
print("fatto")
