# -*- coding: utf-8 -*-
u"""Il pallino «?» delle applicazioni SkillFishOS.

LA REGOLA (Mattia, 20/08/2026)
Nella finestra ci vanno i COMANDI e i DATI. Le spiegazioni — cosa fa una cosa,
perche' esiste, cosa comporta — stanno DIETRO a un pallino «?» accanto al
titolo di cio' che spiegano, e si leggono solo se uno le vuole.

PERCHE'
Una finestra piena di paragrafi si legge una volta sola: la prima. Dalla
seconda in poi sono rumore fra chi guarda e il bottone che cerca, e peggiorano
proprio le pagine che si riaprono spesso. Il riferimento e' PrintFlow, che fa
la stessa cosa sul web.

PERCHE' STA QUI E NON DENTRO A OGNI APPLICAZIONE
Perche' sono sei programmi. Copiato sei volte, alla prima correzione ne
resterebbero cinque sbagliate — e' gia' successo con i dizionari delle lingue,
prima che diventassero un modulo condiviso.

COME SI USA
    import sys; sys.path.insert(0, "/usr/share/skillfish")
    from aiuto import Aiuto
    riga.addWidget(QLabel("Verifica dei dati"))
    riga.addWidget(Aiuto("Rilegge tutto il disco e controlla che..."))

⚠️ Chi lo importa deve reggere la sua assenza: le applicazioni e questo file
stanno in due pacchetti diversi, e uno puo' essere piu' vecchio dell'altro.
Si importa dentro un try, e se manca si mostra il testo com'era prima. Una
spiegazione fuori posto e' un fastidio; una applicazione che non si apre e' un
guasto.
"""
from __future__ import unicode_literals

import html as _html

import os

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QToolButton, QToolTip


def _(en):
    u"""L'unica parola che questo modulo dice di suo: «Aiuto».

    ⚠️ Anche una parola sola va tradotta: e' il titolo del riquadro, e in una
    finestra tedesca un «Aiuto» italiano si nota. Si passa dal dizionario
    condiviso come fanno le applicazioni; se non c'e', resta l'inglese — mai
    l'italiano, che e' la regola del progetto.
    """
    lingua = (os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES")
              or os.environ.get("LANG") or "").lower()[:2]
    if lingua == "it":
        return {"Help": "Aiuto"}.get(en, en)
    try:
        from i18n import traduttore
        return traduttore(lingua)(en)
    except Exception:
        return en

# I colori del tema ottone, gli stessi delle altre applicazioni.
_STILE = ("QToolButton{color:#c8a45c;border:1px solid #7a6034;border-radius:9px;"
          "min-width:18px;max-width:18px;min-height:18px;max-height:18px;"
          "font-weight:700;padding:0;}"
          "QToolButton:hover{color:#f1e3c6;border-color:#c8a45c;}")


class Aiuto(QToolButton):
    u"""Un pallino «?» che mostra `testo` al passaggio e al clic.

    DUE MODI DI MOSTRARLO, E LI SCEGLIE LUI
    Non tutte le spiegazioni sono lunghe uguale, e la stessa forma non va bene
    per tutte:

      - una o due frasi  -> bollicina attaccata al pallino. Leggera, non copre
        niente, sparisce da sola.
      - un testo lungo, con elenchi o avvisi (gli aiuti del Tuner sono cosi')
        -> riquadro con un bottone per chiuderlo. Una bollicina da dodici righe
        che sparisce al primo movimento del mouse e' peggio di niente: uno la
        rilegge tre volte e si arrende.

    Il `titolo` serve solo al riquadro. Se non lo si passa e il testo e' lungo,
    ne mette uno generico — meglio un titolo banale che una finestra senza
    intestazione.
    """

    # ⚠️ La soglia non e' un numero tondo scelto a caso: sotto i ~240 caratteri
    # una bollicina resta di tre righe su 340 pixel, che si legge in un colpo
    # d'occhio. Sopra, o quando il testo ha gia' dei ritorni a capo doppi o dei
    # punti elenco, e' un discorso e vuole una finestra.
    SOGLIA = 240

    def __init__(self, testo, titolo=None, parent=None):
        super().__init__(parent)
        self.testo = testo or ""
        self.titolo = titolo
        self.setText("?")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAutoRaise(True)
        # ⚠️ NoFocus: senza, il pallino entra nel giro del tabulatore e si
        # ritrova selezionato all'apertura della finestra, prima del comando
        # che uno vuole davvero usare.
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setAccessibleName(self.testo)      # per i lettori di schermo
        self.setToolTip(self._ricco())
        self.setStyleSheet(_STILE)
        self.clicked.connect(self._mostra)

    def _ricco(self):
        # ⚠️ Due cose insieme:
        # - la larghezza massima, o Qt scrive il suggerimento su una riga sola
        #   larga quanto tutto lo schermo;
        # - l'escape, o una spiegazione che contiene un < viene presa per un
        #   tag e sparisce da li' in poi.
        return ("<div style='max-width:340px; white-space:normal'>%s</div>"
                % _html.escape(self.testo).replace("\n", "<br>"))

    def _lungo(self):
        return (len(self.testo) > self.SOGLIA
                or "\n\n" in self.testo
                or "•" in self.testo)

    def _mostra(self):
        # Si vede in DUE modi apposta: passandoci sopra lo si scopre per caso,
        # cliccando lo si rilegge quando serve. Un aiuto che si apre solo al
        # clic non lo trova nessuno; uno solo al passaggio non si rilegge.
        if self._lungo():
            from PyQt6.QtWidgets import QMessageBox
            # ⚠️ Il genitore e' self.window(), non self: con il pallino come
            # genitore il riquadro si apre ancorato a un bottone di 18 pixel e
            # Qt lo piazza dove capita, spesso a cavallo del bordo dello schermo.
            QMessageBox.information(self.window(), self.titolo or _("Help"), self.testo)
        else:
            QToolTip.showText(self.mapToGlobal(QPoint(0, self.height() + 2)),
                              self._ricco(), self)


def accanto(layout, etichetta, testo):
    u"""Mette l'etichetta e il suo «?» uno accanto all'altro nel layout.

    Comodo dove il titolo e' gia' un QLabel: evita di ripetere tre righe di
    layout in ogni punto, e soprattutto evita che ogni applicazione metta il
    pallino a una distanza diversa.
    """
    from PyQt6.QtWidgets import QHBoxLayout, QLabel
    riga = QHBoxLayout()
    riga.setSpacing(6)
    riga.addWidget(etichetta if isinstance(etichetta, QLabel) else QLabel(str(etichetta)))
    riga.addWidget(Aiuto(testo))
    riga.addStretch(1)
    layout.addLayout(riga)
    return riga
