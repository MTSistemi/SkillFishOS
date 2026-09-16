#!/usr/bin/env python3
"""Merge the Control Center translations into the shared dictionaries.

    unisci-i18n.py <cc tree> <repo>/system/usr/share/skillfish/i18n

For every cc/i18n/<lang>.json the keys are added to the shared file of that
language (existing entries are kept as they are). it.json is fed from the
(it, en) pairs found in the code: Italian never goes through the dictionary
in the window, but the web pages of the Remote Manager read it from there.
Every placeholder (%s, %d, %.0f, %.1f) is checked to match the English key.
An entry equal to its English key is merged too: HUD, Hub, "Maximum" in German
or "Actions" in French are the translation, and skipping them left those keys
reported as missing forever.
"""
import ast
import glob
import json
import os
import re
import sys

cc, dest = sys.argv[1], sys.argv[2]
SEGNAPOSTO = re.compile(r"%(?:\.\d+)?[sdf]")


def carica(p):
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fp:
        d = json.load(fp)
    return d.get("voci", d) if isinstance(d, dict) else {}


def salva(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(d.items(), key=lambda kv: kv[0].lower())), f, ensure_ascii=False, indent=1)
        f.write("\n")


errori = 0
coppie = {}
for f in glob.glob(os.path.join(cc, "sfcc", "**", "*.py"), recursive=True):
    with open(f, encoding="utf-8") as fp:
        albero = ast.parse(fp.read())
    for n in ast.walk(albero):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "L" and len(n.args) == 2:
            it, en = n.args
            if isinstance(it, ast.Constant) and isinstance(en, ast.Constant) and isinstance(en.value, str):
                coppie[en.value] = it.value
for lingua in ("de", "es", "fr", "pl", "pt", "ru", "uk", "it"):
    nuovo = coppie if lingua == "it" else carica(os.path.join(cc, "i18n", lingua + ".json"))
    percorso = os.path.join(dest, lingua + ".json")
    condiviso = carica(percorso)
    aggiunte = 0
    for k, v in nuovo.items():
        if SEGNAPOSTO.findall(k) != SEGNAPOSTO.findall(v):
            print("SEGNAPOSTO %s: %r -> %r" % (lingua, k[:50], v[:50]), file=sys.stderr)
            errori += 1
            continue
        if k not in condiviso:
            condiviso[k] = v
            aggiunte += 1
    salva(percorso, condiviso)
    print("%s: +%d (totale %d)" % (lingua, aggiunte, len(condiviso)))
sys.exit(1 if errori else 0)
