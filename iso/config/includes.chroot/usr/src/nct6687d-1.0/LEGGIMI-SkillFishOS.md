# nct6687d, il sensore della ventola

Il modulo che legge e comanda la ventola della BC-250. Sta qui, e non lo si
scarica al volo, per due motivi trovati il 12/09/2026 costruendo la prima
immagine dalla VM:

- a monte (Fred78290/nct6687d) non c'e' nessun rilascio: l'indirizzo del .deb
  risponde 404 da sempre, quindi si passava comunque dai sorgenti;
- e il sorgente di oggi NON compila con il nostro kernel 7.2.5. Questa copia
  si': e' quella che gira sulle nostre schede, e ha due correzioni nostre del
  18/08/2026, quando il 7.2 ha rotto la compilazione.

## Cosa abbiamo cambiato rispetto a monte

Dal kernel 7.2 `<linux/string.h>` non arriva piu' per traverso e il kernel
compila con `-Werror` sulle dichiarazioni implicite, quindi:

- l'include di `<linux/string.h>` e' esplicito;
- `strncpy()` e' diventato `strscpy()`. Nel 7.2 `strncpy` resta solo nominata
  in string.h come funzione sostituita: senza questa modifica il modulo non si
  costruisce. `strscpy` fa esattamente la stessa cosa qui (tronca e termina
  sempre) ed esiste da anni, quindi il sorgente vale anche per il 7.1.7.

Undici righe in tutto. Se un giorno a monte le accettano, questa cartella puo'
tornare a essere una copia pulita.

Senza questo modulo la ventola resta alla curva del firmware: niente curva,
niente anticipo, niente controllo dal Control Center.

⚠️ E il modulo giusto e' `nct6687`, non `nct6683`: quello di serie accetta i
comandi PWM e non li esegue, in silenzio.

Licenza GPL-2.0, vedi LICENSE nella cartella.
