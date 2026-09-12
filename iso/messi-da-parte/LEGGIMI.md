# Roba tolta dall'immagine, non buttata

Qui dentro finisce quello che non deve piu' entrare nell'immagine ma che non si
cancella: decide Mattia se serve ancora.

- `99-skillfish-bc250.cfg` - il frammento di GRUB scritto a mano, sostituito dal
  pacchetto **skillfish-boot** il 12/09/2026. Il pacchetto fa la stessa cosa, ma
  aggiunge invece di sostituire e controlla di essere davvero su una BC-250.

⚠️ Questa cartella sta FUORI da `config/includes.chroot` di proposito: li'
dentro live-build copia tutto quello che trova, qualunque nome abbia. Un file
rinominato `.sostituito-da-...` era finito nel sistema installato.

## Chrome, tolto il 12/09/2026

Era un pacchetto Debian da 435 MB installato d'ufficio a chiunque, con il
repository di Google aggiunto alle sorgenti apt. Un utente ha contestato a
Mattia la scelta di Chrome come browser predefinito, e aveva ragione: un
sistema non decide per chi lo usa quale browser deve avere.

Adesso non c'e' nessun browser di serie e al primo avvio si sceglie fra
Firefox, Chrome, Chromium e Brave, tutti come flatpak. Chi vuole Chrome lo ha
in due clic; chi non lo vuole non se lo ritrova sul disco.

⚠️ Se un giorno lo si rimettesse dentro, va rimesso anche il repository di
Google in `config/archives/`, altrimenti il pacchetto non si aggiorna mai piu'.
