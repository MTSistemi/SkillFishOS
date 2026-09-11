# -*- coding: utf-8 -*-
"""Snapshots: the pictures of the system, and the btrfs maintenance schedule.

Reading the list still goes through skillfish-snapshots-read under pkexec
without a password (its own policy allows that); every change goes through
our helper, so one password covers the whole window. The restore work itself
is skillfish-rollback, unchanged.
"""
import subprocess
from datetime import datetime, timezone

from PyQt6.QtCore import QDateTime, QLocale, QTime
from PyQt6.QtWidgets import (QButtonGroup, QComboBox, QFrame, QHBoxLayout, QInputDialog, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QRadioButton, QTabWidget,
                             QTimeEdit, QVBoxLayout, QWidget)

from .. import stile
from ..comune import L, Aiuto
from ..demone import in_sfondo
from ..finestra import PaginaBase
from ..stile import Scheda, intestazione

LEGGI = "/usr/local/bin/skillfish-snapshots-read"


def bytes_leggibili(n):
    try:
        n = float(n)
    except (TypeError, ValueError):
        return "?"
    for u in ("B", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024 or u == "TiB":
            return ("%.0f %s" % (n, u)) if u in ("B", "KiB") else ("%.1f %s" % (n, u))
        n /= 1024.0
    return "?"


class Snapshot:
    def __init__(self, num, data_utc, tipo, pre, descrizione):
        self.num, self.tipo, self.pre, self.descrizione = num, tipo, pre, descrizione
        self.quando = None
        try:
            self.quando = datetime.strptime((data_utc or "").strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).astimezone()
        except ValueError:
            pass

    def data_scritta(self):
        if self.quando is None:
            return L("data sconosciuta", "unknown date")
        return QLocale().toString(QDateTime.fromSecsSinceEpoch(int(self.quando.timestamp())), QLocale.FormatType.ShortFormat)

    def quanto_fa(self):
        if self.quando is None:
            return ""
        s = (datetime.now(timezone.utc) - self.quando.astimezone(timezone.utc)).total_seconds()
        if s < 90:
            return L("adesso", "just now")
        if s < 5400:
            n = int(s // 60)
            return L("un minuto fa", "one minute ago") if n == 1 else L("%d minuti fa", "%d minutes ago") % n
        if s < 172800:
            n = int(s // 3600)
            return L("un'ora fa", "one hour ago") if n == 1 else L("%d ore fa", "%d hours ago") % n
        n = int(s // 86400)
        return L("un giorno fa", "one day ago") if n == 1 else L("%d giorni fa", "%d days ago") % n

    def in_parole(self):
        d = (self.descrizione or "").strip()
        if d in ("apt", "zypp(apt)"):
            return L("prima di installare o aggiornare programmi", "before installing or updating software") if self.tipo == "pre" \
                else L("dopo aver installato o aggiornato programmi", "after installing or updating software")
        if d == "timeline":
            return L("snapshot periodico", "scheduled snapshot")
        if d in ("manual snapshot", ""):
            return L("fatto da te", "made by you")
        b = d.lower()
        if b == "boot":
            return L("all'avvio del sistema", "at system startup")
        if "clean install" in b or ("first" in b and "boot" in b):
            return L("appena installato il sistema", "right after installing the system")
        return d


def leggi_tutto():
    try:
        p = subprocess.run(["pkexec", LEGGI], capture_output=True, text=True, timeout=60)
        rc, out = p.returncode, (p.stdout or "").strip()
    except Exception:
        rc, out = 1, ""
    vuoto = ([], None, [], {}, None, None, [])
    if rc != 0:
        err = L("operazione annullata", "operation cancelled") if rc in (126, 127) else L("Non riesco a leggere gli snapshot.", "cannot read the snapshots")
        return vuoto + (err,)
    snap, spazio, daparte, manut, disco, verifica, bersagli = [], None, [], {}, None, None, []
    for riga in out.splitlines():
        p = riga.split("\t")
        p += [""] * (8 - len(p))
        if p[0] == "SNAP" and p[1]:
            snap.append(Snapshot(p[1], p[2], p[3], p[4], p[5]))
        elif p[0] == "SPAZIO" and p[1]:
            spazio = (p[1], p[2])
        elif p[0] == "DAPARTE" and p[1]:
            daparte.append(p[1])
        elif p[0] == "BERSAGLIO" and p[1]:
            bersagli.append({"dev": p[1], "nome": p[4] or "SkillFishOS", "snap": [], "daparte": [], "spazio": None})
        elif p[0] == "SNAPB" and p[1]:
            for b in bersagli:
                if b["dev"] == p[1]:
                    b["snap"].append(Snapshot(p[2], p[3], p[4], p[5], p[6]))
        elif p[0] == "SPAZIOB" and p[1]:
            for b in bersagli:
                if b["dev"] == p[1]:
                    b["spazio"] = (p[2], p[3])
        elif p[0] == "DAPARTEB" and p[1]:
            for b in bersagli:
                if b["dev"] == p[1]:
                    b["daparte"].append(p[2])
        elif p[0] == "LAVORO" and p[1]:
            manut[p[1]] = {"periodo": p[2], "ora": p[3], "attivo": p[4], "prossima": p[5], "ultima": p[6], "esito": p[7]}
        elif p[0] == "DISCO" and p[1]:
            disco = (p[1], p[2], p[3])
        elif p[0] == "VERIFICA":
            verifica = (p[1], p[2], p[3], p[4])
    snap.sort(key=lambda s: int(s.num), reverse=True)
    for b in bersagli:
        b["snap"].sort(key=lambda s: int(s.num), reverse=True)
    return snap, spazio, daparte, manut, disco, verifica, bersagli, None


def spiega(testo):
    t = (testo or "").strip()
    if not t.startswith("ERR:"):
        return t
    etichetta, _, resto = t[4:].partition(" ")
    return {
        "zero": L("Lo snapshot 0 e' il sistema in funzione, non e' uno snapshot vero.", "Snapshot 0 is the running system, not a snapshot."),
        "non-numero": L("Non e' un numero di snapshot.", "That is not a snapshot number."),
        "inesistente": L("Quello snapshot non esiste piu'.", "That snapshot no longer exists."),
        "in-uso": L("Non si puo': il sistema in funzione e' partito da questo snapshot.", "Not possible: the running system booted from this snapshot."),
        "vuoto": L("Non hai scelto niente da cancellare.", "You have not chosen anything to delete."),
        "cancellazione": L("Non sono riuscito a cancellare uno degli snapshot.", "One of the snapshots could not be deleted."),
    }.get(etichetta, resto or t)


class Pagina(PaginaBase):
    LAVORI = (
        ("verifica", ("Verifica dei dati", "Data check"), ("Rilegge tutto il disco e controlla che niente si sia guastato in silenzio. Ripara da sola le copie doppie quando puo'.", "Reads the whole disk back and checks nothing has quietly gone bad. Repairs from the duplicate copies where it can.")),
        ("spazio", ("Recupero dello spazio", "Space reclaim"), ("Ricompatta le zone del disco rimaste quasi vuote. Su btrfs lo spazio libero puo' risultare occupato finche' non si fa questo.", "Repacks the areas of the disk left nearly empty. On btrfs free space can look taken until this is done.")),
        ("trim", ("Pulizia dell'SSD", "SSD cleanup"), ("Dice all'SSD quali blocchi non servono piu', cosi' resta veloce nel tempo.", "Tells the SSD which blocks are no longer needed, so it stays fast over time.")),
        ("deframmenta", ("Deframmentazione", "Defragmentation"), ("Sconsigliata qui: riscrive i file e i dati condivisi con gli snapshot smettono di esserlo. Lo spazio occupato puo' crescere di parecchio.", "Not advised here: it rewrites files and data shared with the snapshots stops being shared. Used space can grow a lot.")),
    )
    PERIODI = (("mai", ("mai", "never")), ("giorno", ("ogni giorno", "every day")), ("settimana", ("ogni settimana", "every week")), ("mese", ("ogni mese", "every month")))
    TIENE = 3

    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 0
        self.snap, self.daparte, self.spazio, self.manut, self.disco, self.verifica = [], [], None, {}, None, None
        self.bersagli, self.bersaglio = [], None

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione(L("Snapshot", "Snapshots"), L(
            "Fotografie del sistema: se qualcosa si rompe, si torna a prima. I tuoi file non vengono "
            "toccati.", "Pictures of the system: if something breaks, go back to before. Your files "
            "are not touched.")))
        self.riga_bersaglio = QFrame()
        rb = QHBoxLayout(self.riga_bersaglio)
        rb.addWidget(QLabel(L("Sistema da riparare:", "System to repair:")))
        self.scelta_bersaglio = QComboBox()
        self.scelta_bersaglio.currentIndexChanged.connect(self._cambia_bersaglio)
        rb.addWidget(self.scelta_bersaglio, 1)
        self.riga_bersaglio.hide()
        v.addWidget(self.riga_bersaglio)
        self.avviso = Scheda(L("Sistema messo da parte", "System set aside"))
        self.avviso_testo = QLabel("")
        self.avviso_testo.setWordWrap(True)
        self.avviso.aggiungi(self.avviso_testo)
        self.avviso.bottoni((L("Torna indietro", "Go back"), self._annulla, False), (L("Butta il vecchio", "Discard the old one"), self._pulisci, False))
        self.avviso.hide()
        v.addWidget(self.avviso)

        self.schede = QTabWidget()
        v.addWidget(self.schede, 1)
        foto = QWidget()
        fv = QVBoxLayout(foto)
        self.lista = QVBoxLayout()
        self.lista.setSpacing(4)
        fv.addLayout(self.lista)
        fv.addStretch(1)
        self.stato = QLabel("")
        self.stato.setWordWrap(True)
        self.stato.setObjectName("quieto")
        fv.addWidget(self.stato)
        b = QHBoxLayout()
        self.bcancella = QPushButton(L("Cancella", "Delete"))
        self.bcancella.setObjectName("pericolo")
        self.bcancella.clicked.connect(self._cancella)
        self.bpulizia = QPushButton(L("Fai pulizia", "Clean up"))
        self.bpulizia.clicked.connect(self._pulizia)
        self.bcrea = QPushButton(L("Fai uno snapshot adesso", "Take a snapshot now"))
        self.bcrea.clicked.connect(self._crea)
        self.bripristina = QPushButton(L("Torna a questo", "Go back to this one"))
        self.bripristina.setObjectName("primario")
        self.bripristina.clicked.connect(self._ripristina)
        b.addWidget(self.bcancella)
        b.addWidget(self.bpulizia)
        b.addStretch(1)
        b.addWidget(self.bcrea)
        b.addWidget(self.bripristina)
        fv.addLayout(b)
        self.schede.addTab(foto, L("Snapshot", "Snapshots"))
        self.schede.addTab(self._pagina_manutenzione(), L("Manutenzione", "Maintenance"))
        self.gruppo = QButtonGroup(self)
        self.ricarica()

    def _pagina_manutenzione(self):
        p = QWidget()
        v = QVBoxLayout(p)
        v.setSpacing(10)
        self.m_testa = QLabel("")
        self.m_testa.setObjectName("quieto")
        v.addWidget(self.m_testa)
        self.m_righe = {}
        for chiave, titolo, spiega_ in self.LAVORI:
            s = Scheda(L(*titolo), L(*spiega_))
            r = QHBoxLayout()
            quando = QComboBox()
            for valore, et in self.PERIODI:
                quando.addItem(L(*et), valore)
            ora = QTimeEdit()
            ora.setDisplayFormat("HH:mm")
            ora.setTime(QTime(3, 0))
            e = QLabel(L("alle", "at"))
            r.addWidget(quando)
            r.addWidget(e)
            r.addWidget(ora)
            r.addStretch(1)
            s.aggiungi(r)
            st = QLabel("")
            st.setWordWrap(True)
            st.setObjectName("quieto")
            s.aggiungi(st)

            def collega(c=quando, o=ora, e=e):
                def f():
                    o.setEnabled(c.currentData() != "mai")
                    e.setEnabled(c.currentData() != "mai")
                return f
            f = collega()
            quando.currentIndexChanged.connect(f)
            self.m_righe[chiave] = {"quando": quando, "ora": ora, "stato": st, "attiva": f}
            v.addWidget(s)
        self.m_stato = QLabel("")
        self.m_stato.setWordWrap(True)
        self.m_stato.setObjectName("quieto")
        v.addWidget(self.m_stato)
        r = QHBoxLayout()
        r.addStretch(1)
        b = QPushButton(L("Salva la programmazione", "Save the schedule"))
        b.setObjectName("primario")
        b.clicked.connect(self._salva_manutenzione)
        r.addWidget(b)
        v.addLayout(r)
        v.addStretch(1)
        return p

    # ---- list ---------------------------------------------------------------------
    def ricarica(self):
        for b in list(self.gruppo.buttons()):
            self.gruppo.removeButton(b)
        while self.lista.count():
            it = self.lista.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        (self.snap, spazio, self.daparte, self.manut, self.disco, self.verifica, self.bersagli, errore) = leggi_tutto()
        if self.bersagli:
            vecchio = self.bersaglio["dev"] if self.bersaglio else None
            self.scelta_bersaglio.blockSignals(True)
            self.scelta_bersaglio.clear()
            i = 0
            for n, b in enumerate(self.bersagli):
                self.scelta_bersaglio.addItem("%s  —  %s" % (b["nome"], b["dev"]), b["dev"])
                if b["dev"] == vecchio:
                    i = n
            self.scelta_bersaglio.setCurrentIndex(i)
            self.scelta_bersaglio.blockSignals(False)
            self.bersaglio = self.bersagli[i]
            self.riga_bersaglio.show()
            self.snap, self.daparte = self.bersaglio["snap"], self.bersaglio["daparte"]
            spazio = self.bersaglio["spazio"] or spazio
        else:
            self.bersaglio = None
            self.riga_bersaglio.hide()
        if errore:
            self.stato.setText(errore)
            self.snap = []
            return
        self.spazio = spazio
        if self.daparte:
            self.avviso_testo.setText(L("C'e' un sistema messo da parte da un ripristino: %s. Finche' resta, puoi tornare com'eri prima.",
                                        "There is a system set aside by a restore: %s. While it is there, you can go back to how you were.") % self.daparte[0])
            self.avviso.show()
        else:
            self.avviso.hide()
        if not self.snap:
            testo = (L("Hai appena ripristinato. Gli snapshot sono nel sistema che parte al prossimo riavvio.",
                       "You have just restored. The snapshots are in the system that boots on the next restart.") if self.daparte
                     else L("Non c'e' ancora nessuno snapshot. Il sistema ne fa uno da solo prima di ogni installazione o aggiornamento.",
                            "There are no snapshots yet. The system takes one by itself before every install or update."))
            e = QLabel(testo)
            e.setWordWrap(True)
            e.setObjectName("quieto")
            self.lista.addWidget(e)
        for i, s in enumerate(self.snap):
            riga = QFrame()
            riga.setObjectName("riga")
            rv = QHBoxLayout(riga)
            rv.setContentsMargins(4, 4, 4, 6)
            rb = QRadioButton()
            rb.setProperty("num", s.num)
            self.gruppo.addButton(rb)
            rb.toggled.connect(self._aggiorna_bottoni)
            if i == 0:
                rb.setChecked(True)
            rv.addWidget(rb)
            col = QVBoxLayout()
            col.setSpacing(0)
            nm = QLabel("%s   %s" % (s.data_scritta(), s.quanto_fa()))
            nm.setStyleSheet("font-weight:700;")
            meta = QLabel(s.in_parole())
            meta.setObjectName("quieto")
            col.addWidget(nm)
            col.addWidget(meta)
            rv.addLayout(col, 1)
            self.lista.addWidget(riga)
        n = len(self.snap)
        t = L("uno snapshot.", "one snapshot.") if n == 1 else L("%d snapshot.", "%d snapshots.") % n
        if self.spazio:
            t += "   " + L("Spazio libero: %s su %s", "Free space: %s of %s") % (bytes_leggibili(self.spazio[0]), bytes_leggibili(self.spazio[1]))
        self.stato.setText(t)
        self._aggiorna_bottoni()
        self._mostra_manutenzione()

    def _mostra_manutenzione(self):
        for chiave, r in self.m_righe.items():
            d = self.manut.get(chiave)
            if d is None:
                r["stato"].setText(L("stato sconosciuto", "state unknown"))
                continue
            i = r["quando"].findData(d["periodo"])
            r["quando"].setCurrentIndex(i if i >= 0 else 0)
            hh, mm = (d["ora"] or "03:00").split(":")[:2] if d["ora"] else ("00", "00")
            r["ora"].setTime(QTime(int(hh), int(mm)))
            r["attiva"]()
            pezzi = []
            if d["prossima"]:
                pezzi.append(L("prossima volta: %s", "next time: %s") % d["prossima"])
            elif d["periodo"] == "mai":
                pezzi.append(L("non programmata", "not scheduled"))
            if d["ultima"]:
                pezzi.append(L("ultima: %s", "last: %s") % d["ultima"])
            if chiave == "spazio" and self.disco:
                try:
                    sprecato = int(self.disco[1]) - int(self.disco[2])
                except (TypeError, ValueError):
                    sprecato = 0
                if sprecato > 1 << 30:
                    pezzi.insert(0, L("da recuperare: %s", "to reclaim: %s") % bytes_leggibili(sprecato))
            if chiave == "verifica" and self.verifica:
                errori = self.verifica[2]
                pezzi.insert(0, L("nessun errore", "no errors") if errori == "no errors found" else (errori or ""))
            r["stato"].setText("   ·   ".join(x for x in pezzi if x))
        if self.disco:
            self.m_testa.setText(L("Spazio libero: %s.", "Free space: %s.") % bytes_leggibili(self.disco[0]))

    def _salva_manutenzione(self):
        da_fare = []
        for chiave, r in self.m_righe.items():
            periodo = r["quando"].currentData()
            ora = r["ora"].time().toString("HH:mm")
            d = self.manut.get(chiave) or {}
            if periodo == d.get("periodo") and (periodo == "mai" or ora == (d.get("ora") or "")):
                continue
            da_fare.append((chiave, periodo, ora))
        if not da_fare:
            self.m_stato.setText(L("Non hai cambiato niente.", "Nothing has changed."))
            return
        for chiave, periodo, _ in da_fare:
            if chiave == "deframmenta" and periodo != "mai":
                if QMessageBox.question(self, L("Accendere la deframmentazione?", "Turn defragmentation on?"), L(
                        "Con gli snapshot questa operazione fa CRESCERE lo spazio occupato, anche di decine di gigabyte in una notte. La accendo lo stesso?",
                        "With snapshots this makes used space GROW, even by tens of gigabytes in a night. Turn it on anyway?")) != QMessageBox.StandardButton.Yes:
                    return
        self.m_stato.setText(L("Sto programmando…", "Setting the schedule…"))
        errore = None
        for chiave, periodo, ora in da_fare:
            r = self.demone.cmd(cmd="manutenzione", args=["imposta", chiave, periodo, ora])
            if not r.get("ok"):
                errore = spiega(r.get("err") or r.get("out"))
                break
        self.ricarica()
        self.m_stato.setText(errore or L("Programmazione salvata.", "Schedule saved."))

    def _scelto(self):
        for b in self.gruppo.buttons():
            if b.isChecked():
                return next((s for s in self.snap if s.num == b.property("num")), None)
        return None

    def _aggiorna_bottoni(self):
        c = self._scelto() is not None
        altrove = self.bersaglio is not None
        self.bcancella.setEnabled(c and not altrove)
        self.bripristina.setEnabled(c)
        self.bcrea.setEnabled(not altrove)

    def _cambia_bersaglio(self, i):
        if 0 <= i < len(self.bersagli):
            self.bersaglio = self.bersagli[i]
            self.ricarica()

    def _esegui(self, args, attesa=600):
        if self.bersaglio:
            args = ["--disco", self.bersaglio["dev"]] + list(args)
        r = self.demone.cmd(cmd="snapshot", args=args, attesa=attesa)
        return r.get("ok"), r.get("out", ""), r.get("err", "")

    def _esito(self, ok, bene, out, err):
        self.ricarica()
        self.stato.setText(bene if ok else (spiega(err or out) or L("operazione annullata", "operation cancelled")))
        self.stato.setObjectName("bene" if ok else "male")
        self.stato.style().polish(self.stato)

    def _crea(self):
        testo, ok = QInputDialog.getText(self, L("Fai uno snapshot", "Take a snapshot"), L("A cosa ti serve?", "What is it for?"),
                                         QLineEdit.EchoMode.Normal, L("prima di una prova", "before trying something"))
        if not ok:
            return
        self.stato.setText(L("Sto facendo lo snapshot…", "Taking the snapshot…"))
        ok, out, err = self._esegui(["crea", testo.strip()], 300)
        self._esito(ok, L("Fatto.", "Done."), out, err)

    def _cancella(self):
        s = self._scelto()
        if s is None:
            return
        if QMessageBox.question(self, L("Cancellare?", "Delete?"), L("Cancello lo snapshot del %s (%s)? Il sistema di adesso non cambia.",
                                                                    "Delete the snapshot from %s (%s)? Your current system does not change.") % (s.data_scritta(), s.in_parole())) != QMessageBox.StandardButton.Yes:
            return
        ok, out, err = self._esegui(["cancella", s.num], 300)
        self._esito(ok, L("Cancellato.", "Deleted."), out, err)

    def _pulizia(self):
        rc = subprocess.run(["findmnt", "-no", "SOURCE", "/"], capture_output=True, text=True).stdout
        tieni, butta = [], []
        for i, s in enumerate(self.snap):
            d = (s.descrizione or "").lower()
            protetta = i < self.TIENE or "clean install" in d or ("first" in d and "boot" in d) or ("/.snapshots/%s/snapshot" % s.num) in rc
            (tieni if protetta else butta).append(s)
        if not butta:
            self.stato.setText(L("Non c'e' niente da buttare.", "Nothing to clean up."))
            return
        elenco = "\n".join("   • %s   %s" % (s.data_scritta(), s.in_parole()) for s in butta)
        if QMessageBox.question(self, L("Fare pulizia?", "Clean up?"), L("Butto %d snapshot e ne tengo %d.\n\nVANNO VIA:\n%s", "I will remove %d snapshots and keep %d.\n\nGOING:\n%s") % (len(butta), len(tieni), elenco),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        if QMessageBox.warning(self, L("Sicuro?", "Are you sure?"), L("Cancello per sempre %d snapshot. Non si torna indietro.", "I will permanently delete %d snapshots. There is no undo.") % len(butta),
                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        self.stato.setText(L("Sto facendo pulizia…", "Cleaning up…"))
        ok, out, err = self._esegui(["cancella-molti", ",".join(s.num for s in butta)], 900)
        self._esito(ok, L("Buttati %d snapshot.", "Removed %d snapshots.") % len(butta), out, err)

    def _ripristina(self):
        s = self._scelto()
        if s is None:
            return
        if QMessageBox.question(self, L("Tornare indietro?", "Go back?"), L(
                "Riporto il sistema a com'era il %s (%s).\n\n• I tuoi file NON vengono toccati.\n• Il sistema di adesso resta da parte e puoi tornarci.\n• Ha effetto al prossimo riavvio.\n\nProcedo?",
                "I will put the system back to how it was on %s (%s).\n\n• Your files are NOT touched.\n• The current system stays aside and you can return to it.\n• It takes effect on the next restart.\n\nGo ahead?") % (s.data_scritta(), s.in_parole())) != QMessageBox.StandardButton.Yes:
            return
        self.stato.setText(L("Sto tornando indietro…", "Going back…"))
        ok, out, err = self._esegui(["ripristina", s.num], 900)
        if self.bersaglio:
            self._esito(ok, L("Fatto. Togli la chiavetta e avvia da disco.", "Done. Remove the live media and start from the disk."), out, err)
            return
        self._esito(ok, L("Fatto. Al prossimo riavvio parte il sistema di quella data.", "Done. On the next restart the system from that date will boot."), out, err)
        if ok and QMessageBox.question(self, L("Riavviare adesso?", "Restart now?"), L("Al ritorno troverai il sistema di quella data.", "When it comes back you will have the system from that date.")) == QMessageBox.StandardButton.Yes:
            self.demone.cmd(cmd="riavvia")

    def _annulla(self):
        if QMessageBox.question(self, L("Tornare com'eri?", "Back to how you were?"), L("Rimetto il sistema com'era prima del ripristino. Ha effetto al riavvio.", "I will put back the system as it was before the restore. It takes effect on restart.")) != QMessageBox.StandardButton.Yes:
            return
        ok, out, err = self._esegui(["annulla"], 600)
        self._esito(ok, L("Fatto. Riavvia per tornare al sistema di prima.", "Done. Restart to go back to the previous system."), out, err)

    def _pulisci(self):
        if QMessageBox.question(self, L("Buttare il vecchio sistema?", "Discard the old system?"), L("Cancello per sempre il sistema messo da parte. Lo spazio torna libero.", "I will permanently delete the system set aside. The space is freed.")) != QMessageBox.StandardButton.Yes:
            return
        ok, out, err = self._esegui(["pulisci"], 600)
        self._esito(ok, L("Spazio liberato.", "Space freed."), out, err)
