# -*- coding: utf-8 -*-
u"""Legge la tabella di scoperta della BC-250: quali blocchi il chip dichiara.

Le strutture non sono indovinate: i nomi degli HWID e i formati vengono letti
da discovery.h e soc15_hw_ip.h presi dal kernel, così se domani AMD
aggiunge un blocco il lettore non racconta bugie.
"""
from __future__ import unicode_literals
import io, re, struct, sys

BIN = sys.argv[1] if len(sys.argv) > 1 else "discovery.bin"
with open(BIN, "rb") as f:
    dati = f.read()

# --- i nomi dei blocchi, dal sorgente -------------------------------------
with io.open("discovery.h", encoding="utf-8", errors="replace") as f:
    h = f.read()
# ⚠️ Gli HWID NON stanno in discovery.h: sono in soc15_hw_ip.h. Senza
# questo file il lettore stampa «sconosciuto» per ogni blocco, e sembra
# che il chip non dichiari niente.
with io.open("soc15_hw_ip.h", encoding="utf-8", errors="replace") as f:
    h += f.read()

hwid = {}
for m in re.finditer(r'#define\s+(\w+)_HWID\s+(\d+)', h):
    hwid[int(m.group(2))] = m.group(1)
# gli alias tipo «#define VCN_HWID UVD_HWID» dicono che due nomi sono lo stesso id
alias = {}
for m in re.finditer(r'#define\s+(\w+)_HWID\s+(\w+)_HWID', h):
    alias.setdefault(m.group(2), []).append(m.group(1))
for base, altri in alias.items():
    for k, v in list(hwid.items()):
        if v == base:
            hwid[k] = v + "/" + "/".join(altri)

TAVOLE = ["IP_DISCOVERY", "GC", "HARVEST_INFO", "VCN_INFO", "MALL_INFO", "NPS_INFO"]

# --- intestazione ----------------------------------------------------------
firma, vmaj, vmin, csum, size = struct.unpack_from("<IHHHH", dati, 0)
print("Intestazione")
print("   firma      0x%08X  %s" % (firma, "ok" if firma == 0x28211407 else "NON RICONOSCIUTA"))
print("   versione   %d.%d" % (vmaj, vmin))
print("   dimensione %d byte (il file ne ha %d)" % (size, len(dati)))
print()

print("Tavole presenti")
tavole = {}
for i in range(6):
    off, ck, sz, _ = struct.unpack_from("<HHHH", dati, 12 + i * 8)
    nome = TAVOLE[i] if i < len(TAVOLE) else "?%d" % i
    if off or sz:
        tavole[nome] = (off, sz)
        print("   %-14s offset %5d  %4d byte" % (nome, off, sz))
    else:
        print("   %-14s assente" % nome)
print()

# --- elenco dei blocchi ----------------------------------------------------
off, _ = tavole["IP_DISCOVERY"]
firma, versione, sz, tid, ndie = struct.unpack_from("<IHHIH", dati, off)
print("Tabella dei blocchi: firma 0x%08X (%s), versione %d, %d die"
      % (firma, "IPDS" if firma == 0x53445049 else "?", versione, ndie))
print()

righe = []
for d in range(ndie):
    # ⚠️ L'elenco dei die comincia al byte 14, non 16: l'intestazione è
    # firma(4) + versione(2) + dimensione(2) + id(4) + numero die(2), senza
    # nessun riempimento. Contandone 16 si legge spazzatura che sembra vera —
    # 10273 blocchi su un die, e il lettore va a sbattere.
    die_id, die_off = struct.unpack_from("<HH", dati, off + 14 + d * 4)
    dh_id, num_ips = struct.unpack_from("<HH", dati, die_off)
    print("Die %d (id 0x%04X): %d blocchi" % (d, dh_id, num_ips))
    p = die_off + 4
    for _ in range(num_ips):
        hw, ist, nbase, maj, mino, rev, harv = struct.unpack_from("<HBBBBBB", dati, p)
        nome = hwid.get(hw, "sconosciuto")
        basi = struct.unpack_from("<%dI" % nbase, dati, p + 8) if nbase else ()
        righe.append((nome, hw, ist, maj, mino, rev, harv & 0xF, basi))
        p += 8 + 4 * nbase

# raggruppo per nome, contando le istanze
visti = {}
for nome, hw, ist, maj, mino, rev, harv, basi in righe:
    k = (nome, hw, maj, mino, rev)
    visti.setdefault(k, {"ist": [], "harv": set(), "basi": []})
    visti[k]["ist"].append(ist)
    visti[k]["harv"].add(harv)
    visti[k]["basi"] += list(basi)

print("%-22s %-6s %-9s %-8s %s" % ("BLOCCO", "HWID", "VERSIONE", "ISTANZE", "MIETUTO"))
for (nome, hw, maj, mino, rev), v in sorted(visti.items()):
    print("%-22s %-6d %-9s %-8d %s"
          % (nome, hw, "%d.%d.%d" % (maj, mino, rev), len(v["ist"]),
             "sì" if any(v["harv"]) else "no"))

# --- quello che il chip dichiara di NON avere ------------------------------
if "HARVEST_INFO" in tavole:
    off, sz = tavole["HARVEST_INFO"]
    firma, versione = struct.unpack_from("<II", dati, off)
    print("\nTabella dei blocchi disattivati: firma 0x%08X (%s), versione %d"
          % (firma, "HARV" if firma == 0x56524148 else "?", versione))
    trovato = False
    for i in range(32):
        hw, ist, _ = struct.unpack_from("<HBB", dati, off + 8 + i * 4)
        if hw:
            trovato = True
            print("   %-20s (hwid %d) istanza %d" % (hwid.get(hw, "sconosciuto"), hw, ist))
    if not trovato:
        print("   vuota: il chip non dichiara nessun blocco disattivato")

# --- la tabella GC: quante unità di calcolo -------------------------------
if "GC" in tavole:
    off, sz = tavole["GC"]
    tid, vmaj_gc, vmin_gc, hsz = struct.unpack_from("<IHHI", dati, off)
    campi = ["num_se", "num_wgp0_per_sa", "num_wgp1_per_sa", "num_rb_per_se",
             "num_gl2c", "num_gprs", "num_max_gs_thds", "gs_table_depth",
             "gsprim_buff_depth", "parameter_cache_depth", "double_offchip_lds_buffer",
             "wave_size", "max_waves_per_simd", "max_scratch_slots_per_cu",
             "lds_size", "num_sc_per_se", "num_sa_per_se", "num_packer_per_sc",
             "num_gl2a"]
    val = struct.unpack_from("<%dI" % len(campi), dati, off + 12)
    print("\nTabella GC (id 0x%04X, versione %d.%d)" % (tid & 0xFFFF, vmaj_gc, vmin_gc))
    for n, v in zip(campi, val):
        print("   %-26s %d" % (n, v))
