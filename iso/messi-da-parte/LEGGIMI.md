# Roba tolta dall'immagine, non buttata

Qui dentro finisce quello che non deve piu' entrare nell'immagine ma che non si
cancella: decide Mattia se serve ancora.

- `99-skillfish-bc250.cfg` - il frammento di GRUB scritto a mano, sostituito dal
  pacchetto **skillfish-boot** il 12/09/2026. Il pacchetto fa la stessa cosa, ma
  aggiunge invece di sostituire e controlla di essere davvero su una BC-250.

⚠️ Questa cartella sta FUORI da `config/includes.chroot` di proposito: li'
dentro live-build copia tutto quello che trova, qualunque nome abbia. Un file
rinominato `.sostituito-da-...` era finito nel sistema installato.
