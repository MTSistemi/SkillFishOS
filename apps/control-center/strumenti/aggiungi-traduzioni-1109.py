#!/usr/bin/env python3
"""Add the 2026-09-11 strings (CSV export, gamepad, VRAM note) to the seven
dictionaries in apps/control-center/i18n/ and merge them into the shared ones.

    aggiungi-traduzioni-1109.py <repo>
"""
import json
import os
import subprocess
import sys

repo = sys.argv[1]
d = os.path.join(repo, "apps", "control-center", "i18n")

NUOVE = {
    "Export the open recording, or the last one made, as CSV": {
        "de": "Die geöffnete Aufzeichnung, oder die zuletzt gemachte, als CSV exportieren",
        "es": "Exportar la grabación abierta, o la última hecha, como CSV",
        "fr": "Exporter l'enregistrement ouvert, ou le dernier fait, en CSV",
        "pl": "Eksportuj otwarte nagranie, albo ostatnie zrobione, jako CSV",
        "pt": "Exportar a gravação aberta, ou a última feita, como CSV",
        "ru": "Экспортировать открытую запись, или последнюю сделанную, в CSV",
        "uk": "Експортувати відкритий запис, або останній зроблений, у CSV",
    },
    "Record or open a recording first.": {
        "de": "Zuerst aufzeichnen oder eine Aufzeichnung öffnen.",
        "es": "Primero graba o abre una grabación.",
        "fr": "Enregistrez ou ouvrez d'abord un enregistrement.",
        "pl": "Najpierw nagraj albo otwórz nagranie.",
        "pt": "Primeiro grave ou abra uma gravação.",
        "ru": "Сначала запишите или откройте запись.",
        "uk": "Спочатку запишіть або відкрийте запис.",
    },
    "Export CSV": {"de": "CSV exportieren", "es": "Exportar CSV", "fr": "Exporter en CSV", "pl": "Eksportuj CSV",
                   "pt": "Exportar CSV", "ru": "Экспорт CSV", "uk": "Експорт CSV"},
    "seconds": {"de": "Sekunden", "es": "segundos", "fr": "secondes", "pl": "sekundy", "pt": "segundos",
                "ru": "секунды", "uk": "секунди"},
    "Exported to %s": {"de": "Exportiert nach %s", "es": "Exportado en %s", "fr": "Exporté dans %s",
                       "pl": "Wyeksportowano do %s", "pt": "Exportado para %s", "ru": "Экспортировано в %s",
                       "uk": "Експортовано до %s"},
    "XeSS, where a game has it built in (Cyberpunk does), costs the same as FSR 3 here: 97.7 against 97.8 fps at 1080p Balanced. The community sees it ahead only with ray tracing.": {
        "de": "XeSS, wo ein Spiel es eingebaut hat (Cyberpunk ja), kostet hier so viel wie FSR 3: 97,7 gegen 97,8 fps bei 1080p Ausgewogen. Die Community sieht es nur mit Raytracing vorn.",
        "es": "XeSS, donde un juego lo trae de serie (Cyberpunk sí), aquí cuesta lo mismo que FSR 3: 97,7 contra 97,8 fps a 1080p Equilibrado. La comunidad lo ve por delante solo con ray tracing.",
        "fr": "XeSS, quand un jeu l'intègre (Cyberpunk oui), coûte ici autant que FSR 3 : 97,7 contre 97,8 fps en 1080p Équilibré. La communauté ne le voit devant qu'avec le ray tracing.",
        "pl": "XeSS, tam gdzie gra ma go wbudowanego (Cyberpunk tak), kosztuje tu tyle co FSR 3: 97,7 wobec 97,8 fps w 1080p Zbalansowany. Społeczność widzi jego przewagę tylko z ray tracingiem.",
        "pt": "XeSS, onde um jogo o traz de série (Cyberpunk sim), custa aqui o mesmo que FSR 3: 97,7 contra 97,8 fps a 1080p Equilibrado. A comunidade vê-o à frente só com ray tracing.",
        "ru": "XeSS, где игра имеет его встроенным (Cyberpunk да), здесь стоит столько же, сколько FSR 3: 97,7 против 97,8 fps в 1080p Сбалансированный. Сообщество видит его впереди только с трассировкой лучей.",
        "uk": "XeSS, де гра має його вбудованим (Cyberpunk так), тут коштує стільки ж, скільки FSR 3: 97,7 проти 97,8 fps у 1080p Збалансований. Спільнота бачить його попереду лише з трасуванням променів.",
    },
    "Controller: %s. D-pad or stick to move, A confirms, B goes back, LB/RB switch section.": {
        "de": "Controller: %s. Steuerkreuz oder Stick zum Bewegen, A bestätigt, B geht zurück, LB/RB wechseln den Bereich.",
        "es": "Mando: %s. Cruceta o palanca para moverse, A confirma, B vuelve atrás, LB/RB cambian de sección.",
        "fr": "Manette : %s. Croix ou stick pour se déplacer, A confirme, B revient, LB/RB changent de section.",
        "pl": "Kontroler: %s. Krzyżak lub gałka do poruszania, A potwierdza, B cofa, LB/RB zmieniają sekcję.",
        "pt": "Comando: %s. Cruz ou alavanca para mover, A confirma, B volta, LB/RB mudam de secção.",
        "ru": "Контроллер: %s. Крестовина или стик для перемещения, A подтверждает, B назад, LB/RB меняют раздел.",
        "uk": "Контролер: %s. Хрестовина або стік для руху, A підтверджує, B назад, LB/RB змінюють розділ.",
    },
    "How much memory the firmware sets aside for the GPU. Written to the CMOS, in force from the next boot. The rest is shared anyway through the GTT. With the 512 MB dynamic split some games measure the VRAM at start and pick low texture quality: if textures look blurry, try 4 or 6 GB fixed.": {
        "de": "Wie viel Speicher die Firmware für die GPU reserviert. Wird ins CMOS geschrieben und gilt ab dem nächsten Start. Der Rest wird ohnehin über das GTT geteilt. Mit der dynamischen 512-MB-Aufteilung messen manche Spiele beim Start den VRAM und wählen niedrige Texturqualität: wirken die Texturen unscharf, versuche 4 oder 6 GB fest.",
        "es": "Cuánta memoria reserva el firmware para la GPU. Se escribe en la CMOS y vale desde el próximo arranque. El resto se comparte igualmente a través del GTT. Con el reparto dinámico de 512 MB algunos juegos miden la VRAM al arrancar y eligen texturas de baja calidad: si las texturas se ven borrosas, prueba 4 o 6 GB fijos.",
        "fr": "Combien de mémoire le firmware réserve au GPU. Écrit dans la CMOS, en vigueur au prochain démarrage. Le reste est de toute façon partagé par le GTT. Avec le partage dynamique de 512 Mo, certains jeux mesurent la VRAM au lancement et choisissent des textures de basse qualité : si les textures sont floues, essayez 4 ou 6 Go fixes.",
        "pl": "Ile pamięci firmware rezerwuje dla GPU. Zapisywane w CMOS, obowiązuje od następnego uruchomienia. Reszta i tak jest dzielona przez GTT. Przy dynamicznym podziale 512 MB niektóre gry mierzą VRAM na starcie i wybierają niską jakość tekstur: jeśli tekstury są rozmyte, spróbuj 4 lub 6 GB na stałe.",
        "pt": "Quanta memória o firmware reserva para a GPU. Escrito no CMOS, em vigor a partir do próximo arranque. O resto é partilhado na mesma através do GTT. Com a divisão dinâmica de 512 MB alguns jogos medem a VRAM no arranque e escolhem texturas de baixa qualidade: se as texturas parecem desfocadas, tente 4 ou 6 GB fixos.",
        "ru": "Сколько памяти прошивка выделяет GPU. Записывается в CMOS, действует со следующей загрузки. Остальное всё равно делится через GTT. При динамическом разделе 512 МБ некоторые игры измеряют VRAM при запуске и выбирают низкое качество текстур: если текстуры размыты, попробуйте 4 или 6 ГБ фиксированно.",
        "uk": "Скільки пам'яті прошивка виділяє для GPU. Записується в CMOS, діє з наступного завантаження. Решта все одно ділиться через GTT. З динамічним розподілом 512 МБ деякі ігри вимірюють VRAM під час запуску й обирають низьку якість текстур: якщо текстури розмиті, спробуйте 4 або 6 ГБ фіксовано.",
    },
}

for lang in ("de", "es", "fr", "pl", "pt", "ru", "uk"):
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
