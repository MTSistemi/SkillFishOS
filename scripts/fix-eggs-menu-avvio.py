# -*- coding: utf-8 -*-
u"""Il menu di avvio della ISO: in inglese, e con le voci che fanno qualcosa.

Aprendo la 26.06.5 sono venute fuori tre cose sulla primissima schermata che
vede chiunque, prima di qualunque scelta di lingua:

1. IL TITOLO ERA IN ITALIANO - "SkillFishOS - gioca e impara Linux" - e accanto
   c'era una scritta in spagnolo, "Linea de Comando de GRUB", rimasta dal tema
   originale. La regola del progetto e' che il testo di base e il ripiego sono
   sempre in inglese: qui e' il caso piu' evidente di tutti, perche' e' prima
   ancora che l'utente possa scegliere.
   ⚠️ L'attribuzione a Quirinux / Charlie Martinez nei commenti RESTA: il tema
   deriva dal suo lavoro, e toglierla per fare pulizia sarebbe scorretto.

2. "SAFE MODE" E "TEXT MODE" ERANO COPIE ESATTE della voce normale: stessa riga
   di avvio, byte per byte. Chi ha lo schermo nero sceglie Safe Mode, ottiene lo
   stesso schermo nero e conclude che la ISO e' rotta. Sull'edizione Generic,
   che finisce su hardware sconosciuto, e' la voce che serve di piu'.

3. LA LIVE NON GIRAVA CON I PARAMETRI DEL SISTEMA CHE SI INSTALLA. Chi prova la
   live prima di installare provava una macchina diversa da quella che si sarebbe
   portato a casa: niente mitigations=off, niente split_lock_detect=off.
   ⚠️ ttm.pages_limit NON lo aggiungo alla live: e' calcolato sui 7,5 GB della
   BC-250, e la stessa riga la legge anche la Generic, che puo' finire su un PC
   con 4 GB. Un tetto GTT piu' grande della RAM non e' un regalo.

E una quarta, arrivata dalla issue #53 (20/08/2026): IL MENU NON DICEVA PER
QUALE MACCHINA E' FATTA L'IMMAGINE. Le due edizioni si chiamavano tutte e due
"SkillFishOS Live/Installation", identiche. Chi scarica la BC-250 e la mette in
un PC normale vede il menu, sceglie, e finisce su uno schermo nero: il kernel e'
compilato per quella scheda e non parte altrove. Da fuori sembra una ISO rotta.
Il menu e' l'ULTIMO punto in cui si puo' ancora dirglielo - dopo non c'e' piu'
niente da leggere - e costa una riga di testo. Vedi la sezione 5.

Questi file appartengono al pacchetto penguins-eggs: un suo aggiornamento li
riscrive. Per questo la correzione sta in uno script che si rilancia, come gia'
si fa per branding.js e per la configurazione di Calamares.

  uso:  fix-eggs-menu-avvio.py [bc250|generic]

L'edizione e' facoltativa: senza, si fanno solo le correzioni 1-4 e il menu
resta generico. build-iso.sh la ricava dal nome del file .iso, che e' l'unico
posto dove l'edizione e' gia' scritta.
"""
import glob, io, os, re, sys

BASE = "/usr/lib/penguins-eggs/addons"
fatti = []

EDIZIONE = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()

# Per ogni edizione: la coda della voce di menu, e il titolo in cima allo
# schermo. Corte apposta: la scritta sta dentro a una cornice di larghezza fissa
# e quella di prima ("SkillFishOS - play and learn Linux", 34 caratteri) e' il
# tetto pratico che sappiamo entrarci.
# ⚠️ Trattino ASCII, non lineetta lunga: la stessa stringa la disegna anche
# isolinux, che in avvio BIOS non e' in UTF-8.
EDIZIONI = {
    "bc250":   ("for AMD BC-250 boards only", "SkillFishOS - AMD BC-250 edition"),
    "generic": ("for standard PCs",           "SkillFishOS - Generic PC edition"),
}
if EDIZIONE and EDIZIONE not in EDIZIONI:
    sys.exit("edizione sconosciuta: %s (attese: %s)"
             % (EDIZIONE, ", ".join(sorted(EDIZIONI))))


def salva(p, t):
    if not os.path.exists(p + ".skfbak"):
        io.open(p + ".skfbak", "w", encoding="utf-8", newline="\n").write(
            io.open(p, encoding="utf-8", errors="replace").read())
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)


# --- 1. il tema: titolo e etichette ----------------------------------------
for p in glob.glob(BASE + "/*/theme/livecd/*grub.theme.cfg"):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    o = t
    t = t.replace('title-text: "SkillFishOS - gioca e impara Linux"',
                  'title-text: "SkillFishOS - play and learn Linux"')
    t = t.replace('text = "Linea de Comando de GRUB"', 'text = "GRUB command line"')
    t = t.replace('text = "Linea de comando de GRUB"', 'text = "GRUB command line"')
    if t != o:
        salva(p, t)
        fatti.append("tema: " + os.path.basename(p))

