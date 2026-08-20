# -*- coding: utf-8 -*-
u"""I sensori che la macchina legge DAVVERO, separati da quelli che finge.

PERCHE' ESISTE
Un pannello ventole qualunque elenca tutto quello che il chip Super-I/O dichiara.
Misurato sulle nostre due macchine, quell'elenco e' per lo piu' falso:

  BC-250, chip nct6686
    ventole   8 canali dichiarati, UNO legge davvero (fan2, "Pump Fan", 1324 giri)
    tensioni  14 dichiarate, TRE leggono (+3,3V 3,42 / AVSB 3,42 / VBat 2,03)
              ⚠️ +12V e +5V danno 0,00: su questa scheda le rail
              dell'alimentatore non sono cablate al chip e non si possono
              sorvegliare da qui.
    temperature 7 dichiarate, TRE leggono (CPU 51, System 50, VRM MOS 50)

  Fujitsu D3521-A1, chip nct6792
    temperature 12 dichiarate. CPUTIN dice 127,5 gradi mentre coretemp dice 47:
              e' il valore che il chip restituisce quando al pin non c'e'
              attaccato niente. AUXTIN1/2/3 dicono -128, che e' lo stesso
              messaggio scritto dall'altra parte. Le PCH_* dicono 0.
              Ne legge UNA in modo plausibile.
    ventole   due, 967 e 2027 giri, tutte e due vere
    tensioni  15 dichiarate, sei diverse da zero, e SENZA ETICHETTA: il driver
              non sa come sono cablate, quindi si chiamano in0..in14 e basta.
              E' il motivo per cui le etichette devono poterle scrivere le
              persone.

Quindi "mostrare solo i sensori veri" non e' una rifinitura: sulle macchine che
abbiamo, la roba finta e' la maggioranza. E un pannello che mostra 127 gradi
accanto a una ventola che non esiste non e' solo brutto, e' pericoloso: se poi
ci si attacca una curva, quella curva la comanda un numero inventato.

COME SI DECIDE
Non basta leggere una volta. Un canale si guarda per qualche secondo:

  temperatura  fuori da -40..+120 gradi   -> finta (i -128 e i 127,5 di sopra)
               sempre esattamente 0       -> finta (le PCH_* e le M2_*)
  ventola      sempre 0                   -> ferma o non collegata: NON si
               butta, si mette da parte. Distinguerle davvero vuol dire muovere
               il PWM e guardare se il contagiri risponde, ed e' una prova che
               tocca l'hardware: la fa il controllo ventola quando glielo si
               chiede, non la scoperta all'avvio.
  tensione     sempre sotto 50 mV         -> finta
  potenza      sempre 0                   -> finta

⚠️ SI GUARDA ANCHE SE CAMBIA, ma non si butta niente per questo: una ventola
ferma e una stanza a temperatura costante danno letture immobili e sono vere.
Il fatto che cambi si registra e basta, serve dopo per capire quale canale
segue il carico.

LA CHIAVE DI UN CANALE
`hwmon3` oggi e' il Nuvoton e domani puo' essere la NVMe: la numerazione dipende
dall'ordine in cui si caricano i driver. Per ricordarsi le etichette scritte
dall'utente serve una chiave che non cambia, e si ricava dal collegamento
`device`:

  nct6687.2592     l'indirizzo ISA del Super-I/O sulla BC-250
  nct6775.2576     lo stesso sul Fujitsu
  0000:01:00.0     l'indirizzo PCI della GPU

Quindi la chiave e' `<device>:<tipo><indice>`, per esempio `nct6687.2592:fan2`.
"""
from __future__ import unicode_literals

import glob
import io
import json
import os
import time

BASE = "/sys/class/hwmon"
ETICHETTE = "/etc/skillfish/sensori.json"

