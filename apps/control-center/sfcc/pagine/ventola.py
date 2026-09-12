# -*- coding: utf-8 -*-
"""Fan: the curve, and the controller that applies it whether or not we look.

Nothing here moves the fan. skillfish-fand does, once a second, from root, and
publishes what it reads in /run/skillfish/ventola.json; this page draws that
and writes the curve through the helper. The split is deliberate: cooling
must not depend on a window being open.
"""
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (QButtonGroup, QCheckBox, QComboBox, QDoubleSpinBox, QFrame,
                             QHBoxLayout, QInputDialog, QLabel, QMessageBox, QPushButton,
                             QRadioButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget)

from .. import stile
from ..comune import VENTOLA_CONF, VENTOLA_STATO, L, Aiuto, leggi_json
from ..finestra import PaginaBase
from ..grafico import CurvaVentola, Grafico, GraficoSingolo
from ..stile import Tessera, intestazione
from .tuner import Pannello

ETICHETTE = "/etc/skillfish/sensori.json"
PROVA = "/etc/skillfish/ventola-prova.json"

# Measured on the BC-250 fan: PWM 20 = 567 rpm, 90 = 1244, 255 = 3100, linear.
PRESET = {
    "silenzioso": [[45, 20], [60, 30], [70, 45], [80, 70], [88, 100]],
    "equilibrato": [[40, 30], [55, 40], [65, 60], [75, 85], [85, 100]],
    "prestazioni": [[35, 40], [50, 60], [60, 80], [70, 100], [85, 100]],
    "massimo": [[0, 100], [100, 100]],
}

RAIL_FISSE = {"+12v": 12.0, "+5v": 5.0, "+3.3v": 3.3, "3vcc": 3.3, "avcc": 3.3, "avcc3": 3.3, "avsb": 3.3, "vcc": 3.3}
DINAMICHE = ("vddgfx", "vddnb", "vcore", "cpu vcore", "cpu soc", "cpu vddp", "cpu sa", "cpu 1p8", "dram", "chipset", "vbat", "vid", "vtt")
CAMPIONI_RIPOSO = 20


def nome_preset(k):
    return {"silenzioso": L("Silenziosa", "Silent"), "equilibrato": L("Equilibrata", "Balanced"),
            "prestazioni": L("Prestazioni", "Performance"), "massimo": L("Massima", "Full"),
            "personalizzata": L("Personalizzata", "Custom")}.get(k, k)


def aiuto_preset(k):
    return {
        "silenzioso": L("La ventola resta bassa finche' si puo': al minimo sotto i 45 gradi, sale sul serio solo oltre i 70. Sotto carico pesante la scheda arriva piu' in alto: e' il prezzo del silenzio.",
                        "The fan stays low as long as it can: minimum below 45 C, climbs in earnest only past 70. Under heavy load the board runs hotter: that is what quiet costs."),
        "equilibrato": L("Il compromesso che consigliamo: sale dai 40 gradi in su, al massimo a 85. Nei giochi si sente appena.",
                         "The compromise we suggest: climbs from 40 C, full at 85. In games you barely hear it."),
        "prestazioni": L("Priorita' al fresco: parte gia' al 40%, al massimo a 70 gradi. Per l'overclock e le sessioni lunghe. Si sente.",
                         "Cool first: starts at 40% straight away, full at 70 C. For overclocking and long sessions. You will hear it."),
        "massimo": L("Sempre al 100%. Per una prova o per cercare un problema termico. Rumorosa.",
                     "Always 100%. For a test, or while chasing a thermal problem. Loud."),
    }.get(k, "")


def nominale(etichetta):
    e = (etichetta or "").strip().lower()
    if any(d in e for d in DINAMICHE):
        return "dinamica"
    return RAIL_FISSE.get(e)


