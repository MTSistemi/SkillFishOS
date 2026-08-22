#!/usr/bin/env python3
"""Ripara i riferimenti a gradienti orfani nel tema SkillFishSteampunk.

Ogni icona definisce i propri gradienti <prefisso>_<suffisso> (brass, brassR,
copper, glow, recess, rivet, sh). Un bug di generazione ha lasciato in 88 file
dei riferimenti url(#<ALTRA_icona>_<suffisso>) che qtsvg >= 6.10.2-9 non
risolve piu -> l'elemento non viene dipinto e l'icona appare vuota.

Fix: riscrive ogni riferimento orfano usando il gradiente OMONIMO del file
stesso (stesso suffisso). Se il file non ha quel suffisso, lo segnala e NON
tocca il file.
"""
import re, sys, pathlib, collections

THEME = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/icons/SkillFishSteampunk"
APPLY = "--apply" in sys.argv

SUFFIXES = ["brassR", "brass", "copper", "glow", "recess", "rivet", "sh"]

def own_prefix(defined):
    """Deduce il prefisso proprio del file dagli id definiti."""
    cand = collections.Counter()
    for d in defined:
        for s in SUFFIXES:
            if d.endswith("_" + s):
                cand[d[: -(len(s) + 1)]] += 1
                break
    return cand.most_common(1)[0][0] if cand else None

changed = files_changed = skipped = 0
report = []
for f in sorted(pathlib.Path(THEME).rglob("*.svg")):
    txt = f.read_text(encoding="utf-8", errors="replace")
    defined = set(re.findall(r'id="([^"]+)"', txt))
    refs = set(re.findall(r'url\(#([^)]+)\)', txt))
    orphans = sorted(refs - defined)
    if not orphans:
        continue
    prefix = own_prefix(defined)
    if not prefix:
        report.append(f"  SKIP (nessun prefisso deducibile): {f.name} -> {orphans}")
        skipped += 1
        continue
    new = txt
    local = []
    for o in orphans:
        suf = next((s for s in SUFFIXES if o.endswith("_" + s)), None)
        target = f"{prefix}_{suf}" if suf else None
        if not suf or target not in defined:
            report.append(f"  SKIP (manca {target or '?'} nel file): {f.name} <- #{o}")
            skipped += 1
            continue
        new = new.replace(f"url(#{o})", f"url(#{target})")
        local.append(f"#{o} -> #{target}")
        changed += 1
    if local and new != txt:
        files_changed += 1
        report.append(f"  {f.relative_to(THEME)}: " + ", ".join(local))
        if APPLY:
            f.write_text(new, encoding="utf-8")

print("\n".join(report[:40]))
if len(report) > 40:
    print(f"  ... e altre {len(report)-40} righe")
print(f"\n=== {'APPLICATO' if APPLY else 'DRY-RUN'}: {files_changed} file, {changed} riferimenti riscritti, {skipped} saltati ===")

# Uscita non-zero se restano riferimenti rotti: in dry-run e' la guardia CI
# (qtsvg >= 6.10.2-9 non dipinge gli elementi con paint irrisolvibile ->
# icone vuote nel menu), in --apply segnala i casi che non ha saputo riparare.
if skipped or (files_changed and not APPLY):
    sys.exit(1)
