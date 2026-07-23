---
title: Domande frequenti (FAQ)
description: Le domande più comuni su SkillFishOS e sulla BC-250, con risposte brevi.
group: Riferimenti
order: 2
---

Risposte rapide alle domande più comuni. Per gli approfondimenti, ogni risposta rimanda alla pagina giusta.

## In generale

**Cos'è SkillFishOS?**
Una distribuzione Linux (Debian + KDE Plasma 6) pensata e ottimizzata per la scheda **AMD BC-250**: gaming, emulazione, AI locale e uso desktop, già configurati. Vedi [Introduzione](/docs/introduzione).

**Su quale hardware gira?**
Esclusivamente sulla **AMD BC-250** (APU Zen 2 + RDNA 2 "gfx1013", 16 GB GDDR6). È un sistema costruito attorno a *quella* scheda, non una distro generica. Vedi [Hardware BC-250](/docs/hardware-bc250).

**Quanto costa? È open source?**
È **gratuito**. Integra software open source di tante comunità; il codice del progetto è su [GitHub](https://github.com/MTSistemi/SkillFishOS). Vedi [Fonti](/docs/fonti).

**Include giochi, ROM o BIOS?**
No. SkillFishOS fornisce gli **strumenti** (Steam, EmuDeck, emulatori, frontend); i contenuti li aggiungi tu, legalmente. Vedi [Gaming](/docs/gaming).

## Installazione

**Come si installa?**
Si scrive la ISO su una chiavetta USB e si avvia l'installer grafico **Calamares**. Tutto col mouse. Vedi [Installazione](/docs/installazione).

**Posso provarlo senza installare?**
Sì: la ISO è **live**, puoi esplorare il desktop prima di installare.

**Cancella il mio disco?**
L'installazione automatica ("Cancella disco") sì. Se vuoi conservare dati esistenti, usa il partizionamento manuale. SkillFishOS usa **Btrfs** con sottovolumi `@rootfs` e `@home` separati.

**Serve la connessione a Internet?**
Per installare no; serve poi per Steam, aggiornamenti e AI.

## Prestazioni e overclock

**Perché parte "lento" / in Stock?**
Per sicurezza: ogni BC-250 è diversa (*silicon lottery*). Si sale di profilo dal **[Tuner](/docs/app-native)**, che valida tutto sulla tua scheda. Vedi [GPU e overclock](/docs/gpu-overclock).

**L'overclock è pericoloso?**
Il Tuner applica un profilo, lo **testa** e fa **rollback** se la scheda non regge; il cap termico 85 °C e il thermal-guard sono sempre attivi. È pensato per essere sicuro.

**Quanti FPS fa nel gioco X?**
Dipende: alcuni giochi sono **CPU-bound** (es. *Black Myth: Wukong*) e non scalano con la GPU. Vedi [Prestazioni e benchmark](/docs/prestazioni).

**Posso usare FSR 4?**
No, richiede hardware RDNA 4. Si usano gamescope (FSR1/NIS) o OptiScaler. Vedi [Gaming](/docs/gaming).

## Uso quotidiano

**Perché lo schermo a volte resta nero?**
L'**HPD del DisplayPort è guasto** sulla BC-250: SkillFishOS lo aggira con un demone dedicato. Usa un monitor DP o un adattatore **passivo**. Vedi [Risoluzione problemi](/docs/risoluzione-problemi).

**Perché non c'è audio dalla TV?**
Spesso è colpa di un adattatore **attivo** DP→HDMI: usane uno passivo, un monitor DP, un DAC USB o l'audio Bluetooth.

**Posso mettere il PC in standby?**
No. La **sospensione è guasta** a livello hardware e la scheda non si risveglia: SkillFishOS la disabilita di proposito. **Non riattivarla.** Vedi [Desktop](/docs/desktop).

**Posso usarlo da un altro computer?**
Sì: la sessione predefinita è X11 e gira **x11vnc**, quindi controlli il desktop via VNC sulla LAN. Vedi [Desktop](/docs/desktop).

## AI locale

**Che modello AI posso usare?**
Il riferimento pratico è **`qwen3:14b`**, che gira al 100% su GPU. Lo stack è Ollama + OpenWebUI in **Vulkan** (non ROCm, non supportato su gfx1013). Vedi [AI in locale](/docs/ai-locale).

**Posso giocare mentre l'AI è accesa?**
No: AI e giochi pesanti condividono GPU e memoria. Spegni lo stack AI prima di giocare.

## Aggiornamenti

**Come aggiorno il sistema?**
`sudo apt update && sudo apt full-upgrade` o l'app **Discover**. Prima/dopo ogni aggiornamento parte uno snapshot automatico. Vedi [Aggiornamenti](/docs/aggiornamenti).

**Un aggiornamento ha rotto qualcosa: che faccio?**
Riavvia e scegli uno snapshot da **GRUB → "SkillFishOS snapshots"**. Vedi [Storage e snapshot](/docs/storage-snapshot).

**Il kernel viene aggiornato da Debian?**
No: il kernel di SkillFishOS è **bloccato** (`apt-mark hold`) e aggiornato solo dal nostro repo testato. Vedi [Kernel](/docs/kernel).

## Progetto

**Posso contribuire o segnalare un bug?**
Sì, tramite le **Issue** su [GitHub](https://github.com/MTSistemi/SkillFishOS/issues).

**Dove scarico la ISO?**
Dalla pagina [Download](/download) (ospitata su SourceForge).