# Come si legge il valore grezzo di ogni tipo, e come si scrive.
#   divisore  il kernel espone millesimi per gradi, millivolt e microwatt
#   unita     quella che si mostra
TIPI = {
    "temp":  {"divisore": 1000.0,    "unita": "C",   "decimali": 1},
    "fan":   {"divisore": 1.0,       "unita": "rpm", "decimali": 0},
    "in":    {"divisore": 1000.0,    "unita": "V",   "decimali": 3},
    "power": {"divisore": 1000000.0, "unita": "W",   "decimali": 2},
    "curr":  {"divisore": 1000.0,    "unita": "A",   "decimali": 3},
}

# I limiti di plausibilita', uno per tipo. Sono i valori misurati sulle nostre
# due macchine, non numeri scelti a sentimento: vedi il commento in cima.
LIMITI = {
    "temp":  (-40.0, 120.0),
    "fan":   (0.0, 60000.0),
    "in":    (0.05, 30.0),
    "power": (0.0, 2000.0),
    "curr":  (0.0, 200.0),
}


def _leggi(percorso):
    try:
        with io.open(percorso, encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except (IOError, OSError):
        return None


class Canale(object):
    u"""Un ingresso di un chip: una temperatura, una ventola, una tensione."""

    def __init__(self, chip, chiave_chip, tipo, indice, percorso, etichetta_driver):
        self.chip = chip
        self.chiave_chip = chiave_chip
        self.tipo = tipo
        self.indice = indice
        self.percorso = percorso
        self.etichetta_driver = etichetta_driver or ""
        self.campioni = []
        self.vero = None          # deciso da scopri()
        self.motivo = ""          # perche' no, quando e' no
        self.cambia = False

    @property
    def chiave(self):
        return "%s:%s%d" % (self.chiave_chip, self.tipo, self.indice)

    @property
    def unita(self):
        return TIPI[self.tipo]["unita"]

    def leggi(self):
        g = _leggi(self.percorso)
        if g is None:
            return None
        try:
            return int(g) / TIPI[self.tipo]["divisore"]
        except ValueError:
            return None

    def valore(self):
        return self.campioni[-1] if self.campioni else None

    def etichetta(self, utente=None):
        u"""Quella scritta dall'utente, se c'e'; poi quella del driver; poi il
        nome grezzo. Il ripiego non e' mai vuoto: una riga senza nome in un
        pannello e' peggio di un nome brutto."""
        if utente and utente.get(self.chiave):
            return utente[self.chiave]
        if self.etichetta_driver:
            return self.etichetta_driver
        return "%s%d" % (self.tipo, self.indice)

    def __repr__(self):
        return "<Canale %s %s>" % (self.chiave, self.etichetta_driver)


class Pwm(object):
    u"""Un'uscita su cui si puo' scrivere per far girare una ventola."""

    def __init__(self, chip, chiave_chip, indice, percorso):
        self.chip = chip
        self.chiave_chip = chiave_chip
        self.indice = indice
        self.percorso = percorso

    @property
    def chiave(self):
        return "%s:pwm%d" % (self.chiave_chip, self.indice)

    @property
    def valore(self):
        g = _leggi(self.percorso)
        return int(g) if g and g.lstrip("-").isdigit() else None

    @property
    def modo(self):
        u"""0 = sempre al massimo, 1 = comandata a mano, 2+ = la governa il chip.
        Per scrivere un valore nostro serve il modo 1."""
        g = _leggi(self.percorso + "_enable")
        return int(g) if g and g.lstrip("-").isdigit() else None

    def __repr__(self):
        return "<Pwm %s>" % self.chiave


def _chiave_chip(cartella, nome):
    d = os.path.join(cartella, "device")
    if os.path.islink(d):
        b = os.path.basename(os.path.realpath(d))
        if b:
            return b
    return nome or os.path.basename(cartella)


def elenca():
    u"""Tutti i canali e tutti i PWM che il sistema dichiara, senza giudizio."""
    canali, pwm = [], []
    for cartella in sorted(glob.glob(os.path.join(BASE, "hwmon*"))):
        nome = _leggi(os.path.join(cartella, "name")) or ""
        chiave = _chiave_chip(cartella, nome)
        for tipo in TIPI:
            for p in sorted(glob.glob(os.path.join(cartella, tipo + "*_input"))):
                base = os.path.basename(p)[:-len("_input")]
                cifre = "".join(c for c in base if c.isdigit())
                if not cifre:
                    continue
                et = _leggi(os.path.join(cartella, base + "_label"))
                canali.append(Canale(nome, chiave, tipo, int(cifre), p, et))
        for p in sorted(glob.glob(os.path.join(cartella, "pwm[0-9]"))):
            pwm.append(Pwm(nome, chiave, int(os.path.basename(p)[3:]), p))
    return canali, pwm


def scopri(durata=4.0, campioni=5):
    u"""Guarda per qualche secondo e decide chi e' vero.

    Restituisce (veri, scartati, fermi, pwm):
      veri      da mostrare
      scartati  con il motivo, da mostrare solo a chi vuole vedere tutto
      fermi     ventole a zero: potrebbero esistere e stare ferme
    """
    canali, pwm = elenca()
    passo = durata / max(1, campioni - 1) if campioni > 1 else 0
    for i in range(campioni):
        for c in canali:
            v = c.leggi()
            if v is not None:
                c.campioni.append(v)
        if i < campioni - 1 and passo:
            time.sleep(passo)

    veri, scartati, fermi = [], [], []
    for c in canali:
        if not c.campioni:
            c.vero, c.motivo = False, "cannot be read"
            scartati.append(c)
            continue
        c.cambia = len(set(c.campioni)) > 1
        basso, alto = LIMITI[c.tipo]
        fuori = [v for v in c.campioni if v < basso or v > alto]
        if fuori:
            c.vero = False
            c.motivo = "out of range (%.1f %s)" % (fuori[0], c.unita)
            scartati.append(c)
        elif all(v == 0 for v in c.campioni):
            if c.tipo == "fan":
                # Non e' un verdetto: e' un "non lo so". Per saperlo bisogna
                # muovere il PWM e vedere se risponde, e quella prova tocca
                # l'hardware, quindi non si fa qui.
                c.vero = None
                c.motivo = "always zero: stopped, or nothing connected"
                fermi.append(c)
            else:
                c.vero = False
                c.motivo = "always zero"
                scartati.append(c)
        else:
            c.vero = True
            veri.append(c)

    _segna_sospetti(veri)
    return veri, scartati, fermi, pwm


# Quanto piu' calda delle altre, e ferma, prima di non fidarsi.
SCARTO_SOSPETTO = 25.0


def _segna_sospetti(veri):
    u"""Marca le temperature che passano i limiti ma non convincono.

    Sul Fujitsu SYSTIN dichiara 80 gradi mentre i quattro core stanno a 38 e la
    GPU a 37, e non si muove di un decimo in nessun campione. Non e' fuori
    scala, quindi nessun limite lo prende: e' semplicemente un pin a cui non e'
    attaccato niente che restituisce sempre lo stesso numero. Se qualcuno ci
    aggancia una curva ventola, quella curva la comanda una costante — la
    ventola non salira' mai, oppure stara' al massimo per sempre.

    La regola e' un confronto fra pari, non una soglia fissa: e' sospetta la
    temperatura che sta almeno 25 gradi sopra la MEDIANA delle altre e che in
    tutta la finestra non cambia mai. La mediana perche' basta un secondo
    canale rotto per sballare una media.

    ⚠️ Non si nasconde: si segna. Una temperatura davvero alta e davvero ferma
    esiste (un dissipatore passivo saturo), e nasconderla sarebbe peggio che
    mostrarla con un avvertimento. Chi sceglie la sorgente della curva vede il
    segno e decide.
    """
    temp = [c for c in veri if c.tipo == "temp" and c.campioni]
    if len(temp) < 3:
        return                      # con due sole temperature non c'e' un "resto"
    for c in temp:
        altre = sorted(x.campioni[-1] for x in temp if x is not c)
        n = len(altre)
        mediana = altre[n // 2] if n % 2 else (altre[n // 2 - 1] + altre[n // 2]) / 2.0
        if not c.cambia and c.campioni[-1] - mediana >= SCARTO_SOSPETTO:
            c.motivo = ("never changes and is %.0f C above the other sensors"
                        % (c.campioni[-1] - mediana))


def etichette_utente(percorso=ETICHETTE):
    try:
        with io.open(percorso, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (IOError, OSError, ValueError):
        return {}


def salva_etichette(d, percorso=ETICHETTE):
    cartella = os.path.dirname(percorso)
    if cartella and not os.path.isdir(cartella):
        os.makedirs(cartella)
    tmp = percorso + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(d, indent=2, ensure_ascii=False, sort_keys=True))
    os.rename(tmp, percorso)


# --------------------------------------------------------------------------
# Riga di comando: serve a guardare una macchina nuova prima di fidarsi.
# ⚠️ Il testo e' in inglese, come tutto il testo di base del progetto.
if __name__ == "__main__":
    import sys

    solo_json = "--json" in sys.argv
    veri, scartati, fermi, pwm = scopri()
    ut = etichette_utente()

    if solo_json:
        def d(c):
            return {"key": c.chiave, "chip": c.chip, "type": c.tipo,
                    "label": c.etichetta(ut), "driver_label": c.etichetta_driver,
                    "unit": c.unita, "value": c.valore(), "varies": c.cambia,
                    "suspect": bool(c.vero and c.motivo), "reason": c.motivo}
        print(json.dumps({
            "real": [d(c) for c in veri],
            "stopped": [d(c) for c in fermi],
            "rejected": [d(c) for c in scartati],
            "pwm": [{"key": p.chiave, "chip": p.chip, "value": p.valore,
                     "mode": p.modo} for p in pwm],
        }, indent=2, ensure_ascii=False))
        sys.exit(0)

    def riga(c):
        dec = TIPI[c.tipo]["decimali"]
        v = c.valore()
        v = ("%%.%df" % dec) % v if v is not None else "-"
        return "   %-22s %-13s %10s %-4s %s" % (
            c.chiave, c.etichetta(ut), v, c.unita,
            "varies" if c.cambia else "")

    print("REAL (%d)" % len(veri))
    for c in veri:
        print(riga(c))
    sospetti = [c for c in veri if c.motivo]
    if sospetti:
        print("\n   ! do not drive a fan curve from these:")
        for c in sospetti:
            print("     %-22s %-13s %s" % (c.chiave, c.etichetta(ut), c.motivo))
    if fermi:
        print("\nFANS READING ZERO (%d) - stopped, or nothing connected" % len(fermi))
        for c in fermi:
            print(riga(c))
    print("\nPWM OUTPUTS (%d)" % len(pwm))
    for p in pwm:
        # ⚠️ -1 lo scrive la nouveau del Fujitsu: l'uscita esiste nel sysfs ma il
        # driver non la lascia comandare. Vale come "non toccabile", non come
        # modo sconosciuto: chi sceglie l'uscita da pilotare non deve trovarla.
        modo = {0: "always full", 1: "manual", 2: "chip controlled",
                -1: "NOT CONTROLLABLE", None: "unknown"}.get(p.modo, "chip controlled")
        print("   %-22s value=%-5s mode=%s (%s)" % (p.chiave, p.valore, p.modo, modo))
    print("\nHIDDEN (%d) - declared by the chip, not actually readable" % len(scartati))
    for c in scartati:
        print("   %-22s %-13s %s" % (c.chiave, c.etichetta_driver or "-", c.motivo))
