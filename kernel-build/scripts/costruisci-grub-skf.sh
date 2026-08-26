#!/bin/bash
# Costruisce il GRUB di SkillFishOS: uno solo, che si porta dentro la propria
# configurazione, e che poi firmiamo con la nostra chiave.
#
# ⚠️ PERCHE' NON BASTA `grub-mkimage -p /boot/grub`. Provato: il grub costruito
# cosi' arriva al prompt con $prefix e $root VUOTI. Su EFI, GRUB deve dedurre da
# quale dispositivo e' stato caricato per trasformare «/boot/grub» in
# «(qualcosa)/boot/grub», e da un'immagine avviata via El Torito quella deduzione
# non gli riesce. Risultato: non cerca la configurazione da nessuna parte e
# l'utente si ritrova a `grub>`.
#
# ⚠️ E NON BASTA NEMMENO IL GRUB DI DEBIAN. Il suo, firmato e monolitico, ha
# scritto dentro «/EFI/debian», mentre eggs la sua configurazione la scrive in
# «(efi.img)/boot/grub/grub.cfg». Due percorsi che non si incontrano.
#
# LA SOLUZIONE: si INCORPORA la configurazione dentro grubx64.efi, con
# `grub-mkimage -c`. Quella configurazione parte sempre, qualunque cosa GRUB
# creda di essere e da qualunque supporto arrivi. Da li' si cerca il volume e si
# passa la mano al menu vero della ISO.
#
# ⚠️ SI CERCA PER ETICHETTA, non per UUID. eggs scrive un marcatore
# /.disk/id/<uuid> che cambia a ogni build: legarci l'immagine di GRUB
# vorrebbe dire ricostruirla e rifirmarla ogni volta. L'etichetta del volume e'
# «SkillFishOS» e non cambia, quindi lo stesso binario firmato vale per tutte le
# immagini. C'e' comunque un ripiego che cerca un file che esiste solo sulle
# nostre.
set -euo pipefail
export LC_ALL=C

W=/root/sb-prova
D=/root/.skillfishos-secureboot
OUT="$W/grub-skf.efi"
mkdir -p "$W"

# ⚠️ QUESTA CONFIGURAZIONE GIRA PRIMA CHE GRUB CARICHI IL SUO INTERPRETE.
# Prima di `normal`, GRUB conosce solo i comandi di base: niente `if`, niente
# `fi`, nemmeno i commenti con #. Provato: usciva una cascata di
#     Unknown command `#'.   Unknown command `if'.   Unknown command `fi'.
# e il messaggio di errore veniva stampato sempre, anche quando il supporto era
# stato trovato. Qui dentro quindi si scrivono SOLO comandi, uno per riga.
#
# I due `search` si possono mettere in fila senza guardia: `--set=root` cambia
# root solo quando trova, quindi il secondo e' semplicemente un ripiego.
# `normal` alla fine legge $prefix/grub.cfg, cioe' il menu vero della ISO.
cat > "$W/grub-dentro.cfg" <<'CFG'
search --no-floppy --set=root --label SkillFishOS
search --no-floppy --set=root --file /live/filesystem.squashfs
set prefix=($root)/boot/grub
normal
CFG

# --- SBAT: senza, lo shim rifiuta anche una firma valida --------------------
# ⚠️ TROVATO PROVANDO, e non era per niente ovvio. Il nostro grub, firmato con la
# nostra chiave GIA' REGISTRATA nel firmware della macchina di prova, veniva
# comunque respinto con
#     Verification failed: (0x1A) Security Violation
# La firma era buona: mancava la sezione .sbat. Lo shim moderno non guarda solo
# chi ha firmato, guarda anche i metadati di revoca, e un binario che non li ha
# non passa. Il grub monolitico di Debian ce l'ha: ecco perche' quello, firmato
# con la stessa chiave, funzionava e il nostro no.
#
# Si parte dai metadati di Debian — siamo il loro grub ricompilato — e si
# aggiunge la riga nostra. E' quello che fa ogni distribuzione, e serve a poter
# revocare le NOSTRE versioni senza toccare le loro.
echo "=== metadati SBAT ==="
objcopy -O binary --only-section=.sbat \
    /usr/lib/grub/x86_64-efi/monolithic/grubx64.efi "$W/sbat-debian.csv" 2>/dev/null
tr -d '\000' < "$W/sbat-debian.csv" | grep -E '^[a-z]' > "$W/sbat.csv"
printf 'grub.skillfishos,1,SkillFishOS,grub2,2.14-3,https://skillfishos.com\n' >> "$W/sbat.csv"
sed 's/^/   /' "$W/sbat.csv"

echo
echo "=== costruisco ==="
# ⚠️ NON tutti e 293 i moduli. Con tutti dentro l'immagine viene 15 MB, e la
# partizione EFI ne ha 16 in tutto, dove devono starci anche lo shim (1 MB) e
# MokManager (0,9 MB). Qui c'e' quello che serve davvero: trovare il supporto,
# disegnare il menu col nostro tema, avviare il kernel.
MODULI="search search_fs_file search_fs_uuid search_label \
part_gpt part_msdos fat iso9660 ext2 udf \
normal configfile echo test sleep true loadenv \
linux chain halt reboot \
all_video video video_fb efi_gop \
gfxterm gfxterm_background gfxmenu font png jpeg tga bitmap bitmap_scale \
terminal terminfo gettext regexp minicmd ls cat help \
gzio xzio boot bufio datetime disk extcmd file fshelp keystatus \
priority_queue trig read serial"
# ⚠️ grub-mkimage -c, NON grub-mkstandalone. Provati tutti e due:
# grub-mkstandalone si porta dentro TUTTI i moduli qualunque cosa gli si dica
# con --modules, e l'immagine viene 13-15 MB. Nella partizione EFI da 16 MB, con
# shim e MokManager, non ci sta. `grub-mkimage -c` incorpora la configurazione
# nello stesso modo ma mette solo i moduli elencati.
grub-mkimage -O x86_64-efi -o "$OUT" -c "$W/grub-dentro.cfg" -p /boot/grub \
    --sbat "$W/sbat.csv" \
    $MODULI 2>&1 | head -4 | sed 's/^/   /'
ls -sh "$OUT" | sed 's/^/   /'

echo
echo "=== la configurazione e' davvero dentro? ==="
if strings -a "$OUT" | grep -q 'label SkillFishOS'; then
    echo "   sì, si legge dentro il binario"
else
    echo "   ⚠️ NO: non la trovo, non ha senso firmarlo" >&2
    exit 1
fi
strings -a "$OUT" | grep -E '^/boot/grub$' | sort -u | sed 's/^/   prefisso: /'
if objdump -h "$OUT" 2>/dev/null | grep -q '\.sbat'; then
    echo "   sezione .sbat: c'e'"
else
    echo "   ⚠️ sezione .sbat ASSENTE: lo shim lo rifiuterebbe anche firmato" >&2
    exit 1
fi

echo
echo "=== firmo ==="
sbattach --remove "$OUT" >/dev/null 2>&1 || true
sbsign --key "$D/SkillFishOS-SB.key" --cert "$D/SkillFishOS-SB.crt" \
       --output "$OUT.firmato" "$OUT" >/dev/null
mv -f "$OUT.firmato" "$OUT"
sbverify --cert "$D/SkillFishOS-SB.crt" "$OUT" 2>&1 | sed 's/^/   /'
