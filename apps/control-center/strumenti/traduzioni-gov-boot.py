#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The four sentences the Governor checkbox gained with issue #79.

Runs ON the build VM, inside ~/sfx-src.

    python3 traduzioni-gov-boot.py

They go in the tooltip, one about now and one about the next boot, so a user
can tell which of the two halves is missing. No placeholders in any of them,
which is the one thing unisci-i18n.py refuses to merge when it does not match.
"""
import io
import json
import os

RADICE = os.path.expanduser("~/sfx-src/apps/control-center/i18n")

ORA_SI = "It is on now."
ORA_NO = "It is off now."
BOOT_SI = "It comes back at the next boot."
BOOT_NO = "It does not come back at the next boot."

VOCI = {
    "de": {
        ORA_SI: "Läuft jetzt.",
        ORA_NO: "Läuft jetzt nicht.",
        BOOT_SI: "Kommt beim nächsten Start wieder.",
        BOOT_NO: "Kommt beim nächsten Start nicht wieder.",
    },
    "es": {
        ORA_SI: "Ahora está activo.",
        ORA_NO: "Ahora está parado.",
        BOOT_SI: "Vuelve en el próximo arranque.",
        BOOT_NO: "No vuelve en el próximo arranque.",
    },
    "fr": {
        ORA_SI: "Il tourne maintenant.",
        ORA_NO: "Il est arrêté maintenant.",
        BOOT_SI: "Il revient au prochain démarrage.",
        BOOT_NO: "Il ne revient pas au prochain démarrage.",
    },
    "pl": {
        ORA_SI: "Teraz działa.",
        ORA_NO: "Teraz nie działa.",
        BOOT_SI: "Wróci przy następnym uruchomieniu.",
        BOOT_NO: "Nie wróci przy następnym uruchomieniu.",
    },
    "pt": {
        ORA_SI: "Agora está ativo.",
        ORA_NO: "Agora está parado.",
        BOOT_SI: "Volta no próximo arranque.",
        BOOT_NO: "Não volta no próximo arranque.",
    },
    "ru": {
        ORA_SI: "Сейчас работает.",
        ORA_NO: "Сейчас остановлен.",
        BOOT_SI: "После перезагрузки запустится.",
        BOOT_NO: "После перезагрузки не запустится.",
    },
    "uk": {
        ORA_SI: "Зараз працює.",
        ORA_NO: "Зараз зупинений.",
        BOOT_SI: "Після перезавантаження запуститься.",
        BOOT_NO: "Після перезавантаження не запуститься.",
    },
}

for lingua, nuove in sorted(VOCI.items()):
    percorso = os.path.join(RADICE, lingua + ".json")
    with io.open(percorso, encoding="utf-8") as f:
        d = json.load(f)
    aggiunte = [k for k in nuove if k not in d]
    d.update({k: v for k, v in nuove.items() if k not in d})
    with io.open(percorso, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(d.items(), key=lambda kv: kv[0].lower())), f,
                  ensure_ascii=False, indent=1)
        f.write("\n")
    print("%s: +%d (totale %d)" % (lingua, len(aggiunte), len(d)))