class Prova(QThread):
    finita = pyqtSignal(bool, str)

    def __init__(self, demone, pwm, fan, parent=None):
        super().__init__(parent)
        self.demone, self.pwm, self.fan = demone, pwm, fan

    def run(self):
        r = self.demone.cmd(cmd="ventola", azione="prova", dati={"pwm": self.pwm, "fan": self.fan})
        if not r.get("ok"):
            self.finita.emit(False, r.get("err", ""))
            return
        d = r.get("dati") or {}
        giri = ", ".join("%s%% -> %s" % (round(x["pwm"] * 100 / 255), x["rpm"]) for x in d.get("letture", []))
        self.finita.emit(bool(d.get("risponde")), giri)


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 1000
        self.conf = {}
        self.stato = {}
        self.etichette = {}
        self.riposo = {}
        self.caselle_sorgente = {}
        self.tessere = {}
        self.pannelli_serie = {}
        self.pannelli = {}

    def costruisci(self):
        self.conf = leggi_json(VENTOLA_CONF, {})
        self.stato = leggi_json(VENTOLA_STATO, {})
        self.etichette = leggi_json(ETICHETTE, {})
        v = self.corpo_pieno()
        testa = QHBoxLayout()
        testa.addWidget(intestazione(L("Ventola", "Fan"), "", L("I sensori degli ultimi cinque minuti e la curva della ventola nel riquadro: trascina i punti, doppio clic per aggiungerne uno.",
            "The sensors of the last five minutes and the fan curve in the box: drag the knots, double-click to add one.")))
        testa.addStretch(1)
        self.et_motivo = QLabel("")
        self.et_motivo.setObjectName("quieto")
        testa.addWidget(self.et_motivo)
        testa.addSpacing(12)
        testa.addWidget(QLabel(L("Aggiornamento", "Refresh")))
        self.intervallo = QComboBox()
        for testo, ms in (("1 s", 1000), ("2 s", 2000), ("5 s", 5000), ("10 s", 10000), ("30 s", 30000)):
            self.intervallo.addItem(testo, ms)
        self.intervallo.currentIndexChanged.connect(lambda: self.timer.setInterval(self.intervallo.currentData() or 1000))
        testa.addWidget(self.intervallo)
        v.addLayout(testa)

        corpo = QHBoxLayout()
        corpo.setSpacing(10)
        v.addLayout(corpo, 1)
        lato = QScrollArea()
        lato.setWidgetResizable(True)
        lato.setFrameShape(QFrame.Shape.NoFrame)
        lato.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        lato.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        lato.setFixedWidth(168)
        gabbia = QWidget()
        self.colonna = QVBoxLayout(gabbia)
        self.colonna.setContentsMargins(0, 0, 4, 0)
        self.colonna.setSpacing(5)
        self.colonna.addStretch(1)
        lato.setWidget(gabbia)
        corpo.addWidget(lato, 0)
        destra = QVBoxLayout()
        destra.setSpacing(6)
        corpo.addLayout(destra, 1)
        self.curva = CurvaVentola()
        self.curva.cambiata.connect(self._curva_toccata)
        self.curva.imposta(self.conf.get("curva") or PRESET["equilibrato"])
        self.grafico = Grafico(self.curva)
        self.grafico.nuova_serie = self._rifai_tessere
        self.grafico.apri_serie = self._apri_serie
        destra.addWidget(self.grafico, 1)
        self.et_allarme = QLabel("")
        self.et_allarme.setWordWrap(True)
        self.et_allarme.setObjectName("male")
        destra.addWidget(self.et_allarme)

        basso = QHBoxLayout()
        basso.setSpacing(12)
        v.addLayout(basso, 0)
        gc = QVBoxLayout()
        gc.setSpacing(2)
        gc.addWidget(QLabel("<b>%s</b>" % L("Curva", "Curve")))
        pr = QHBoxLayout()
        pr.setSpacing(4)
        self.gruppo = QButtonGroup(self)
        for k in ("silenzioso", "equilibrato", "prestazioni", "massimo"):
            r = QRadioButton(nome_preset(k))
            r.chiave = k
            self.gruppo.addButton(r)
            pr.addWidget(r)
            pr.addWidget(Aiuto(aiuto_preset(k), nome_preset(k)))
            if self.conf.get("preset") == k:
                r.setChecked(True)
        self.gruppo.buttonClicked.connect(self._prova_preset)
        pr.addStretch(1)
        gc.addLayout(pr)
        basso.addLayout(gc)

        pulsanti = QHBoxLayout()
        pulsanti.setSpacing(6)
        for nome, titolo, costruisci in (("sorgente", L("Sorgente", "Source"), self._sez_sorgente),
                                         ("anticipo", L("Anticipo", "Lead"), self._sez_anticipo),
                                         ("sicurezza", L("Sicurezza", "Safety"), self._sez_sicurezza)):
            self.pannelli[nome] = Pannello(titolo, costruisci(), self)
            b = QPushButton(titolo)
            b.clicked.connect(lambda _c=False, k=nome: self.pannelli[k].mostra())
            pulsanti.addWidget(b)
        basso.addLayout(pulsanti)
        basso.addStretch(1)

        fine = QVBoxLayout()
        fine.setSpacing(4)
        ri = QHBoxLayout()
        self.interruttore = QCheckBox(L("Controllo", "Control"))
        self.interruttore.setChecked(bool(self.conf.get("attivo")))
        ri.addWidget(self.interruttore)
        ri.addWidget(Aiuto(L("Acceso: la curva comanda la ventola. Spento: torna al firmware, e non c'e' nemmeno l'emergenza.",
            "On: the curve drives the fan. Off: back to the firmware, with no emergency either."), L("Controllo", "Control")))
        ri.addStretch(1)
        fine.addLayout(ri)
        self.et_salva = QLabel("")
        self.et_salva.setObjectName("quieto")
        fine.addWidget(self.et_salva)
        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.setMinimumHeight(34)
        b.clicked.connect(self.salva)
        fine.addWidget(b)
        basso.addLayout(fine)

    # ---- panels ---------------------------------------------------------------
    def _box(self, titolo, aiuto=""):
        g = QWidget()
        v = QVBoxLayout(g)
        v.setContentsMargins(0, 0, 0, 0)
        r = QHBoxLayout()
        r.addWidget(QLabel("<b>%s</b>" % titolo))
        if aiuto:
            r.addWidget(Aiuto(aiuto, titolo))
        r.addStretch(1)
        v.addLayout(r)
        return g, v

    def _sez_sorgente(self):
        g, v = self._box(L("Sorgente", "Source"), L(
            "La curva si legge su UNA temperatura; se ne scegli piu' d'una comanda la piu' alta. "
            "Compaiono solo i sensori che la macchina legge davvero: quelli che il chip dichiara "
            "ma non aggiorna sono nascosti apposta.",
            "The curve is read against ONE temperature; pick more than one and the hottest wins. "
            "Only sensors the machine actually reads are listed: the ones the chip declares but "
            "never updates are hidden on purpose."))
        self.contenitore_sorgente = QVBoxLayout()
        v.addLayout(self.contenitore_sorgente)
        v.addStretch(1)
        return g

    def _sez_anticipo(self):
        g, v = self._box(L("Anticipo", "Lead"), L(
            "La ventola impiega un paio di secondi a prendere giri e l'APU si scalda in pochi: qui si "
            "guarda quanto sta salendo e si legge la curva un po' piu' avanti. GUADAGNO: gradi di "
            "anticipo per ogni grado al secondo di salita. FINESTRA: su quanti secondi si misura. Sulla "
            "BC-250 si leggono anche i watt, che salgono PRIMA della temperatura. L'anticipo puo' solo "
            "alzare la ventola, mai abbassarla.",
            "A fan takes a couple of seconds to spin up and the APU heats in a few: this watches how "
            "fast it is rising and reads the curve a little further along. GAIN: degrees of lead per "
            "degree-per-second of rise. WINDOW: how many seconds the rise is measured over. On the "
            "BC-250 the watts are read too, and they rise BEFORE the temperature. Lead can only raise "
            "the fan, never lower it."))
        p = self.conf.get("predittivo") or {}
        self.pred_attivo = QCheckBox(L("Attivo", "On"))
        self.pred_attivo.setChecked(bool(p.get("attivo", True)))
        v.addWidget(self.pred_attivo)

        def riga(testo, w, suff=""):
            h = QHBoxLayout()
            h.addWidget(QLabel(testo))
            h.addStretch(1)
            h.addWidget(w)
            if suff:
                h.addWidget(QLabel(suff))
            v.addLayout(h)
        self.guadagno = QDoubleSpinBox()
        self.guadagno.setRange(0.0, 10.0)
        self.guadagno.setSingleStep(0.5)
        self.guadagno.setValue(float(p.get("guadagno", 2.5)))
        riga(L("Guadagno", "Gain"), self.guadagno)
        self.finestra_s = QSpinBox()
        self.finestra_s.setRange(2, 30)
        self.finestra_s.setValue(int(p.get("finestra", 6)))
        riga(L("Finestra", "Window"), self.finestra_s, "s")
        self.preraffredda = QSpinBox()
        self.preraffredda.setRange(20, 100)
        self.preraffredda.setValue(int(p.get("preraffredda", 55)))
        riga(L("Pre-raffredda", "Pre-cool"), self.preraffredda, "%")
        h = QHBoxLayout()
        h.addWidget(QLabel(L("Giochi", "Games")))
        h.addWidget(Aiuto(L("Un gioco pesante scalda venti secondi dopo l'avvio: la ventola parte prima.",
            "A heavy game heats up twenty seconds after launch: the fan starts before."), L("Giochi", "Games")))
        h.addStretch(1)
        v.addLayout(h)
        self.et_gioco = QLabel("")
        self.et_gioco.setObjectName("quieto")
        v.addWidget(self.et_gioco)
        v.addStretch(1)
        return g

    def _sez_sicurezza(self):
        g, v = self._box(L("Sicurezza", "Safety"), L(
            "MINIMO: la ventola non scende mai sotto. ISTERESI: di quanto deve scendere la temperatura "
            "prima che la ventola cali, o mezzo grado di tremolio la farebbe ballare. EMERGENZA: sopra "
            "questa temperatura si va al 100% senza passare dalla curva, e non si puo' spegnere. Se un "
            "sensore sparisce, la ventola va al massimo.",
            "MINIMUM: the fan never goes below. HYSTERESIS: how far the temperature must fall before "
            "the fan eases off, or half a degree of jitter would have it hunting. EMERGENCY: above this "
            "temperature it goes to 100% without consulting the curve, and it cannot be turned off. If "
            "a sensor disappears, the fan goes to full."))

        def riga(testo, w, suff=""):
            h = QHBoxLayout()
            h.addWidget(QLabel(testo))
            h.addStretch(1)
            h.addWidget(w)
            if suff:
                h.addWidget(QLabel(suff))
            v.addLayout(h)
        self.minimo = QSpinBox()
        self.minimo.setRange(20, 100)
        self.minimo.setValue(int(self.conf.get("minimo", 30)))
        riga(L("Minimo", "Minimum"), self.minimo, "%")
        self.isteresi = QDoubleSpinBox()
        self.isteresi.setRange(0.0, 20.0)
        self.isteresi.setSingleStep(0.5)
        self.isteresi.setValue(float(self.conf.get("isteresi", 3.0)))
        riga(L("Isteresi", "Hysteresis"), self.isteresi, "°C")
        self.emergenza = QDoubleSpinBox()
        self.emergenza.setRange(60.0, 105.0)
        self.emergenza.setValue(float(self.conf.get("emergenza", 88.0)))
        riga(L("Emergenza", "Emergency"), self.emergenza, "°C")
        h = QHBoxLayout()
        self.bottone_prova = QPushButton(L("Test PWM", "PWM test"))
        self.bottone_prova.clicked.connect(self._prova_uscita)
        h.addWidget(self.bottone_prova, 1)
        h.addWidget(Aiuto(L("Ventola al massimo, poi al 35%, poi di nuovo al massimo: se i giri seguono, il PWM comanda davvero. Trenta secondi.",
            "Fan to full, then 35%, then full again: if the speed follows, the PWM really drives it. Thirty seconds."), "Test PWM"))
        v.addLayout(h)
        self.et_prova = QLabel("")
        self.et_prova.setWordWrap(True)
        v.addWidget(self.et_prova)
        self._mostra_prova(leggi_json(PROVA, {}))
        v.addStretch(1)
        return g

    def _mostra_prova(self, d):
        if not d:
            self.et_prova.setText("")
            return
        if d.get("risponde"):
            self.et_prova.setObjectName("bene")
            self.et_prova.setText(L("Provata: la ventola risponde.", "Tested: the fan responds."))
        else:
            self.et_prova.setObjectName("male")
            self.et_prova.setText(L("Provata: la ventola NON risponde. Su questa macchina la governa il firmware.",
                                    "Tested: the fan does NOT respond. On this machine the firmware keeps it."))
        self.et_prova.style().polish(self.et_prova)

    def _prova_uscita(self):
        sensori = (self.stato or {}).get("sensori") or []
        ventole = [x for x in sensori if x.get("type") == "fan" and x.get("value")]
        pwm = self.conf.get("pwm") or self._scegli_pwm()
        if not ventole or not pwm:
            QMessageBox.information(self, L("Non si puo' provare", "Cannot test"), L(
                "Serve un'uscita PWM e una ventola che dia i giri.", "This needs a PWM output and a fan that reports its speed."))
            return
        self.bottone_prova.setEnabled(False)
        self.et_prova.setText(L("Prova in corso, una trentina di secondi.", "Testing, about thirty seconds."))
        self._filo = Prova(self.demone, pwm, ventole[0]["key"], self)
        self._filo.finita.connect(self._prova_finita)
        self._filo.start()

    def _prova_finita(self, risponde, dettaglio):
        self.bottone_prova.setEnabled(True)
        self._mostra_prova(leggi_json(PROVA, {}) or {"risponde": risponde})
        if dettaglio:
            self.et_prova.setText(self.et_prova.text() + "\n" + dettaglio)

    # ---- curve ------------------------------------------------------------------
    def _prova_preset(self, b):
        self.curva.imposta(PRESET[b.chiave])
        self.et_salva.setText(L("%s: premi Applica", "%s: press Apply") % nome_preset(b.chiave))

    def _curva_toccata(self):
        for b in self.gruppo.buttons():
            self.gruppo.setExclusive(False)
            b.setChecked(False)
            self.gruppo.setExclusive(True)
        self.et_salva.setText(L("modificata, non applicata", "changed, not applied"))

    def _preset_scelto(self):
        for b in self.gruppo.buttons():
            if b.isChecked():
                return b.chiave
        return "personalizzata"

    # ---- readings ---------------------------------------------------------------
    def aggiorna(self):
        self.stato = leggi_json(VENTOLA_STATO, {})
        s = self.stato
        if not s:
            self.et_motivo.setText(L("Il controllo non sta girando: premi Applica per accenderlo.",
                                     "The controller is not running: press Apply to start it."))
            return
        t = s.get("temperatura")
        motivo = s.get("motivo") or ""
        testo = {"curve": L("segue la curva", "following the curve"),
                 "no temperature: full speed": L("nessuna temperatura: al massimo", "no temperature: full speed")}.get(motivo, motivo)
        if motivo.startswith("emergency"):
            testo = L("EMERGENZA: al massimo", "EMERGENCY: full speed")
        elif motivo.startswith("anticipating"):
            testo = L("anticipa la salita", "anticipating the rise")
        elif motivo.startswith("pre-cooling"):
            testo = L("pre-raffredda per %s", "pre-cooling for %s") % (s.get("gioco") or "")
        if not s.get("in_controllo"):
            testo = L("la ventola e' del firmware: la curva non comanda", "the fan is the firmware's: the curve is not in charge")
        self.et_motivo.setText(testo)
        sensori = s.get("sensori") or []
        self._riempi_sorgente(sensori)
        self._allarmi(sensori)
        meta = {x["key"]: (x.get("label") or x["key"], x.get("unit") or "") for x in sensori}
        meta["__ventola__"] = (L("Ventola", "Fan"), "%")
        meta["__temperatura__"] = (L("Temperatura", "Temperature"), "C")
        self.grafico.carica(s.get("storia") or {}, meta)
        for chiave, serie in self.grafico.elenco():
            w = self.tessere.get(chiave)
            if w is not None:
                w.aggiorna(serie)
        self.curva.aggiorna_vivo(t, float(s.get("duty") or 0))
        if s.get("gioco") and hasattr(self, "et_gioco"):
            self.et_gioco.setText(L("Ultimo riconosciuto: %s", "Last recognised: %s") % s["gioco"])

    def _allarmi(self, sensori):
        allarmi = []
        for x in sensori:
            if x.get("type") != "in" or x.get("value") is None:
                continue
            v = x["value"]
            atteso = nominale(x.get("label"))
            if atteso == "dinamica":
                continue
            if atteso is None:
                storia = self.riposo.setdefault(x["key"], [])
                if len(storia) < CAMPIONI_RIPOSO:
                    storia.append(v)
                    continue
                o = sorted(storia)
                atteso = o[len(o) // 2]
                toll = 0.10
            else:
                toll = 0.05
            if atteso and abs(v - atteso) / atteso > toll:
                allarmi.append(L("%s: %.3f V invece di %.2f V", "%s: %.3f V instead of %.2f V") % (x.get("label") or x["key"], v, atteso))
        self.et_allarme.setText("\n".join(allarmi[:3]))

    def _riempi_sorgente(self, sensori):
        if not hasattr(self, "contenitore_sorgente"):
            return
        temp = [x for x in sensori if x.get("type") == "temp"]
        chiavi = [x["key"] for x in temp]
        if set(chiavi) != set(self.caselle_sorgente):
            while self.contenitore_sorgente.count():
                it = self.contenitore_sorgente.takeAt(0)
                if it.layout():
                    while it.layout().count():
                        w = it.layout().takeAt(0).widget()
                        if w:
                            w.deleteLater()
            self.caselle_sorgente = {}
            scelte = set(self.conf.get("sorgente") or [])
            for x in temp:
                c = QCheckBox(x["label"])
                c.setChecked(x["key"] in scelte)
                self.caselle_sorgente[x["key"]] = c
                h = QHBoxLayout()
                h.addWidget(c)
                h.addStretch(1)
                val = QLabel("")
                val.setStyleSheet("color:%s;" % stile.OTTONE)
                h.addWidget(val)
                c.valore = val
                self.contenitore_sorgente.addLayout(h)
        for x in temp:
            c = self.caselle_sorgente.get(x["key"])
            if c is not None and x.get("value") is not None:
                c.valore.setText("%.1f °C" % x["value"])

    def _rifai_tessere(self):
        elenco = self.grafico.elenco()
        primi = ["__temperatura__", "__ventola__"]
        for unita in ("rpm", "W"):
            for k, s in elenco:
                if s["unita"] == unita:
                    primi.append(k)
                    break
        while self.colonna.count():
            it = self.colonna.takeAt(0)
            if it.widget():
                it.widget().setParent(None)
        for k in primi:
            if k in self.grafico.serie:
                self.colonna.addWidget(self._tessera(k))
        for k, s in elenco:
            if k not in primi:
                self.colonna.addWidget(self._tessera(k))
        self.colonna.addStretch(1)

    def _tessera(self, k):
        t = self.tessere.get(k)
        if t is None:
            t = Tessera(k)
            t.premuta.connect(self._accendi_serie)
            t.rinominata.connect(self._rinomina_serie)
            self.tessere[k] = t
        return t

    def _accendi_serie(self, k):
        s = self.grafico.serie.get(k)
        if s:
            s["visibile"] = not s["visibile"]
            self.grafico.update()
            self._tessera(k).aggiorna(s)

    def _rinomina_serie(self, k):
        s = self.grafico.serie.get(k)
        if not s or k.startswith("__"):
            return
        nuovo, ok = QInputDialog.getText(self, L("Nome del sensore", "Sensor name"),
                                         L("Come si chiama davvero questo sensore?", "What is this sensor really called?"), text=s["etichetta"])
        if not ok or not nuovo.strip():
            return
        self.etichette[k] = nuovo.strip()[:40]
        s["etichetta"] = nuovo.strip()[:40]
        self._tessera(k).aggiorna(s)
        self.demone.cmd(cmd="ventola", azione="etichette", dati=self.etichette)

    def _apri_serie(self, k):
        s = self.grafico.serie.get(k)
        if not s:
            return
        p = self.pannelli_serie.get(k)
        if p is None:
            p = Pannello(s["etichetta"], GraficoSingolo(self.grafico, k), self)
            p.resize(700, 400)
            self.pannelli_serie[k] = p
        p.mostra()

    # ---- save -------------------------------------------------------------------
    def _scegli_pwm(self):
        sensori = (self.stato or {}).get("sensori") or []
        ventole = [x for x in sensori if x.get("type") == "fan" and x.get("value")]
        chip = ventole[0]["key"].split(":")[0] if ventole else ""
        try:
            import hwmon
            _, pwm = hwmon.elenca()
        except Exception:
            return ""
        candidate = [p for p in pwm if p.modo is not None and p.modo >= 0]
        if chip:
            stesso = [p for p in candidate if p.chiave.split(":")[0] == chip]
            candidate = stesso or candidate
        for p in candidate:
            if p.modo == 1:
                return p.chiave
        return candidate[0].chiave if candidate else ""

    def salva(self):
        sorgenti = [k for k, c in self.caselle_sorgente.items() if c.isChecked()] or list(self.conf.get("sorgente") or [])
        pwm = self.conf.get("pwm") or self._scegli_pwm()
        if self.interruttore.isChecked() and not sorgenti:
            QMessageBox.warning(self, L("Manca la sorgente", "No source chosen"),
                                L("Scegli almeno una temperatura (pannello Sorgente).", "Pick at least one temperature (Source panel)."))
            return
        if self.interruttore.isChecked() and not pwm:
            QMessageBox.warning(self, L("Nessuna uscita", "No output"),
                                L("Non ho trovato un'uscita PWM comandabile.", "No controllable PWM output found."))
            return
        conf = {"attivo": self.interruttore.isChecked(), "pwm": pwm, "sorgente": sorgenti,
                "curva": self.curva.punti, "minimo": self.minimo.value(), "isteresi": self.isteresi.value(),
                "emergenza": self.emergenza.value(), "preset": self._preset_scelto(),
                "predittivo": {"attivo": self.pred_attivo.isChecked(), "guadagno": self.guadagno.value(),
                               "finestra": self.finestra_s.value(), "preraffredda": self.preraffredda.value()}}
        r = self.demone.cmd(cmd="ventola", azione="scrivi", dati=conf)
        if r.get("ok"):
            self.conf = conf
            self.et_salva.setText(L("applicata", "applied"))
        else:
            QMessageBox.critical(self, L("Non riesco a salvare", "Could not save"), r.get("err", "?"))
