# -*- coding: utf-8 -*-
"""Kernel: the ones installed, which is running, which GRUB picks next."""
import glob
import os

from PyQt6.QtWidgets import (QButtonGroup, QFrame, QHBoxLayout, QLabel, QMessageBox, QRadioButton,
                             QVBoxLayout)

from .. import stile
from ..comune import L, leggi_testo, sh
from ..demone import in_sfondo
from ..finestra import PaginaBase
from ..stile import Scheda, intestazione


def grub_default():
    for line in leggi_testo("/etc/default/grub").splitlines():
        if line.startswith("GRUB_DEFAULT="):
            return line.split("=", 1)[1].strip().strip('"')
    return ""


def sapore(kv):
    if kv.endswith("-x64") or kv.endswith("-generic"):
        return L("x64 · qualunque PC", "x64 · any PC")
    if "skillfishos" in kv:
        return L("BC-250 · znver2", "BC-250 · znver2")
    return L("kernel esterno", "external kernel")


def dimensione_mb(kv):
    tot = 0
    for p in ("/boot/vmlinuz-%s" % kv, "/boot/initrd.img-%s" % kv, "/boot/System.map-%s" % kv, "/boot/config-%s" % kv):
        try:
            tot += os.path.getsize(p)
        except OSError:
            # this piece is missing on this kernel: just skip it
            pass
    md = "/usr/lib/modules/%s" % kv
    if not os.path.isdir(md):
        md = "/lib/modules/%s" % kv
    rc, out, _ = sh("du -sb %s 2>/dev/null" % md, 30)
    try:
        tot += int(out.split()[0])
    except (ValueError, IndexError):
        # du failed or gave no output: modules size stays out of the total
        pass
    return tot / 1e6


def installati():
    ks = set()
    for p in glob.glob("/boot/vmlinuz-*"):
        kv = os.path.basename(p).replace("vmlinuz-", "")
        if not kv.endswith((".dpkg-tmp", ".old")):
            ks.add(kv)
    return sorted(ks, reverse=True)


class Pagina(PaginaBase):
    def __init__(self, finestra):
        super().__init__(finestra)
        self.intervallo_ms = 0

    def costruisci(self):
        v = self.corpo_scorrevole()
        v.addWidget(intestazione("Kernel", L(
            "Scegli il kernel di avvio o togli quelli che non servono. Quello in esecuzione non si "
            "puo' togliere.", "Choose the boot kernel or remove the ones you no longer need. The "
            "running one cannot be removed.")))
        self.scheda = Scheda(L("Kernel installati", "Installed kernels"))
        self.lista = QVBoxLayout()
        self.lista.setSpacing(6)
        self.scheda.aggiungi(self.lista)
        self.et = QLabel("")
        self.et.setObjectName("quieto")
        self.et.setWordWrap(True)
        self.scheda.aggiungi(self.et)
        self.b_pred, self.b_una, self.b_togli, self.b_riavvia = self.scheda.bottoni(
            (L("Predefinito", "Default"), self._predefinito, True),
            (L("Una volta", "Once"), self._una_volta, False),
            (L("Disinstalla", "Uninstall"), self._disinstalla, False),
            (L("Riavvia", "Reboot"), self._riavvia, False))
        self.b_togli.setObjectName("pericolo")
        v.addWidget(self.scheda)
        v.addStretch(1)
        self.gruppo = QButtonGroup(self)
        self.ricarica()

    def ricarica(self):
        for b in list(self.gruppo.buttons()):
            self.gruppo.removeButton(b)
        while self.lista.count():
            it = self.lista.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        self.run = os.uname().release
        self.default_raw = grub_default()
        self.kernels = installati()
        for kv in self.kernels:
            riga = QFrame()
            riga.setObjectName("riga")
            rl = QHBoxLayout(riga)
            rl.setContentsMargins(6, 4, 6, 6)
            rb = QRadioButton()
            rb.setProperty("kver", kv)
            self.gruppo.addButton(rb)
            col = QVBoxLayout()
            col.setSpacing(0)
            tag = []
            if kv == self.run:
                tag.append("● " + L("in esecuzione", "running"))
            if kv and kv in self.default_raw:
                tag.append("★ " + L("predefinito", "default"))
            nm = QLabel(kv + (("   " + "  ·  ".join(tag)) if tag else ""))
            nm.setStyleSheet("font-weight:700;color:%s;" % (stile.VERDE if kv == self.run else stile.TESTO))
            meta = QLabel("%s   ·   ~%.0f MB" % (sapore(kv), dimensione_mb(kv)))
            meta.setObjectName("quieto")
            col.addWidget(nm)
            col.addWidget(meta)
            rl.addWidget(rb)
            rl.addLayout(col, 1)
            self.lista.addWidget(riga)
            if kv == self.run:
                rb.setChecked(True)
        n = len(self.kernels)
        self.et.setText(L("%d kernel installati.", "%d installed kernels.") % n)
        self.b_togli.setEnabled(n > 1)

    def _scelto(self):
        b = self.gruppo.checkedButton()
        return b.property("kver") if b else None

    def _predefinito(self):
        kv = self._scelto()
        if not kv:
            return
        r = self.demone.cmd(cmd="kernel", azione="default", kv=kv)
        self.et.setText(L("Predefinito: %s. Vale dal prossimo riavvio.", "Default: %s. From the next reboot.") % kv if r.get("ok") else (r.get("err") or r.get("out") or "?"))
        self.ricarica()

    def _una_volta(self):
        kv = self._scelto()
        if not kv:
            return
        r = self.demone.cmd(cmd="kernel", azione="once", kv=kv)
        if r.get("ok"):
            if QMessageBox.question(self, "Kernel", L("%s partira' al prossimo riavvio, una volta sola. Riavviare ora?", "%s will boot next time, once. Reboot now?") % kv) == QMessageBox.StandardButton.Yes:
                self.demone.cmd(cmd="riavvia")
        else:
            self.et.setText(r.get("err") or r.get("out") or "?")

    def _disinstalla(self):
        kv = self._scelto()
        if not kv:
            return
        if kv == self.run:
            QMessageBox.warning(self, "Kernel", L("Non puoi togliere il kernel in esecuzione.", "You cannot remove the running kernel."))
            return
        if len(self.kernels) <= 1:
            return
        testo = L("Tolgo COMPLETAMENTE il kernel %s (~%.0f MB)?", "COMPLETELY remove kernel %s (~%.0f MB)?") % (kv, dimensione_mb(kv))
        if kv in self.default_raw:
            testo += "\n" + L("E' il predefinito: il predefinito tornera' a quello in esecuzione.", "It is the default: the default moves to the running one.")
        if QMessageBox.question(self, "Kernel", testo, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        self.b_togli.setEnabled(False)
        self.et.setText(L("Disinstallo…", "Uninstalling…"))
        in_sfondo(lambda: self.demone.cmd(cmd="kernel", azione="uninstall", kv=kv), self._tolto, self)

    def _tolto(self, r):
        self.et.setText(L("Fatto.", "Done.") if r.get("ok") else (r.get("err") or r.get("out") or L("non riuscito", "failed")))
        self.ricarica()

    def _riavvia(self):
        if QMessageBox.question(self, "Kernel", L("Riavviare ora?", "Reboot now?")) == QMessageBox.StandardButton.Yes:
            self.demone.cmd(cmd="riavvia")
