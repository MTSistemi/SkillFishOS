#!/usr/bin/env python3
# Rende affidabile l'avvio dopo l'installazione da Calamares.
#
# DUE PROBLEMI DISTINTI, non uno solo (verificati in VM il 10/08/2026)
# =====================================================================
#
# A) #12 - btrfs: GRUB non riesce a leggere il kernel
# ---------------------------------------------------
# Sintomo: il menu GRUB compare, poi "fine prematura del file
# /@/boot/vmlinuz-...". Quindi NON e' un problema di bootloader installato
# male: GRUB ha trovato grub.cfg e ha risolto correttamente il sottovolume.
#
# Causa misurata: i file del kernel scritti da `unpackfs` hanno una mappa
# degli extent che NON copre la dimensione dichiarata. Mancano gli ultimi
# 512 byte, e filefrag mostra l'ultimo extent senza il flag `eof`. GRUB
# legge l'albero degli extent e si ferma li': ha ragione a lamentarsi, il
# file su disco e' davvero incompleto. Il kernel Linux lo legge lo stesso,
# quindi il problema si vede solo all'avvio.
#
# Prova nella stessa installazione: il kernel copiato con `cp` dal modulo
# boot_deploy risulta sano (`last,eof`), quelli usciti da unpackfs no.
# Su un sistema sano ogni modo di scrivere (cp, dd, cat, unsquashfs) con
# qualunque opzione di mount (defaults, zstd, zlib) produce file corretti.
#
# Correzione: riscrivere kernel e initrd dopo l'installazione, con
# --reflink=never (senza, btrfs riusa gli stessi extent rotti e non ripara
# niente - errore in cui sono cascato al primo tentativo). Cosi' /boot resta
# DENTRO btrfs: gli snapshot continuano a comprenderlo e il rollback resta
# possibile, che era il requisito.
#
# Il lavoro lo fa /usr/local/bin/skillfish-fix-boot-extents, spedito da
# skillfish-base. NON si puo' mettere il ciclo di shell direttamente nello
# YAML: il modulo shellprocess di Calamares espande i $... come proprie
# variabili e l'installazione muore con "variabili mancanti: f,f,f,f,f".
#
# B) #20 - il fallback EFI removibile e' incompleto
# --------------------------------------------------
# Il firmware della BC-250 avvia molto spesso dal percorso EFI *removibile*
# \EFI\BOOT\BOOTX64.EFI invece che dalla voce NVRAM della distribuzione.
# Con `installEFIFallback: true` Calamares ci copia shim + grubx64, ma NON
# lo stub `grub.cfg` che sta accanto al binario nella directory della
# distribuzione. Il GRUB avviato da li' ha quindi un prefix che non risolve
# nessuna configurazione e cade in `grub rescue>`.
#
# Digitando `exit` il controllo torna al firmware, che prova la voce
# successiva (quella buona) e il sistema parte: e' esattamente il sintomo
# descritto nella #20. La causa non c'entra col filesystem, ed e' il motivo
# per cui colpisce sia btrfs sia ext4.
#
# LA CORREZIONE
# -------------
# Dopo il modulo `bootloader`, nel chroot del sistema appena installato,
# rieseguiamo grub-install due volte: una per la voce NVRAM normale e una
# con `--removable`, che scrive un BOOTX64.EFI **autonomo** (prefix corretto
# e stub di configurazione al posto giusto). Poi un update-grub finale.
#
# Su btrfs grub-install viene eseguito con il layout di mount reale, quindi
# grub-probe calcola da solo il prefix comprensivo di sottovolume (/@/boot/grub).
#
# Nota su Secure Boot: `--removable` scrive grub direttamente, non shim. Sulla
# BC-250 il Secure Boot non e' attivo. Se un giorno lo fosse, la voce NVRAM
# firmata resta comunque installata dal primo grub-install: il fallback non
# sostituisce nulla, si aggiunge.
#
# Da eseguire DOPO che eggs ha generato /etc/calamares e PRIMA di produrre la ISO.
import os
import re
import shutil

