#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La novità del sito per il pavimento delle CU (#77) e quello che è uscito con
la 26.09.28 e la 26.09.29.

Runs on the build VM inside ~/sfx-src/website. Inserts one post at the top of
`news`.

⚠️ UNA VOCE SOLA E NON DUE. La 26.09.28 e la 26.09.29 sono uscite a un giorno
di distanza e sono lo stesso lavoro visto dall'utente: il Control Center che
smette di proporre cose che la scheda rifiuta e comincia a dire perché. Due
voci consecutive che raccontano mezza cosa ciascuna si leggono peggio di una
che le racconta tutte.

⚠️ SI DICE COSA CAMBIA PER CHI USA IL SISTEMA, non cosa abbiamo fatto noi.
Niente numeri di issue, niente nomi di funzioni: quelli stanno su GitHub.
"""
import io
import os

PERCORSO = os.path.expanduser("~/sfx-src/website/src/news.ts")

QUANDO = {
    "it": "17 settembre 2026", "en": "17 September 2026",
    "pl": "17 września 2026", "uk": "17 вересня 2026",
    "ru": "17 сентября 2026", "es": "17 de septiembre de 2026",
    "pt": "17 de setembro de 2026", "de": "17. September 2026",
    "fr": "17 septembre 2026",
}

ETICHETTA = {
    "it": "novità", "en": "new", "pl": "nowość", "uk": "новинка",
    "ru": "новинка", "es": "novedad", "pt": "novidade", "de": "Neu",
    "fr": "nouveauté",
}

TITOLO = {
    "it": "Anche le prime tre coppie di CU si possono spegnere",
    "en": "The first three CU pairs can be switched off too",
    "pl": "Trzy pierwsze pary CU też można wyłączyć",
    "uk": "Перші три пари CU теж можна вимкнути",
    "ru": "Первые три пары CU тоже можно выключить",
    "es": "Los tres primeros pares de CU también se pueden apagar",
    "pt": "Os três primeiros pares de CU também se podem desligar",
    "de": "Auch die ersten drei CU-Paare lassen sich abschalten",
    "fr": "Les trois premières paires de CU peuvent aussi être éteintes",
}

TESTO = {
    "it": "Il pannello delle Compute Unit teneva grigie le prime tre coppie, perché un nostro commento diceva che le tiene accese il driver. Non è vero, e l'abbiamo misurato sulla scheda: si spengono, e le prestazioni calano in proporzione esatta. Adesso <strong>si spengono tutte</strong>, con almeno una coppia accesa per riga, e la scelta si può <strong>mantenere all'avvio</strong>: serve a chi ha una Compute Unit guasta e la vuole lasciare spenta. Nello stesso giro il pannello CPU ha smesso di proporre frequenze che la scheda rifiuta e adesso dice quale valore non va, e la casella del Governor risponde anche per il prossimo avvio invece che solo per adesso. La segnalazione è di tom lima, che ci ha anche trovato un difetto nel codice delle maschere.",
    "en": "The Compute Unit panel kept the first three pairs greyed out, because a comment of ours said the driver holds them on. It does not, and we measured it on the board: they switch off, and the performance drops in exact proportion. Now <strong>every pair can be switched off</strong>, with at least one left on per row, and the choice can be <strong>kept at boot</strong>: that is what you need when a Compute Unit is faulty and has to stay off. In the same round the CPU panel stopped offering clocks the board refuses and now says which value is wrong, and the Governor box answers for the next boot as well, not just for right now. Reported by tom lima, who also found a bug of ours in the mask code.",
    "pl": "Panel Compute Unit trzymał trzy pierwsze pary wyszarzone, bo nasz komentarz twierdził, że sterownik trzyma je włączone. Tak nie jest, i zmierzyliśmy to na płycie: wyłączają się, a wydajność spada dokładnie proporcjonalnie. Teraz <strong>można wyłączyć każdą parę</strong>, zostawiając co najmniej jedną włączoną w wierszu, a wybór można <strong>zachować przy starcie</strong>: tego potrzebuje ktoś, kto ma uszkodzoną Compute Unit i chce ją zostawić wyłączoną. W tej samej turze panel CPU przestał proponować taktowania, które płyta odrzuca, i mówi teraz, która wartość jest zła, a pole Governora odpowiada też za następny start, nie tylko za teraz. Zgłosił to tom lima, który znalazł u nas również błąd w kodzie masek.",
    "uk": "Панель Compute Unit тримала перші три пари сірими, бо наш коментар стверджував, що драйвер тримає їх увімкненими. Це не так, і ми виміряли це на платі: вони вимикаються, а продуктивність падає точно пропорційно. Тепер <strong>можна вимкнути будь-яку пару</strong>, лишивши щонайменше одну ввімкненою в рядку, а вибір можна <strong>зберегти при завантаженні</strong>: саме це потрібно тому, у кого несправна Compute Unit і хто хоче лишити її вимкненою. У цьому ж заході панель CPU перестала пропонувати частоти, які плата відхиляє, і тепер каже, яке значення не годиться, а прапорець Governor відповідає й за наступне завантаження, а не лише за зараз. Про це повідомив tom lima, який знайшов у нас також помилку в коді масок.",
    "ru": "Панель Compute Unit держала первые три пары серыми, потому что наш комментарий утверждал, что драйвер держит их включёнными. Это не так, и мы измерили это на плате: они выключаются, а производительность падает строго пропорционально. Теперь <strong>можно выключить любую пару</strong>, оставив хотя бы одну включённой в строке, а выбор можно <strong>сохранить при загрузке</strong>: именно это нужно тому, у кого неисправна Compute Unit и кто хочет оставить её выключенной. В том же заходе панель CPU перестала предлагать частоты, которые плата отклоняет, и теперь говорит, какое значение не годится, а флажок Governor отвечает и за следующую загрузку, а не только за сейчас. Сообщил об этом tom lima, который нашёл у нас и ошибку в коде масок.",
    "es": "El panel de Compute Units mantenía en gris los tres primeros pares, porque un comentario nuestro decía que el controlador los mantiene encendidos. No es así, y lo medimos en la placa: se apagan, y el rendimiento baja en proporción exacta. Ahora <strong>se puede apagar cualquier par</strong>, dejando al menos uno encendido por fila, y la elección se puede <strong>mantener al arranque</strong>: eso es lo que hace falta cuando una Compute Unit está defectuosa y tiene que quedarse apagada. En la misma tanda el panel de CPU dejó de ofrecer frecuencias que la placa rechaza y ahora dice qué valor no vale, y la casilla del Governor responde también por el próximo arranque, no sólo por ahora. Lo avisó tom lima, que además nos encontró un fallo en el código de las máscaras.",
    "pt": "O painel das Compute Units mantinha a cinzento os três primeiros pares, porque um comentário nosso dizia que o controlador os mantém ligados. Não é verdade, e medimo-lo na placa: desligam-se, e o desempenho cai em proporção exata. Agora <strong>pode desligar-se qualquer par</strong>, deixando pelo menos um ligado por linha, e a escolha pode ser <strong>mantida no arranque</strong>: é isso que faz falta quando uma Compute Unit está defeituosa e tem de ficar desligada. Na mesma volta o painel da CPU deixou de oferecer frequências que a placa recusa e agora diz que valor não serve, e a caixa do Governor responde também pelo próximo arranque, não só por agora. Avisou-nos tom lima, que também nos encontrou um defeito no código das máscaras.",
    "de": "Die Compute-Unit-Karte hielt die ersten drei Paare ausgegraut, weil ein Kommentar von uns behauptete, der Treiber halte sie an. Das stimmt nicht, und wir haben es auf der Karte gemessen: sie lassen sich abschalten, und die Leistung sinkt genau proportional. Jetzt <strong>lässt sich jedes Paar abschalten</strong>, mindestens eines bleibt je Zeile an, und die Auswahl kann <strong>beim Start erhalten bleiben</strong>: genau das braucht man, wenn eine Compute Unit defekt ist und aus bleiben muss. In derselben Runde bietet die CPU-Karte keine Takte mehr an, die die Karte ablehnt, und sagt jetzt, welcher Wert nicht geht, und das Governor-Kästchen antwortet auch für den nächsten Start, nicht nur für jetzt. Gemeldet hat es tom lima, der bei uns außerdem einen Fehler im Masken-Code gefunden hat.",
    "fr": "Le panneau des Compute Units gardait les trois premières paires en grisé, parce qu'un commentaire de notre part affirmait que le pilote les maintient allumées. C'est faux, et nous l'avons mesuré sur la carte : elles s'éteignent, et les performances baissent exactement en proportion. Désormais <strong>toute paire peut être éteinte</strong>, avec au moins une allumée par ligne, et le choix peut être <strong>conservé au démarrage</strong> : c'est ce qu'il faut quand une Compute Unit est défectueuse et doit rester éteinte. Dans la même série, le panneau CPU a cessé de proposer des fréquences que la carte refuse et dit maintenant quelle valeur ne convient pas, et la case du Governor répond aussi pour le prochain démarrage, pas seulement pour l'instant. C'est tom lima qui l'a signalé, et qui nous a aussi trouvé un défaut dans le code des masques.",
}

LINGUE = ["it", "en", "pl", "uk", "ru", "es", "pt", "de", "fr"]


def riga(nome, d, indent):
    pezzi = ", ".join('%s: %s' % (l, json_str(d[l])) for l in LINGUE)
    return "%s%s: { %s }," % (" " * indent, nome, pezzi)


def json_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


def blocco(nome, d, indent):
    fuori = [" " * indent + nome + ": {"]
    for l in LINGUE:
        fuori.append("%s%s: %s," % (" " * (indent + 2), l, json_str(d[l])))
    fuori.append(" " * indent + "},")
    return "\n".join(fuori)


VOCE = "\n".join([
    "  {",
    "    // cu-pavimento-2026-09-17",
    "    data: '2026-09-17',",
    riga("quando", QUANDO, 4),
    riga("etichetta", ETICHETTA, 4),
    blocco("titolo", TITOLO, 4),
    blocco("testo", TESTO, 4),
    "  },",
    "",
])

testo = io.open(PERCORSO, encoding="utf-8").read()
if "cu-pavimento-2026-09-17" in testo:
    raise SystemExit("la voce c'e' gia'")

ancora = "export const news: Post[] = [\n"
if testo.count(ancora) != 1:
    raise SystemExit("non trovo dove comincia l'elenco delle novita'")
testo = testo.replace(ancora, ancora + VOCE)
io.open(PERCORSO, "w", encoding="utf-8", newline="\n").write(testo)
print("voce aggiunta in testa, %d lingue" % len(LINGUE))
