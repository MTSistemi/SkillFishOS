---
title: Installation
description: Comment écrire l'ISO, démarrer l'installateur et terminer la mise en place.
group: Installation
order: 1
---

SkillFishOS s'installe depuis une **image live** qui contient l'installateur graphique [Calamares](https://calamares.io/). Tout se fait à la souris, sans terminal.

> L'image **26.06.4 « Aetherium »** est disponible — téléchargez-la depuis la page [Téléchargement](/fr/download). Elle démarre en **anglais** pour rester universelle et vous laisse choisir votre langue et votre clavier pendant l'installation.

## Ce qu'il faut

- une carte **AMD BC-250** (voir [matériel](/fr/docs/hardware-bc250)) ;
- un **SSD ou NVMe** pour l'installation ;
- un écran branché en **DisplayPort** (un adaptateur DP→HDMI *passif* peut convenir, mais lisez les remarques sur l'image et le son dans [Dépannage](/fr/docs/risoluzione-problemi)) ;
- une **clé USB d'au moins 8 Go** pour l'installateur ;
- un clavier et une souris pour l'installation.

## 1. Écrire l'ISO sur la clé USB

Téléchargez l'ISO depuis la page [Téléchargement](/fr/download) et écrivez-la sur une clé avec l'un de ces outils :

- **[balenaEtcher](https://etcher.balena.io/)** (Windows/macOS/Linux, graphique, conseillé) ;
- **[Ventoy](https://www.ventoy.net/)** (permet de garder plusieurs images sur la même clé) ;
- depuis un terminal Linux avec `dd` :

```bash
sudo dd if=SkillFishOS_amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

> Remplacez `/dev/sdX` par le bon périphérique pour votre clé. **Attention** : `dd` écrit sans rien demander et efface tout ce qu'il y a sur la cible.

## 2. Démarrer la BC-250 sur la clé

Branchez la clé, allumez la carte et entrez dans le menu de démarrage ou l'UEFI pour choisir l'USB comme périphérique de démarrage. L'environnement **live** de SkillFishOS (KDE Plasma) se lance : vous pouvez explorer le système avant de l'installer.

## 3. Installer avec Calamares

Depuis le bureau live, lancez l'installateur (icône *Install SkillFishOS*). Calamares vous guide pas à pas :

1. **Langue et fuseau horaire.**
2. **Clavier.**
3. **Partitionnement.** SkillFishOS utilise **Btrfs** avec des sous-volumes séparés : `@` (système), `@home` (vos données), `@cache` et `@log` (tenus hors des instantanés), `@games` (la bibliothèque de jeux). Cela permet de *revenir en arrière* sur le système sans toucher à vos fichiers. Une petite partition **EFI** complète le tableau, et la partition d'échange est un **fichier**, pas une partition. Pour la plupart des gens, l'installation automatique (« Effacer le disque ») convient.
4. **Utilisateur.** Créez votre compte (il sera dans les bons groupes pour le jeu, le son, le rendu, etc.).
5. **Résumé et installation.**

Une fois l'installation terminée, redémarrez et retirez la clé.

## 4. Le premier démarrage

Au premier démarrage **tout est déjà configuré** : noyau optimisé, gouverneur, overclock, thème, jeu et instantanés sont actifs. Aucun réglage à la main.

À partir de là vous pouvez :

- appairer vos [manettes](/fr/docs/gaming) (DualShock 4 en Bluetooth ou une manette USB) ;
- ajouter vos jeux dans [Steam et EmuDeck](/fr/docs/gaming) ;
- allumer l'[IA locale](/fr/docs/ai-locale) quand vous en avez besoin ;
- régler le matériel avec le [Tuner](/fr/docs/app-native) si vous le souhaitez.

## Schéma du disque

| Partition | Système de fichiers | Contenu |
|---|---|---|
| `nvme0n1p1` | FAT32 (EFI) | Chargeur de démarrage GRUB |
| `nvme0n1p2` | **Btrfs** | `@` (système) · `@home` (données) · `@cache` · `@log` · `@games` · `@swap` |

Il n'y a pas de partition d'échange : l'échange est un **fichier** dans le sous-volume `@swap`. Sur Btrfs il se redimensionne sans toucher à la table des partitions, et il reste hors des instantanés.

## Sources

- [Calamares](https://calamares.io/) — l'installateur universel
- [balenaEtcher](https://etcher.balena.io/) · [Ventoy](https://www.ventoy.net/)
- [Wiki de Btrfs](https://btrfs.readthedocs.io/) — sous-volumes et instantanés
