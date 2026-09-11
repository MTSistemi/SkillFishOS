#!/usr/bin/env python3
"""The last strings the dictionaries lacked after the AI section: a few real
words missing in one or two languages, and the ones that are the same word
everywhere (product names, flatpak, SMT, the chip name) which still have to be
in the file or the "?" of the check keeps reporting them.

    aggiungi-traduzioni-1209b.py <repo>
"""
import json
import os
import subprocess
import sys

repo = sys.argv[1]
d = os.path.join(repo, "apps", "control-center", "i18n")
L = ("de", "es", "fr", "pl", "pt", "ru", "uk")


def T(*tr):
    return dict(zip(L, tr))


def UGUALE(s):
    return {lang: s for lang in L}


NUOVE = {
    # the same in every language: names, formats, units
    "HUD": UGUALE("HUD"),
    "Hub": UGUALE("Hub"),
    "Remote Manager": UGUALE("Remote Manager"),
    "BC-250 · znver2": UGUALE("BC-250 · znver2"),
    "SMT %s": UGUALE("SMT %s"),
    "flatpak": UGUALE("flatpak"),
    "24 CU: %s GFLOPS": UGUALE("24 CU: %s GFLOPS"),
    "%d MHz @ %d: %s (min %d MHz)": UGUALE("%d MHz @ %d: %s (min %d MHz)"),
    "Watts max": UGUALE("Watts max"),
    "Watts ok": UGUALE("Watts ok"),
    # real words, missing in one or two languages
    "Engine": T("Motor", "Motor", "Moteur", "Silnik", "Motor", "Движок", "Рушій"),
    "Status": T("Status", "Estado", "État", "Stan", "Estado", "Состояние", "Стан"),
    "Scheduler": T("Scheduler", "Planificador", "Ordonnanceur", "Scheduler", "Escalonador", "Планировщик", "Планувальник"),
    "Maximum": T("Maximum", "Máximo", "Maximum", "Maksimum", "Máximo", "Максимум", "Максимум"),
    "Actions": T("Aktionen", "Acciones", "Actions", "Akcje", "Ações", "Действия", "Дії"),
    "Documentation": T("Dokumentation", "Documentación", "Documentation", "Dokumentacja", "Documentação", "Документация", "Документація"),
    "Guide": T("Anleitung", "Guía", "Guide", "Przewodnik", "Guia", "Руководство", "Посібник"),
    "system": T("System", "sistema", "système", "system", "sistema", "система", "система"),
    "no": T("nein", "no", "non", "nie", "não", "нет", "ні"),
}

for lang in L:
    p = os.path.join(d, lang + ".json")
    with open(p, encoding="utf-8") as f:
        j = json.load(f)
    n = 0
    for en, tr in NUOVE.items():
        if en not in j:
            j[en] = tr[lang]
            n += 1
    with open(p, "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(lang, "+%d" % n, "totale", len(j))

subprocess.run([sys.executable, os.path.join(repo, "apps", "control-center", "strumenti", "unisci-i18n.py"),
                os.path.join(repo, "apps", "control-center"),
                os.path.join(repo, "system", "usr", "share", "skillfish", "i18n")], check=True)
