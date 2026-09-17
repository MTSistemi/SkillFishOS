#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hub release notes for 26.09.30: housekeeping, and it says so.

Runs on the build VM inside ~/sfx-src. Inserts one <release> above the others.

⚠️ BEFORE build-debs-ci.sh: the .deb carries the metainfo, so a note written
afterwards ships one version late.

Only two packages move. The rest of the commit is files that are not shipped:
the removed Tuner window, the CI workflow, the build script, the one-shot
patch scripts.

⚠️ AND THE NOTE SAYS NOTHING CHANGES ON SCREEN, because nothing does. A
maintenance release that dresses itself up as a feature teaches people to stop
reading the notes.
"""
import io
import os

VER, DATE = "26.09.30", "2026-09-17"
ROOT = os.path.expanduser("~/sfx-src/apps")

NOTES = {
    "control-center/os.skillfish.control-center.metainfo.xml": [
        ("", "Housekeeping. The limits the CPU panel reads from the board are kept in a form the code checker can follow, so it stops reporting a cache nobody uses. Nothing changes on screen."),
        ("it", "Manutenzione. I limiti che il pannello CPU legge dalla scheda sono tenuti in una forma che il controllo del codice sa seguire, così smette di segnalare una cache che nessuno userebbe. Sullo schermo non cambia niente."),
        ("fr", "Entretien. Les limites que le panneau CPU lit sur la carte sont conservées sous une forme que le contrôle de code sait suivre, il cesse donc de signaler un cache que personne n'utiliserait. Rien ne change à l'écran."),
        ("es", "Mantenimiento. Los límites que el panel de CPU lee de la placa se guardan de una forma que el revisor de código sabe seguir, así deja de avisar de una caché que nadie usaría. En pantalla no cambia nada."),
        ("pt", "Manutenção. Os limites que o painel da CPU lê da placa são guardados numa forma que o verificador de código sabe seguir, por isso deixa de assinalar uma cache que ninguém usaria. No ecrã não muda nada."),
        ("de", "Wartung. Die Grenzwerte, die die CPU-Karte von der Karte liest, liegen jetzt in einer Form vor, der die Codeprüfung folgen kann, sodass sie keinen ungenutzten Zwischenspeicher mehr meldet. Auf dem Bildschirm ändert sich nichts."),
        ("pl", "Konserwacja. Limity, które panel CPU odczytuje z płyty, są trzymane w formie, za którą kontrola kodu potrafi nadążyć, więc przestaje zgłaszać pamięć podręczną, której nikt by nie użył. Na ekranie nic się nie zmienia."),
        ("ru", "Обслуживание. Пределы, которые панель CPU читает с платы, теперь хранятся в виде, понятном проверке кода, и она перестаёт сообщать о кэше, которым никто не пользуется. На экране ничего не меняется."),
        ("uk", "Обслуговування. Межі, які панель CPU читає з плати, тепер зберігаються у вигляді, зрозумілому перевірці коду, і вона перестає повідомляти про кеш, яким ніхто не користується. На екрані нічого не змінюється."),
    ],
    "hub/os.skillfish.hub.metainfo.xml": [
        ("", "Housekeeping. When even the last-resort error message cannot be shown, the code now says in writing why it gives up rather than staying silent. Nothing changes on screen."),
        ("it", "Manutenzione. Quando nemmeno il messaggio d'errore di ultima istanza riesce ad aprirsi, adesso il codice scrive perché rinuncia invece di tacere. Sullo schermo non cambia niente."),
        ("fr", "Entretien. Quand même le message d'erreur de dernier recours ne peut pas s'afficher, le code écrit désormais pourquoi il renonce au lieu de se taire. Rien ne change à l'écran."),
        ("es", "Mantenimiento. Cuando ni siquiera el mensaje de error de último recurso puede mostrarse, ahora el código deja escrito por qué se rinde en vez de callar. En pantalla no cambia nada."),
        ("pt", "Manutenção. Quando nem a mensagem de erro de último recurso consegue aparecer, agora o código deixa escrito porque desiste em vez de ficar calado. No ecrã não muda nada."),
        ("de", "Wartung. Wenn nicht einmal die allerletzte Fehlermeldung angezeigt werden kann, schreibt der Code jetzt hin, warum er aufgibt, statt zu schweigen. Auf dem Bildschirm ändert sich nichts."),
        ("pl", "Konserwacja. Gdy nawet komunikat o błędzie ostatniej szansy nie może się pokazać, kod zapisuje teraz, dlaczego rezygnuje, zamiast milczeć. Na ekranie nic się nie zmienia."),
        ("ru", "Обслуживание. Когда даже последнее сообщение об ошибке не удаётся показать, код теперь пишет, почему он сдаётся, вместо того чтобы промолчать. На экране ничего не меняется."),
        ("uk", "Обслуговування. Коли навіть останнє повідомлення про помилку не вдається показати, код тепер пише, чому здається, замість того щоб змовчати. На екрані нічого не змінюється."),
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
