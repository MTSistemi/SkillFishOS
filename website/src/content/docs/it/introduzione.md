---
title: Introduzione
description: Cos'è SkillFishOS, perché esiste e per chi è pensato.
group: Introduzione
order: 1
---

**SkillFishOS** è una distribuzione Linux pensata e ottimizzata per una singola, particolare scheda: l'**AMD BC-250**. È un sistema *console-PC* pronto all'uso — gaming, emulazione, intelligenza artificiale locale e uso desktop quotidiano — costruito su [Debian](https://www.debian.org/) e [KDE Plasma 6](https://kde.org/plasma-desktop/), con un'estetica steampunk coerente dal boot fino al desktop.

## La filosofia

La BC-250 è una scheda nata per il mining di criptovalute e finita sul mercato dell'usato a prezzi molto bassi. Sotto al dissipatore però c'è un'**APU semi-custom AMD** della stessa famiglia delle console di nuova generazione: CPU Zen 2, grafica RDNA 2 e 16 GB di GDDR6. Con il software giusto diventa una piccola console-PC sorprendentemente capace.

Il problema è che farla funzionare bene su Linux richiede patch del kernel, un governor dedicato per le frequenze, overclock, profili termici e una lunga serie di accorgimenti hardware. SkillFishOS esiste per **fare tutto questo lavoro una volta sola** e consegnare un sistema che *"si accende e funziona al massimo"*, senza che l'utente debba smanettare con il terminale.

> SkillFishOS non distribuisce giochi né ROM: fornisce gli **strumenti** (Steam, EmuDeck, emulatori, frontend). I contenuti li aggiunge l'utente, legalmente.

## Per chi è

Il progetto nasce da un'esigenza concreta e personale: **far usare e imparare Linux ai più piccoli mentre giocano**. Il gioco è la "carota" che invoglia, e gli **snapshot automatici di Btrfs** sono la rete di sicurezza che permette di smanettare senza paura di rompere il sistema — se qualcosa va storto, si torna indietro in un clic dal menu di avvio.

Di conseguenza SkillFishOS è adatto a:

- chi possiede una **BC-250** e vuole usarla per giocare senza diventare un esperto di kernel Linux;
- **famiglie** che vogliono una console economica e al tempo stesso un PC educativo;
- **smanettoni** che vogliono partire da una base già ottimizzata invece di ricostruire tutto da zero.

## Cosa c'è dentro, in breve

- **Kernel su misura** ([linux-tkg](https://github.com/Frogging-Family/linux-tkg)) con le patch per la BC-250: 40 Compute Unit sbloccate, frequenze sbloccate, governor SMU dedicato.
- **Desktop KDE Plasma 6** a tema steampunk (icone, cursori, wallpaper, HUD di sistema).
- **Gaming pronto**: Steam, [gamescope](https://github.com/ValveSoftware/gamescope), [EmuDeck](https://www.emudeck.com/), [ES-DE](https://es-de.org/), [Heroic](https://heroicgameslauncher.com/), Proton.
- **AI in locale**: stack [Ollama](https://ollama.com/) + [OpenWebUI](https://openwebui.com/) accelerato in Vulkan sulla GPU integrata.
- **Snapshot Btrfs** con [Snapper](http://snapper.io/) e rollback dal menu GRUB.
- **App native**: il *Tuner* (controllo hardware senza terminale) e il pannello *AI*.
- **Aggiornamenti dedicati** da un repository APT proprio, testati, per non farsi sorprendere dagli aggiornamenti di Debian.

Le pagine successive entrano nel dettaglio di ciascun componente.

## Fonti

- Documentazione comunitaria BC-250 — [bc250.info](https://bc250.info)
- AMD BC-250 docs (elektricm) — [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- Debian — [debian.org](https://www.debian.org/)
- KDE Plasma — [kde.org/plasma-desktop](https://kde.org/plasma-desktop/)
