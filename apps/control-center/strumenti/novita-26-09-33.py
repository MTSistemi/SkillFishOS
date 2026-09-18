#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add the 26.09.33 post at the top of website/src/news.ts.

Runs on the build VM inside ~/sfx-src.

Four sentences, per the short-news rule. It says what changes for someone who
uses the machine and not how it is wired: the frame rate is the same, the point
is that the desktop and the games now run on the same driver, and that a PC
which is not a BC-250 is left alone.
"""
import io
import os

PATH = os.path.expanduser("~/sfx-src/website/src/news.ts")
ANCHOR = "export const news: Post[] = [\n"

QUANDO = {
    "it": "18 settembre 2026", "en": "18 September 2026", "pl": "18 września 2026",
    "uk": "18 вересня 2026", "ru": "18 сентября 2026",
    "es": "18 de septiembre de 2026", "pt": "18 de setembro de 2026",
    "de": "18. September 2026", "fr": "18 septembre 2026",
}
ETICHETTA = {
    "it": "novità", "en": "new", "pl": "nowość", "uk": "новинка",
    "ru": "новинка", "es": "novedad", "pt": "novidade",
    "de": "Neu", "fr": "nouveauté",
}
TITOLO = {
    "it": "La nostra Mesa diventa il driver di tutta la scheda",
    "en": "Our Mesa becomes the driver of the whole board",
    "pl": "Nasza Mesa staje się sterownikiem całej płyty",
    "uk": "Наша Mesa стає драйвером усієї плати",
    "ru": "Наша Mesa становится драйвером всей платы",
    "es": "Nuestra Mesa pasa a ser el controlador de toda la placa",
    "pt": "A nossa Mesa passa a ser o driver de toda a placa",
    "de": "Unsere Mesa wird zum Treiber der ganzen Platine",
    "fr": "Notre Mesa devient le pilote de toute la carte",
}
TESTO = {
    "it": "Fino a ieri la Mesa che compiliamo noi la usavano solo i giochi, e tutto il resto della BC-250, desktop compreso, girava su quella della distribuzione. Da questo aggiornamento, su una BC-250 con il nostro kernel, <strong>è il driver della macchina fin dall'avvio</strong>, e Steam e Heroic ci vengono indirizzati da soli, senza accendere niente. I fotogrammi nei giochi restano gli stessi, misurati: 92,3 contro 92,6 in Cyberpunk 2077. Su un PC che non è una BC-250 non cambia nulla, perché il sistema lo riconosce dal firmware e lascia al suo posto il driver di serie: e quella decisione la rifà a ogni avvio, non una volta sola quando si installa.",
    "en": "Until yesterday the Mesa we build was used by the games only, and everything else on the BC-250, desktop included, ran on the distribution's one. From this update, on a BC-250 running our kernel, <strong>it is the driver of the machine from the moment it boots</strong>, and Steam and Heroic are pointed at it by themselves, with nothing to switch on. The frame rate in games is the same, measured: 92.3 against 92.6 in Cyberpunk 2077. On a PC that is not a BC-250 nothing changes, because the system recognises the machine from its firmware and leaves the stock driver where it is: and that decision is taken again at every boot, not once at installation.",
    "pl": "Do wczoraj Mesa, którą kompilujemy, była używana tylko przez gry, a cała reszta BC-250, łącznie z pulpitem, działała na tej z dystrybucji. Od tej aktualizacji, na BC-250 z naszym jądrem, <strong>jest sterownikiem maszyny od samego startu</strong>, a Steam i Heroic są na nią kierowane same, bez włączania czegokolwiek. Liczba klatek w grach zostaje taka sama, zmierzona: 92,3 wobec 92,6 w Cyberpunk 2077. Na pececie, który nie jest BC-250, nic się nie zmienia, bo system rozpoznaje maszynę po firmware i zostawia fabryczny sterownik na miejscu — a tę decyzję podejmuje przy każdym starcie, nie raz przy instalacji.",
    "uk": "До вчора Mesa, яку ми збираємо, використовували лише ігри, а решта BC-250, разом зі стільницею, працювала на дистрибутивній. Від цього оновлення на BC-250 з нашим ядром <strong>вона є драйвером машини від самого запуску</strong>, а Steam і Heroic спрямовуються на неї самі, без вмикання чогось. Кадри в іграх лишаються ті самі, виміряно: 92,3 проти 92,6 у Cyberpunk 2077. На ПК, який не є BC-250, нічого не змінюється, бо система впізнає машину за мікропрограмою і лишає штатний драйвер на місці — і це рішення вона ухвалює під час кожного запуску, а не один раз під час встановлення.",
    "ru": "До вчерашнего дня собранную нами Mesa использовали только игры, а всё остальное на BC-250, включая рабочий стол, работало на дистрибутивной. С этим обновлением на BC-250 с нашим ядром <strong>она становится драйвером машины с самого запуска</strong>, а Steam и Heroic направляются на неё сами, ничего включать не нужно. Кадры в играх остаются прежними, по замерам: 92,3 против 92,6 в Cyberpunk 2077. На ПК, который не является BC-250, ничего не меняется: система узнаёт машину по прошивке и оставляет штатный драйвер на месте, и это решение принимается при каждом запуске, а не один раз при установке.",
    "es": "Hasta ayer la Mesa que compilamos la usaban solo los juegos, y todo lo demás de la BC-250, escritorio incluido, funcionaba con la de la distribución. Desde esta actualización, en una BC-250 con nuestro kernel, <strong>es el controlador de la máquina desde el arranque</strong>, y Steam y Heroic quedan apuntados a él solos, sin activar nada. Los fotogramas en los juegos se quedan igual, medidos: 92,3 frente a 92,6 en Cyberpunk 2077. En un PC que no es una BC-250 no cambia nada, porque el sistema reconoce la máquina por su firmware y deja el controlador de serie donde está: y esa decisión se vuelve a tomar en cada arranque, no una sola vez al instalar.",
    "pt": "Até ontem a Mesa que compilamos era usada só pelos jogos, e todo o resto da BC-250, ambiente de trabalho incluído, corria com a da distribuição. A partir desta atualização, numa BC-250 com o nosso kernel, <strong>é o driver da máquina desde o arranque</strong>, e o Steam e o Heroic ficam apontados para ele sozinhos, sem ligar nada. Os fotogramas nos jogos ficam iguais, medidos: 92,3 contra 92,6 no Cyberpunk 2077. Num PC que não é uma BC-250 nada muda, porque o sistema reconhece a máquina pelo firmware e deixa o driver de série onde está — e essa decisão é refeita em cada arranque, não uma só vez na instalação.",
    "de": "Bis gestern nutzten nur die Spiele die Mesa, die wir bauen, und alles andere auf der BC-250, Desktop eingeschlossen, lief mit der aus der Distribution. Mit diesem Update ist sie auf einer BC-250 mit unserem Kernel <strong>ab dem Start der Treiber der Maschine</strong>, und Steam und Heroic werden von selbst darauf gelenkt, ohne dass etwas eingeschaltet wird. Die Bildrate in Spielen bleibt gleich, gemessen: 92,3 gegenüber 92,6 in Cyberpunk 2077. Auf einem PC, der keine BC-250 ist, ändert sich nichts, denn das System erkennt die Maschine an ihrer Firmware und lässt den Serientreiber, wo er ist — und diese Entscheidung fällt bei jedem Start neu, nicht einmal bei der Installation.",
    "fr": "Jusqu'à hier, la Mesa que nous compilons ne servait qu'aux jeux, et tout le reste de la BC-250, bureau compris, tournait avec celle de la distribution. À partir de cette mise à jour, sur une BC-250 avec notre noyau, <strong>c'est le pilote de la machine dès le démarrage</strong>, et Steam et Heroic y sont dirigés tout seuls, sans rien activer. Le nombre d'images dans les jeux reste le même, mesuré : 92,3 contre 92,6 dans Cyberpunk 2077. Sur un PC qui n'est pas une BC-250, rien ne change, car le système reconnaît la machine à son micrologiciel et laisse le pilote d'origine en place : et ce choix est refait à chaque démarrage, pas une seule fois à l'installation.",
}

ORDINE = ["it", "en", "pl", "uk", "ru", "es", "pt", "de", "fr"]


def riga(d):
    return ", ".join('%s: "%s"' % (k, d[k].replace('"', '\\"')) for k in ORDINE)


def blocco(d, ind):
    return "\n".join('%s%s: "%s",' % (ind, k, d[k].replace('"', '\\"'))
                     for k in ORDINE).rstrip(",")


voce = (
    "  {\n"
    "    // mesa-di-sistema-2026-09-18\n"
    "    data: '2026-09-18',\n"
    "    quando: { %s },\n"
    "    etichetta: { %s },\n"
    "    titolo: {\n%s\n    },\n"
    "    testo: {\n%s\n    },\n"
    "  },\n"
) % (riga(QUANDO), riga(ETICHETTA), blocco(TITOLO, "      "), blocco(TESTO, "      "))

with io.open(PATH, encoding="utf-8") as f:
    text = f.read()

if "mesa-di-sistema-2026-09-18" in text:
    raise SystemExit("il post c'e' gia'")
at = text.index(ANCHOR) + len(ANCHOR)
text = text[:at] + voce + text[at:]
with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(text)
print("news.ts: post 26.09.33 in testa (%d lingue)" % len(ORDINE))