for p in glob.glob(BASE + "/*/theme/livecd/*isolinux.theme.cfg"):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    o = t
    t = t.replace("gioca e impara Linux", "play and learn Linux")
    if t != o:
        salva(p, t)
        fatti.append("tema: " + os.path.basename(p))


# --- 2. Safe Mode e Text Mode che fanno davvero qualcosa --------------------
# Safe: niente impostazione della modalita' video da parte del kernel, niente
#       splash, messaggi visibili. E' la voce per "non vedo niente".
# Text: si ferma a multi-user, senza interfaccia grafica. E' la voce per
#       "la grafica si pianta" e per chi vuole lavorare da riga di comando.
SAFE = "nomodeset nosplash noquiet"
TEXT = "systemd.unit=multi-user.target nosplash noquiet"

for p in glob.glob(BASE + "/*/theme/livecd/*grub.main.cfg"):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    o = t
    pezzi = t.split('menuentry "{{{fullname}}} ')
    for i, pz in enumerate(pezzi):
        if pz.startswith("Safe Mode"):
            pezzi[i] = pz.replace("{{{kernel_parameters}}} quiet splash loglevel=2",
                                  "{{{kernel_parameters}}} " + SAFE, 1)
        elif pz.startswith("Text Mode"):
            pezzi[i] = pz.replace("{{{kernel_parameters}}} quiet splash loglevel=2",
                                  "{{{kernel_parameters}}} " + TEXT, 1)
    t = 'menuentry "{{{fullname}}} '.join(pezzi)
    if t != o:
        salva(p, t)
        fatti.append("menu UEFI: " + os.path.basename(p))

for p in glob.glob(BASE + "/*/theme/livecd/*isolinux.main.cfg"):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    o = t
    # ⚠️ isolinux non passava nemmeno quiet splash: la stessa ISO avviata in BIOS
    #    mostrava tutti i messaggi del kernel, avviata in UEFI mostrava lo splash.
    t = t.replace("label Live\n  menu label {{{fullname}}} Live/Installation Mode  \n"
                  "  say \"Booting {{{fullname}}} GNU/Linux (kernel {{{kernel}}})\"\n"
                  "  linux {{{vmlinuz}}}\n"
                  "  append initrd={{{initrdImg}}} {{{kernel_parameters}}}",
                  "label Live\n  menu label {{{fullname}}} Live/Installation Mode  \n"
                  "  say \"Booting {{{fullname}}} GNU/Linux (kernel {{{kernel}}})\"\n"
                  "  linux {{{vmlinuz}}}\n"
                  "  append initrd={{{initrdImg}}} {{{kernel_parameters}}} quiet splash loglevel=2")
    t = t.replace("label Safe\n  menu label {{{fullname}}} Safe Mode\n"
                  "  say \"Booting {{{fullname}}} GNU/Linux (kernel {{{kernel}}})\"\n"
                  "  linux {{{vmlinuz}}} \n"
                  "  append initrd={{{initrdImg}}} {{{kernel_parameters}}} ",
                  "label Safe\n  menu label {{{fullname}}} Safe Mode\n"
                  "  say \"Booting {{{fullname}}} GNU/Linux in safe mode\"\n"
                  "  linux {{{vmlinuz}}} \n"
                  "  append initrd={{{initrdImg}}} {{{kernel_parameters}}} " + SAFE + " ")
    t = t.replace("label Text\n  menu label {{{fullname}}} Text Mode\n"
                  "  say \"Booting {{{fullname}}} GNU/Linux (kernel {{{kernel}}})\"\n"
                  "  linux {{{vmlinuz}}} \n"
                  "  append initrd={{{initrdImg}}} {{{kernel_parameters}}} ",
                  "label Text\n  menu label {{{fullname}}} Text Mode\n"
                  "  say \"Booting {{{fullname}}} GNU/Linux to a text console\"\n"
                  "  linux {{{vmlinuz}}} \n"
                  "  append initrd={{{initrdImg}}} {{{kernel_parameters}}} " + TEXT + " ")
    if t != o:
        salva(p, t)
        fatti.append("menu BIOS: " + os.path.basename(p))


# --- 3. la live gira come il sistema installato ----------------------------
D = "/usr/lib/penguins-eggs/dist/classes/diversions.js"
t = io.open(D, encoding="utf-8", errors="replace").read()
VECCHIO = "kp += `boot=live components locales=${process.env.LANG} cow_spacesize=2G`;"
NUOVO = ("kp += `boot=live components locales=${process.env.LANG} cow_spacesize=2G "
         "mitigations=off split_lock_detect=off`;")
if VECCHIO in t:
    salva(D, t.replace(VECCHIO, NUOVO, 1))
    fatti.append("riga di avvio della live allineata al sistema installato")
elif NUOVO.split("cow_spacesize=2G ")[1][:14] in t:
    fatti.append("riga di avvio della live: gia' allineata")


# --- 4. compressione btrfs anche sugli SSD ---------------------------------
for p in ("/etc/calamares/modules/fstab.conf",
          "/etc/penguins-eggs.d/distros/forky/calamares/modules/fstab.yaml"):
    if os.path.exists(p):
        t = io.open(p, encoding="utf-8").read()
        if "btrfs: discard,compress=lzo" in t:
            salva(p, t.replace("btrfs: discard,compress=lzo",
                               "btrfs: discard=async,compress=zstd:1"))
            fatti.append("fstab: sugli SSD btrfs usa zstd e discard asincrono")


