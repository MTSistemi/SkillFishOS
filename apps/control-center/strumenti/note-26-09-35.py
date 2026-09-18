#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""26.09.35: the Hub note, and the post on the site rewritten with the real cause.

Runs on the build VM inside ~/sfx-src.

⚠️ IL POST DELLA 26.09.34 DICEVA UNA COSA VERA MA NON LA CAUSA. Quella sera
avevamo corretto la presentazione (il ramo accanto al nome) e la pulizia dei
runtime abbandonati, e il post raccontava quello. La causa era un'altra:
flatpak tiene DUE archivi, quello di sistema e uno per utente, e «Aggiorna
tutto» girava da root, che il secondo non lo vede nemmeno. Il post si riscrive
invece di aggiungerne un altro a un'ora di distanza: chi legge il sito vuole
sapere cos'e' successo, non seguire i nostri passi.
"""
import io
import os

VER, DATE = "26.09.35", "2026-09-19"
ROOT = os.path.expanduser("~/sfx-src")
HUB = os.path.join(ROOT, "apps/hub/os.skillfish.hub.metainfo.xml")
NEWS = os.path.join(ROOT, "website/src/news.ts")

NOTE = [
    ("", "Updates that never went away. Flatpak keeps two separate stores: the system one and one for each user, and the programs installed for your own user — the emulators, for instance — live in the second. «Update all» ran with system privileges and only ever touched the first, so those entries came back at every check no matter how many times they were updated. Both are updated now, components no program uses any more are removed afterwards, and the list shows the version beside the name, because two rows that looked identical were two different versions of the same thing."),
    ("it", "Aggiornamenti che non se ne andavano mai. Flatpak tiene due archivi separati: quello di sistema e uno per ogni utente, e i programmi installati per il tuo utente — per esempio gli emulatori — stanno nel secondo. «Aggiorna tutto» girava con i permessi di sistema e toccava solo il primo, così quelle voci tornavano a ogni controllo per quante volte le si aggiornasse. Adesso vengono aggiornati tutti e due, i componenti che non usa più nessun programma vengono tolti dopo, e nell'elenco accanto al nome c'è la versione, perché due righe che sembravano uguali erano due versioni diverse della stessa cosa."),
    ("fr", "Des mises à jour qui ne partaient jamais. Flatpak tient deux dépôts séparés : celui du système et un par utilisateur, et les programmes installés pour votre utilisateur — les émulateurs, par exemple — sont dans le second. « Tout mettre à jour » s'exécutait avec les droits du système et ne touchait que le premier : ces entrées revenaient donc à chaque vérification, quel que soit le nombre de mises à jour lancées. Les deux sont désormais mis à jour, les composants que plus aucun programme n'utilise sont ensuite retirés, et la liste affiche la version à côté du nom, car deux lignes identiques étaient deux versions différentes de la même chose."),
    ("es", "Actualizaciones que nunca se iban. Flatpak mantiene dos almacenes separados: el del sistema y uno por cada usuario, y los programas instalados para tu usuario —los emuladores, por ejemplo— están en el segundo. «Actualizar todo» se ejecutaba con permisos del sistema y solo tocaba el primero, así que esas entradas volvían en cada comprobación por muchas veces que se actualizara. Ahora se actualizan los dos, después se quitan los componentes que ya no usa ningún programa, y la lista muestra la versión junto al nombre, porque dos filas que parecían iguales eran dos versiones distintas de lo mismo."),
    ("pt", "Atualizações que nunca desapareciam. O flatpak mantém dois arquivos separados: o do sistema e um para cada utilizador, e os programas instalados para o seu utilizador — os emuladores, por exemplo — estão no segundo. O «Atualizar tudo» corria com permissões de sistema e só mexia no primeiro, por isso aquelas entradas voltavam em cada verificação por mais vezes que se atualizasse. Agora são atualizados os dois, os componentes que já nenhum programa usa são retirados a seguir, e a lista mostra a versão ao lado do nome, porque duas linhas que pareciam iguais eram duas versões diferentes da mesma coisa."),
    ("de", "Aktualisierungen, die nie verschwanden. Flatpak führt zwei getrennte Ablagen: die des Systems und eine je Benutzer, und die für Ihren Benutzer installierten Programme — etwa die Emulatoren — liegen in der zweiten. «Alles aktualisieren» lief mit Systemrechten und rührte nur die erste an, also kamen diese Einträge bei jeder Prüfung zurück, so oft man auch aktualisierte. Jetzt werden beide aktualisiert, danach werden Komponenten entfernt, die kein Programm mehr nutzt, und die Liste zeigt die Version neben dem Namen, denn zwei gleich aussehende Zeilen waren zwei verschiedene Versionen derselben Sache."),
    ("pl", "Aktualizacje, które nigdy nie znikały. Flatpak prowadzi dwa osobne magazyny: systemowy i po jednym dla każdego użytkownika, a programy zainstalowane dla twojego użytkownika — na przykład emulatory — są w tym drugim. „Zaktualizuj wszystko” działało z uprawnieniami systemu i ruszało tylko pierwszy, więc te wpisy wracały przy każdym sprawdzeniu, ile razy by ich nie aktualizować. Teraz aktualizowane są oba, składniki, z których nie korzysta już żaden program, są potem usuwane, a lista pokazuje wersję obok nazwy, bo dwa wiersze wyglądające tak samo były dwiema różnymi wersjami tej samej rzeczy."),
    ("ru", "Обновления, которые никогда не исчезали. Flatpak держит два отдельных хранилища: системное и по одному на каждого пользователя, а программы, установленные для вашего пользователя, — например эмуляторы — лежат во втором. «Обновить всё» выполнялось с системными правами и трогало только первое, поэтому те записи возвращались при каждой проверке, сколько бы раз их ни обновляли. Теперь обновляются оба, компоненты, которыми больше не пользуется ни одна программа, затем удаляются, а список показывает версию рядом с именем: две одинаковые на вид строки были двумя разными версиями одного и того же."),
    ("uk", "Оновлення, які ніколи не зникали. Flatpak веде два окремі сховища: системне і по одному на кожного користувача, а програми, встановлені для вашого користувача — наприклад емулятори — лежать у другому. «Оновити все» виконувалося із системними правами й чіпало лише перше, тож ті записи поверталися під час кожної перевірки, скільки б разів їх не оновлювали. Тепер оновлюються обидва, компоненти, якими більше не користується жодна програма, потім прибираються, а список показує версію поряд з назвою: два однакові на вигляд рядки були двома різними версіями того самого."),
]

TESTO = dict((lang if lang else "en", testo) for lang, testo in NOTE)
ORDINE = ["it", "en", "pl", "uk", "ru", "es", "pt", "de", "fr"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --- Hub ---------------------------------------------------------------------
with io.open(HUB, encoding="utf-8") as f:
    text = f.read()
if 'version="%s"' % VER in text:
    print("Hub: gia' presente")
else:
    at = text.index("    <release ")
    righe = ['    <release version="%s" date="%s">' % (VER, DATE), "      <description>"]
    for lang, p in NOTE:
        attr = ' xml:lang="%s"' % lang if lang else ""
        righe.append("        <p%s>%s</p>" % (attr, esc(p)))
    righe += ["      </description>", "    </release>", ""]
    text = text[:at] + "\n".join(righe) + text[at:]
    with io.open(HUB, "w", encoding="utf-8") as f:
        f.write(text)
    print("hub metainfo: +%s (%d lingue)" % (VER, len(NOTE)))

# --- il post di ieri sera, riscritto -----------------------------------------
with io.open(NEWS, encoding="utf-8") as f:
    news = f.read()

inizio = news.index("// flatpak-elenco-2026-09-18")
apri = news.index("testo: {", inizio)
chiudi = news.index("    },", apri)
nuovo = "testo: {\n" + "\n".join(
    '      %s: "%s",' % (k, TESTO[k].replace('"', '\\"')) for k in ORDINE).rstrip(",") + "\n"
news = news[:apri] + nuovo + news[chiudi:]
with io.open(NEWS, "w", encoding="utf-8") as f:
    f.write(news)
print("news.ts: il post del 18/09 adesso racconta la causa vera")