# ATTENZIONE: `eggs produce` RIGENERA /etc/calamares dai propri template e
# butta via qualunque modifica fatta a mano al file generato. Verificato il
# 10/08/2026 ispezionando la ISO prodotta: dentro c'era la versione di eggs.
# Quindi la correzione va scritta nel TEMPLATE, che e' quello che finisce
# davvero nell'immagine. Il file generato lo aggiorniamo comunque, cosi' la
# configurazione viva e quella della ISO restano coerenti.
MODDIR = "/etc/calamares/modules"

# Il template GIUSTO non e' quello in /usr/lib (che e' solo la copia di
# riferimento del pacchetto). eggs legge da:
#     /etc/penguins-eggs.d/distros/<distroUniqueId>/calamares/modules
# come si vede in dist/classes/incubation/installer.js. Sulla nostra immagine
# distroUniqueId e' "forky". Cercarlo con una glob invece di scriverlo fisso:
# cambiera' quando cambiera' la base Debian.
import glob as _glob
_c = _glob.glob("/etc/penguins-eggs.d/distros/*/calamares/modules")
TPLDIRS = _c if _c else []

# --- 1. il passo post-bootloader ------------------------------------------
RECONF = os.path.join(MODDIR, "shellprocess@boot_reconfigure.conf")
RECONF_BODY = """---
message: Final reconfiguration of the kernel and bootloader...
dontChroot: false
timeout: 900
script:
    - chmod 644 /boot/vmlinuz-`uname -r`
    - chown 0:0 /boot/vmlinuz-`uname -r`
    - INITRD=No dpkg-reconfigure -fnoninteractive linux-image-`uname -r` || true
    - test -s /boot/initrd.img-`uname -r` || update-initramfs -c -k `uname -r`
    - /usr/local/bin/skillfish-fix-boot-extents
    - >-
      grub-install --target=x86_64-efi --efi-directory=/boot/efi
      --bootloader-id=skillfishos --recheck || true
    - >-
      grub-install --target=x86_64-efi --efi-directory=/boot/efi
      --removable --recheck || true
    - update-grub || true
    - /usr/local/bin/skillfish-clean-live-autologin || true
"""

# --- 1b. partizionamento predefinito: btrfs con swap su file --------------
# Il template di eggs propone ext4 e nessuno swap. Noi vogliamo btrfs (serve
# per snapshot e rollback, che sono un pezzo dell'identita' del sistema) e lo
# swap su FILE invece che su partizione: su btrfs si ridimensiona senza
# ripartizionare, e non sporca la tabella delle partizioni.
PART_SUBS = [
    ('defaultFileSystemType:  "ext4"', 'defaultFileSystemType:  "btrfs"'),
    ("defaultFileSystemType: \"ext4\"", 'defaultFileSystemType:  "btrfs"'),
    ("initialSwapChoice: none", "initialSwapChoice: file"),
]


def btrfs_first(text):
    """Mette btrfs in cima ad availableFileSystemTypes.

    Non basta defaultFileSystemType. Verificato avviando la ISO in VM: il menu a
    tendina del filesystem mostrava **ext4** mentre l'anteprima delle partizioni
    sotto diceva Btrfs — i due leggono cose diverse. L'anteprima usa
    defaultFileSystemType, il menu preseleziona il PRIMO elemento di
    availableFileSystemTypes, che era ext4.

    Un utente che non guarda l'anteprima installa ext4 credendo di aver preso
    quello che gli proponiamo, e si perde snapshot e rollback, che sono meta'
    del motivo per cui usiamo btrfs. Con btrfs in cima all'elenco il menu e
    l'anteprima dicono la stessa cosa qualunque delle due logiche prevalga.
    """
    m = re.search(r"^availableFileSystemTypes:\s*\n((?:\s*-\s*\S+\s*\n)+)", text, re.M)
    if not m:
        return text, None
    items = re.findall(r"-\s*(\S+)", m.group(1))
    if not items or items[0] == "btrfs" or "btrfs" not in items:
        return text, items
    ordered = ["btrfs"] + [i for i in items if i != "btrfs"]
    indent = re.match(r"(\s*)-", m.group(1)).group(1)
    block = "".join("%s- %s\n" % (indent, i) for i in ordered)
    return text[:m.start(1)] + block + text[m.end(1):], ordered