# --- 5. il menu dice per quale macchina e' fatta l'immagine ----------------
# Deve stare DOPO la 2: quella cerca le voci di isolinux per intero, compresa
# la riga dell'etichetta, e se la trovasse gia' allungata non le riconoscerebbe.
#
# ⚠️ Le sostituzioni sono scritte in modo da poter girare piu' volte, e con
# edizioni DIVERSE: l'espressione regolare mangia anche una coda gia' aggiunta
# prima di rimetterne una. Senza, la seconda build della giornata avrebbe
# prodotto "Live/Installation for AMD BC-250 boards only for standard PCs" -
# oppure, peggio, avrebbe lasciato alla Generic la scritta della BC-250 perche'
# "c'e' gia' una coda, non tocco niente". I due modelli restano nel pacchetto
# fra una build e l'altra, quindi il caso non e' teorico: e' quello normale.
if EDIZIONE:
    coda, titolo = EDIZIONI[EDIZIONE]

    # Una riga di registro per gruppo, non una per file: i modelli sono otto
    # (quattro nomi per due cartelle di addon) e otto righe uguali nel log della
    # build non dicono niente piu' di una.
    def per_tutti(schema, regola, cosa):
        n_file = 0
        for p in glob.glob(BASE + schema):
            t = io.open(p, encoding="utf-8", errors="replace").read()
            n = regola(t)
            if n != t:
                salva(p, n)
                n_file += 1
        if n_file:
            fatti.append("%s (%d modelli)" % (cosa, n_file))

    # GRUB (avvio UEFI): menuentry "{{{fullname}}} Live/Installation"
    R_GRUB = re.compile(r'(menuentry "\{\{\{fullname\}\}\} Live/Installation)'
                        r'(?: - [^"\n]*)?(")')
    per_tutti("/*/theme/livecd/*grub.main.cfg",
              lambda t: R_GRUB.sub(lambda m: m.group(1) + " - " + coda + m.group(2), t),
              "menu UEFI: dice «%s»" % coda)

    # isolinux (avvio BIOS): menu label {{{fullname}}} Live/Installation Mode
    R_ISO = re.compile(r'(menu label \{\{\{fullname\}\}\} Live/Installation Mode)'
                       r'(?: - [^\n]*?)?(\s*\n)')
    per_tutti("/*/theme/livecd/*isolinux.main.cfg",
              lambda t: R_ISO.sub(lambda m: m.group(1) + " - " + coda + m.group(2), t),
              "menu BIOS: dice «%s»" % coda)

    # il titolo in cima allo schermo: e' la scritta piu' grande che c'e'
    R_TIT = re.compile(r'title-text:\s*"[^"]*"')
    per_tutti("/*/theme/livecd/*grub.theme.cfg",
              lambda t: R_TIT.sub('title-text: "%s"' % titolo, t),
              "titolo: «%s»" % titolo)

if not fatti:
    print("   niente da fare, e' gia' tutto a posto")
for f in fatti:
    print("   " + f)


# --- controprova ------------------------------------------------------------
print("\n   controprova:")
brutte = 0
for p in glob.glob(BASE + "/*/theme/livecd/*.cfg"):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    for frase in ("gioca e impara", "Linea de Comando"):
        if frase in t:
            print("      ANCORA: %s in %s" % (frase, os.path.basename(p)))
            brutte += 1
for p in glob.glob(BASE + "/*/theme/livecd/grub.main.cfg"):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    righe = [r for r in t.splitlines() if r.strip().startswith("linux ")]
    if len(set(righe)) < len(righe):
        print("      ANCORA: in %s ci sono voci di menu identiche" % os.path.basename(p))
        brutte += 1

# Che la coda ci sia, che sia UNA sola, e che sia quella di QUESTA edizione:
# la coda sbagliata e' peggio di nessuna coda, perche' manda via la persona
# giusta convincendola di avere l'immagine sbagliata.
if EDIZIONE:
    coda, titolo = EDIZIONI[EDIZIONE]
    altre = [c for e, (c, _) in EDIZIONI.items() if e != EDIZIONE]
    for p in (glob.glob(BASE + "/*/theme/livecd/*grub.main.cfg")
              + glob.glob(BASE + "/*/theme/livecd/*isolinux.main.cfg")):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        if t.count(coda) != 1:
            print("      ANCORA: %s nomina l'edizione %d volte invece di 1"
                  % (os.path.basename(p), t.count(coda)))
            brutte += 1
        for a in altre:
            if a in t:
                print("      ANCORA: %s porta la scritta dell'altra edizione (%s)"
                      % (os.path.basename(p), a))
                brutte += 1
    print("      la voce di avvio dice: Live/Installation - %s" % coda)
else:
    print("      nessuna edizione indicata: il menu resta generico")
print("      testo in altre lingue o voci doppie rimaste: %d" % brutte)
sys.exit(1 if brutte else 0)
