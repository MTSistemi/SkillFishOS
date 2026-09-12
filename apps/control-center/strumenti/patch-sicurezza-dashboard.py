#!/usr/bin/env python3
"""The two code-scanning findings that are worth fixing: a path built from a
name that arrives over HTTP, and a URL whose tail arrives the same way.

    patch-sicurezza-dashboard.py <repo>

Both are behind the PAM login and both are already checked by their callers.
That is exactly the kind of "already checked somewhere else" that stops being
true the day somebody adds a second caller: the check goes where the value is
used.
"""
import os
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
p = os.path.join(repo, "apps", "dashboard", "skillfish-dashboardd")
s = open(p, encoding="utf-8").read()

# ---- 1. the Proton folder name (py/path-injection)
VECCHIO = '''    import re as _re
    try:
        with open(os.path.join(_cc_proton_dir(dove), n, "compatibilitytool.vdf"),
                  encoding="utf-8", errors="replace") as f:'''
NUOVO = '''    import re as _re
    # il nome arriva anche dalla rete: qui si pretende che sia un nome di
    # cartella e nient'altro, cosi' nessun ".." puo' uscire da tools.d
    if not _re.match(r"^[A-Za-z0-9._-]+$", n or "") or n in (".", ".."):
        return n
    try:
        with open(os.path.join(_cc_proton_dir(dove), n, "compatibilitytool.vdf"),
                  encoding="utf-8", errors="replace") as f:'''
if VECCHIO not in s:
    raise SystemExit("non trovo il blocco del nome interno")
s = s.replace(VECCHIO, NUOVO, 1)

# ---- 2. the repository id in the Studio URL (py/partial-ssrf)
VECCHIO = '''def ai_variants(repo):
    key = _unsloth_key()
    if not key or not repo or "/" not in repo:
        return {"ok": False, "error": "key or repository missing"}'''
NUOVO = '''def ai_variants(repo):
    key = _unsloth_key()
    if not key or not repo or "/" not in repo:
        return {"ok": False, "error": "key or repository missing"}
    # un repository di Hugging Face e' utente/nome: due pezzi, niente altro.
    # Il valore arriva dal browser e finisce dentro un indirizzo: si controlla
    # la forma prima, non ci si affida a quote()
    if not re.match(r"^[A-Za-z0-9._-]{1,80}/[A-Za-z0-9._-]{1,120}$", repo):
        return {"ok": False, "error": "nome del repository non valido"}'''
if VECCHIO not in s:
    raise SystemExit("non trovo ai_variants")
s = s.replace(VECCHIO, NUOVO, 1)

# and the same shape where the download is asked for
VECCHIO = '''def ai_download(repo, variant):
    key = _unsloth_key()
    if not key or not repo:
        return {"ok": False, "error": "key or repository missing"}'''
NUOVO = '''def ai_download(repo, variant):
    key = _unsloth_key()
    if not key or not repo:
        return {"ok": False, "error": "key or repository missing"}
    if not re.match(r"^[A-Za-z0-9._-]{1,80}/[A-Za-z0-9._-]{1,120}$", repo):
        return {"ok": False, "error": "nome del repository non valido"}
    if variant is not None and not re.match(r"^[A-Za-z0-9._-]{1,60}$", str(variant)):
        return {"ok": False, "error": "variante non valida"}'''
if VECCHIO in s:
    s = s.replace(VECCHIO, NUOVO, 1)
    print("anche ai_download")

# ai_downloads builds the same URL from what Studio itself reports: that one
# comes back from localhost, but the shape check costs nothing
VECCHIO = '''        prog = _studio("/api/hub/download-progress?repo_id=" + urllib.parse.quote(repo, safe=""), key=key, t=6) or {}'''
NUOVO = '''        if not re.match(r"^[A-Za-z0-9._-]{1,80}/[A-Za-z0-9._-]{1,120}$", repo or ""):
            continue
        prog = _studio("/api/hub/download-progress?repo_id=" + urllib.parse.quote(repo, safe=""), key=key, t=6) or {}'''
if VECCHIO in s:
    s = s.replace(VECCHIO, NUOVO, 1)
    print("anche ai_downloads")

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fatto")
