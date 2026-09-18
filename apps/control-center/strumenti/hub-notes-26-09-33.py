#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hub release notes for 26.09.33: our Mesa becomes the driver of the machine.

Runs on the build VM inside ~/sfx-src.

⚠️ BEFORE build-debs-ci.sh: the .deb carries the metainfo, so a note written
afterwards ships one release late.

Two packages, because two of them changed in a way the user sees: the Control
Center, whose card is now about the whole driver, and the Remote Manager, whose
page was showing two empty boxes while the games ran on our driver.
"""
import io
import os

VER, DATE = "26.09.33", "2026-09-18"
ROOT = os.path.expanduser("~/sfx-src")

CC = os.path.join(ROOT, "apps/control-center/os.skillfish.control-center.metainfo.xml")
RM = os.path.join(ROOT, "apps/dashboard/os.skillfish.remote-manager.metainfo.xml")

NOTE_CC = [
    ("", "The graphics driver panel is about the whole driver now, not Vulkan alone. On a BC-250 running our kernel, our Mesa is the driver of the machine from the moment it boots, desktop included, and Steam and Heroic are pointed at it without anybody switching anything. On a PC that is not a BC-250 nothing changes: the driver that comes with the system stays exactly where it is, and the choice is made again at every boot rather than once at installation. While the system driver is on, the two launcher boxes are shown ticked and locked, because there they have nothing left to decide."),
    ("it", "Il pannello del driver grafico adesso riguarda tutto il driver, non solo Vulkan. Su una BC-250 con il nostro kernel la nostra Mesa è il driver della macchina fin dall'avvio, desktop compreso, e Steam e Heroic ci vengono indirizzati senza che nessuno accenda niente. Su un PC che non è una BC-250 non cambia nulla: resta quello di serie, e la scelta si rifà a ogni avvio invece che una volta sola all'installazione. Con il driver di sistema acceso le due caselle dei lanciatori si vedono spuntate e bloccate, perché lì non decidono più niente."),
    ("fr", "Le panneau du pilote graphique concerne désormais tout le pilote, et pas seulement Vulkan. Sur une BC-250 avec notre noyau, notre Mesa est le pilote de la machine dès le démarrage, bureau compris, et Steam et Heroic y sont dirigés sans que personne n'active quoi que ce soit. Sur un PC qui n'est pas une BC-250, rien ne change : celui d'origine reste en place, et le choix est refait à chaque démarrage plutôt qu'une seule fois à l'installation. Quand le pilote système est activé, les deux cases des lanceurs sont cochées et verrouillées, car elles n'ont plus rien à décider."),
    ("es", "El panel del controlador gráfico ahora trata de todo el controlador, no solo de Vulkan. En una BC-250 con nuestro kernel, nuestra Mesa es el controlador de la máquina desde el arranque, escritorio incluido, y Steam y Heroic quedan apuntados a él sin que nadie active nada. En un PC que no es una BC-250 no cambia nada: se queda el de serie, y la decisión se vuelve a tomar en cada arranque en vez de una sola vez al instalar. Con el controlador del sistema activado, las dos casillas de los lanzadores se ven marcadas y bloqueadas, porque ahí ya no deciden nada."),
    ("pt", "O painel do driver gráfico passa a ser sobre todo o driver, não só sobre o Vulkan. Numa BC-250 com o nosso kernel, a nossa Mesa é o driver da máquina desde o arranque, ambiente de trabalho incluído, e o Steam e o Heroic ficam apontados para ele sem que ninguém ligue nada. Num PC que não é uma BC-250 nada muda: fica o de série, e a escolha é refeita em cada arranque em vez de uma só vez na instalação. Com o driver do sistema ligado, as duas caixas dos lançadores aparecem marcadas e bloqueadas, porque ali já não decidem nada."),
    ("de", "Die Karte für den Grafiktreiber betrifft jetzt den ganzen Treiber, nicht nur Vulkan. Auf einer BC-250 mit unserem Kernel ist unsere Mesa ab dem Start der Treiber der Maschine, Desktop eingeschlossen, und Steam und Heroic werden darauf gelenkt, ohne dass jemand etwas einschaltet. Auf einem PC, der keine BC-250 ist, ändert sich nichts: der mitgelieferte Treiber bleibt, und die Entscheidung fällt bei jedem Start neu statt einmal bei der Installation. Solange der Systemtreiber an ist, sind die beiden Kästchen der Starter angehakt und gesperrt, denn dort entscheiden sie nichts mehr."),
    ("pl", "Panel sterownika graficznego dotyczy teraz całego sterownika, nie tylko Vulkana. Na BC-250 z naszym jądrem nasza Mesa jest sterownikiem maszyny od samego startu, łącznie z pulpitem, a Steam i Heroic są na nią skierowane bez włączania czegokolwiek. Na pececie, który nie jest BC-250, nic się nie zmienia: zostaje fabryczny, a wybór jest podejmowany przy każdym starcie, a nie raz przy instalacji. Gdy sterownik systemowy jest włączony, dwa pola programów uruchamiających są zaznaczone i zablokowane, bo nie mają już o czym decydować."),
    ("ru", "Панель графического драйвера теперь про весь драйвер, а не только про Vulkan. На BC-250 с нашим ядром наша Mesa становится драйвером машины с самого запуска, включая рабочий стол, а Steam и Heroic направляются на неё без того, чтобы кто-то что-то включал. На ПК, который не является BC-250, ничего не меняется: остаётся штатный, а решение принимается заново при каждом запуске, а не один раз при установке. Пока системный драйвер включён, два поля лаунчеров показаны отмеченными и заблокированными: решать им там больше нечего."),
    ("uk", "Панель графічного драйвера тепер стосується всього драйвера, а не лише Vulkan. На BC-250 з нашим ядром наша Mesa є драйвером машини від самого запуску, разом зі стільницею, а Steam і Heroic спрямовані на неї без того, щоб хтось щось вмикав. На ПК, який не є BC-250, нічого не змінюється: лишається штатний, а вибір робиться заново під час кожного запуску, а не один раз під час встановлення. Поки системний драйвер увімкнено, два поля запускачів показані позначеними та заблокованими: вирішувати їм там уже нічого."),
]

NOTE_RM = [
    ("", "The games page follows the driver switch instead of reading one override file of its own. With the system driver on, the Steam and Heroic boxes are ticked and locked: before this they came up empty while the games were in fact running on our driver."),
    ("it", "La pagina dei giochi segue l'interruttore del driver invece di leggersi un file di override per conto suo. Con il driver di sistema acceso, le caselle di Steam e Heroic si vedono spuntate e bloccate: prima uscivano vuote mentre i giochi giravano sulla nostra Mesa."),
    ("fr", "La page des jeux suit l'interrupteur du pilote au lieu de lire un fichier de redéfinition de son côté. Quand le pilote système est activé, les cases de Steam et Heroic sont cochées et verrouillées : avant, elles apparaissaient vides alors que les jeux tournaient bel et bien sur notre pilote."),
    ("es", "La página de juegos sigue el interruptor del controlador en vez de leer por su cuenta un archivo de anulación. Con el controlador del sistema activado, las casillas de Steam y Heroic aparecen marcadas y bloqueadas: antes salían vacías mientras los juegos ya corrían con el nuestro."),
    ("pt", "A página dos jogos segue o interruptor do driver em vez de ler por sua conta um ficheiro de substituição. Com o driver do sistema ligado, as caixas do Steam e do Heroic aparecem marcadas e bloqueadas: antes apareciam vazias enquanto os jogos já corriam com o nosso."),
    ("de", "Die Spieleseite folgt dem Treiberschalter, statt sich eine eigene Override-Datei zu lesen. Bei eingeschaltetem Systemtreiber sind die Kästchen von Steam und Heroic angehakt und gesperrt: vorher waren sie leer, während die Spiele längst auf unserem Treiber liefen."),
    ("pl", "Strona gier idzie za przełącznikiem sterownika zamiast czytać własny plik nadpisania. Przy włączonym sterowniku systemowym pola Steam i Heroic są zaznaczone i zablokowane: wcześniej były puste, choć gry działały już na naszym."),
    ("ru", "Страница игр следует за переключателем драйвера, а не читает собственный файл переопределения. При включённом системном драйвере поля Steam и Heroic отмечены и заблокированы: раньше они были пустыми, хотя игры уже шли на нашем."),
    ("uk", "Сторінка ігор іде за перемикачем драйвера, а не читає власний файл перевизначення. З увімкненим системним драйвером поля Steam і Heroic позначені та заблоковані: раніше вони були порожні, хоча ігри вже працювали на нашому."),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inserisci(path, note):
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    if 'version="%s"' % VER in text:
        print("gia' presente in %s" % os.path.basename(path))
        return
    ancora = "    <release "
    at = text.index(ancora)
    righe = ['    <release version="%s" date="%s">' % (VER, DATE), "      <description>"]
    for lang, p in note:
        attr = ' xml:lang="%s"' % lang if lang else ""
        righe.append("        <p%s>%s</p>" % (attr, esc(p)))
    righe += ["      </description>", "    </release>", ""]
    text = text[:at] + "\n".join(righe) + text[at:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("%s: +%s (%d lingue)" % (os.path.basename(path), VER, len(note)))


inserisci(CC, NOTE_CC)
inserisci(RM, NOTE_RM)
