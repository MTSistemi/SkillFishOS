# Chiave Secure Boot di SkillFishOS

Qui c'è solo la parte **pubblica**, ed è giusto che sia pubblica: serve a
chiunque per verificare che un kernel di SkillFishOS sia davvero nostro, e serve
all'utente per registrarla nel proprio firmware.

    SkillFishOS-SB.crt   certificato in formato PEM, per sbverify --cert
    SkillFishOS-SB.cer   lo stesso in formato DER, è quello che vuole MokManager

## La chiave privata non è qui, e non ci deve finire

Sta in `/root/.skillfishos-secureboot/SkillFishOS-SB.key` sulla macchina che
firma, con i permessi 600. Va custodita come la chiave di firma dell'archivio
apt: se si perde, chi ha registrato la nostra chiave nel firmware smette di
ricevere kernel che quel firmware accetti.

## A cosa serve

Con Secure Boot acceso — come esce di fabbrica quasi ogni PC — un kernel che
nessuno ha firmato viene rifiutato dallo shim e la macchina non parte. È la
segnalazione #53. Il kernel firmato con questa chiave parte, dopo che l'utente
l'ha registrata una volta sola con MokManager.

Provato il 26/08/2026 sulla VM 953 del Proxmox 192.168.5.102, con Secure Boot
acceso e le chiavi Microsoft nel firmware: allo stesso prompt di GRUB, il kernel
non firmato è stato respinto con «Verification failed: Security Policy
Violation» e quello firmato è stato caricato senza un errore.

## Come si firma

    kernel-build/scripts/firma-kernel.sh /root/linux-tkg/DEBS/linux-image-*.deb

Si può rilanciare: un pacchetto già firmato lo lascia stare, quindi non c'è il
rischio di accodare due firme.

`scripts/publish-kernel.sh` si rifiuta di caricare un kernel non firmato, e dice
quale comando lanciare. Senza quella guardia la regola durerebbe finché qualcuno
se ne ricorda.

## Una trappola, misurata

`sbverify --list` **esce 0 anche quando non c'è nessuna firma**: stampa
«No signature table present» e non si lamenta. Un controllo scritto sul codice
di uscita dichiara «firmato» qualunque cosa. Si guarda il testo, non il codice.