# --- 1c. il menu del filesystem deve proporre per primo il predefinito -------
# Verificato avviando la ISO: il menu mostrava ext4 mentre l'anteprima delle
# partizioni sotto diceva Btrfs. I due leggono cose diverse — l'anteprima usa
# defaultFileSystemType, il menu preseleziona il PRIMO di availableFileSystemTypes.
#
# E la lista non viene dal template: la costruisce eggs a ogni produce, in
# customize-partitions.js, partendo da ['ext4'] e aggiungendo gli altri. Anche
# defaultFileSystemType lo decide lui, leggendo `df -T /`, cioe' il filesystem
# della macchina su cui si costruisce. Correggere il template non serviva a
# niente: viene sovrascritto.
#
# La patch non caccia btrfs a forza: mette in cima QUELLO che eggs ha scelto
# come predefinito, cosi' menu e anteprima concordano sempre. Se un giorno
# costruissimo da una macchina ext4, il menu proporrebbe ext4 — coerente.
#
# ATTENZIONE: e' un file del pacchetto penguins-eggs. Un aggiornamento di eggs
# lo sovrascrive, come per branding.js. Va rilanciato dopo ogni apt upgrade.
CUSTPART = "/usr/lib/penguins-eggs/dist/classes/incubation/customize/customize-partitions.js"
CUSTPART_MARK = "SkillFishOS: il predefinito per primo"
CUSTPART_PATCH = """    // %s
    if (partition.availableFileSystemTypes.includes(partition.defaultFileSystemType)) {
        partition.availableFileSystemTypes = [partition.defaultFileSystemType].concat(
            partition.availableFileSystemTypes.filter(function (f) { return f !== partition.defaultFileSystemType; }));
    }
""" % CUSTPART_MARK


def patch_eggs_fslist():
    if not os.path.exists(CUSTPART):
        print("ATTENZIONE: manca", CUSTPART)
        return False
    with open(CUSTPART, encoding="utf-8") as f:
        t = f.read()
    if CUSTPART_MARK in t:
        print("OK  : customize-partitions.js gia' corretto")
        return True
    anchor = "    fs.writeFileSync(filePartition, yaml.dump(partition), 'utf-8');"
    if anchor not in t:
        print("KO  : customize-partitions.js non ha la forma attesa, non lo tocco")
        return False
    backup(CUSTPART)
    with open(CUSTPART, "w", encoding="utf-8") as f:
        f.write(t.replace(anchor, CUSTPART_PATCH + anchor, 1))
    print("OK  : customize-partitions.js -> il predefinito va in cima al menu")
    return True



# --- 1d. la presentazione durante l'installazione, in quattro lingue ---------
# I testi erano cablati in italiano: chi installava in polacco si guardava
# cinque schermate in una lingua che magari non conosce, proprio mentre il
# sistema si presenta. Non sono immagini con il testo dentro (lo sfondo e' uno
# solo), quindi bastava tradurli: ora il QML legge Qt.locale(), che Calamares
# imposta quando l'utente sceglie la lingua nella prima pagina.
#
# QUI C'ERA L'ERRORE, ed e' costato due ISO da rifare.
#
# Copiavo la presentazione solo in /etc/calamares/branding/*/show.qml. Quella e'
# la cartella GENERATA: eggs la riscrive da capo a ogni `produce`, prendendo il
# file dai propri addon. Risultato, nell'immagine finiva la sua versione italiana
# da 4127 byte al posto della nostra multilingua da 9617 — e l'installazione in
# polacco mostrava l'interfaccia in polacco e le diapositive in italiano.
#
# Stavamo correggendo il RISULTATO invece dell'ORIGINE. Adesso si scrive in
# entrambi:
#   /usr/lib/penguins-eggs/addons/*/theme/calamares/branding/show.qml   <- origine
#   /etc/calamares/branding/*/show.qml                                  <- generato
# La seconda serve solo perche' l'installer parta subito corretto anche senza
# rigenerare; e' la prima che finisce nella ISO.
SLIDESHOW_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "theme", "calamares", "show.qml")
SLIDESHOW_ADDONS = "/usr/lib/penguins-eggs/addons/*/theme/calamares/branding/show.qml"


