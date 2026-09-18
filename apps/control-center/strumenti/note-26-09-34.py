#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""26.09.34: the Hub release note and the post on the site.

Runs on the build VM inside ~/sfx-src.

⚠️ BEFORE build-debs-ci.sh: the .deb carries the metainfo, so a note written
afterwards ships one release late.

The note is on skillfish-hub, which is the window where the problem was seen.
Both texts say what the user sees, not how flatpak is wired: nothing was
failing to download, the list was showing rows that no update could ever take
away.
"""
import io
import os

VER, DATE = "26.09.34", "2026-09-18"
ROOT = os.path.expanduser("~/sfx-src")
HUB = os.path.join(ROOT, "apps/hub/os.skillfish.hub.metainfo.xml")
NEWS = os.path.join(ROOT, "website/src/news.ts")

NOTE = [
    ("", "Some flatpak entries used to sit in the update list looking as if they could never update. Nothing was failing to download: two identical-looking rows were two different versions of the same component, and system components no application uses any more came back at every check. The version now appears next to the name, what nothing depends on is removed after the update, and the list is read afresh instead of trusting the copy kept on the machine."),
    ("it", "Nell'elenco degli aggiornamenti restavano voci flatpak che sembravano non aggiornarsi mai. Non era un download che falliva: due righe uguali erano due versioni diverse dello stesso componente, e alcuni componenti di sistema che non usa più nessun programma tornavano a ogni controllo. Adesso accanto al nome c'è la versione, quello che non serve più viene tolto dopo l'aggiornamento, e l'elenco si rilegge da capo invece di fidarsi della copia tenuta sulla macchina."),
    ("fr", "Certaines entrées flatpak restaient dans la liste des mises à jour comme si elles ne pouvaient jamais se mettre à jour. Rien n'échouait au téléchargement : deux lignes identiques étaient deux versions différentes du même composant, et des composants système que plus aucune application n'utilise revenaient à chaque vérification. La version apparaît maintenant à côté du nom, ce dont plus rien ne dépend est retiré après la mise à jour, et la liste est relue au lieu de faire confiance à la copie gardée sur la machine."),
    ("es", "En la lista de actualizaciones quedaban entradas flatpak que parecían no actualizarse nunca. No fallaba ninguna descarga: dos filas iguales eran dos versiones distintas del mismo componente, y componentes del sistema que ya no usa ningún programa volvían en cada comprobación. Ahora la versión aparece junto al nombre, lo que ya no hace falta se quita después de actualizar, y la lista se vuelve a leer en vez de fiarse de la copia guardada en la máquina."),
    ("pt", "Na lista de atualizações ficavam entradas flatpak que pareciam nunca se atualizar. Não havia nenhuma transferência a falhar: duas linhas iguais eram duas versões diferentes do mesmo componente, e componentes do sistema que já nenhum programa usa voltavam em cada verificação. Agora a versão aparece ao lado do nome, o que já não é preciso é retirado depois da atualização, e a lista é lida de novo em vez de confiar na cópia guardada na máquina."),
    ("de", "In der Aktualisierungsliste blieben Flatpak-Einträge stehen, als könnten sie sich nie aktualisieren. Es schlug kein Download fehl: zwei gleich aussehende Zeilen waren zwei verschiedene Versionen derselben Komponente, und Systemkomponenten, die keine Anwendung mehr nutzt, kamen bei jeder Prüfung zurück. Jetzt steht die Version neben dem Namen, was nicht mehr gebraucht wird, verschwindet nach der Aktualisierung, und die Liste wird neu gelesen, statt der auf dem Rechner liegenden Kopie zu vertrauen."),
    ("pl", "Na liście aktualizacji zostawały wpisy flatpaka, które wyglądały, jakby nigdy nie mogły się zaktualizować. Nic nie zawodziło przy pobieraniu: dwa takie same wiersze to były dwie różne wersje tego samego składnika, a składniki systemu, z których nie korzysta już żaden program, wracały przy każdym sprawdzeniu. Teraz obok nazwy widać wersję, to, czego już nic nie potrzebuje, jest usuwane po aktualizacji, a lista jest czytana od nowa zamiast polegać na kopii trzymanej na maszynie."),
    ("ru", "В списке обновлений оставались записи flatpak, которые будто никогда не могли обновиться. Ничего не срывалось при загрузке: две одинаковые строки были двумя разными версиями одного компонента, а системные компоненты, которыми больше не пользуется ни одна программа, возвращались при каждой проверке. Теперь версия видна рядом с именем, ненужное удаляется после обновления, а список перечитывается заново, а не берётся из копии, лежащей на машине."),
    ("uk", "У списку оновлень лишалися записи flatpak, які ніби ніколи не могли оновитися. Нічого не зривалося під час завантаження: два однакові рядки були двома різними версіями того самого компонента, а системні компоненти, якими більше не користується жодна програма, поверталися під час кожної перевірки. Тепер версія видно поряд з назвою, непотрібне прибирається після оновлення, а список перечитується заново, замість того щоб довіряти копії на машині."),
]

QUANDO = {
    "it": "18 settembre 2026", "en": "18 September 2026", "pl": "18 września 2026",
    "uk": "18 вересня 2026", "ru": "18 сентября 2026",
    "es": "18 de septiembre de 2026", "pt": "18 de setembro de 2026",
    "de": "18. September 2026", "fr": "18 septembre 2026",
}
ETICHETTA = {
    "it": "correzione", "en": "fix", "pl": "poprawka", "uk": "виправлення",
    "ru": "исправление", "es": "corrección", "pt": "correção",
    "de": "Korrektur", "fr": "correctif",
}
TITOLO = {
    "it": "Gli aggiornamenti flatpak che non se ne andavano mai",
    "en": "The flatpak updates that never went away",
    "pl": "Aktualizacje flatpaka, które nigdy nie znikały",
    "uk": "Оновлення flatpak, які ніколи не зникали",
    "ru": "Обновления flatpak, которые никогда не исчезали",
    "es": "Las actualizaciones de flatpak que nunca se iban",
    "pt": "As atualizações flatpak que nunca desapareciam",
    "de": "Die Flatpak-Aktualisierungen, die nie verschwanden",
    "fr": "Les mises à jour flatpak qui ne partaient jamais",
}
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


# --- sito --------------------------------------------------------------------
def riga(d):
    return ", ".join('%s: "%s"' % (k, d[k].replace('"', '\\"')) for k in ORDINE)


def blocco(d, ind):
    return "\n".join('%s%s: "%s",' % (ind, k, d[k].replace('"', '\\"'))
                     for k in ORDINE).rstrip(",")


voce = (
    "  {\n"
    "    // flatpak-elenco-2026-09-18\n"
    "    data: '2026-09-18',\n"
    "    quando: { %s },\n"
    "    etichetta: { %s },\n"
    "    titolo: {\n%s\n    },\n"
    "    testo: {\n%s\n    },\n"
    "  },\n"
) % (riga(QUANDO), riga(ETICHETTA), blocco(TITOLO, "      "), blocco(TESTO, "      "))

ANCHOR = "export const news: Post[] = [\n"
with io.open(NEWS, encoding="utf-8") as f:
    news = f.read()
if "flatpak-elenco-2026-09-18" in news:
    print("news: gia' presente")
else:
    at = news.index(ANCHOR) + len(ANCHOR)
    news = news[:at] + voce + news[at:]
    with io.open(NEWS, "w", encoding="utf-8") as f:
        f.write(news)
    print("news.ts: post 26.09.34 in testa (%d lingue)" % len(ORDINE))
