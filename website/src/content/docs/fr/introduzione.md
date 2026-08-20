---
title: Introduction
description: Ce qu'est SkillFishOS, pourquoi il existe et à qui il s'adresse.
group: Introduction
order: 1
---

**SkillFishOS** est une distribution Linux pensée et réglée pour une carte bien particulière : l'**AMD BC-250**. C'est un système *PC-console* prêt à l'emploi — jeu, émulation, IA sur la machine et usage quotidien de bureau — bâti sur [Debian](https://www.debian.org/) et [KDE Plasma 6](https://kde.org/plasma-desktop/), avec une allure steampunk cohérente du démarrage jusqu'au bureau.

## La philosophie

La BC-250 est née comme carte de minage de cryptomonnaie et s'est retrouvée sur le marché de l'occasion à très bas prix. Sous le dissipateur, pourtant, il y a un **APU AMD semi-personnalisé** de la même famille de silicium que les consoles de cette génération : un CPU Zen 2, une partie graphique RDNA 2 et 16 Go de GDDR6. Avec le bon logiciel, cela devient un petit PC-console étonnamment capable.

Le problème, c'est que la faire bien tourner sous Linux demande des correctifs de noyau, un gouverneur de fréquence dédié, de l'overclock, des profils thermiques et une longue liste de contournements matériels. SkillFishOS existe pour **faire ce travail une fois pour toutes** et livrer un système qui *« s'allume et donne son meilleur »*, sans que l'utilisateur ait à toucher au terminal.

> SkillFishOS ne distribue ni jeux ni ROM : il fournit les **outils** (Steam, EmuDeck, émulateurs, interfaces). Le contenu, c'est vous qui l'ajoutez, légalement.

## À qui il s'adresse

Le projet est né d'un besoin concret et personnel : **faire utiliser et apprendre Linux aux enfants pendant qu'ils jouent**. Le jeu est la « carotte » qui les attire, et les **instantanés automatiques** de Btrfs sont le filet qui leur permet de bricoler sans craindre de casser le système — si quelque chose tourne mal, on revient en arrière en un clic depuis le menu de démarrage.

SkillFishOS convient donc bien :

- à qui possède une **BC-250** et veut jouer sans devenir expert du noyau Linux ;
- aux **familles** qui veulent une console bon marché qui soit aussi un PC pour apprendre ;
- aux **bricoleurs** qui préfèrent partir d'une base déjà réglée plutôt que de tout refaire depuis zéro.

## Ce qu'il y a dedans, en bref

- Un **noyau sur mesure** ([linux-tkg](https://github.com/Frogging-Family/linux-tkg)) avec les correctifs pour la BC-250 : 40 unités de calcul déverrouillées, fréquences libérées, gouverneur SMU dédié.
- Un **bureau KDE Plasma 6** en thème steampunk (icônes, curseurs, fond d'écran, affichage système).
- **Prêt à jouer** : Steam, [gamescope](https://github.com/ValveSoftware/gamescope), [EmuDeck](https://www.emudeck.com/), [ES-DE](https://es-de.org/), [Heroic](https://heroicgameslauncher.com/), Proton.
- **IA sur la machine** : [Unsloth Studio](https://unsloth.ai/) accéléré en Vulkan sur le GPU intégré — **5,1×** plus rapide que le CPU, mesuré.
- **Instantanés Btrfs** avec [Snapper](http://snapper.io/) et retour en arrière depuis le menu GRUB.
- **Applications natives** : le *Tuner* (piloter le matériel sans terminal) et le panneau *IA*.
- **Mises à jour dédiées et testées** depuis notre propre dépôt APT, pour que les mises à jour de Debian ne vous surprennent pas.

Les pages qui suivent détaillent chaque élément.

## Sources

- Documentation communautaire sur la BC-250 — [bc250.info](https://bc250.info)
- AMD BC-250 docs (elektricm) — [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- Debian — [debian.org](https://www.debian.org/)
- KDE Plasma — [kde.org/plasma-desktop](https://kde.org/plasma-desktop/)
