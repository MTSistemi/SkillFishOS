---
title: Storage e snapshot Btrfs
description: "La rete di sicurezza di SkillFishOS: snapshot automatici e rollback dal boot."
group: Sistema
order: 3
---

Una delle idee centrali di SkillFishOS è poter **smanettare senza paura**. Questo è reso possibile dal filesystem **[Btrfs](https://btrfs.readthedocs.io/)** con snapshot automatici: ogni modifica importante è fotografata, e se qualcosa si rompe si torna indietro in un clic.

## Sottovolumi separati

Il disco usa due sottovolumi Btrfs distinti:

- **`@rootfs`** — il sistema operativo;
- **`@home`** — i dati dell'utente.

Tenerli separati è fondamentale: fare il **rollback del sistema non tocca i file personali**. Si può tornare a un sistema "di ieri" mantenendo documenti, salvataggi e configurazioni di oggi.

## Snapshot automatici con Snapper

SkillFishOS usa **[Snapper](http://snapper.io/)** con una configurazione `root` e degli **hook pre/post su APT**: ogni volta che installi o aggiorni pacchetti, vengono creati automaticamente uno snapshot *prima* e uno *dopo*. Così, se un aggiornamento causa problemi, lo snapshot "prima" è già lì.

Caratteristiche della configurazione:

- limite di snapshot mantenuti per non riempire il disco;
- snapshot conservati ai *milestone* importanti del sistema;
- gestione anche da interfaccia grafica con **Btrfs Assistant**.

## Rollback dal menu di avvio

Grazie a **[grub-btrfs](https://github.com/Antynea/grub-btrfs)** (con il demone `grub-btrfsd`), gli snapshot compaiono direttamente nel menu di **GRUB**, sotto la voce *"SkillFishOS snapshots"*. In caso di problema:

1. riavvia;
2. dal menu GRUB scegli uno snapshot precedente funzionante;
3. avvii in quello stato e, se vuoi rendere permanente il ritorno, completi il rollback.

> Questa è la "rete di sicurezza" che permette anche ai più piccoli di esplorare il sistema senza il timore di romperlo in modo irreversibile.

## Perché Btrfs e non Timeshift

SkillFishOS ha scelto **Btrfs + Snapper + grub-btrfs** invece di soluzioni come Timeshift perché:

- l'integrazione con APT è automatica (snapshot a ogni operazione sui pacchetti);
- gli snapshot sono nativi del filesystem (istantanei, *copy-on-write*, poco costosi);
- il rollback è disponibile **dal boot**, anche se il sistema non si avvia più normalmente.

## Fonti

- [Documentazione Btrfs](https://btrfs.readthedocs.io/)
- [Snapper](http://snapper.io/)
- [grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)
- [Btrfs Assistant](https://gitlab.com/btrfs-assistant/btrfs-assistant)
