#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The three sentences the CPU panel gained with issue #78, in seven languages.

Runs ON the build VM, inside ~/sfx-src.

    python3 traduzioni-cpu-limiti.py

Adds the keys to apps/control-center/i18n/<lang>.json. The shared dictionaries
under system/usr/share/skillfish/i18n/ are then fed by unisci-i18n.py, which
also builds it.json out of the (it, en) pairs in the code and checks that the
placeholders match.

⚠️ The wording reuses the terms already in the dictionaries instead of
inventing new ones: Clock is Takt / Frecuencia / Fréquence / Zegar /
Frequência / Частота, Degree limit is Gradgrenze / Límite de grados / Limite de
degrés / Limit stopni / Limite de graus / Предел градусов / Межа градусів, and
the undervolt is "UV" in the western languages, снижение / зниження in the
other two. A user should read the same word in the error as on the knob.

⚠️ Portuguese says "válida" rather than a past participle, because "aceite"
and "aceito" split pt-PT from pt-BR and the file serves both.
"""
import io
import json
import os

RADICE = os.path.expanduser("~/sfx-src/apps/control-center/i18n")

CLOCK = "The accepted clock runs from %d to %d MHz."
UV = "The accepted undervolt runs from %d to %d steps."
GRADI = "The accepted degree limit runs from %d to %d."

VOCI = {
    "de": {
        CLOCK: "Der akzeptierte Takt reicht von %d bis %d MHz.",
        UV: "Das akzeptierte UV reicht von %d bis %d Stufen.",
        GRADI: "Die akzeptierte Gradgrenze reicht von %d bis %d.",
    },
    "es": {
        CLOCK: "La frecuencia aceptada va de %d a %d MHz.",
        UV: "El UV aceptado va de %d a %d pasos.",
        GRADI: "El límite de grados aceptado va de %d a %d.",
    },
    "fr": {
        CLOCK: "La fréquence acceptée va de %d à %d MHz.",
        UV: "L'UV accepté va de %d à %d crans.",
        GRADI: "La limite de degrés acceptée va de %d à %d.",
    },
    "pl": {
        CLOCK: "Akceptowany zegar to od %d do %d MHz.",
        UV: "Akceptowany UV to od %d do %d kroków.",
        GRADI: "Akceptowany limit stopni to od %d do %d.",
    },
    "pt": {
        CLOCK: "A frequência válida vai de %d a %d MHz.",
        UV: "O UV válido vai de %d a %d passos.",
        GRADI: "O limite de graus válido vai de %d a %d.",
    },
    "ru": {
        CLOCK: "Допустимая частота: от %d до %d МГц.",
        UV: "Допустимое снижение: от %d до %d ступеней.",
        GRADI: "Допустимый предел градусов: от %d до %d.",
    },
    "uk": {
        CLOCK: "Допустима частота: від %d до %d МГц.",
        UV: "Допустиме зниження: від %d до %d кроків.",
        GRADI: "Допустима межа градусів: від %d до %d.",
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
