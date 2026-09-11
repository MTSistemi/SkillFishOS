#!/usr/bin/env python3
"""The gallery and the home page still showed the separate applications: the
Tuner with the four presets, the "My silicon" panel, the AI window. Those
programs are one window now, so the pictures and the words follow.

    sito-galleria-home.py <repo>

Five shots are replaced by five of the Control Center; two gallery keys are
renamed, because a key called "tunerctl" holding the Status page is a trap for
whoever edits this next.
"""
import glob
import os
import re
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
SRC = os.path.join(repo, "website", "src")

# old picture -> new picture, in the gallery and on the home page
IMMAGINI = {
    "tuner.jpg": "control-center-tuner.png",
    "tuner-controls.jpg": "control-center-stato.png",
    "monitor.jpg": "control-center-monitor.png",
    "cu-test.jpg": "control-center-giochi.png",
    "ai-panel.jpg": "control-center-ai.png",
}
CHIAVI = {"gal.tunerctl": "gal.stato", "gal.cutest": "gal.giochi"}

# key -> language -> (title, description)
T = {
"gal.tuner": {
 "it": ("Tuner — la curva del governor", "MHz e millivolt: i nodi si trascinano o si scrivono nella tabella, e Applica è una prova a tempo."),
 "en": ("Tuner — the governor curve", "MHz and millivolts: drag the knots or type them in the table, and Apply is a timed trial."),
 "de": ("Tuner — die Governor-Kurve", "MHz und Millivolt: Knoten ziehen oder in der Tabelle eintippen, und Anwenden ist eine Probe auf Zeit."),
 "fr": ("Tuner — la courbe du governor", "MHz et millivolts : on tire les points ou on les tape dans le tableau, et Appliquer est un essai chronométré."),
 "es": ("Tuner — la curva del governor", "MHz y milivoltios: los puntos se arrastran o se escriben en la tabla, y Aplicar es una prueba con cuenta atrás."),
 "pt": ("Tuner — a curva do governor", "MHz e milivolts: os pontos arrastam-se ou escrevem-se na tabela, e Aplicar é uma prova cronometrada."),
 "pl": ("Tuner — krzywa governora", "MHz i miliwolty: węzły przeciąga się albo wpisuje w tabeli, a Zastosuj to próba na czas."),
 "ru": ("Тюнер — кривая governor", "МГц и милливольты: узлы тянут мышью или вводят в таблице, а «Применить» это проба на время."),
 "uk": ("Тюнер — крива governor", "МГц і мілівольти: вузли тягнуть мишею або вводять у таблиці, а «Застосувати» це проба на час."),
},
"gal.stato": {
 "it": ("Stato — tutto a colpo d'occhio", "Un numero per scheda: GPU e tetto, CPU, unità di calcolo, ventola, kernel e driver Vulkan."),
 "en": ("Status — everything at a glance", "One number per card: GPU and ceiling, CPU, compute units, fan, kernel and Vulkan driver."),
 "de": ("Status — alles auf einen Blick", "Eine Zahl pro Karte: GPU und Obergrenze, CPU, Recheneinheiten, Lüfter, Kernel und Vulkan-Treiber."),
 "fr": ("État — tout d'un coup d'œil", "Un chiffre par carte : GPU et plafond, CPU, unités de calcul, ventilateur, noyau et pilote Vulkan."),
 "es": ("Estado — todo de un vistazo", "Un número por tarjeta: GPU y techo, CPU, unidades de cálculo, ventilador, kernel y driver Vulkan."),
 "pt": ("Estado — tudo num relance", "Um número por cartão: GPU e teto, CPU, unidades de cálculo, ventoinha, kernel e driver Vulkan."),
 "pl": ("Stan — wszystko na jednym ekranie", "Jedna liczba na kafelek: GPU i sufit, CPU, jednostki obliczeniowe, wentylator, jądro i sterownik Vulkan."),
 "ru": ("Состояние — всё сразу", "По одному числу на карточку: GPU и потолок, CPU, вычислительные блоки, вентилятор, ядро и драйвер Vulkan."),
 "uk": ("Стан — усе одразу", "По одному числу на картку: GPU і стеля, CPU, обчислювальні блоки, вентилятор, ядро і драйвер Vulkan."),
},
"gal.monitor": {
 "it": ("Monitor — un grafico per grandezza", "Temperature, frequenze, carico, potenza, tensioni, ventola e memoria, con una barra per thread."),
 "en": ("Monitor — one chart per quantity", "Temperatures, clocks, load, power, voltages, fan and memory, with one bar per thread."),
 "de": ("Monitor — ein Diagramm je Größe", "Temperaturen, Takte, Last, Leistung, Spannungen, Lüfter und Speicher, mit einem Balken je Thread."),
 "fr": ("Moniteur — un graphique par grandeur", "Températures, fréquences, charge, puissance, tensions, ventilateur et mémoire, avec une barre par thread."),
 "es": ("Monitor — un gráfico por magnitud", "Temperaturas, frecuencias, carga, potencia, tensiones, ventilador y memoria, con una barra por hilo."),
 "pt": ("Monitor — um gráfico por grandeza", "Temperaturas, frequências, carga, potência, tensões, ventoinha e memória, com uma barra por thread."),
 "pl": ("Monitor — jeden wykres na wielkość", "Temperatury, częstotliwości, obciążenie, moc, napięcia, wentylator i pamięć, ze słupkiem na wątek."),
 "ru": ("Монитор — по графику на величину", "Температуры, частоты, нагрузка, мощность, напряжения, вентилятор и память, со столбиком на поток."),
 "uk": ("Монітор — по графіку на величину", "Температури, частоти, навантаження, потужність, напруги, вентилятор і пам'ять, зі стовпчиком на потік."),
},
"gal.giochi": {
 "it": ("Giochi — Mesa, scheduler e Proton", "La nostra Mesa per lanciatore o di sistema, scx_bpfland durante il gioco, FSR 4 e GE-Proton 11."),
 "en": ("Games — Mesa, scheduler and Proton", "Our Mesa per launcher or system-wide, scx_bpfland while a game runs, FSR 4 and GE-Proton 11."),
 "de": ("Spiele — Mesa, Scheduler und Proton", "Unsere Mesa pro Launcher oder systemweit, scx_bpfland während des Spiels, FSR 4 und GE-Proton 11."),
 "fr": ("Jeux — Mesa, ordonnanceur et Proton", "Notre Mesa par lanceur ou pour tout le système, scx_bpfland pendant le jeu, FSR 4 et GE-Proton 11."),
 "es": ("Juegos — Mesa, planificador y Proton", "Nuestra Mesa por lanzador o de sistema, scx_bpfland mientras juegas, FSR 4 y GE-Proton 11."),
 "pt": ("Jogos — Mesa, escalonador e Proton", "A nossa Mesa por lançador ou de sistema, scx_bpfland durante o jogo, FSR 4 e GE-Proton 11."),
 "pl": ("Gry — Mesa, scheduler i Proton", "Nasza Mesa dla launchera albo systemowo, scx_bpfland podczas gry, FSR 4 i GE-Proton 11."),
 "ru": ("Игры — Mesa, планировщик и Proton", "Наша Mesa для лаунчера или для всей системы, scx_bpfland во время игры, FSR 4 и GE-Proton 11."),
 "uk": ("Ігри — Mesa, планувальник і Proton", "Наша Mesa для лаунчера або для всієї системи, scx_bpfland під час гри, FSR 4 і GE-Proton 11."),
},
"gal.ai": {
 "it": ("AI — Unsloth Studio sulla GPU", "Motore, modelli scaricati dall'Hub, memoria e una chat di prova con i token al secondo."),
 "en": ("AI — Unsloth Studio on the GPU", "Engine, models pulled from the Hub, memory and a chat test with the tokens per second."),
 "de": ("KI — Unsloth Studio auf der GPU", "Motor, Modelle aus dem Hub, Speicher und ein Chat-Test mit den Token pro Sekunde."),
 "fr": ("IA — Unsloth Studio sur le GPU", "Moteur, modèles tirés du Hub, mémoire et un essai de chat avec les tokens par seconde."),
 "es": ("IA — Unsloth Studio en la GPU", "Motor, modelos descargados del Hub, memoria y una prueba de chat con los tokens por segundo."),
 "pt": ("IA — Unsloth Studio na GPU", "Motor, modelos transferidos do Hub, memória e um teste de chat com os tokens por segundo."),
 "pl": ("AI — Unsloth Studio na GPU", "Silnik, modele pobrane z Hubu, pamięć i próbny czat ze zmierzonymi tokenami na sekundę."),
 "ru": ("ИИ — Unsloth Studio на GPU", "Движок, модели из Hub, память и проба чата с токенами в секунду."),
 "uk": ("ШІ — Unsloth Studio на GPU", "Рушій, моделі з Hub, пам'ять і проба чату з токенами за секунду."),
},
"s4": {
 "it": ("L'AI in casa, dentro il Control Center", "La sezione AI accende il motore locale sulla GPU Vulkan, scarica i modelli e misura i token al secondo. Quando si gioca si spegne, e la memoria torna al gioco."),
 "en": ("AI at home, inside the Control Center", "The AI section starts the local engine on the Vulkan GPU, downloads the models and measures the tokens per second. Turn it off to play, and the memory goes back to the game."),
 "de": ("KI zu Hause, im Control Center", "Der KI-Bereich startet den lokalen Motor auf der Vulkan-GPU, lädt die Modelle und misst die Token pro Sekunde. Zum Spielen ausschalten, dann gehört der Speicher wieder dem Spiel."),
 "fr": ("L'IA à la maison, dans le Control Center", "La section IA allume le moteur local sur le GPU Vulkan, télécharge les modèles et mesure les tokens par seconde. On l'éteint pour jouer, et la mémoire revient au jeu."),
 "es": ("La IA en casa, dentro del Control Center", "La sección IA enciende el motor local en la GPU Vulkan, descarga los modelos y mide los tokens por segundo. Se apaga para jugar, y la memoria vuelve al juego."),
 "pt": ("A IA em casa, dentro do Control Center", "A secção IA liga o motor local na GPU Vulkan, transfere os modelos e mede os tokens por segundo. Desliga-se para jogar, e a memória volta ao jogo."),
 "pl": ("AI w domu, w Control Center", "Sekcja AI włącza lokalny silnik na GPU przez Vulkan, pobiera modele i mierzy tokeny na sekundę. Przed graniem się ją wyłącza i pamięć wraca do gry."),
 "ru": ("ИИ дома, внутри Control Center", "Раздел ИИ включает локальный движок на GPU через Vulkan, скачивает модели и измеряет токены в секунду. Перед игрой его выключают, и память возвращается игре."),
 "uk": ("ШІ вдома, усередині Control Center", "Розділ ШІ вмикає локальний рушій на GPU через Vulkan, завантажує моделі й міряє токени за секунду. Перед грою його вимикають, і пам'ять повертається грі."),
},
"s5": {
 "it": ("Tuning a portata di clic", "Il Tuner disegna la curva tensione/frequenza del governor, con il tetto e tre preset. Applica è una prova a tempo: se non confermi, al riavvio torna la curva di prima."),
 "en": ("Tuning a click away", "The Tuner draws the voltage/frequency curve of the governor, with the ceiling and three presets. Apply is a timed trial: without your confirmation the previous curve is what boots."),
 "de": ("Tuning einen Klick entfernt", "Der Tuner zeichnet die Spannungs-/Frequenzkurve des Governors, mit Obergrenze und drei Vorgaben. Anwenden ist eine Probe auf Zeit: ohne Bestätigung startet wieder die vorige Kurve."),
 "fr": ("Le réglage à un clic", "Le Tuner dessine la courbe tension/fréquence du governor, avec le plafond et trois préréglages. Appliquer est un essai chronométré : sans confirmation, c'est la courbe précédente qui redémarre."),
 "es": ("Ajustar a un clic", "El Tuner dibuja la curva tensión/frecuencia del governor, con el techo y tres preajustes. Aplicar es una prueba con cuenta atrás: sin confirmar, al arrancar vuelve la curva anterior."),
 "pt": ("Afinação a um clique", "O Tuner desenha a curva tensão/frequência do governor, com o teto e três predefinições. Aplicar é uma prova cronometrada: sem confirmação, arranca a curva anterior."),
 "pl": ("Strojenie jednym kliknięciem", "Tuner rysuje krzywą napięcie/częstotliwość governora, z sufitem i trzema presetami. Zastosuj to próba na czas: bez potwierdzenia wraca poprzednia krzywa."),
 "ru": ("Настройка в один клик", "Тюнер рисует кривую напряжение/частота governor, со стелей и тремя пресетами. «Применить» это проба на время: без подтверждения загрузится прежняя кривая."),
 "uk": ("Налаштування в один клік", "Тюнер малює криву напруга/частота governor, зі стелею і трьома пресетами. «Застосувати» це проба на час: без підтвердження завантажиться попередня крива."),
},
}


