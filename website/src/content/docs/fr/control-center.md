---
title: "Control Center"
description: "Tous les outils SkillFishOS dans une fenêtre : Tuner, Ventilateur, Moniteur, Jeux, Profils, Noyau, Instantanés, IA, Émulateurs, Console, ISO."
group: Utilisation
order: 4
---

Tous les outils SkillFishOS tiennent dans une fenêtre. Elle s'ouvre depuis le menu (SkillFishOS → Control Center) ou avec `skillfish-control-center`. Une manette la pilote aussi : croix ou stick pour se déplacer, A confirme, B revient, LB et RB changent de section.

## Les sections

- **État**: un chiffre par carte : fréquence et plafond du GPU, CPU, unités de calcul, ventilateur, noyau, governor, pilote Vulkan, si le dernier démarrage a suivi un arrêt propre. Rien ne se règle ici.
- **Tuner**: la courbe tension/fréquence du governor du GPU, le CPU, les cœurs, les unités de calcul, la VRAM.
- **Ventilateur**: la courbe du ventilateur avec son avance, les capteurs sources, les limites de sécurité, le test PWM.
- **Moniteur**: toutes les mesures, un graphique par unité, plus les barres de fréquence par thread. REC enregistre, CSV exporte.
- **Jeux**: notre Mesa par lanceur ou pour tout le système, l'ordonnanceur scx_bpfland, FSR 4, installation et défaut de GE-Proton.
- **Profils**: plafond, CPU, ventilateur et ordonnanceur en un clic ; enregistrez les vôtres.
- **Noyau**: les noyaux installés, celui par défaut, démarrer une fois, désinstaller.
- **Instantanés**: les instantanés du système et l'entretien btrfs planifié.
- **IA**: Unsloth Studio sur Vulkan : marche/arrêt, matériel, la limite GTT.
- **Émulateurs**: EmuDeck, ou les émulateurs un par un depuis Flathub.
- **Console**: Steam Big Picture dans gamescope, maintenant ou depuis l'écran de connexion.
- **ISO**: images disque montées via udisks.

## Tuner

La courbe est le graphique : MHz en abscisse, millivolts en ordonnée. Glissez un point, double-clic pour en ajouter un, clic droit pour le retirer, ou tapez les nombres dans le tableau à côté du graphique (+ et − ajoutent et retirent des points). La ligne verticale en pointillés est le plafond, le point bleu est le GPU à l'instant. Trois presets : **Cautious 1850** (le point idéal avec le dissipateur d'origine, presque les mêmes images et dix degrés de moins), **Balanced 2000**, **Performance 2100** (la courbe à quinze points mesurée sur la carte de développement, celle que nous livrons).

**Appliquer est un essai.** Une courbe qui demande trop peu de tension bloque la carte, et sur la BC-250 un blocage se règle en débranchant. Appliquer lance donc la candidate en gardant l'ancienne courbe sur le disque et compte 25 secondes : appuyez sur Garder et la candidate est écrite pour de bon ; ne faites rien, ou la carte meurt et revient, et c'est l'ancienne courbe qui démarre.

Les panneaux s'ouvrent à la demande :

- **CPU** : fréquence, palier d'undervolt (6,25 mV chacun) et limite thermique, chacun avec un curseur et un champ numérique au pas de 1. *Suggérer UV* descend l'undervolt de deux paliers à la fois avec douze secondes de charge par palier ; *Trouver mon max* monte de 3600 à 4000 MHz ; *Test 60 s* charge les valeurs actuelles. Chaque essai affiche un compte à rebours et un bouton Stop ; les valeurs testées ne sont jamais écrites sur le disque, un blocage redémarre donc avec les précédentes. Au-dessus de 3500 MHz avec huit cœurs le gain est nul : c'est la chaleur qui commande.
- **Cœurs** : quels cœurs sont actifs, le SMT, le déblocage des 8 cœurs (6c/12t devient 8c/16t, +20 % mesuré) et *Avant le démarrage (EFI)* : le déblocage fait avant GRUB en un seul démarrage, au lieu du redémarrage supplémentaire du service dans le système.
- **CU** : les 40 unités de calcul en 20 cases (paires) : vert allumé, rouge éteint, gris gardé allumé par le pilote. Tapez le nombre de CU voulu (24 à 40, par paires) ou cliquez les cases ; *Test CU* allume les paires supplémentaires une à une sous vkpeak et signale les erreurs, pour la loterie du silicium.
- **VRAM** : le partage UMA dans la CMOS, appliqué au prochain démarrage. Avec les 512 Mo dynamiques certains jeux choisissent des textures basses : si elles sont floues, essayez 4 ou 6 Go fixes.
- **Avancé** : les réglages propres du governor : marge en montée, pas, confirmations en descente, seuils thermiques et de puissance, droop.
- **Test** : vkpeak et le journal de l'assistant.

## Moniteur

Un graphique par grandeur, chacun avec sa vraie échelle : températures (CPU, GPU, VRM, système, NVMe), fréquences (CPU moyenne, min, max, GPU et son plafond), charge, puissance, tensions, ventilateur et mémoire (RAM, VRAM, GTT), plus une barre par thread. Cliquez sur une entrée de la légende pour masquer une ligne ; survolez pour lire tous les graphiques au même instant. REC écrit un fichier `.sfmon` (CSV) qu'Ouvrir recharge avec un curseur ; CSV l'exporte pour un tableur.

## Jeux

- **Pilote Vulkan** : notre Mesa ouvre les files de calcul que le pilote d'origine garde fermées sur ce GPU : +4 % dans Cyberpunk 2077, +12 % avec FSR 4. Par lanceur (Steam, Heroic) via un override flatpak, ou pour tout le système. Il faut le noyau SkillFishOS : sur un autre noyau ces files bloquent le GPU, et l'interrupteur système refuse d'y démarrer. La carte affiche le noyau en cours.
- **Ordonnanceur** : scx_bpfland, chargé seulement pendant qu'un jeu tourne (GameMode le lance et l'arrête) : +1,5-2 % dans Cyberpunk et des images plus régulières. Si le noyau l'éjecte deux fois, le service s'arrête jusqu'à la remise à zéro du compteur : c'est la ligne « Éjecté par le noyau ».
- **FSR 4** : via OptiScaler sur le chemin DLSS du jeu. GE-Proton 11 télécharge OptiScaler tout seul quand il trouve `PROTON_USE_OPTISCALER=1`, le jeu doit être réglé sur DLSS, et la bibliothèque FSR 4 d'AMD (`amdxcffx64.dll`, du pilote Windows d'AMD) va à côté du jeu. XeSS, quand un jeu l'intègre, coûte autant que FSR 3 en 1080p.
- **Proton** : les versions GE-Proton 11 ; Installer en télécharge une (environ 500 Mo) dans les dossiers de Steam et Heroic, Par défaut la choisit. Steam doit être fermé pour que son défaut soit écrit.

## Ventilateur, profils et le reste

La page **Ventilateur** dessine la courbe dans le graphique des capteurs : à cette température le ventilateur tourne ainsi, avec une avance pour que la vitesse monte avant la température. Les **Profils** déplacent le plafond dans la courbe déjà en place et règlent ensemble CPU, preset du ventilateur et ordonnanceur. Les **Instantanés** sont des photos du système, vos fichiers ne sont pas touchés. **IA** garde la mémoire du GPU tant qu'elle est allumée : éteignez-la avant de jouer. **Console** lance Steam Big Picture dans gamescope par-dessus le bureau, ou comme session depuis l'écran de connexion. Le **Remote Manager** reprend les pages Tuner, Jeux et Profils dans un navigateur.
