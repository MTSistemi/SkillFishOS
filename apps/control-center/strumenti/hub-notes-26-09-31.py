#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hub release notes for 26.09.31: skillfish-cu stops writing the always-on mask.

Runs on the build VM inside ~/sfx-src. Inserts one <release> above the others.

⚠️ BEFORE build-debs-ci.sh: the .deb carries the metainfo.

⚠️ AND IT GOES IN THE HUD'S METAINFO, which reads oddly and is not a mistake.
One package moves, skillfish-tuner, and the only metainfo that package ships is
`apps/hud/os.skillfish.hud.metainfo.xml`: the HUD lives inside skillfish-tuner
and has no package of its own, while the Tuner stopped being a separate
application in 26.09 and its metainfo was dropped in 0d9b630. So in the Hub this
update shows up under "SkillFishOS HUD". The note says outright that the HUD is
not what changed, rather than dressing a CU routing fix as a HUD feature.
"""
import io
import os

VER, DATE = "26.09.31", "2026-09-17"
ROOT = os.path.expanduser("~/sfx-src/apps")

NOTES = {
    "hud/os.skillfish.hud.metainfo.xml": [
        ("", "Nothing changes in the HUD. This package also carries the tool that routes the Compute Units, and that tool has stopped forcing a power register the graphics driver is meant to manage on its own. Measured on the board: the same compute, to within a fifth of a percent, and one less obstacle in the way of ROCm."),
        ("it", "Nell'HUD non cambia niente. Questo pacchetto porta anche lo strumento che instrada le Compute Unit, e quello strumento ha smesso di forzare un registro di alimentazione che deve gestire il driver grafico da sé. Misurato sulla scheda: stesso calcolo, entro un quinto di percento, e un ostacolo in meno sulla strada di ROCm."),
        ("fr", "Rien ne change dans le HUD. Ce paquet contient aussi l'outil qui route les Compute Units, et cet outil a cessé de forcer un registre d'alimentation que le pilote graphique doit gérer lui-même. Mesuré sur la carte : le même calcul, à un cinquième de pour cent près, et un obstacle en moins sur la route de ROCm."),
        ("es", "En el HUD no cambia nada. Este paquete lleva también la herramienta que enruta las Compute Units, y esa herramienta ha dejado de forzar un registro de alimentación que debe gestionar el propio controlador gráfico. Medido en la placa: el mismo cálculo, dentro de un quinto de por ciento, y un obstáculo menos en el camino de ROCm."),
        ("pt", "No HUD não muda nada. Este pacote leva também a ferramenta que encaminha as Compute Units, e essa ferramenta deixou de forçar um registo de alimentação que deve ser gerido pelo próprio controlador gráfico. Medido na placa: o mesmo cálculo, dentro de um quinto de por cento, e um obstáculo a menos no caminho do ROCm."),
        ("de", "Am HUD ändert sich nichts. Dieses Paket enthält auch das Werkzeug, das die Compute Units verteilt, und dieses Werkzeug erzwingt kein Energieregister mehr, das der Grafiktreiber selbst verwalten soll. Auf der Karte gemessen: dieselbe Rechenleistung, auf ein Fünftel Prozent genau, und ein Hindernis weniger auf dem Weg zu ROCm."),
        ("pl", "W HUD nic się nie zmienia. Ten pakiet zawiera też narzędzie, które rozdziela Compute Unity, i to narzędzie przestało wymuszać rejestr zasilania, którym ma zarządzać sam sterownik graficzny. Zmierzone na płycie: te same obliczenia, z dokładnością do jednej piątej procenta, i o jedną przeszkodę mniej na drodze do ROCm."),
        ("ru", "В HUD ничего не меняется. В этом пакете есть и средство, распределяющее Compute Unit, и оно перестало принудительно задавать регистр питания, которым должен управлять сам графический драйвер. Измерено на плате: те же вычисления, с точностью до пятой доли процента, и на одно препятствие меньше на пути к ROCm."),
        ("uk", "У HUD нічого не змінюється. У цьому пакунку є й засіб, що розподіляє Compute Unit, і він перестав примусово задавати регістр живлення, яким має керувати сам графічний драйвер. Виміряно на платі: ті самі обчислення, з точністю до п'ятої частки відсотка, і на одну перешкоду менше на шляху до ROCm."),
    ],
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


for rel, paras in NOTES.items():
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    if 'version="%s"' % VER in text:
        print("%s: gia' presente" % rel)
        continue
    anchor = "    <release "
    at = text.index(anchor)
    lines = ['    <release version="%s" date="%s">' % (VER, DATE), "      <description>"]
    for lang, p in paras:
        attr = ' xml:lang="%s"' % lang if lang else ""
        lines.append("        <p%s>%s</p>" % (attr, esc(p)))
    lines += ["      </description>", "    </release>", ""]
    text = text[:at] + "\n".join(lines) + text[at:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("%s: +%s (%d lingue)" % (rel, VER, len(paras)))
