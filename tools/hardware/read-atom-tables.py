# -*- coding: utf-8 -*-
u"""Legge le tabelle ATOM del VBIOS della BC-250.

Niente strutture ricopiate a mano: campi e scostamenti si ricavano da
atomfirmware.h, il file del kernel. È il motivo per cui questo lettore trova
la tabella dati e il primo tentativo no: gli scostamenti scritti a occhio
sbagliavano di due byte e leggevano zero dove c'era un puntatore.

Uso:  python leggi_atom.py vbios.rom [atomfirmware.h]
"""
from __future__ import unicode_literals
import io, re, struct, sys

ROM = sys.argv[1] if len(sys.argv) > 1 else "vbios.rom"
HDR = sys.argv[2] if len(sys.argv) > 2 else "atomfirmware.h"
with open(ROM, "rb") as f:
    d = f.read()
with io.open(HDR, encoding="utf-8", errors="replace") as f:
    h = f.read()

TIPI = {"uint8_t": ("B", 1), "int8_t": ("b", 1), "uint16_t": ("H", 2),
        "int16_t": ("h", 2), "uint32_t": ("I", 4), "int32_t": ("i", 4),
        "uint64_t": ("Q", 8), "int64_t": ("q", 8)}

STRUTTURE = set(re.findall(r'struct\s+(atom_\w+)\s*\{', h))


def campi(nome):
    u"""Campi scalari di una struct, con lo scostamento calcolato.

    ⚠️ Si ferma al primo campo che non è uno scalare o un vettore di scalari:
    da lì gli scostamenti non sarebbero più affidabili, e un numero sbagliato
    detto con sicurezza è peggio di nessun numero.
    """
    m = re.search(r'struct\s+' + nome + r'\s*\{(.*?)\n\};', h, re.S)
    if not m:
        return None, "struttura %s non trovata in atomfirmware.h" % nome
    fuori, off, nota = [], 0, None
    for riga in m.group(1).split("\n"):
        riga = re.sub(r'/\*.*?\*/', '', riga).split("//")[0].strip()
        if not riga or riga.startswith("#"):
            continue
        if re.match(r'struct\s+atom_common_table_header\s+\w+\s*;', riga):
            fuori.append(("[intestazione]", off, None, 4)); off += 4; continue
        mm = re.match(r'(\w+)\s+(\w+)\s*(\[\s*(\w+)\s*\])?\s*;', riga)
        if not mm or mm.group(1) not in TIPI:
            nota = "mi fermo a «%s»" % riga[:56]
            break
        f, dim = TIPI[mm.group(1)]
        n = mm.group(4)
        n = int(n) if (n and n.isdigit()) else (1 if not n else None)
        if n is None:
            nota = "mi fermo a «%s» (dimensione non numerica)" % riga[:44]
            break
        fuori.append((mm.group(2), off, f if n == 1 else None, dim * n))
        off += dim * n
    return fuori, nota


def valore(nome_struct, base, campo):
    lista, _ = campi(nome_struct)
    for f, o, fmt, dim in lista or []:
        if f == campo and fmt:
            return struct.unpack_from("<" + fmt, d, base + o)[0]
    return None


def mostra(nome_struct, base, limite=40):
    lista, nota = campi(nome_struct)
    if lista is None:
        print("      %s" % nota); return
    n = 0
    for f, o, fmt, dim in lista:
        if fmt is None:
            continue
        try:
            v = struct.unpack_from("<" + fmt, d, base + o)[0]
        except struct.error:
            break
        print("      %-38s %-12d 0x%X" % (f, v, v))
        n += 1
        if n >= limite:
            print("      ..."); break
    if nota:
        print("      (%s)" % nota)


# Il nome nell'elenco e quello della struct non coincidono, e non si ricavano
# l'uno dall'altro: «integratedsysteminfo» sta in atom_integrated_system_info,
# «dce_info» in atom_display_controller_info. Questa corrispondenza è scritta,
# non indovinata.
CORRISPONDENZE = {
    "firmwareinfo": "firmware_info",
    "integratedsysteminfo": "integrated_system_info",
    "gfx_info": "gfx_info",
    "smu_info": "smu_info",
    "umc_info": "umc_info",
    "vram_info": "vram_info_header",
    "multimedia_info": "multimedia_info",
    "dce_info": "display_controller_info",
    "lcd_info": "lcd_info",
    "gpio_pin_lut": "gpio_pin_lut",
    "smc_dpm_info": "smc_dpm_info",
    "asic_profiling_info": "asic_profiling_info",
    "vram_usagebyfirmware": "vram_usagebyfirmware",
}


