---
title: Stockage et instantanés Btrfs
description: "Le filet de sécurité de SkillFishOS : instantanés automatiques et retour en arrière dès le démarrage."
group: Système
order: 3
---

Une des idées centrales de SkillFishOS est de pouvoir **bricoler sans crainte**. C'est le système de fichiers **[Btrfs](https://btrfs.readthedocs.io/)** et ses instantanés automatiques qui le permettent : chaque changement important est saisi, et si quelque chose casse on revient en arrière en un clic.

## Des sous-volumes séparés

Le disque porte une seule partition Btrfs, divisée en sous-volumes distincts :

- **`@`** — le système d'exploitation ;
- **`@home`** — les données de l'utilisateur ;
- **`@cache`** et **`@log`** — les caches et les journaux, tenus hors des instantanés pour qu'un retour en arrière ne ramène pas avec lui les journaux d'hier ;
- **`@games`** — la bibliothèque de jeux, qui sinon rendrait chaque instantané énorme ;
- **`@swap`** — le fichier d'échange.

Les garder séparés est essentiel : revenir en arrière sur le système **ne touche pas aux fichiers personnels**. Vous pouvez retrouver un système « d'hier » en gardant les documents, les sauvegardes et les réglages d'aujourd'hui.

## Les instantanés automatiques avec Snapper

SkillFishOS utilise **[Snapper](http://snapper.io/)** avec une configuration `root` et des **accrochages avant et après APT** : chaque fois que vous installez ou mettez à jour des paquets, un instantané est créé tout seul *avant* et *après*. Ainsi, si une mise à jour pose problème, l'instantané « d'avant » est déjà là.

Les points saillants de la configuration :

- un plafond sur le nombre d'instantanés gardés, pour que le disque ne se remplisse pas ;
- des instantanés conservés aux *étapes* importantes du système ;
- la gestion possible aussi par l'outil graphique **Btrfs Assistant**.

## Combien en sont gardés

**Cinq**, par défaut : trois ordinaires (la paire avant/après autour de chaque
opération `apt`) et deux « importants » — les mises à jour qui touchent au noyau
ou à systemd, celles qu'on a le plus de chances de vouloir récupérer. Au-dessus
se trouve le point *« SkillFishOS - clean install »*, qui n'expire jamais : le
chemin de retour vers le système tel qu'il sortait de la boîte.

La chronologie horaire est **éteinte**. Sur une console de salon elle ne fait
que manger du disque sans que personne ne regarde jamais ces instantanés. Les
instantanés que vous créez **à la main** ne comptent pas parmi les cinq et ne
sont jamais effacés tout seuls : si vous en avez fait un exprès, il reste
jusqu'à ce que vous l'enleviez.

## Le retour en arrière depuis le menu de démarrage

Grâce à **[grub-btrfs](https://github.com/Antynea/grub-btrfs)**, les instantanés
apparaissent directement dans le menu **GRUB**, sous *« SkillFishOS snapshots »*.
Redémarrez, choisissez l'instantané d'avant l'ennui, et vous voilà dedans.

Deux choses à savoir avant de compter dessus :

- **Ce que vous démarrez est en lecture seule.** C'est un environnement de
  secours : regardez autour, vérifiez que l'état plus ancien allait vraiment
  bien, sortez les fichiers dont vous avez besoin. Quelques services signaleront
  une erreur au démarrage — ils ne peuvent tout simplement pas écrire. C'est
  attendu, ce n'est pas une panne.
- **Le menu de démarrage est rafraîchi après chaque transaction `apt`**, si bien
  que l'instantané pris *avant* une mise à jour est dans la liste exactement
  quand vous en avez besoin.

## Rendre le retour définitif

Démarrer sur un instantané ne change rien en soi, et `snapper rollback` n'aide
pas ici : il échange le sous-volume par défaut, alors que notre entrée GRUB
impose `subvol=@` et l'emporte. La commande qui fait le travail est :

```bash
sudo skillfish-rollback --list    # quels instantanés sont disponibles
sudo skillfish-rollback 12        # l'instantané 12 devient le système, dès le prochain démarrage
```

Elle met le système actuel de côté — il n'est pas effacé, il devient
`@-rotto-<date>` — et construit un nouveau `@` inscriptible à partir de
l'instantané choisi, en emportant avec lui toute l'histoire des instantanés. Si
l'état plus ancien n'est pas la réponse non plus,
`sudo skillfish-rollback --undo` remet tout en place, et `--clean` libère la
place quand vous êtes sûr.

Elle marche depuis le système normal comme depuis un instantané démarré en
lecture seule, ce qui est le cas qui compte quand la machine ne démarre plus.

> **Votre dossier personnel n'est jamais touché.** `@home` est un sous-volume à
> part : le système remonte le temps, vos fichiers restent tels quels. Bon à
> savoir, et bon à retenir avant de compter sur un retour en arrière pour
> retrouver un document que vous avez supprimé — il ne le fera pas.

> C'est le filet qui permet même aux plus jeunes d'explorer le système sans
> craindre de le casser pour de bon.

## Pourquoi Btrfs et pas Timeshift

SkillFishOS a choisi **Btrfs + Snapper + grub-btrfs** plutôt que des solutions comme Timeshift parce que :

- l'intégration à APT est automatique (un instantané à chaque opération sur les paquets) ;
- les instantanés sont natifs au système de fichiers (immédiats, en *copie sur écriture*, peu coûteux) ;
- le retour en arrière est disponible **dès le démarrage**, même si le système ne se lance plus normalement.

## Sources

- [La documentation de Btrfs](https://btrfs.readthedocs.io/)
- [Snapper](http://snapper.io/)
- [grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)
- [Btrfs Assistant](https://gitlab.com/btrfs-assistant/btrfs-assistant)