def js(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---- the two components: pictures and key names
for nome in ("GalleryContent.astro", "HomeContent.astro"):
    p = os.path.join(SRC, "components", nome)
    with open(p, encoding="utf-8") as f:
        s = f.read()
    for vecchia, nuova in IMMAGINI.items():
        s = s.replace(vecchia, nuova)
    for vecchia, nuova in CHIAVI.items():
        s = s.replace("'%s.t'" % vecchia, "'%s.t'" % nuova).replace("'%s.d'" % vecchia, "'%s.d'" % nuova)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("ok", nome)

# ---- the dictionaries: i18n.ts holds {it, en}, the others one string each
for p in sorted(glob.glob(os.path.join(SRC, "i18n*.ts"))):
    lingua = os.path.basename(p)[len("i18n."):-len(".ts")] if os.path.basename(p) != "i18n.ts" else None
    with open(p, encoding="utf-8") as f:
        s = f.read()
    for vecchia, nuova in CHIAVI.items():
        s = s.replace('"%s.t"' % vecchia, '"%s.t"' % nuova).replace('"%s.d"' % vecchia, '"%s.d"' % nuova)
    n = 0
    for chiave, per_lingua in T.items():
        for suffisso, indice in ((".t", 0), (".d", 1)):
            k = chiave + suffisso
            if lingua is None:
                valore = "{ it: %s, en: %s }" % (js(per_lingua["it"][indice]), js(per_lingua["en"][indice]))
                schema = r'"%s":\s*\{[^{}]*\}' % re.escape(k)
            else:
                if lingua not in per_lingua:
                    continue
                valore = js(per_lingua[lingua][indice])
                schema = r'"%s":\s*(?:"(?:[^"\\]|\\.)*"\s*\+?\s*)+' % re.escape(k)
            nuovo, quante = re.subn(schema, '"%s": %s' % (k, valore.replace("\\", "\\\\")), s, count=1)
            if quante:
                s = nuovo
                n += 1
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("ok", os.path.basename(p), "voci rifatte:", n)
