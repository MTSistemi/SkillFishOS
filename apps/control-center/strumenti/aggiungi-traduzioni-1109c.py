#!/usr/bin/env python3
"""The shortened help texts of 2026-09-12 in the seven dictionaries, then the
merge into the shared ones.

    aggiungi-traduzioni-1109c.py <repo>
"""
import json
import os
import subprocess
import sys

repo = sys.argv[1]
d = os.path.join(repo, "apps", "control-center", "i18n")
L = ("de", "es", "fr", "pl", "pt", "ru", "uk")


def T(*tr):
    return dict(zip(L, tr))


NUOVE = {
    "Clock forced by the governor and its ceiling: under load it jumps to the ceiling, which drops when the board gets hot or draws too much.": T(
        "Vom Governor erzwungener Takt und seine Obergrenze: unter Last springt er auf die Obergrenze, die sinkt, wenn die Karte heiß wird oder zu viel zieht.",
        "Frecuencia forzada por el governor y su techo: bajo carga sube al techo, que baja cuando la placa se calienta o consume demasiado.",
        "Fréquence forcée par le governor et son plafond : sous charge elle saute au plafond, qui baisse quand la carte chauffe ou tire trop.",
        "Zegar wymuszony przez governora i jego sufit: pod obciążeniem skacze do sufitu, który spada, gdy płyta się grzeje albo pobiera za dużo.",
        "Frequência forçada pelo governor e o seu teto: sob carga salta para o teto, que desce quando a placa aquece ou puxa demasiado.",
        "Частота, принудительно заданная governor, и её потолок: под нагрузкой она прыгает к потолку, который снижается, когда плата греется или тянет слишком много.",
        "Частота, примусово задана governor, і її стеля: під навантаженням вона стрибає до стелі, яка знижується, коли плата гріється або тягне забагато."),
    "24 units on by default: we turn the other 16 on at boot.": T(
        "24 Einheiten ab Werk an: die anderen 16 schalten wir beim Start ein.", "24 unidades activas de serie: las otras 16 las encendemos al arrancar.",
        "24 unités actives d'origine : nous allumons les 16 autres au démarrage.", "24 jednostki włączone fabrycznie: pozostałe 16 włączamy przy starcie.",
        "24 unidades ligadas de série: as outras 16 ligamo-las no arranque.", "24 блока включены по умолчанию: остальные 16 мы включаем при загрузке.",
        "24 блоки увімкнені типово: решту 16 ми вмикаємо під час завантаження."),
    "If the orderly-shutdown mark is missing, the last time it went down on its own: with an overclock that is the symptom that counts.": T(
        "Fehlt die Markierung des geordneten Herunterfahrens, ging es beim letzten Mal von selbst aus: mit Übertaktung ist das das Symptom, das zählt.",
        "Si falta la marca del apagado ordenado, la última vez se cayó sola: con overclock es el síntoma que cuenta.",
        "Si la marque d'arrêt ordonné manque, la dernière fois elle est tombée toute seule : avec l'overclock c'est le symptôme qui compte.",
        "Jeśli brakuje znaku uporządkowanego zamknięcia, ostatnim razem padła sama: przy podkręcaniu to objaw, który się liczy.",
        "Se falta a marca do encerramento ordenado, da última vez foi abaixo sozinha: com overclock é o sintoma que conta.",
        "Если метки штатного выключения нет, в прошлый раз плата упала сама: при разгоне это симптом, который важен.",
        "Якщо позначки штатного вимкнення немає, минулого разу плата впала сама: при розгоні це симптом, який важить."),
    "The sensors of the last five minutes and the fan curve in the box: drag the knots, double-click to add one.": T(
        "Die Sensoren der letzten fünf Minuten und die Lüfterkurve im Kasten: Punkte ziehen, Doppelklick fügt einen hinzu.",
        "Los sensores de los últimos cinco minutos y la curva del ventilador en el recuadro: arrastra los puntos, doble clic para añadir uno.",
        "Les capteurs des cinq dernières minutes et la courbe du ventilateur dans le cadre : glissez les points, double-clic pour en ajouter un.",
        "Czujniki z ostatnich pięciu minut i krzywa wentylatora w ramce: przeciągaj punkty, dwuklik dodaje punkt.",
        "Os sensores dos últimos cinco minutos e a curva da ventoinha na caixa: arraste os pontos, duplo clique para acrescentar um.",
        "Датчики за последние пять минут и кривая вентилятора в рамке: перетаскивайте узлы, двойной щелчок добавляет узел.",
        "Датчики за останні п'ять хвилин і крива вентилятора в рамці: перетягуйте вузли, подвійне клацання додає вузол."),
    "On: the curve drives the fan. Off: back to the firmware, with no emergency either.": T(
        "An: die Kurve steuert den Lüfter. Aus: zurück zur Firmware, auch ohne Notfallschutz.", "Encendido: la curva manda el ventilador. Apagado: vuelve al firmware, sin emergencia tampoco.",
        "Marche : la courbe pilote le ventilateur. Arrêt : retour au firmware, sans urgence non plus.", "Włączone: krzywa steruje wentylatorem. Wyłączone: powrót do firmware, bez awaryjnego też.",
        "Ligado: a curva comanda a ventoinha. Desligado: volta ao firmware, sem emergência também.", "Вкл.: кривая управляет вентилятором. Выкл.: обратно к прошивке, без аварийного режима.",
        "Увімк.: крива керує вентилятором. Вимк.: назад до прошивки, без аварійного режиму."),
    "A heavy game heats up twenty seconds after launch: the fan starts before.": T(
        "Ein schweres Spiel wird zwanzig Sekunden nach dem Start heiß: der Lüfter legt vorher los.", "Un juego pesado se calienta veinte segundos después de arrancar: el ventilador arranca antes.",
        "Un jeu lourd chauffe vingt secondes après le lancement : le ventilateur démarre avant.", "Ciężka gra grzeje się dwadzieścia sekund po starcie: wentylator rusza wcześniej.",
        "Um jogo pesado aquece vinte segundos depois de arrancar: a ventoinha arranca antes.", "Тяжёлая игра греется через двадцать секунд после запуска: вентилятор стартует раньше.",
        "Важка гра гріється через двадцять секунд після запуску: вентилятор стартує раніше."),
    "Fan to full, then 35%, then full again: if the speed follows, the PWM really drives it. Thirty seconds.": T(
        "Lüfter auf voll, dann 35 %, dann wieder voll: folgt die Drehzahl, steuert das PWM wirklich. Dreißig Sekunden.", "Ventilador al máximo, luego al 35 %, luego al máximo otra vez: si las revoluciones siguen, el PWM manda de verdad. Treinta segundos.",
        "Ventilateur à fond, puis 35 %, puis à fond : si la vitesse suit, le PWM commande vraiment. Trente secondes.", "Wentylator na maks, potem 35 %, potem znów maks: jeśli obroty nadążają, PWM naprawdę steruje. Trzydzieści sekund.",
        "Ventoinha no máximo, depois 35 %, depois máximo outra vez: se as rotações seguem, o PWM comanda mesmo. Trinta segundos.", "Вентилятор на максимум, затем 35 %, затем снова максимум: если обороты следуют, PWM действительно управляет. Тридцать секунд.",
        "Вентилятор на максимум, потім 35 %, потім знову максимум: якщо оберти слідують, PWM справді керує. Тридцять секунд."),
    "Our Mesa opens the compute queues: +4% in Cyberpunk, +12% with FSR 4. It needs our kernel.": T(
        "Unsere Mesa öffnet die Compute-Warteschlangen: +4 % in Cyberpunk, +12 % mit FSR 4. Braucht unseren Kernel.", "Nuestra Mesa abre las colas de cómputo: +4 % en Cyberpunk, +12 % con FSR 4. Necesita nuestro kernel.",
        "Notre Mesa ouvre les files de calcul : +4 % dans Cyberpunk, +12 % avec FSR 4. Il faut notre noyau.", "Nasza Mesa otwiera kolejki obliczeniowe: +4 % w Cyberpunk, +12 % z FSR 4. Wymaga naszego jądra.",
        "A nossa Mesa abre as filas de cálculo: +4 % no Cyberpunk, +12 % com FSR 4. Precisa do nosso kernel.", "Наша Mesa открывает вычислительные очереди: +4 % в Cyberpunk, +12 % с FSR 4. Нужно наше ядро.",
        "Наша Mesa відкриває обчислювальні черги: +4 % у Cyberpunk, +12 % із FSR 4. Потрібне наше ядро."),
    "scx_bpfland only while a game runs (GameMode raises it): +1.5-2% in Cyberpunk. Ejected twice by the kernel, it stops until you reset.": T(
        "scx_bpfland nur solange ein Spiel läuft (GameMode startet ihn): +1,5-2 % in Cyberpunk. Zweimal vom Kernel hinausgeworfen, hält er bis zum Zurücksetzen an.",
        "scx_bpfland solo mientras corre un juego (lo levanta GameMode): +1,5-2 % en Cyberpunk. Expulsado dos veces por el kernel, se para hasta que lo pongas a cero.",
        "scx_bpfland seulement pendant qu'un jeu tourne (GameMode le lance) : +1,5-2 % dans Cyberpunk. Éjecté deux fois par le noyau, il s'arrête jusqu'à la remise à zéro.",
        "scx_bpfland tylko gdy działa gra (podnosi go GameMode): +1,5-2 % w Cyberpunk. Wyrzucony dwa razy przez jądro, zatrzymuje się do wyzerowania.",
        "scx_bpfland só enquanto corre um jogo (o GameMode lança-o): +1,5-2 % no Cyberpunk. Expulso duas vezes pelo kernel, pára até repor a zero.",
        "scx_bpfland только пока идёт игра (его поднимает GameMode): +1,5-2 % в Cyberpunk. Выброшенный ядром дважды, останавливается до сброса.",
        "scx_bpfland лише поки йде гра (його піднімає GameMode): +1,5-2 % у Cyberpunk. Викинутий ядром двічі, зупиняється до скидання."),
    "Ejected by the kernel": T("Vom Kernel hinausgeworfen", "Expulsado por el kernel", "Éjecté par le noyau", "Wyrzucony przez jądro", "Expulso pelo kernel", "Выброшен ядром", "Викинутий ядром"),
    "Through OptiScaler on the DLSS path: GE-Proton 11 downloads it and the game must be set to DLSS. Needs amdxcffx64.dll from the AMD driver.": T(
        "Über OptiScaler auf dem DLSS-Pfad: GE-Proton 11 lädt es, das Spiel muss auf DLSS stehen. Braucht amdxcffx64.dll aus dem AMD-Treiber.",
        "Vía OptiScaler en la ruta DLSS: GE-Proton 11 lo descarga y el juego debe ponerse en DLSS. Necesita amdxcffx64.dll del driver AMD.",
        "Via OptiScaler sur le chemin DLSS : GE-Proton 11 le télécharge et le jeu doit être réglé sur DLSS. Il faut amdxcffx64.dll du pilote AMD.",
        "Przez OptiScaler na ścieżce DLSS: GE-Proton 11 go pobiera, a grę trzeba ustawić na DLSS. Potrzebny amdxcffx64.dll ze sterownika AMD.",
        "Via OptiScaler no caminho DLSS: o GE-Proton 11 descarrega-o e o jogo tem de ficar em DLSS. Precisa do amdxcffx64.dll do driver AMD.",
        "Через OptiScaler по пути DLSS: GE-Proton 11 скачивает его, игру нужно поставить на DLSS. Нужен amdxcffx64.dll из драйвера AMD.",
        "Через OptiScaler шляхом DLSS: GE-Proton 11 завантажує його, гру треба поставити на DLSS. Потрібен amdxcffx64.dll із драйвера AMD."),
    "GloriousEggroll's GE-Proton 11: Install downloads 500 MB for Steam and Heroic, Default picks it. Steam must be closed.": T(
        "GE-Proton 11 von GloriousEggroll: Installieren lädt 500 MB für Steam und Heroic, Standard wählt es. Steam muss geschlossen sein.",
        "GE-Proton 11 de GloriousEggroll: Instalar descarga 500 MB para Steam y Heroic, Predeterminada lo elige. Steam debe estar cerrado.",
        "GE-Proton 11 de GloriousEggroll : Installer télécharge 500 Mo pour Steam et Heroic, Par défaut le choisit. Steam doit être fermé.",
        "GE-Proton 11 od GloriousEggroll: Zainstaluj pobiera 500 MB dla Steam i Heroic, Domyślny go wybiera. Steam musi być zamknięty.",
        "GE-Proton 11 do GloriousEggroll: Instalar descarrega 500 MB para Steam e Heroic, Predefinida escolhe-o. O Steam tem de estar fechado.",
        "GE-Proton 11 от GloriousEggroll: «Установить» скачивает 500 МБ для Steam и Heroic, «По умолчанию» выбирает его. Steam должен быть закрыт.",
        "GE-Proton 11 від GloriousEggroll: «Встановити» завантажує 500 МБ для Steam і Heroic, «Типовий» обирає його. Steam має бути закритий."),
    "Unsloth Studio with llama.cpp on Vulkan. On, it holds GPU memory: turn it off before gaming.": T(
        "Unsloth Studio mit llama.cpp auf Vulkan. Eingeschaltet hält es GPU-Speicher: vor dem Spielen ausschalten.", "Unsloth Studio con llama.cpp sobre Vulkan. Encendido retiene memoria de la GPU: apágalo antes de jugar.",
        "Unsloth Studio avec llama.cpp sur Vulkan. Allumé, il garde la mémoire du GPU : éteignez-le avant de jouer.", "Unsloth Studio z llama.cpp na Vulkanie. Włączone trzyma pamięć GPU: wyłącz przed graniem.",
        "Unsloth Studio com llama.cpp em Vulkan. Ligado retém memória da GPU: desligue-o antes de jogar.", "Unsloth Studio с llama.cpp на Vulkan. Включённый, он держит память GPU: выключите перед игрой.",
        "Unsloth Studio з llama.cpp на Vulkan. Увімкнений, він тримає пам'ять GPU: вимкніть перед грою."),
    "Share of RAM the model may use on top of VRAM. Kernel parameter: a reboot is needed.": T(
        "Anteil des RAM, den das Modell zusätzlich zum VRAM nutzen darf. Kernel-Parameter: Neustart nötig.", "Cuota de RAM que el modelo puede usar además de la VRAM. Parámetro del kernel: hace falta reiniciar.",
        "Part de RAM que le modèle peut utiliser en plus de la VRAM. Paramètre du noyau : un redémarrage est nécessaire.", "Udział RAM, który model może użyć poza VRAM. Parametr jądra: potrzebny restart.",
        "Quota de RAM que o modelo pode usar além da VRAM. Parâmetro do kernel: é preciso reiniciar.", "Доля RAM, которую модель может использовать сверх VRAM. Параметр ядра: нужна перезагрузка.",
        "Частка RAM, яку модель може використати понад VRAM. Параметр ядра: потрібне перезавантаження."),
    "Installs and configures emulators, ROM folders, BIOS files and controls, all in your home.": T(
        "Installiert und konfiguriert Emulatoren, ROM-Ordner, BIOS-Dateien und Steuerung, alles in deinem Home.", "Instala y configura emuladores, carpetas de ROM, BIOS y controles, todo en tu home.",
        "Installe et configure émulateurs, dossiers de ROM, BIOS et contrôles, le tout dans votre dossier personnel.", "Instaluje i konfiguruje emulatory, foldery ROM, pliki BIOS i sterowanie, wszystko w twoim katalogu domowym.",
        "Instala e configura emuladores, pastas de ROM, ficheiros BIOS e controlos, tudo na sua home.", "Устанавливает и настраивает эмуляторы, папки ROM, файлы BIOS и управление, всё в вашем домашнем каталоге.",
        "Встановлює і налаштовує емулятори, теки ROM, файли BIOS і керування, усе у вашій домашній теці."),
    "Flatpaks from Flathub: the Debian packages are old and run badly on this GPU. The recommended ones are ticked.": T(
        "Flatpaks aus Flathub: die Debian-Pakete sind alt und laufen auf dieser GPU schlecht. Die empfohlenen sind angehakt.", "Flatpaks de Flathub: los paquetes Debian son viejos y en esta GPU rinden mal. Los recomendados están marcados.",
        "Flatpaks de Flathub : les paquets Debian sont vieux et tournent mal sur ce GPU. Les recommandés sont cochés.", "Flatpaki z Flathuba: pakiety Debiana są stare i źle działają na tym GPU. Polecane są zaznaczone.",
        "Flatpaks do Flathub: os pacotes Debian são velhos e correm mal nesta GPU. Os recomendados estão marcados.", "Flatpak из Flathub: пакеты Debian старые и плохо работают на этом GPU. Рекомендуемые отмечены.",
        "Flatpak із Flathub: пакети Debian старі й погано працюють на цьому GPU. Рекомендовані позначені."),
    "Starts on top of the desktop: gamescope takes the screen and Steam opens in console mode.": T(
        "Startet über dem Desktop: gamescope übernimmt den Bildschirm und Steam öffnet im Konsolenmodus.", "Arranca sobre el escritorio: gamescope toma la pantalla y Steam se abre en modo consola.",
        "Démarre par-dessus le bureau : gamescope prend l'écran et Steam s'ouvre en mode console.", "Startuje nad pulpitem: gamescope przejmuje ekran i Steam otwiera się w trybie konsoli.",
        "Arranca por cima do ambiente de trabalho: o gamescope toma o ecrã e o Steam abre em modo consola.", "Запускается поверх рабочего стола: gamescope забирает экран, и Steam открывается в режиме консоли.",
        "Запускається поверх стільниці: gamescope забирає екран, і Steam відкривається в режимі консолі."),
    "On the login screen pick the «SkillFishOS Console» session: the board starts into Steam, no desktop.": T(
        "Im Anmeldebildschirm die Sitzung «SkillFishOS Console» wählen: die Karte startet direkt in Steam, ohne Desktop.", "En la pantalla de inicio elige la sesión «SkillFishOS Console»: la placa arranca en Steam, sin escritorio.",
        "Sur l'écran de connexion choisissez la session « SkillFishOS Console » : la carte démarre dans Steam, sans bureau.", "Na ekranie logowania wybierz sesję «SkillFishOS Console»: płyta startuje prosto do Steam, bez pulpitu.",
        "No ecrã de início escolha a sessão «SkillFishOS Console»: a placa arranca no Steam, sem ambiente de trabalho.", "На экране входа выберите сеанс «SkillFishOS Console»: плата загружается прямо в Steam, без рабочего стола.",
        "На екрані входу оберіть сеанс «SkillFishOS Console»: плата завантажується просто у Steam, без стільниці."),
    "Saves ceiling, CPU, fan and scheduler as they are now in a profile of yours.": T(
        "Speichert Obergrenze, CPU, Lüfter und Scheduler so wie jetzt in einem eigenen Profil.", "Guarda techo, CPU, ventilador y planificador tal como están ahora en un perfil tuyo.",
        "Enregistre plafond, CPU, ventilateur et ordonnanceur tels qu'ils sont dans un profil à vous.", "Zapisuje sufit, CPU, wentylator i planistę takie, jakie są teraz, we własnym profilu.",
        "Guarda teto, CPU, ventoinha e escalonador como estão agora num perfil seu.", "Сохраняет потолок, CPU, вентилятор и планировщик как есть сейчас в ваш профиль.",
        "Зберігає стелю, CPU, вентилятор і планувальник як є зараз у ваш профіль."),
}

for lang in L:
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