def struttura_per(tabella, fr, cr):
    u"""Il nome della struct per questa tabella e questa versione.

    ⚠️ Prima qui c'era un punteggio di somiglianza fra nomi. A parità di
    punteggio l'ordine dipendeva da un insieme, e Python mescola gli insiemi a
    ogni avvio: lo stesso VBIOS dava «display_controller_info» in una stampa e
    «asic_profiling_info» in quella dopo, con i numeri sbagliati stampati con la
    stessa faccia sicura. Meglio dire «non lo so» che tirare a indovinare.
    """
    base = CORRISPONDENZE.get(tabella)
    if not base:
        return None
    n = "atom_%s_v%d_%d" % (base, fr, cr)
    if n in STRUTTURE:
        return n
    vicine = sorted(s for s in STRUTTURE
                    if s.startswith("atom_%s_v%d_" % (base, fr)))
    return vicine[-1] + "  (⚠️ versione diversa da quella del VBIOS)" if vicine else None


# ------------------------------------------------------------- intestazione
print("=" * 72)
print("VBIOS: %d byte" % len(d))
rh = struct.unpack_from("<H", d, 0x48)[0]
sz, frev, crev = struct.unpack_from("<HBB", d, rh)
print("Intestazione ROM a 0x%X — versione %d.%d, firma %r"
      % (rh, frev, crev, d[rh + 4:rh + 8].decode("ascii", "replace")))

ST = "atom_rom_header_v%d_%d" % (frev, crev)
for c in ("bios_segment_address", "subsystem_vendor_id", "subsystem_id",
          "masterhwfunction_offset", "masterdatatable_offset", "pspdirtableoffset",
          "vbios_bootupmessageoffset", "crc_block_offset"):
    v = valore(ST, rh, c)
    print("   %-28s 0x%08X" % (c, v if v is not None else 0))

bm = valore(ST, rh, "vbios_bootupmessageoffset") or 0
if bm and bm < len(d):
    print("   messaggio di avvio: %r"
          % d[bm:bm + 160].split(b"\x00")[0].decode("ascii", "replace").strip())

# ------------------------------------------------------------ tabelle dati
mdt = valore(ST, rh, "masterdatatable_offset") or 0
nomi = re.findall(r'uint16_t\s+(\w+)\s*;', re.search(
    r'struct atom_master_list_of_data_tables_v2_1\s*\{(.*?)\n\};', h, re.S).group(1))
print("\nTabelle dati (elenco a 0x%04X)" % mdt)
print("%-26s %-8s %-9s %-8s %s" % ("TABELLA", "OFFSET", "VERSIONE", "BYTE", "STRUTTURA"))
presenti = {}
for i, n in enumerate(nomi):
    off = struct.unpack_from("<H", d, mdt + 4 + i * 2)[0]
    if not off or off + 4 > len(d):
        continue
    tsz, fr, cr = struct.unpack_from("<HBB", d, off)
    if tsz == 0 or off + tsz > len(d):
        continue
    st = struttura_per(n, fr, cr)
    presenti[n] = (off, fr, cr, tsz, st)
    print("%-26s 0x%04X   %-9s %-8d %s" % (n, off, "%d.%d" % (fr, cr), tsz, st or "—"))

vuote = [n for n in nomi if n not in presenti and not n.startswith("sw_datatable")]
print("\nNon dichiarate da questo VBIOS: %s" % (", ".join(vuote) if vuote else "nessuna"))

# ------------------------------------------------------- contenuto tabelle
for n in ("firmwareinfo", "integratedsysteminfo", "gfx_info", "smu_info",
          "umc_info", "multimedia_info", "vram_info", "dce_info", "smc_dpm_info"):
    if n not in presenti:
        continue
    off, fr, cr, tsz, st = presenti[n]
    print("\n--- %s  (v%d.%d, %d byte, %s) ---" % (n, fr, cr, tsz, st or "struttura ignota"))
    if st:
        mostra(st.split("  ")[0], off)
    else:
        print("      nessuna struttura per questa versione in atomfirmware.h")
