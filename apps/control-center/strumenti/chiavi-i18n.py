#!/usr/bin/env python3
"""List the English keys of every L(it, en) call in the Control Center, and
which of them are missing from each shared dictionary.

    chiavi-i18n.py <tree with sfcc/> [i18n dir]   -> JSON on stdout

The keys are the second argument of L(); the shared dictionary is keyed by
that English string. Nothing here writes: the translations are added by hand
(or by whoever helps), one file per language.
"""
import ast
import glob
import json
import os
import sys

radice = sys.argv[1] if len(sys.argv) > 1 else "."
cartella = sys.argv[2] if len(sys.argv) > 2 else "/usr/share/skillfish/i18n"
chiavi = {}
for f in sorted(glob.glob(os.path.join(radice, "sfcc", "**", "*.py"), recursive=True)):
    with open(f, encoding="utf-8") as fp:
        tree = ast.parse(fp.read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "L" and len(n.args) == 2:
            it, en = n.args
            if isinstance(en, ast.Constant) and isinstance(en.value, str) and isinstance(it, ast.Constant):
                chiavi[en.value] = it.value
out = {"chiavi": len(chiavi), "mancanti": {}}
for lingua in sorted(os.listdir(cartella)) if os.path.isdir(cartella) else []:
    if not lingua.endswith(".json"):
        continue
    with open(os.path.join(cartella, lingua), encoding="utf-8") as fp:
        d = json.load(fp)
    d = d.get("voci", d)
    out["mancanti"][lingua[:-5]] = sorted(k for k in chiavi if k not in d)
out["coppie"] = chiavi
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
