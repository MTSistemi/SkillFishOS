# -*- coding: utf-8 -*-
"""Profiles: one click that sets the ceiling, the CPU, the fan and the scheduler.

A profile is a small dictionary; the shipped three live in
/usr/share/skillfish/profili.json, the ones you save in ~/.config/skillfish.
Applying a profile does not touch the curve itself: it moves the ceiling
within the curve that is already there, which is why it needs no trial.
"""
import os

from PyQt6.QtWidgets import (QCheckBox, QComboBox, QGridLayout, QHBoxLayout, QInputDialog,
                             QLabel, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QWidget)

from .. import stile
from ..comune import (GOV_CONF, PROFILI_SISTEMA, PROFILI_UTENTE, VENTOLA_CONF, L, Aiuto,
                      leggi_json, leggi_testo, scrivi_json, sh)
from ..finestra import PaginaBase
from ..stile import Scheda, Stato, griglia_schede, intestazione
from .ventola import PRESET as PRESET_VENTOLA, nome_preset

PREDEFINITI = {
    "silenzioso": {"nome_it": "Silenzioso", "nome_en": "Quiet", "tetto": 1850, "cpu": 3500,
                   "ventola": "silenzioso", "scx": False,
                   "desc_it": "Tetto 1850, ventola bassa: per film, navigazione e giochi leggeri. Dieci gradi in meno, quasi gli stessi fotogrammi.",
                   "desc_en": "Ceiling 1850, fan low: for films, browsing and light games. Ten degrees less, nearly the same frames."},
    "equilibrato": {"nome_it": "Equilibrato", "nome_en": "Balanced", "tetto": 2000, "cpu": 3500,
                    "ventola": "equilibrato", "scx": True,
                    "desc_it": "Tetto 2000, ventola equilibrata, schedulatore nei giochi. Quello di tutti i giorni.",
                    "desc_en": "Ceiling 2000, balanced fan, scheduler while gaming. The everyday one."},
    "prestazioni": {"nome_it": "Prestazioni", "nome_en": "Performance", "tetto": 2100, "cpu": 3500,
                    "ventola": "prestazioni", "scx": True,
                    "desc_it": "Tetto 2100, la curva misurata, ventola pronta. Si sente la ventola.",
                    "desc_en": "Ceiling 2100, the measured curve, fan ready. You will hear the fan."},
}


def profili_tutti():
    out = dict(PREDEFINITI)
    out.update(leggi_json(PROFILI_SISTEMA, {}) or {})
    for k, v in (leggi_json(PROFILI_UTENTE, {}) or {}).items():
        v = dict(v)
        v["utente"] = True
        out[k] = v
    return out


