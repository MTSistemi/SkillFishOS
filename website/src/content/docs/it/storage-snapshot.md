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

## Quanti se ne tengono

**Cinque**, di serie: tre ordinari (la coppia prima/dopo che accompagna ogni
operazione di `apt`) e due "importanti", cioè gli aggiornamenti che toccano il
kernel o systemd — quelli che con più probabilità vorrai indietro. Oltre a questi
c'è il punto *"SkillFishOS - clean install"*, che non scade mai: la strada per
tornare al sistema com'era appena installato.

La linea temporale oraria è **spenta**. Su una console di casa consuma disco
senza che quegli snapshot li guardi mai nessuno. Gli snapshot che crei **a mano**
non rientrano nei cinque e non vengono mai cancellati da soli: se l'hai fatto
apposta, resta finché non lo togli tu.

## Rollback dal menu di avvio

Grazie a **[grub-btrfs](https://github.com/Antynea/grub-btrfs)** gli snapshot
compaiono direttamente nel menu di **GRUB**, sotto la voce *"SkillFishOS
snapshots"*. Riavvii, scegli quello di prima del guaio, e ci sei dentro.

Due cose da sapere prima di contarci:

- **Quello che avvii è in sola lettura.** È un ambiente di soccorso: ci guardi
  dentro, verifichi che lo stato precedente fosse davvero sano, ti porti via i
  file che ti servono. Qualche servizio segnalerà un errore all'avvio, perché non
  riesce a scrivere: è previsto, non è un guasto.
- **Il menu viene rigenerato dopo ogni transazione di `apt`**, così lo snapshot
  fatto *prima* di un aggiornamento è nell'elenco proprio quando serve.

## Rendere permanente il ritorno

Avviare uno snapshot non cambia niente da solo, e qui `snapper rollback` non
serve: cambia il sottovolume predefinito, mentre la voce di GRUB fissa
`subvol=@` e vince lei. Il comando che fa il lavoro è:

```bash
sudo skillfish-rollback --elenco   # quali snapshot ci sono
sudo skillfish-rollback 12         # lo snapshot 12 diventa il sistema, dal prossimo avvio
```

Sposta da parte il sistema attuale — non lo cancella, diventa
`@-rotto-<data>` — e costruisce un `@` nuovo e scrivibile dallo snapshot scelto,
portandosi dietro tutta la cronologia degli snapshot. Se anche lo stato
precedente non era la risposta, `sudo skillfish-rollback --annulla` rimette
tutto com'era, e `--pulisci` libera lo spazio quando sei sicuro.

Funziona sia dal sistema normale sia da dentro uno snapshot avviato in sola
lettura, che è poi il caso che conta davvero: quando la macchina non parte più.

> **La cartella personale non viene mai toccata.** `/home` è un sottovolume a
> parte: torna indietro il sistema, i tuoi file restano quelli di adesso. È
> comodo saperlo, ed è bene ricordarlo prima di contare su un ripristino per
> riavere un documento cancellato: quello non torna.

> Questa è la rete di sicurezza che permette anche ai più piccoli di esplorare il
> sistema senza il timore di romperlo in modo irreversibile.

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
