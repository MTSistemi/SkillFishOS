#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #77, the window: the CU grid stops greying out the first three pairs,
and gains a way to keep a mapping at boot.

Runs ON the build VM, inside ~/sfx-src, after patch-cu-4.py.

    python3 patch-cu-5.py [--prova]

The panel used to build itself around a floor of three pairs: the first three
buttons were disabled so they could not even be clicked, the count started at
24, and every mask was OR-ed with 0x07 on its way in and on its way out. None
of that was true, and together it made a defective CU in that range impossible
to switch off from the interface.

⚠️ THE MINIMUM COMES FROM THE DAEMON, not from a number written here. It is one
pair per row, and the grid enforces it by refusing the click that would empty a
row rather than by disabling anything: a user who wants to know why gets told.
"""
import io
import os
import sys

PROVA = "--prova" in sys.argv
T = os.path.expanduser("~/sfx-src/apps/control-center/sfcc/pagine/tuner.py")

CAMBI = []


def cambia(vecchio, nuovo, etichetta):
    CAMBI.append((vecchio, nuovo, etichetta))


# ------------------------------------------------- what the panel starts from
cambia('''        self.cu_floor = int(cu.get("floor", 7))
        self.cu_ordine = ["0.0", "0.1", "1.0", "1.1"]
        righe = cu.get("rows") or {k: 7 for k in self.cu_ordine}
        self.cu_righe = {k: int(righe.get(k, 7)) | self.cu_floor for k in self.cu_ordine}
        e = QLabel(L("Verde acceso, rosso spento, grigio sempre acceso (lo tiene il driver). Ogni casella e' una coppia di CU.",
                     "Green on, red off, grey always on (the driver keeps it). Every cell is a pair of CUs."))
''', '''        # One pair per row, and the daemon says so rather than this file
        # guessing. There used to be a floor of three here, greyed out and
        # OR-ed into everything, and it was not real.
        self.cu_min = int(cu.get("min_wgp", 1)) or 1
        self.cu_ordine = ["0.0", "0.1", "1.0", "1.1"]
        righe = cu.get("rows") or {k: 31 for k in self.cu_ordine}
        self.cu_righe = {k: int(righe.get(k, 31)) or self.cu_min for k in self.cu_ordine}
        e = QLabel(L("Verde acceso, rosso spento. Ogni casella e' una coppia di CU. Almeno una per riga deve restare accesa.",
                     "Green on, red off. Every cell is a pair of CUs. At least one per row has to stay on."))
''', "niente pavimento nella costruzione")

cambia('''                b.setChecked(bool(self.cu_righe[rk] & (1 << wgp)))
                b.setEnabled(not bool(self.cu_floor & (1 << wgp)))
''', '''                b.setChecked(bool(self.cu_righe[rk] & (1 << wgp)))
''', "tutte le caselle si possono cliccare")

cambia('''        self.cu_n.setRange(24, 40)
''', '''        self.cu_n.setRange(len(self.cu_ordine) * 2, 40)
''', "il numero puo' scendere fino al minimo vero")

# ------------------------------------------------------ keeping it at boot
cambia('''        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.clicked.connect(self._applica_cu)
        r.addWidget(b)
        v.addLayout(r)
        self._cu_colora()
        return w
''', '''        b = QPushButton(L("Applica", "Apply"))
        b.setObjectName("primario")
        b.clicked.connect(self._applica_cu)
        r.addWidget(b)
        v.addLayout(r)
        r = QHBoxLayout()
        self.cu_al_boot = QCheckBox(L("Mantieni all'avvio", "Keep at boot"))
        self.cu_al_boot.setToolTip(L(
            "La scheda riparte con questa mappatura invece che con tutte le CU accese. Applica prima, poi spunta.",
            "The board comes back with this mapping instead of every CU on. Apply first, then tick."))
        self.cu_al_boot.setChecked(bool(cu.get("keep_boot")))
        self.cu_al_boot.clicked.connect(self._cu_boot_switch)
        r.addWidget(self.cu_al_boot)
        r.addWidget(Aiuto(L(
            "Senza la spunta la scheda accende tutte le CU a ogni avvio, che e' quello che serve quasi sempre. "
            "Con la spunta riparte con le coppie scelte qui: serve quando una coppia e' guasta e va lasciata spenta.",
            "Unticked, the board turns every CU on at each boot, which is what almost everyone wants. Ticked, it "
            "comes back with the pairs chosen here: that is what you need when a pair is faulty and has to stay off."),
            L("Mantieni all'avvio", "Keep at boot")))
        r.addStretch(1)
        v.addLayout(r)
        self._cu_colora()
        return w

    def _cu_motivo(self, r):
        """Why a CU change did not go through, in words the user can act on."""
        return {
            "riga-vuota": L("Ogni riga deve avere almeno una coppia accesa.",
                            "Every row needs at least one pair on."),
            "maschere-storte": L("Le quattro righe non sono valide.",
                                 "The four rows are not valid."),
            "non-applicata": L("Applica la scelta prima di tenerla all'avvio.",
                               "Apply the selection before keeping it at boot."),
        }.get(r.get("motivo")) or r.get("err") or "?"

    def _cu_boot_switch(self, on):
        r = self.demone.cmd(cmd="cu-keep-boot", on=bool(on),
                            rows=[self.cu_righe[rk] for rk in self.cu_ordine]) or {}
        if not r.get("ok"):
            self.toast(self._cu_motivo(r), 6)
            self.cu_al_boot.blockSignals(True)
            self.cu_al_boot.setChecked(not on)
            self.cu_al_boot.blockSignals(False)
            return
        self.toast(L("La scheda ripartira' con questa mappatura", "The board will come back with this mapping")
                   if on else L("Al prossimo avvio tornano tutte accese", "Every CU comes back on at the next boot"), 5)
''', "la casella mantieni all'avvio")

# ------------------------------------------------------------- the grid logic
cambia('''    def _cu_toggle(self, rk, wgp, on):
        m = self.cu_righe.get(rk, 7)
        m = (m | (1 << wgp)) if on else (m & ~(1 << wgp))
        self.cu_righe[rk] = m | self.cu_floor
        self._cu_colora()

    def _cu_conta(self):
        return sum(bin(self.cu_righe.get(rk, 7) | self.cu_floor).count("1") * 2 for rk in self.cu_ordine)

    def _cu_colora(self):
        for (rk, wgp), b in self.cu_celle.items():
            fisso = bool(self.cu_floor & (1 << wgp))
            acceso = bool(self.cu_righe.get(rk, 7) & (1 << wgp))
            b.setStyleSheet(self.CU_GRIGIO if fisso else (self.CU_VERDE if acceso else self.CU_ROSSO))
''', '''    def _cu_toggle(self, rk, wgp, on):
        m = self.cu_righe.get(rk, 31)
        nuova = (m | (1 << wgp)) if on else (m & ~(1 << wgp))
        if nuova == 0:
            # the last pair of a row: refused, and said out loud. Disabling the
            # button instead is what the old floor did, and it left the user
            # with no idea why the cell would not move.
            self.cu_celle[(rk, wgp)].blockSignals(True)
            self.cu_celle[(rk, wgp)].setChecked(True)
            self.cu_celle[(rk, wgp)].blockSignals(False)
            self.et_cu.setText(L("Almeno una coppia per riga", "At least one pair per row"))
            return
        self.cu_righe[rk] = nuova
        self._cu_colora()

    def _cu_conta(self):
        return sum(bin(self.cu_righe.get(rk, 31)).count("1") * 2 for rk in self.cu_ordine)

    def _cu_colora(self):
        for (rk, wgp), b in self.cu_celle.items():
            acceso = bool(self.cu_righe.get(rk, 31) & (1 << wgp))
            b.setStyleSheet(self.CU_VERDE if acceso else self.CU_ROSSO)
''', "la griglia senza pavimento, con il minimo detto a parole")

cambia('''    def _cu_da_numero(self, n):
        """n CUs = 24 fixed + pairs: fill WGP3 down the rows, then WGP4."""
        coppie = max(0, (n - 24) // 2)
        for rk in self.cu_ordine:
            self.cu_righe[rk] = self.cu_floor
        for wgp in range(5):
            if self.cu_floor & (1 << wgp):
                continue
            for rk in self.cu_ordine:
                if coppie <= 0:
                    break
                self.cu_righe[rk] |= (1 << wgp)
                coppie -= 1
''', '''    def _cu_da_numero(self, n):
        """n CUs into pairs: one per row first, then a column at a time."""
        coppie = max(len(self.cu_ordine), n // 2)
        for rk in self.cu_ordine:
            self.cu_righe[rk] = 1 << 0
        coppie -= len(self.cu_ordine)
        for wgp in range(1, 5):
            for rk in self.cu_ordine:
                if coppie <= 0:
                    break
                self.cu_righe[rk] |= (1 << wgp)
                coppie -= 1
''', "il numero si distribuisce senza pavimento")

cambia('''    def _applica_cu(self):
        r = self.demone.cmd(cmd="cu-apply", rows=[self.cu_righe.get(rk, 7) | self.cu_floor for rk in self.cu_ordine])
        self.toast(L("CU applicate: %s/40", "CUs applied: %s/40") % r.get("active", "?") if r.get("ok") else r.get("err", "?"), 6)
''', '''    def _applica_cu(self):
        r = self.demone.cmd(cmd="cu-apply",
                            rows=[self.cu_righe.get(rk, 31) for rk in self.cu_ordine]) or {}
        if not r.get("ok"):
            self.toast(self._cu_motivo(r), 6)
            return
        self.toast(L("CU applicate: %s/40", "CUs applied: %s/40") % r.get("active", "?"), 6)
        # a mapping kept for boot and then changed is no longer what was kept
        if self.cu_al_boot.isChecked():
            self._cu_boot_switch(True)
''', "Applica dice perche' non e' andata, e riallinea il boot")

# -------------------------------------------------------------- the CU test
cambia('''        b.setToolTip(L("Accende una coppia alla volta sotto vkpeak e guarda se la GPU fa errori. Due o tre minuti.",
                       "Turns on one pair at a time under vkpeak and watches for GPU errors. Two or three minutes."))
''', '''        b.setToolTip(L("Prova una coppia alla volta sotto vkpeak, tutte e cinque le posizioni, e guarda se la GPU fa errori. Cinque minuti circa.",
                       "Tries one pair at a time under vkpeak, all five positions, and watches for GPU errors. About five minutes."))
''', "il suggerimento del Test CU")

cambia('''        if QMessageBox.question(self, "Test CU", L(
                "Accende una coppia di CU extra alla volta sotto vkpeak e guarda se la GPU fa errori. Due o tre minuti. Procedere?",
                "Turns on one extra CU pair at a time under vkpeak and watches for GPU errors. Two or three minutes. Proceed?")) != QMessageBox.StandardButton.Yes:
''', '''        if QMessageBox.question(self, "Test CU", L(
                "Prova una coppia di CU alla volta sotto vkpeak, in tutte e cinque le posizioni, e guarda se la GPU fa errori. "
                "Circa cinque minuti, e alla fine rimette la scelta di adesso. Procedere?",
                "Tries one CU pair at a time under vkpeak, in all five positions, and watches for GPU errors. "
                "About five minutes, and it puts the current selection back at the end. Proceed?")) != QMessageBox.StandardButton.Yes:
''', "la domanda del Test CU")

testo = io.open(T, encoding="utf-8").read()
esito = 0
for vecchio, nuovo, etichetta in CAMBI:
    n = testo.count(vecchio)
    stato = "ok" if n == 1 else "NON TROVATO" if n == 0 else "%d VOLTE" % n
    print("[%-11s] %s" % (stato, etichetta))
    if n != 1:
        esito = 1
        continue
    testo = testo.replace(vecchio, nuovo)

if esito:
    sys.exit("\nqualche ancoraggio non combacia: non ho scritto niente")

vivo = [r for r in testo.splitlines()
        if "cu_floor" in r and not r.lstrip().startswith("#")]
if vivo:
    for r in vivo:
        print("  resta vivo: %s" % r.strip())
    sys.exit("cu_floor e' ancora nel codice: non ho scritto niente")

if PROVA:
    sys.exit("\n--prova: non ho scritto niente")

io.open(T, "w", encoding="utf-8", newline="\n").write(testo)
import py_compile
py_compile.compile(T, cfile="/tmp/sfx-cu5.pyc", doraise=True)
os.remove("/tmp/sfx-cu5.pyc")
print("scritto e compila: %s" % T)