def nome_profilo(k, p):
    return p.get("nome_it" if L("it", "en") == "it" else "nome_en") or p.get("nome") or k


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 4000
        self.schede = {}

    def costruisci(self):
        self.v = self.corpo_scorrevole()
        self.v.addWidget(intestazione(L("Profili", "Profiles"), L(
            "Un clic per tetto GPU, CPU, ventola e schedulatore insieme. La curva non si tocca: "
            "il profilo sposta il tetto dentro alla curva che c'e' gia'.",
            "One click for GPU ceiling, CPU, fan and scheduler together. The curve is not "
            "touched: a profile moves the ceiling within the curve that is already there.")))
        self.griglia = QWidget()
        self.v.addWidget(self.griglia)
        r = QHBoxLayout()
        b = QPushButton(L("Salva lo stato attuale come profilo", "Save the current state as a profile"))
        b.clicked.connect(self._salva_attuale)
        r.addWidget(b)
        r.addWidget(Aiuto(L(
            "Prende tetto, CPU, preset della ventola e schedulatore come sono adesso e li mette in "
            "un profilo tuo, in ~/.config/skillfish/profili.json.",
            "Takes the ceiling, CPU, fan preset and scheduler as they are now and puts them in a "
            "profile of yours, in ~/.config/skillfish/profili.json."), L("Profili", "Profiles")))
        r.addStretch(1)
        self.v.addLayout(r)
        self.v.addStretch(1)
        self._rifai()

    def _stato_attuale(self):
        g = leggi_json(GOV_CONF, {})
        f = leggi_json(VENTOLA_CONF, {})
        import re
        m = re.search(r"frequency\s*=\s*(\d+)", leggi_testo("/etc/bc250-smu-oc.conf"))
        rc, en, _ = sh("systemctl is-enabled skillfish-scx.path 2>/dev/null", 5)
        return {"tetto": int(g.get("freq_max", 0) or 0), "cpu": int(m.group(1)) if m else 0,
                "ventola": f.get("preset", ""), "scx": en == "enabled"}

    def _rifai(self):
        vecchio = self.griglia
        schede = []
        att = self._stato_attuale()
        self.schede = {}
        for k, p in profili_tutti().items():
            desc = p.get("desc_it" if L("it", "en") == "it" else "desc_en") or p.get("desc", "")
            s = Scheda(nome_profilo(k, p), desc)
            attivo = (att["tetto"] == p.get("tetto") and att["ventola"] == p.get("ventola")
                      and att["scx"] == bool(p.get("scx")) and (not p.get("cpu") or att["cpu"] == p.get("cpu")))
            b = Stato(L("attivo", "active") if attivo else "", "bene")
            if attivo:
                s.testa.insertWidget(s.testa.count() - 1, b)
            s.riga(L("Tetto GPU", "GPU ceiling"), "%s MHz" % p.get("tetto", "—"))
            s.riga("CPU", "%s MHz" % p.get("cpu", "—"))
            s.riga(L("Ventola", "Fan"), nome_preset(p.get("ventola", "")))
            s.riga(L("Schedulatore", "Scheduler"), L("nei giochi", "while gaming") if p.get("scx") else L("di serie", "stock"))
            voci = [(L("Applica", "Apply"), lambda _c=False, k=k: self._applica(k), True)]
            if p.get("utente"):
                voci.append((L("Elimina", "Delete"), lambda _c=False, k=k: self._elimina(k), False))
            s.bottoni(*voci)
            schede.append(s)
            self.schede[k] = s
        self.griglia = griglia_schede(*schede, colonne=3)
        self.v.replaceWidget(vecchio, self.griglia)
        vecchio.deleteLater()

    def aggiorna(self):
        self._rifai()

    def _applica(self, k):
        p = profili_tutti().get(k)
        if not p:
            return
        errori = []
        g = dict(leggi_json(GOV_CONF, {}))
        pts = g.get("curva") or []
        if pts and p.get("tetto"):
            g["freq_max"] = max(pts[0][0], min(pts[-1][0], int(p["tetto"])))
            r = self.demone.cmd(cmd="gov-set", conf=g)
            if r.get("annullato"):
                return
            if not r.get("ok"):
                errori.append("GPU: " + r.get("err", "?"))
        if p.get("cpu"):
            import re
            t = leggi_testo("/etc/bc250-smu-oc.conf")
            scale = re.search(r"scale\s*=\s*(-?\d+)", t)
            temp = re.search(r"max_temperature\s*=\s*(\d+)", t)
            r = self.demone.cmd(cmd="apply-cpu", mhz=int(p["cpu"]), scale=int(scale.group(1)) if scale else 0,
                                temp=int(temp.group(1)) if temp else 85)
            if not r.get("ok"):
                errori.append("CPU: " + r.get("err", "?"))
        if p.get("ventola") in PRESET_VENTOLA:
            f = dict(leggi_json(VENTOLA_CONF, {}))
            if f.get("pwm") and f.get("sorgente"):
                f["curva"] = PRESET_VENTOLA[p["ventola"]]
                f["preset"] = p["ventola"]
                f["attivo"] = True
                r = self.demone.cmd(cmd="ventola", azione="scrivi", dati=f)
                if not r.get("ok"):
                    errori.append(L("ventola", "fan") + ": " + r.get("err", "?"))
            else:
                errori.append(L("ventola: configurala prima una volta dalla sua pagina", "fan: set it up once from its page first"))
        if "scx" in p:
            r = self.demone.cmd(cmd="scx-set", on=bool(p["scx"]))
            if not r.get("ok") and bool(p["scx"]):
                errori.append(L("schedulatore", "scheduler") + ": " + r.get("err", "?"))
        self.toast(("; ".join(errori)) if errori else L("Profilo «%s» applicato", "Profile «%s» applied") % nome_profilo(k, p), 7)
        self._rifai()

    def _salva_attuale(self):
        nome, ok = QInputDialog.getText(self, L("Nuovo profilo", "New profile"), L("Come lo chiami?", "What do you call it?"))
        if not ok or not nome.strip():
            return
        att = self._stato_attuale()
        chiave = "".join(c for c in nome.strip().lower().replace(" ", "-") if c.isalnum() or c == "-") or "profilo"
        d = leggi_json(PROFILI_UTENTE, {}) or {}
        d[chiave] = {"nome_it": nome.strip(), "nome_en": nome.strip(), "tetto": att["tetto"], "cpu": att["cpu"],
                     "ventola": att["ventola"] or "equilibrato", "scx": att["scx"],
                     "desc_it": L("Salvato da te.", "Saved by you."), "desc_en": "Saved by you."}
        scrivi_json(PROFILI_UTENTE, d)
        self._rifai()

    def _elimina(self, k):
        d = leggi_json(PROFILI_UTENTE, {}) or {}
        if k in d and QMessageBox.question(self, L("Eliminare?", "Delete?"), L("Tolgo il profilo «%s»?", "Remove profile «%s»?") % k) == QMessageBox.StandardButton.Yes:
            del d[k]
            scrivi_json(PROFILI_UTENTE, d)
            self._rifai()
