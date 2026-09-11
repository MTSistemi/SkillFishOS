#!/usr/bin/env python3
"""The website documentation loses the "Native apps" page: those apps are one
window now, and the page that described them as separate programs contradicted
every other page.

    docs-sito-unifica-app-native.py <repo>

- every link to /docs/app-native (and its eight translated paths) points to
  /docs/control-center; the link text stays "Tuner" where the sentence talks
  about the Tuner, which is still called Tuner, and becomes "Control Center"
  where it named the set of applications;
- app-native.md is removed in the nine languages;
- astro.config.mjs keeps a redirect for each of the nine old addresses, so the
  links already published elsewhere still land somewhere.
"""
import glob
import os
import re
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
DOCS = os.path.join(repo, "website", "src", "content", "docs")
LINGUE = ("it", "en", "pl", "uk", "ru", "es", "pt", "de", "fr")

# link texts that named the SET of applications: they become the window's name
INSIEME = ("App native", "Native apps", "Eigene Anwendungen", "Aplicaciones propias",
           "Applications natives", "Własne aplikacje", "Родные приложения", "Власні програми",
           "Aplicativos próprios", "Aplicativos nativos",
           "Tuner e AI", "Tuner and AI", "Tuner und AI", "Tuner y AI", "Tuner et IA",
           "Tuner i AI", "Tuner и AI", "Tuner і AI")

LINK = re.compile(r"\[([^\]]*)\]\((/(?:[a-z]{2}/)?)docs/app-native(#[^)]*)?\)")


def sostituisci(m):
    testo, prefisso, ancora = m.group(1), m.group(2), m.group(3) or ""
    if testo in INSIEME:
        testo = "Control Center"
    return "[%s](%sdocs/control-center%s)" % (testo, prefisso, ancora)


cambiati = link = 0
for p in sorted(glob.glob(os.path.join(DOCS, "*", "*.md"))):
    if os.path.basename(p) == "app-native.md":
        continue
    with open(p, encoding="utf-8") as f:
        s = f.read()
    nuovo, n = LINK.subn(sostituisci, s)
    if n:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(nuovo)
        cambiati += 1
        link += n
print("collegamenti rifatti: %d in %d file" % (link, cambiati))

tolti = 0
for lingua in LINGUE:
    p = os.path.join(DOCS, lingua, "app-native.md")
    if os.path.exists(p):
        os.remove(p)
        tolti += 1
print("pagine tolte: %d" % tolti)

# the redirects: /docs/app-native -> /docs/control-center, one per language
conf = os.path.join(repo, "website", "astro.config.mjs")
with open(conf, encoding="utf-8") as f:
    s = f.read()
if "docs/app-native" not in s:
    righe = ["    // The \"Native apps\" page is gone: those apps are the Control Center now.",
             "    // The old addresses were linked from the forum and from our own posts."]
    for lingua in LINGUE:
        pre = "" if lingua == "it" else "/" + lingua
        righe.append("    '%s/docs/app-native': '%s/docs/control-center'," % (pre, pre))
    s = s.replace("  redirects: {\n", "  redirects: {\n" + "\n".join(righe) + "\n", 1)
    with open(conf, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("redirect aggiunti: %d" % len(LINGUE))
else:
    print("redirect: gia' presenti")

resto = []
for p in sorted(glob.glob(os.path.join(repo, "website", "src", "**", "*"), recursive=True)):
    if os.path.isfile(p) and p.endswith((".md", ".astro", ".ts")):
        with open(p, encoding="utf-8") as f:
            if "app-native" in f.read():
                resto.append(os.path.relpath(p, repo))
print("restano citazioni in:", resto or "nessun file")
