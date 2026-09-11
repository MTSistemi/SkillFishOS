---
title: "Control Center"
description: "Tutti gli strumenti di SkillFishOS in una finestra: Tuner, Ventola, Monitor, Giochi, Profili, Kernel, Snapshot, AI, Emulatori, Console, ISO."
group: Uso
order: 4
---

Tutti gli strumenti di SkillFishOS stanno in una finestra. Si apre dal menu (SkillFishOS → Control Center) o con `skillfish-control-center`. Si guida anche col controller: croce o levetta per muoversi, A conferma, B torna indietro, LB e RB cambiano sezione.

## Le sezioni

- **Stato**: un numero per scheda: frequenza e tetto della GPU, CPU, unità di calcolo, ventola, kernel, governor, driver Vulkan, se l'ultimo avvio è seguito a uno spegnimento pulito. Qui non si imposta niente.
- **Tuner**: la curva tensione/frequenza del governor della GPU, la CPU, i core, le unità di calcolo, la VRAM.
- **Ventola**: la curva della ventola con l'anticipo, i sensori sorgente, i limiti di sicurezza, la prova del PWM.
- **Monitor**: tutte le letture, un grafico per unità, più le barre di frequenza per thread. REC registra, CSV esporta.
- **Giochi**: la nostra Mesa per lanciatore o per tutto il sistema, lo schedulatore scx_bpfland, FSR 4, installazione e predefinita di GE-Proton.
- **Profili**: tetto, CPU, ventola e schedulatore in un clic; salva i tuoi.
- **Kernel**: i kernel installati, quello predefinito, avvia una volta, disinstalla.
- **Snapshot**: le fotografie del sistema e la manutenzione btrfs programmata.
- **AI**: Unsloth Studio su Vulkan: motore, aggiornamento, modelli dall'Hub di Hugging Face, chat di prova, memoria e rete.
- **Emulatori**: EmuDeck, oppure gli emulatori uno per uno da Flathub.
- **Console**: Steam Big Picture dentro gamescope, adesso o dalla schermata di accesso.
- **ISO**: immagini disco montate attraverso udisks.

## Tuner

La curva è il grafico: MHz in orizzontale, millivolt in verticale. Trascina un punto, doppio clic per aggiungerne uno, tasto destro per toglierlo, oppure scrivi i numeri nella tabella accanto al grafico (+ e − aggiungono e tolgono punti). La riga tratteggiata verticale è il tetto, il pallino azzurro è la GPU adesso. Tre preset: **Cautious 1850** (il punto dolce col dissipatore di serie, quasi gli stessi fotogrammi e dieci gradi in meno), **Balanced 2000**, **Performance 2100** (la curva a quindici punti misurata sulla scheda di sviluppo, quella che spediamo).

**Applica è una prova.** Una curva che chiede troppo poca tensione pianta la scheda, e sulla BC-250 un blocco si risolve staccando la corrente. Perciò Applica fa partire la candidata con la curva di prima ancora su disco e conta 25 secondi: premi Tieni e la candidata viene scritta per davvero; non fai niente, o la scheda muore e riparte, e all'avvio torna la curva di prima.

I pannelli si aprono quando servono:

