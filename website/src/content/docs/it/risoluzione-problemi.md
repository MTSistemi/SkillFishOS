---
title: Risoluzione problemi
description: I problemi più comuni della BC-250 e come SkillFishOS li affronta.
group: Riferimenti
order: 1
---

Molti "problemi" della BC-250 sono in realtà difetti hardware noti che SkillFishOS aggira automaticamente. Ecco i più comuni.

## Lo schermo resta nero / il monitor non viene rilevato

L'**HPD (Hot-Plug Detect) del DisplayPort è guasto**: la scheda non rileva quando colleghi un monitor. SkillFishOS lo gestisce con il demone `skillfish-dp-hotswap` (che forza il rilevamento all'avvio e ai cambi di monitor) e con il parametro kernel `video=DP-1:e`.

Cosa controllare:

- usa un **monitor DisplayPort** o un adattatore **passivo** DP→HDMI;
- evita gli adattatori **attivi** DP→HDMI: oltre ai problemi di rilevamento, **rompono l'audio** (vedi sotto);
- se il monitor è cambiato, attendi qualche secondo: il rilevamento è automatico ma non istantaneo.

## La scheda non si risveglia dopo lo standby

La **sospensione è rotta** a livello hardware. SkillFishOS la disabilita completamente proprio per questo (vedi [Desktop](/docs/desktop)). Se la scheda risulta "morta" dopo essere stata inattiva e si era modificata la gestione energetica, l'unica via è il **reset fisico**. Non riabilitare gli stati di sospensione.

## Non c'è audio dal monitor/TV

L'audio del DisplayPort funziona, ma:

- gli **adattatori attivi DP→HDMI** rompono l'audio: usa adattatori passivi, un monitor DP nativo, un **DAC USB** o l'audio **Bluetooth**;
- lo stack audio è **PipeWire**: il sink predefinito si imposta dalle impostazioni audio di KDE.

## I controller non funzionano

- I **DualShock 4** vanno in **Bluetooth** (con giroscopio). Per accoppiarli: tieni *Share + PS* finché lampeggiano, poi accoppia dalla GUI Bluetooth.
- Un controller **via USB** va collegato con un cavo **dati** (non solo di ricarica): viene riconosciuto come Xbox 360.
- I controller clone potrebbero non condividere bene l'adattatore Bluetooth con i DS4: in quel caso usali **via USB**.

## La GPU sembra lenta / temperature alte

- Verifica con il [Tuner](/docs/app-native) che siano attive le **40 CU** e il governor SMU.
- Ricorda che il raffreddamento è marginale: dopo un carico prolungato interviene il **thermal-guard** (85 °C). Per benchmark validi, lascia raffreddare la scheda tra una prova e l'altra (vedi [GPU](/docs/gpu-overclock)).
- Per i giochi **CPU-bound** abbassare la risoluzione non aumenta gli FPS.

## La scheda si è bloccata (freeze)

La BC-250 può andare in **hard freeze** (blocco totale), spesso legato a un **undervolt troppo spinto**: l'instabilità colpisce soprattutto negli stati a **basso carico**, quindi a volte il blocco arriva persino da fermi. SkillFishOS lo affronta su due fronti:

- **Watchdog hardware** — il timer **SP5100 TCO** del chipset è attivo (`RuntimeWatchdogSec=2min`): se il sistema si pianta del tutto, la scheda si **riavvia da sola** entro due minuti, senza staccare la corrente.
- **Rilevatore di freeze** — al boot, un servizio riconosce se lo spegnimento precedente è stato anomalo (nessun marker di shutdown pulito) e lo **registra** in `/var/log/skillfish-freeze.log`, con una notifica sul desktop. Il contatore compare anche nel pannello **«Il mio silicio»** del [Tuner](/docs/app-native).

Se i freeze si ripetono, **scendi di un preset** (es. da Crazy/Turbo a Performance) col Tuner: il valore meno spinto è quasi sempre la cura. Tutti i preset sono **crash-safe** — un blocco a metà test non lascia la scheda su un profilo instabile al riavvio. Se persistono anche in Stock, sospetta l'**alimentatore**.

## Un aggiornamento ha rotto qualcosa

Riavvia e dal menu **GRUB → "SkillFishOS snapshots"** scegli uno snapshot precedente funzionante. Vedi [Storage e snapshot](/docs/storage-snapshot). Gli snapshot pre/post aggiornamento sono automatici.

## L'AI non parte o dà output strano

- L'AI gira in Vulkan (non ROCm) e **non va usata insieme ai giochi** (stessa GPU/RAM).
- Se l'output è corrotto, assicurati di usare la cache KV in **f16** (la `q4_0` corrompe l'output su RADV). Vedi [AI in locale](/docs/ai-locale).

## Fonti

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — DualShock 4](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — troubleshooting](https://docs.pipewire.org/)
