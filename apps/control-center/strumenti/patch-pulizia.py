#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The last two copies of the standalone Tuner window, and the four open code
scanning alerts.

Runs ON the build VM, inside ~/sfx-src.

    python3 patch-pulizia.py [--prova]

⚠️ REMOVING THE FILES IS THE EASY HALF. `apps/tuner/skillfish-tuner` is named
in three places that would fail on a missing file, and all three have to go
with it:

  .github/workflows/ci.yml    the syntax-check loop, and the ruff list
  scripts/build-debs-ci.sh    the setDesktopFileName check, which greps the
                              file and exits 1 when grep finds nothing

`apps/tuner/skillfish-tuner-helper` stays: that one is shipped.

THE FOUR ALERTS

  py/unused-import          patch-cpu-limiti.py imports re, and the only
                            re.findall in the file is inside the replacement
                            string. The scanner is right.
  py/unused-global-variable _CPU_LIMITI is a module cache that is rebound
                            inside the function, so its value is only read on a
                            later call and the scanner cannot see that. A dict
                            that gets filled in is the same cache and reads as
                            used, with no `global` needed.
  py/empty-except x2        the last-resort excepthook in the Hub, in both
                            copies. It swallows on purpose; it just never said
                            why.
"""
import io
import os
import subprocess
import sys

PROVA = "--prova" in sys.argv
R = os.path.expanduser("~/sfx-src")

DA_TOGLIERE = ["apps/tuner/skillfish-tuner", "system/usr/local/bin/skillfish-tuner"]

CAMBI = []


def cambia(rel, vecchio, nuovo, etichetta):
    CAMBI.append((os.path.join(R, rel), vecchio, nuovo, etichetta))


# ------------------------------------------------- i riferimenti che restano
cambia(".github/workflows/ci.yml",
       "          for f in apps/tuner/skillfish-tuner apps/tuner/skillfish-tuner-helper \\\n",
       "          for f in apps/tuner/skillfish-tuner-helper \\\n",
       "ci.yml: il controllo di sintassi")

cambia(".github/workflows/ci.yml",
       '          PYAPPS="apps/tuner/skillfish-tuner apps/tuner/skillfish-tuner-helper \\\n',
       '          PYAPPS="apps/tuner/skillfish-tuner-helper \\\n',
       "ci.yml: l'elenco di ruff")

cambia("scripts/build-debs-ci.sh",
       "            apps/tuner/skillfish-tuner \\\n",
       "",
       "build-debs-ci.sh: il controllo del .desktop")

# ------------------------------------------------------------ py/unused-import
cambia("apps/control-center/strumenti/patch-cpu-limiti.py",
       "import io\nimport os\nimport re\nimport sys\n",
       "import io\nimport os\nimport sys\n",
       "patch-cpu-limiti.py: re non si usa")

# --------------------------------------------------- py/unused-global-variable
cambia("apps/control-center/skillfish-cc-helper",
       '''_CPU_LIMITI = None


def cpu_limiti():
    """What bc250_apply.py will actually accept, read once and kept."""
    global _CPU_LIMITI
    if _CPU_LIMITI is not None:
        return _CPU_LIMITI
''',
       '''# ⚠️ A dict, not a global that gets rebound. The cache used to be None and
# reassigned inside the function, and a scanner reads that as a global whose
# value nobody uses: it cannot follow a value that is only read on a later
# call. Filling a dict in place is the same cache and says so in the code.
_CPU_LIMITI = {}


def cpu_limiti():
    """What bc250_apply.py will actually accept, read once and kept."""
    if _CPU_LIMITI:
        return _CPU_LIMITI
''',
       "cc-helper: la cache non riassegna una globale")

cambia("apps/control-center/skillfish-cc-helper",
       '''    lim["scale_min"] = max(lim["scale_min"], CPU_UV_SICURO)
    _CPU_LIMITI = lim
    return lim
''',
       '''    lim["scale_min"] = max(lim["scale_min"], CPU_UV_SICURO)
    _CPU_LIMITI.update(lim)
    return _CPU_LIMITI
''',
       "cc-helper: si riempie invece di riassegnare")

# --------------------------------------------------------------- py/empty-except
VECCHIO_HUB = '''                                % ("%s: %s" % (tipo.__name__, valore)))
    except Exception:
        pass
'''
NUOVO_HUB = '''                                % ("%s: %s" % (tipo.__name__, valore)))
    except Exception:
        # The dialog itself failed. This is the excepthook, the last place an
        # error can be reported from, so there is nowhere left to report to and
        # raising here would swap one lost error for another. The window stays
        # open, which was the whole point of catching it.
        pass
'''
for rel in ("apps/hub/skillfish-hub", "system/usr/local/bin/skillfish-hub"):
    cambia(rel, VECCHIO_HUB, NUOVO_HUB, "hub: si dice perche' si ingoia (%s)" % rel.split("/")[0])

# ------------------------------------------------------------------- applica
testi = {}
for percorso, _, _, _ in CAMBI:
    testi.setdefault(percorso, io.open(percorso, encoding="utf-8").read())

esito = 0
for percorso, vecchio, nuovo, etichetta in CAMBI:
    n = testi[percorso].count(vecchio)
    stato = "ok" if n == 1 else "NON TROVATO" if n == 0 else "%d VOLTE" % n
    print("[%-11s] %s" % (stato, etichetta))
    if n != 1:
        esito = 1
        continue
    testi[percorso] = testi[percorso].replace(vecchio, nuovo)

if esito:
    sys.exit("\nqualche ancoraggio non combacia: non ho scritto niente")

# le due copie dell'Hub devono restare identiche, la CI lo pretende
a = testi[os.path.join(R, "apps/hub/skillfish-hub")]
b = testi[os.path.join(R, "system/usr/local/bin/skillfish-hub")]
if a != b:
    sys.exit("le due copie dell'Hub divergono: non ho scritto niente")
print("[ok         ] le due copie dell'Hub restano identiche")

if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

for percorso, testo in testi.items():
    io.open(percorso, "w", encoding="utf-8", newline="\n").write(testo)
    print("scritto %s" % percorso.replace(R + "/", ""))

for rel in DA_TOGLIERE:
    subprocess.run(["git", "-C", R, "rm", "-q", rel], check=True)
    print("tolto   %s" % rel)

import py_compile
for rel in ("apps/control-center/skillfish-cc-helper",
            "apps/control-center/strumenti/patch-cpu-limiti.py",
            "apps/hub/skillfish-hub"):
    py_compile.compile(os.path.join(R, rel), cfile="/tmp/sfx-pul.pyc", doraise=True)
os.remove("/tmp/sfx-pul.pyc")
print("compilano tutti")