- **CPU**: frequenza, scalino di undervolt (6,25 mV l'uno) e limite termico, ognuno con un cursore e una casella numerica a passo 1. *Suggerisci UV* scende di due scalini alla volta con dodici secondi di carico per scalino; *Trova il massimo* sale da 3600 a 4000 MHz; *Test 60 s* carica i valori attuali. Ogni prova mostra un conto alla rovescia e un bottone Stop; i valori in prova non vengono mai scritti su disco, quindi un blocco riavvia con quelli di prima. Sopra i 3500 MHz con otto core il guadagno è zero: comanda il calore.
- **Core**: quali core sono attivi, SMT, lo sblocco degli 8 core (6c/12t diventa 8c/16t, +20% misurato) e *Prima dell'avvio (EFI)*: lo sblocco fatto prima di GRUB in un avvio solo, invece del riavvio in più del servizio dentro al sistema.
- **CU**: le 40 unità di calcolo come 20 caselle (coppie): verde accesa, rossa spenta, grigia tenuta accesa dal driver. Scrivi quante CU vuoi (da 24 a 40, a coppie) o clicca le caselle; *Test CU* accende le coppie extra una alla volta sotto vkpeak e riporta gli errori, per la lotteria del silicio.
- **VRAM**: la quota UMA nel CMOS, applicata al prossimo avvio. Con i 512 MB dinamici alcuni giochi scelgono texture basse: se sono sfocate, prova 4 o 6 GB fissi. Va da 512 MB a 12 GB, con i preset 512 MB, 1, 2, 4, 6 e 8 GB.
- **Avanzate**: le manopole del governor: margine in salita, gradino, conferme in discesa, soglie termiche e di potenza, droop.
- **Test**: vkpeak e il registro dell'helper.

## Monitor

Un grafico per grandezza, ognuno con la sua scala vera: temperature (CPU, GPU, VRM, sistema, NVMe), frequenze (CPU media, minima, massima, GPU e il suo tetto), carico, potenza, tensioni, ventola e memoria (RAM, VRAM, GTT), più una barra per thread. Clic su una voce della legenda per nascondere una linea; passa il mouse per leggere tutti i grafici nello stesso istante. REC scrive un file `.sfmon` (CSV) che Apri ricarica con uno scrubber; CSV lo esporta per un foglio di calcolo.

## Giochi

- **Driver Vulkan**: la nostra Mesa apre le code compute che il driver di serie tiene chiuse su questa GPU: +4% in Cyberpunk 2077, +12% con FSR 4 acceso. Per lanciatore (Steam, Heroic) con un override flatpak, o per tutto il sistema. Serve il kernel di SkillFishOS: su un altro kernel quelle code piantano la GPU, e l'interruttore di sistema si rifiuta di partire. La scheda mostra il kernel in esecuzione.
- **Schedulatore**: scx_bpfland, caricato solo mentre gira un gioco (lo alza GameMode all'avvio e lo toglie alla chiusura): +1,5-2% in Cyberpunk e fotogrammi più regolari. Se il kernel lo espelle due volte il servizio si ferma finché non azzeri il contatore: è la riga «Espulso dal kernel».
- **FSR 4**: attraverso OptiScaler sul percorso DLSS del gioco. GE-Proton 11 scarica OptiScaler da solo quando trova `PROTON_USE_OPTISCALER=1`, il gioco va messo su DLSS, e la libreria FSR 4 di AMD (`amdxcffx64.dll`, dal driver Windows di AMD) va accanto al gioco. XeSS, dove un gioco ce l'ha di suo, costa quanto FSR 3 a 1080p.
- **Proton**: le versioni GE-Proton 11; Installa ne scarica una (circa 500 MB) nelle cartelle di Steam e Heroic, Predefinita la sceglie. Steam va chiuso perché la sua predefinita venga scritta.

## AI

Il motore è **Unsloth Studio**: fa girare i modelli GGUF con llama.cpp sul backend **Vulkan**, che sulla gfx1013 della BC-250 è l'unica strada accelerata, perché ROCm non la supporta. Misurato sulla scheda con Qwen3-1.7B Q4_K_M: 210 token al secondo contro i 41 della sola CPU.

- **Motore**: acceso, spento, all'avvio. Acceso tiene la memoria della GPU, quindi si spegne prima di giocare. Accanto stanno la versione, il controllo degli aggiornamenti e *Aggiorna*, che rilancia l'installatore ufficiale con il pacchetto Vulkan di llama.cpp.
- **Accesso**: Unsloth genera una password a caso quando si installa, e si spegne da solo dopo un'ora se non viene cambiata. Il primo accesso si fa da qui: scegli la password di Studio e la chiave API viene creata insieme, e condivisa con il Remote Manager.
- **Modelli**: quelli sul disco con quantizzazione e dimensione. Per scaricarne uno serve il nome del repository su Hugging Face (per esempio `unsloth/Qwen3-4B-GGUF`) e la variante scelta dall'elenco, che riporta le dimensioni.
- **Chat**: una prova rapida sull'API compatibile OpenAI (`http://127.0.0.1:8888/v1`), con i token al secondo misurati. La chat completa, con i file e la ricerca, è dentro Studio.
- **Memoria**: VRAM, GTT, RAM, swap e il budget del modello. Il limite del GTT è un parametro del kernel: vale dal riavvio.
- **Rete**: aperto sulla rete locale, Studio risponde anche agli altri dispositivi di casa, con il suo utente e la sua password. Le chat in parallelo sono i posti di llama-server.

## Ventola, profili e il resto

La pagina **Ventola** disegna la curva dentro il grafico dei sensori: a questa temperatura la ventola gira così, con un anticipo perché la velocità salga prima della temperatura. I **Profili** spostano il tetto dentro alla curva che c'è già e impostano insieme CPU, preset della ventola e schedulatore. Gli **Snapshot** sono fotografie del sistema, i tuoi file non vengono toccati. **AI** tiene la memoria della GPU finché è acceso: spegnilo prima di giocare. **Console** avvia Steam Big Picture dentro gamescope sopra al desktop, o come sessione dalla schermata di accesso. Il **Remote Manager** replica le pagine Tuner, Giochi e Profili in un browser.
