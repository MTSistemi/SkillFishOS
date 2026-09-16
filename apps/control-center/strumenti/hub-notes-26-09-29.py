#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hub release notes for 26.09.29: the CU floor that was not real (#77).

Runs on the build VM inside ~/sfx-src. Inserts one <release> above the others.

⚠️ BEFORE build-debs-ci.sh, never after: the .deb carries the metainfo, so a
note written afterwards ships one version late.

Three packages move. skillfish-tuner has skillfish-cu and its unit,
skillfish-control-center has the grid and the daemon, skillfish-base has the
shared dictionaries the new messages live in.
"""
import io
import os

VER, DATE = "26.09.29", "2026-09-16"
ROOT = os.path.expanduser("~/sfx-src/apps")

NOTES = {
    "control-center/os.skillfish.control-center.metainfo.xml": [
        ("", "Any CU pair can be switched off now, the first three included. They were greyed out because a comment claimed the driver kept them on, and it does not. A row keeps at least one pair and the grid says so, instead of disabling a button and leaving you to guess. The choice can be kept at boot, which is what a board with a faulty pair needs, and the CU test checks all five positions instead of only the last two."),
        ("it", "Adesso ogni coppia di CU si può spegnere, comprese le prime tre. Erano grigie perché un commento diceva che le teneva accese il driver, e non è vero. Ogni riga tiene almeno una coppia e la griglia lo dice, invece di disabilitare un pulsante e lasciarti indovinare. La scelta si può mantenere all'avvio, che è quello che serve a una scheda con una coppia guasta, e il test delle CU controlla tutte e cinque le posizioni invece delle ultime due."),
        ("fr", "Toute paire de CU peut maintenant être éteinte, y compris les trois premières. Elles étaient grisées parce qu'un commentaire affirmait que le pilote les gardait allumées, ce qui est faux. Une ligne garde au moins une paire et la grille le dit, au lieu de désactiver un bouton sans explication. Le choix peut être conservé au démarrage, ce qu'il faut à une carte dont une paire est défectueuse, et le test des CU vérifie les cinq positions au lieu des deux dernières."),
        ("es", "Ahora se puede apagar cualquier par de CU, incluidos los tres primeros. Estaban en gris porque un comentario decía que el controlador los mantenía encendidos, y no es así. Cada fila conserva al menos un par y la cuadrícula lo dice, en vez de desactivar un botón y dejarte adivinando. La elección se puede mantener al arranque, que es lo que necesita una placa con un par defectuoso, y la prueba de CU revisa las cinco posiciones en lugar de solo las dos últimas."),
        ("pt", "Agora qualquer par de CU pode ser desligado, incluindo os três primeiros. Estavam a cinzento porque um comentário dizia que o controlador os mantinha ligados, e não é verdade. Cada linha guarda pelo menos um par e a grelha di-lo, em vez de desativar um botão e deixar-te a adivinhar. A escolha pode ser mantida no arranque, que é o que faz falta a uma placa com um par defeituoso, e o teste de CU verifica as cinco posições em vez de só as duas últimas."),
        ("de", "Jedes CU-Paar lässt sich jetzt abschalten, auch die ersten drei. Sie waren ausgegraut, weil ein Kommentar behauptete, der Treiber halte sie an, und das stimmt nicht. Eine Zeile behält mindestens ein Paar, und das Raster sagt es, statt einen Knopf zu sperren und einen raten zu lassen. Die Auswahl kann beim Start erhalten bleiben, was eine Karte mit einem defekten Paar braucht, und der CU-Test prüft alle fünf Positionen statt nur der letzten beiden."),
        ("pl", "Teraz można wyłączyć każdą parę CU, także trzy pierwsze. Były wyszarzone, bo komentarz twierdził, że sterownik trzyma je włączone, a tak nie jest. Każdy wiersz zachowuje co najmniej jedną parę i siatka to mówi, zamiast blokować przycisk i zostawiać cię w niepewności. Wybór można zachować przy starcie, czego potrzebuje płyta z uszkodzoną parą, a test CU sprawdza wszystkie pięć pozycji zamiast tylko dwóch ostatnich."),
        ("ru", "Теперь можно выключить любую пару CU, включая первые три. Они были серыми из-за комментария, утверждавшего, что драйвер держит их включёнными, а это не так. В каждой строке остаётся хотя бы одна пара, и сетка об этом говорит, а не блокирует кнопку молча. Выбор можно сохранить при загрузке, что и нужно плате с неисправной парой, а проверка CU смотрит все пять позиций, а не только две последние."),
        ("uk", "Тепер можна вимкнути будь-яку пару CU, зокрема перші три. Вони були сірими через коментар, який стверджував, що драйвер тримає їх увімкненими, а це не так. У кожному рядку лишається щонайменше одна пара, і сітка про це каже, а не блокує кнопку мовчки. Вибір можна зберегти при завантаженні, що й потрібно платі з несправною парою, а перевірка CU дивиться всі п'ять позицій, а не лише дві останні."),
    ],
    "tuner/os.skillfish.Tuner.metainfo.xml": [
        ("", "skillfish-cu no longer forces the first three CU pairs on, and it can put a chosen mapping back at boot. All 40 CU stay the default: a saved mapping is used only when there is one, and only when it is complete."),
        ("it", "skillfish-cu non tiene più accese per forza le prime tre coppie di CU, e sa rimettere all'avvio la mappatura scelta. Tutte e 40 restano il valore di serie: una mappatura salvata si usa solo se c'è, e solo se è completa."),
        ("fr", "skillfish-cu ne force plus les trois premières paires de CU à rester allumées, et il peut remettre au démarrage la cartographie choisie. Les 40 CU restent la valeur par défaut : une cartographie enregistrée n'est utilisée que s'il y en a une, et seulement si elle est complète."),
        ("es", "skillfish-cu ya no fuerza encendidos los tres primeros pares de CU, y puede restablecer al arranque el mapa elegido. Las 40 CU siguen siendo lo predeterminado: un mapa guardado se usa solo si existe, y solo si está completo."),
        ("pt", "O skillfish-cu já não força ligados os três primeiros pares de CU, e consegue repor no arranque o mapeamento escolhido. As 40 CU continuam a ser o predefinido: um mapeamento guardado só é usado se existir, e só se estiver completo."),
        ("de", "skillfish-cu erzwingt die ersten drei CU-Paare nicht mehr, und es kann eine gewählte Zuordnung beim Start wiederherstellen. Alle 40 CU bleiben der Standard: eine gespeicherte Zuordnung wird nur benutzt, wenn es eine gibt und sie vollständig ist."),
        ("pl", "skillfish-cu nie wymusza już włączenia trzech pierwszych par CU i potrafi przywrócić przy starcie wybrane przypisanie. Wszystkie 40 CU pozostają domyślne: zapisane przypisanie jest używane tylko wtedy, gdy istnieje i jest kompletne."),
        ("ru", "skillfish-cu больше не держит принудительно включёнными первые три пары CU и умеет восстанавливать выбранную раскладку при загрузке. Все 40 CU остаются значением по умолчанию: сохранённая раскладка используется, только если она есть и если она полная."),
        ("uk", "skillfish-cu більше не тримає примусово увімкненими перші три пари CU і вміє відновлювати вибраний розклад при завантаженні. Усі 40 CU лишаються типовим значенням: збережений розклад використовується, лише якщо він є і якщо він повний."),
    ],
    "base/os.skillfish.base.metainfo.xml": [
        ("", "The shared translations cover the new Compute Unit messages in all nine languages. Maintenance release, nothing else changes."),
        ("it", "Le traduzioni condivise coprono i nuovi messaggi sulle Compute Unit in tutte e nove le lingue. Versione di manutenzione, per il resto non cambia niente."),
        ("fr", "Les traductions partagées couvrent les nouveaux messages sur les Compute Units dans les neuf langues. Version de maintenance, rien d'autre ne change."),
        ("es", "Las traducciones compartidas cubren los nuevos mensajes sobre las Compute Units en los nueve idiomas. Versión de mantenimiento, no cambia nada más."),
        ("pt", "As traduções partilhadas cobrem as novas mensagens sobre as Compute Units nas nove línguas. Versão de manutenção, não muda mais nada."),
        ("de", "Die gemeinsamen Übersetzungen decken die neuen Meldungen zu den Compute Units in allen neun Sprachen ab. Wartungsversion, sonst ändert sich nichts."),
        ("pl", "Wspólne tłumaczenia obejmują nowe komunikaty o Compute Unitach we wszystkich dziewięciu językach. Wersja serwisowa, poza tym nic się nie zmienia."),
        ("ru", "Общие переводы охватывают новые сообщения о Compute Unit на всех девяти языках. Служебная версия, больше ничего не меняется."),
        ("uk", "Спільні переклади охоплюють нові повідомлення про Compute Unit усіма дев'ятьма мовами. Службова версія, більше нічого не змінюється."),
    ],
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


for rel, paras in NOTES.items():
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    if 'version="%s"' % VER in text:
        print("%s: gia' presente" % rel)
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
    print("%s: +%s (%d lingue)" % (rel, VER, len(paras)))
