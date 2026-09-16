#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The twelve sentences the CU panel gained with issue #77, in seven languages.

Runs ON the build VM, inside ~/sfx-src.

    python3 traduzioni-cu-77.py

Adds them to apps/control-center/i18n/<lang>.json; unisci-i18n.py then feeds the
shared dictionaries and builds it.json from the (it, en) pairs in the code.

⚠️ The terms already in the dictionaries are reused rather than reinvented: a
"pair" of CUs, the board, the boot. A user has to read the same word in the
warning as on the control it refers to.
"""
import io
import json
import os

RADICE = os.path.expanduser("~/sfx-src/apps/control-center/i18n")

K = {
    "griglia": "Green on, red off. Every cell is a pair of CUs. At least one per row has to stay on.",
    "mantieni": "Keep at boot",
    "mantieni_tip": "The board comes back with this mapping instead of every CU on. Apply first, then tick.",
    "mantieni_aiuto": ("Unticked, the board turns every CU on at each boot, which is what almost everyone "
                       "wants. Ticked, it comes back with the pairs chosen here: that is what you need when "
                       "a pair is faulty and has to stay off."),
    "vuota": "Every row needs at least one pair on.",
    "storte": "The four rows are not valid.",
    "non_applicata": "Apply the selection before keeping it at boot.",
    "ripartira": "The board will come back with this mapping",
    "tutte_al_boot": "Every CU comes back on at the next boot",
    "almeno_una": "At least one pair per row",
    "test_tip": ("Tries one pair at a time under vkpeak, all five positions, and watches for GPU errors. "
                 "About five minutes."),
    "test_domanda": ("Tries one CU pair at a time under vkpeak, in all five positions, and watches for GPU "
                     "errors. About five minutes, and it puts the current selection back at the end. Proceed?"),
}

VOCI = {
    "de": {
        "griglia": "Grün an, rot aus. Jede Zelle ist ein CU-Paar. Mindestens eines pro Zeile muss an bleiben.",
        "mantieni": "Beim Start beibehalten",
        "mantieni_tip": "Die Karte startet mit dieser Zuordnung statt mit allen CUs. Erst anwenden, dann ankreuzen.",
        "mantieni_aiuto": ("Ohne Haken schaltet die Karte bei jedem Start alle CUs ein, was fast immer das "
                           "Richtige ist. Mit Haken kommt sie mit den hier gewählten Paaren zurück: das braucht "
                           "man, wenn ein Paar defekt ist und aus bleiben muss."),
        "vuota": "Jede Zeile braucht mindestens ein Paar an.",
        "storte": "Die vier Zeilen sind nicht gültig.",
        "non_applicata": "Erst anwenden, dann beim Start beibehalten.",
        "ripartira": "Die Karte startet mit dieser Zuordnung",
        "tutte_al_boot": "Beim nächsten Start sind wieder alle CUs an",
        "almeno_una": "Mindestens ein Paar pro Zeile",
        "test_tip": ("Prüft ein Paar nach dem anderen unter vkpeak, alle fünf Positionen, und achtet auf "
                     "GPU-Fehler. Etwa fünf Minuten."),
        "test_domanda": ("Prüft ein CU-Paar nach dem anderen unter vkpeak, an allen fünf Positionen, und achtet "
                         "auf GPU-Fehler. Etwa fünf Minuten, am Ende wird die aktuelle Auswahl "
                         "wiederhergestellt. Fortfahren?"),
    },
    "es": {
        "griglia": "Verde encendido, rojo apagado. Cada casilla es un par de CU. Al menos uno por fila debe quedar encendido.",
        "mantieni": "Mantener al arranque",
        "mantieni_tip": "La placa arranca con este mapa en vez de con todas las CU. Aplica primero y luego marca.",
        "mantieni_aiuto": ("Sin marcar, la placa enciende todas las CU en cada arranque, que es lo que casi "
                           "siempre conviene. Marcado, vuelve con los pares elegidos aquí: eso hace falta "
                           "cuando un par está defectuoso y tiene que quedarse apagado."),
        "vuota": "Cada fila necesita al menos un par encendido.",
        "storte": "Las cuatro filas no son válidas.",
        "non_applicata": "Aplica la selección antes de mantenerla al arranque.",
        "ripartira": "La placa arrancará con este mapa",
        "tutte_al_boot": "En el próximo arranque vuelven todas las CU",
        "almeno_una": "Al menos un par por fila",
        "test_tip": ("Prueba un par cada vez con vkpeak, en las cinco posiciones, y vigila los errores de la "
                     "GPU. Unos cinco minutos."),
        "test_domanda": ("Prueba un par de CU cada vez con vkpeak, en las cinco posiciones, y vigila los "
                         "errores de la GPU. Unos cinco minutos, y al final restablece la selección actual. "
                         "¿Continuar?"),
    },
    "fr": {
        "griglia": "Vert allumé, rouge éteint. Chaque case est une paire de CU. Au moins une par ligne doit rester allumée.",
        "mantieni": "Garder au démarrage",
        "mantieni_tip": "La carte redémarre avec ce mappage au lieu de toutes les CU. Applique d'abord, coche ensuite.",
        "mantieni_aiuto": ("Sans la coche, la carte allume toutes les CU à chaque démarrage, ce qui convient "
                           "presque toujours. Avec la coche, elle revient avec les paires choisies ici : c'est "
                           "ce qu'il faut quand une paire est défectueuse et doit rester éteinte."),
        "vuota": "Chaque ligne a besoin d'au moins une paire allumée.",
        "storte": "Les quatre lignes ne sont pas valides.",
        "non_applicata": "Applique la sélection avant de la garder au démarrage.",
        "ripartira": "La carte redémarrera avec ce mappage",
        "tutte_al_boot": "Au prochain démarrage toutes les CU reviennent",
        "almeno_una": "Au moins une paire par ligne",
        "test_tip": ("Essaie une paire à la fois sous vkpeak, les cinq positions, et surveille les erreurs "
                     "GPU. Environ cinq minutes."),
        "test_domanda": ("Essaie une paire de CU à la fois sous vkpeak, dans les cinq positions, et surveille "
                         "les erreurs GPU. Environ cinq minutes, et la sélection actuelle est remise à la "
                         "fin. Continuer ?"),
    },
    "pl": {
        "griglia": "Zielone włączone, czerwone wyłączone. Każde pole to para CU. Co najmniej jedna w wierszu musi zostać włączona.",
        "mantieni": "Zachowaj przy starcie",
        "mantieni_tip": "Płyta wstaje z tym przypisaniem zamiast ze wszystkimi CU. Najpierw zastosuj, potem zaznacz.",
        "mantieni_aiuto": ("Bez zaznaczenia płyta włącza przy każdym starcie wszystkie CU, i tak jest prawie "
                           "zawsze najlepiej. Z zaznaczeniem wraca z parami wybranymi tutaj: to potrzebne, gdy "
                           "para jest uszkodzona i ma zostać wyłączona."),
        "vuota": "Każdy wiersz potrzebuje co najmniej jednej włączonej pary.",
        "storte": "Te cztery wiersze nie są prawidłowe.",
        "non_applicata": "Zastosuj wybór, zanim zachowasz go przy starcie.",
        "ripartira": "Płyta wstanie z tym przypisaniem",
        "tutte_al_boot": "Przy następnym starcie wracają wszystkie CU",
        "almeno_una": "Co najmniej jedna para na wiersz",
        "test_tip": ("Sprawdza po jednej parze pod vkpeak, wszystkie pięć pozycji, i obserwuje błędy GPU. "
                     "Około pięciu minut."),
        "test_domanda": ("Sprawdza po jednej parze CU pod vkpeak, na wszystkich pięciu pozycjach, i obserwuje "
                         "błędy GPU. Około pięciu minut, a na koniec przywraca obecny wybór. Kontynuować?"),
    },
    "pt": {
        "griglia": "Verde ligado, vermelho desligado. Cada casa é um par de CU. Pelo menos um por linha tem de ficar ligado.",
        "mantieni": "Manter no arranque",
        "mantieni_tip": "A placa arranca com este mapeamento em vez de todas as CU. Aplica primeiro, depois marca.",
        "mantieni_aiuto": ("Sem marcar, a placa liga todas as CU em cada arranque, que é o que serve quase "
                           "sempre. Marcado, volta com os pares escolhidos aqui: é o que faz falta quando um "
                           "par está defeituoso e tem de ficar desligado."),
        "vuota": "Cada linha precisa de pelo menos um par ligado.",
        "storte": "As quatro linhas não são válidas.",
        "non_applicata": "Aplica a seleção antes de a manter no arranque.",
        "ripartira": "A placa vai arrancar com este mapeamento",
        "tutte_al_boot": "No próximo arranque voltam todas as CU",
        "almeno_una": "Pelo menos um par por linha",
        "test_tip": ("Testa um par de cada vez com o vkpeak, nas cinco posições, e vigia os erros da GPU. "
                     "Cerca de cinco minutos."),
        "test_domanda": ("Testa um par de CU de cada vez com o vkpeak, nas cinco posições, e vigia os erros da "
                         "GPU. Cerca de cinco minutos, e no fim repõe a seleção atual. Continuar?"),
    },
    "ru": {
        "griglia": "Зелёный включён, красный выключен. Каждая ячейка это пара CU. Хотя бы одна в строке должна остаться включённой.",
        "mantieni": "Сохранять при загрузке",
        "mantieni_tip": "Плата стартует с этой раскладкой, а не со всеми CU. Сначала применить, потом отметить.",
        "mantieni_aiuto": ("Без отметки плата включает при каждой загрузке все CU, и почти всегда это то, что "
                           "нужно. С отметкой она возвращается с выбранными здесь парами: это нужно, когда "
                           "пара неисправна и должна оставаться выключенной."),
        "vuota": "В каждой строке нужна хотя бы одна включённая пара.",
        "storte": "Эти четыре строки недопустимы.",
        "non_applicata": "Примените выбор, прежде чем сохранять его при загрузке.",
        "ripartira": "Плата стартует с этой раскладкой",
        "tutte_al_boot": "При следующей загрузке вернутся все CU",
        "almeno_una": "Хотя бы одна пара в строке",
        "test_tip": ("Проверяет по одной паре под vkpeak, все пять позиций, и следит за ошибками GPU. "
                     "Около пяти минут."),
        "test_domanda": ("Проверяет по одной паре CU под vkpeak, во всех пяти позициях, и следит за ошибками "
                         "GPU. Около пяти минут, в конце возвращает текущий выбор. Продолжить?"),
    },
    "uk": {
        "griglia": "Зелений увімкнено, червоний вимкнено. Кожна клітинка це пара CU. Щонайменше одна в рядку має лишитися увімкненою.",
        "mantieni": "Зберігати при завантаженні",
        "mantieni_tip": "Плата стартує з цим розкладом, а не з усіма CU. Спершу застосуйте, потім позначте.",
        "mantieni_aiuto": ("Без позначки плата вмикає при кожному завантаженні всі CU, і майже завжди це те, "
                           "що потрібно. З позначкою вона повертається з вибраними тут парами: це потрібно, "
                           "коли пара несправна і має лишатися вимкненою."),
        "vuota": "У кожному рядку потрібна щонайменше одна увімкнена пара.",
        "storte": "Ці чотири рядки недійсні.",
        "non_applicata": "Застосуйте вибір, перш ніж зберігати його при завантаженні.",
        "ripartira": "Плата стартуватиме з цим розкладом",
        "tutte_al_boot": "При наступному завантаженні повернуться всі CU",
        "almeno_una": "Щонайменше одна пара в рядку",
        "test_tip": ("Перевіряє по одній парі під vkpeak, усі п'ять позицій, і стежить за помилками GPU. "
                     "Близько п'яти хвилин."),
        "test_domanda": ("Перевіряє по одній парі CU під vkpeak, в усіх п'яти позиціях, і стежить за помилками "
                         "GPU. Близько п'яти хвилин, наприкінці повертає поточний вибір. Продовжити?"),
    },
}

for lingua, voci in sorted(VOCI.items()):
    mancano = set(K) - set(voci)
    if mancano:
        raise SystemExit("%s: manca la traduzione di %s" % (lingua, sorted(mancano)))
    percorso = os.path.join(RADICE, lingua + ".json")
    with io.open(percorso, encoding="utf-8") as f:
        d = json.load(f)
    nuove = {K[sigla]: testo for sigla, testo in voci.items()}
    aggiunte = [k for k in nuove if k not in d]
    d.update({k: v for k, v in nuove.items() if k not in d})
    with io.open(percorso, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(d.items(), key=lambda kv: kv[0].lower())), f,
                  ensure_ascii=False, indent=1)
        f.write("\n")
    print("%s: +%d (totale %d)" % (lingua, len(aggiunte), len(d)))
