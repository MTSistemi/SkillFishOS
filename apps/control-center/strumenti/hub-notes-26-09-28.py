#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hub release notes for 26.09.28: Control Center (CPU limits #78, Governor
box #79, AI page translations) and skillfish-base (shared dictionaries).

Runs on the build VM inside ~/sfx-src. Inserts one <release> above the others.
"""
import io
import os

VER, DATE = "26.09.28", "2026-09-16"
ROOT = os.path.expanduser("~/sfx-src/apps")

NOTES = {
    "control-center/os.skillfish.control-center.metainfo.xml": [
        ("", "The CPU panel offers only what the board accepts, 3500 to 4500 MHz and down to -40 undervolt steps, and when a value is refused it says which one. The Governor box is ticked when the governor is running and also starts at boot; the tooltip tells the two apart. The AI page and the cluster card are translated into all nine languages."),
        ("it", "Il pannello CPU propone solo quello che la scheda accetta, da 3500 a 4500 MHz e fino a -40 passi di undervolt, e quando un valore viene rifiutato dice quale. La casella del Governor è spuntata quando il governor gira e parte anche all'avvio; il suggerimento dice quale delle due manca. La pagina AI e la scheda del cluster sono tradotte in tutte e nove le lingue."),
        ("fr", "Le panneau CPU ne propose que ce que la carte accepte, de 3500 à 4500 MHz et jusqu'à -40 pas d'undervolt, et quand une valeur est refusée il dit laquelle. La case du Governor est cochée quand le governor tourne et démarre aussi au lancement ; l'infobulle distingue les deux. La page IA et la carte du cluster sont traduites dans les neuf langues."),
        ("es", "El panel de CPU ofrece solo lo que la placa acepta, de 3500 a 4500 MHz y hasta -40 pasos de undervolt, y cuando rechaza un valor dice cuál. La casilla del Governor queda marcada cuando el governor está en marcha y además arranca con el sistema; la descripción emergente distingue las dos cosas. La página de IA y la tarjeta del clúster están traducidas a los nueve idiomas."),
        ("pt", "O painel da CPU oferece só o que a placa aceita, de 3500 a 4500 MHz e até -40 passos de undervolt, e quando recusa um valor diz qual. A caixa do Governor fica marcada quando o governor está a correr e também arranca com o sistema; a dica distingue as duas coisas. A página de IA e o cartão do cluster estão traduzidos nas nove línguas."),
        ("de", "Die CPU-Karte bietet nur an, was die Karte annimmt, 3500 bis 4500 MHz und bis zu -40 Undervolt-Stufen, und bei einem abgelehnten Wert sagt sie, welcher es ist. Das Governor-Kästchen ist angehakt, wenn der Governor läuft und auch beim Start mitkommt; der Tooltip unterscheidet beides. Die KI-Seite und die Cluster-Karte sind in alle neun Sprachen übersetzt."),
        ("pl", "Panel CPU proponuje tylko to, co płyta przyjmuje, od 3500 do 4500 MHz i do -40 kroków undervoltu, a gdy wartość zostanie odrzucona, mówi która. Pole Governora jest zaznaczone, gdy governor działa i uruchamia się też przy starcie; podpowiedź rozróżnia te dwie rzeczy. Strona AI i karta klastra są przetłumaczone na wszystkie dziewięć języków."),
        ("ru", "Панель CPU предлагает только то, что принимает плата: от 3500 до 4500 МГц и до -40 шагов андервольта, а если значение отклонено, говорит какое. Флажок Governor отмечен, когда регулятор работает и запускается при загрузке; подсказка различает эти два условия. Страница ИИ и карточка кластера переведены на все девять языков."),
        ("uk", "Панель CPU пропонує лише те, що приймає плата: від 3500 до 4500 МГц і до -40 кроків андервольту, а якщо значення відхилено, каже яке. Прапорець Governor позначено, коли регулятор працює і запускається під час завантаження; підказка розрізняє ці дві умови. Сторінку ШІ та картку кластера перекладено всіма дев'ятьма мовами."),
    ],
    "base/os.skillfish.base.metainfo.xml": [
        ("", "The shared translations cover the whole AI page of the Control Center in all nine languages. Maintenance release, nothing else changes."),
        ("it", "Le traduzioni condivise coprono tutta la pagina AI del Control Center in tutte e nove le lingue. Versione di manutenzione, per il resto non cambia niente."),
        ("fr", "Les traductions partagées couvrent toute la page IA du Control Center dans les neuf langues. Version de maintenance, rien d'autre ne change."),
        ("es", "Las traducciones compartidas cubren toda la página de IA del Control Center en los nueve idiomas. Versión de mantenimiento, no cambia nada más."),
        ("pt", "As traduções partilhadas cobrem toda a página de IA do Control Center nas nove línguas. Versão de manutenção, não muda mais nada."),
        ("de", "Die gemeinsamen Übersetzungen decken die ganze KI-Seite des Control Centers in allen neun Sprachen ab. Wartungsversion, sonst ändert sich nichts."),
        ("pl", "Wspólne tłumaczenia obejmują całą stronę AI w Control Center we wszystkich dziewięciu językach. Wersja serwisowa, poza tym nic się nie zmienia."),
        ("ru", "Общие переводы охватывают всю страницу ИИ в Control Center на всех девяти языках. Служебная версия, больше ничего не меняется."),
        ("uk", "Спільні переклади охоплюють усю сторінку ШІ в Control Center усіма дев'ятьма мовами. Службова версія, більше нічого не змінюється."),
    ],
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


for rel, paras in NOTES.items():
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    if 'version="%s"' % VER in text:
        print("%s: already there" % rel)
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
    print("%s: +%s" % (rel, VER))