def install_slideshow():
    src = os.path.normpath(SLIDESHOW_SRC)
    if not os.path.exists(src):
        print("ATTENZIONE: manca", src)
        return False

    sorgenti = 0
    for dst in _glob.glob(SLIDESHOW_ADDONS):
        backup(dst)
        shutil.copy(src, dst)
        sorgenti += 1

    generati = 0
    for d in _glob.glob("/etc/calamares/branding/*"):
        if not os.path.isdir(d):
            continue
        dst = os.path.join(d, "show.qml")
        backup(dst)
        shutil.copy(src, dst)
        generati += 1

    print("OK  : presentazione multilingua in %d sorgenti di eggs e %d branding generati"
          % (sorgenti, generati))
    if sorgenti == 0:
        print("ATTENZIONE: nessun addon di eggs trovato in %s" % SLIDESHOW_ADDONS)
        print("            senza quello, la produce la sovrascrivera' di nuovo")
    return sorgenti > 0


# --- 2. layout dei sottovolumi sicuro per GRUB ----------------------------
# Nessun @boot: /boot resta dentro @, cosi' GRUB non deve attraversare un
# secondo sottovolume per trovare la propria configurazione (era l'errore
# "@boot subvolume not found" della #12).
WANT_SUBVOLS = """btrfsSubvolumes:
    - mountPoint: /
      subvolume: /@
    - mountPoint: /home
      subvolume: /@home
    - mountPoint: /var/cache
      subvolume: /@cache
    - mountPoint: /var/log
      subvolume: /@log
"""


def backup(path):
    if os.path.exists(path) and not os.path.exists(path + ".skfbak"):
        shutil.copy(path, path + ".skfbak")


def main():
    patch_eggs_fslist()
    install_slideshow()
    if not os.path.isdir(MODDIR):
        raise SystemExit("FATAL: %s non esiste — eggs ha gia' generato la config?" % MODDIR)

    # 1) i template di eggs: sono questi che finiscono nella ISO
    if not TPLDIRS:
        print("ATTENZIONE: nessun template sotto /etc/penguins-eggs.d/distros/*/calamares/modules")
        print("            senza il template la correzione NON entrera' nella ISO")
    for d in TPLDIRS:
        tpl = os.path.join(d, "shellprocess@boot_reconfigure.yaml")
        backup(tpl)
        with open(tpl, "w", encoding="utf-8") as f:
            f.write(RECONF_BODY)
        print("OK  : scritto il TEMPLATE", tpl)

    # 2) e la configurazione viva, per coerenza
    backup(RECONF)
    with open(RECONF, "w", encoding="utf-8") as f:
        f.write(RECONF_BODY)
    print("OK  : scritto", RECONF)

    # partizionamento: sia nel template sia nella config viva
    for d in TPLDIRS + [MODDIR]:
        for name in ("partition.yaml", "partition.conf"):
            f = os.path.join(d, name)
            if not os.path.exists(f):
                continue
            with open(f, encoding="utf-8") as fh:
                t = fh.read()
            orig = t
            for a, b in PART_SUBS:
                if a in t:
                    t = t.replace(a, b)
            t, fslist = btrfs_first(t)
            if fslist:
                print("      elenco filesystem:", " ".join(fslist))
            if t != orig:
                backup(f)
                with open(f, "w", encoding="utf-8") as fh:
                    fh.write(t)
                print("OK  : partizionamento corretto in", f)
            fs = "btrfs" if 'defaultFileSystemType:  "btrfs"' in t or "defaultFileSystemType: btrfs" in t else "?"
            sw = "file" if "initialSwapChoice: file" in t else "?"
            print("      %s -> filesystem=%s swap=%s" % (name, fs, sw))

    mount = os.path.join(MODDIR, "mount.conf")
    if os.path.exists(mount):
        with open(mount, encoding="utf-8") as f:
            s = f.read()
        if "/@boot" in s:
            print("ATTENZIONE: mount.conf contiene un sottovolume @boot — GRUB non lo trovera'")
        if "subvolume: /@\n" in s or "subvolume: /@ " in s:
            print("OK  : mount.conf ha gia' il layout con /@")
        else:
            print("ATTENZIONE: mount.conf non ha il layout atteso, controllalo a mano:")
            print(WANT_SUBVOLS)
    else:
        print("ATTENZIONE: manca", mount)

    boot = os.path.join(MODDIR, "bootloader.conf")
    if os.path.exists(boot):
        with open(boot, encoding="utf-8") as f:
            s = f.read()
        print("info: installEFIFallback =",
              "true" if "installEFIFallback: true" in s else "NON impostato a true")

    seq = "/etc/calamares/settings.conf"
    if os.path.exists(seq):
        with open(seq, encoding="utf-8") as f:
            s = f.read()
        i_boot = s.find("- bootloader\n")
        i_reco = s.find("- shellprocess@boot_reconfigure")
        if i_boot == -1 or i_reco == -1:
            print("ATTENZIONE: non trovo i due moduli nella sequenza di settings.conf")
        elif i_reco < i_boot:
            print("ATTENZIONE: boot_reconfigure viene PRIMA di bootloader: il fix non avrebbe effetto")
        else:
            print("OK  : boot_reconfigure viene dopo bootloader nella sequenza")


def verify():
    """Ricontrolla che la correzione sia dove serve. Fidarsi non basta: la prima
    volta eggs aveva sovrascritto tutto e me ne sono accorto solo aprendo la ISO."""
    ok = True
    for d in TPLDIRS + [MODDIR]:
        for name in ("partition.yaml", "partition.conf"):
            f = os.path.join(d, name)
            if not os.path.exists(f):
                continue
            with open(f, encoding="utf-8") as fh:
                t = fh.read()
            bad = []
            if '"ext4"' in t and 'defaultFileSystemType:  "ext4"' in t:
                bad.append("filesystem ancora ext4")
            if "initialSwapChoice: none" in t:
                bad.append("swap ancora none")
            fs = re.search(r"^availableFileSystemTypes:\s*\n\s*-\s*(\S+)", t, re.M)
            if fs and fs.group(1) != "btrfs":
                bad.append("nel menu comparirebbe %s per primo" % fs.group(1))
            print(("KO  : %s -> %s" % (f, ", ".join(bad))) if bad
                  else "OK  : %s -> btrfs + swap su file" % f)
            if bad:
                ok = False

    if os.path.exists(CUSTPART):
        with open(CUSTPART, encoding="utf-8") as f:
            if CUSTPART_MARK in f.read():
                print("OK  : eggs mettera' il filesystem predefinito in cima al menu")
            else:
                print("KO  : customize-partitions.js NON corretto: il menu proporra' ext4")
                ok = False

    for d in _glob.glob("/etc/calamares/branding/*/show.qml"):
        with open(d, encoding="utf-8") as f:
            t = f.read()
        if '"pl":' in t and '"uk":' in t and "Qt.locale()" in t:
            print("OK  : %s -> presentazione in quattro lingue" % d)
        else:
            print("KO  : %s -> presentazione ancora monolingua" % d)
            ok = False

    targets = [(os.path.join(d, "shellprocess@boot_reconfigure.yaml"), "template eggs")
               for d in TPLDIRS] + [(RECONF, "config viva")]
    for path, what in targets:
        if not os.path.exists(path):
            print("KO  : manca %s (%s)" % (path, what)); ok = False; continue
        with open(path, encoding="utf-8") as f:
            t = f.read()
        # ⚠️ Qui prima si cercavano tre stringhe che c'erano comunque, quindi il
        #    controllo passava anche quando mancava la correzione che conta.
        #    Un controllo che non puo' fallire non e' un controllo.
        miss = [k for k in ("skillfish-fix-boot-extents", "--removable", "update-grub",
                            "dpkg-reconfigure -fnoninteractive linux-image-`uname -r` || true",
                            "update-initramfs -c -k") if k not in t]
        if miss:
            print("KO  : %s (%s) senza: %s" % (path, what, ", ".join(miss))); ok = False
        else:
            print("OK  : %s (%s) contiene tutte le correzioni" % (path, what))
    return ok


if __name__ == "__main__":
    main()
    print()
    raise SystemExit(0 if verify() else 1)
