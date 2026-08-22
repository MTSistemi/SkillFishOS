---
title: Le noyau sur mesure
description: Le noyau linux-tkg corrigé pour la BC-250, les paramètres de démarrage et les noyaux à éviter.
group: Système
order: 1
---

Le cœur des optimisations de SkillFishOS est un **noyau construit sur mesure** pour la BC-250, fondé sur [linux-tkg](https://github.com/Frogging-Family/linux-tkg) — une recette de compilation de la *Frogging Family* qui applique des correctifs tournés vers la performance et le jeu.

## Version et correctifs

Le noyau de SkillFishOS est en version **`7.2.0-skillfishos`** (les séries 7.0 et 7.1 sont arrivées en fin de vie). En plus des correctifs habituels de linux-tkg il contient :

- le correctif de **déverrouillage des fréquences** de la BC-250 (plage 350–2230 MHz) ;
- le correctif des **40 CU**, qui active toutes les unités de calcul du GPU ;
- un correctif maison **RDSEED-quiet**, qui fait taire un message bavard du noyau sur ce matériel.

Le paquet du noyau (image et en-têtes) est publié comme version et il est **retenu** (`apt-mark hold`), pour qu'une mise à jour de Debian ne puisse pas le remplacer par un noyau inadapté. C'est le noyau par défaut dans GRUB.

## Les paramètres de démarrage (cmdline)

La ligne de commande du noyau est réglée ainsi, et chaque paramètre a une raison précise :

```
mitigations=off
split_lock_detect=off
ttm.pages_limit=1572864
ttm.page_pool_size=1572864
```

| Paramètre | Ce qu'il fait |
|---|---|
| `mitigations=off` | désactive les protections Spectre et Meltdown pour tirer le maximum de performance (un choix acceptable sur une console de salon) |
| `ttm.pages_limit` / `ttm.page_pool_size` | le plafond du GTT, compté en pages de 4 Kio : 1572864 = 6 Gio, si bien que Vulkan voit environ 13 Gio entre mémoire graphique et GTT (utile pour l'IA). C'était autrefois `amdgpu.gttsize`, abandonné depuis le noyau 7.x : si les deux sont donnés, le pilote obéit à celui-ci et le dit à chaque démarrage |
| `split_lock_detect=off` | désactive le détecteur de *split lock*, qui sinon bride les processus faisant des accès atomiques mal alignés (les jeux et les émulateurs en font) |

> **Et le DisplayPort ?** Le HPD de la BC-250 est cassé (voir [matériel](/fr/docs/hardware-bc250)), mais SkillFishOS n'utilise **pas** le paramètre `video=DP-1:e` : le service `skillfish-dp-hotswap` surveille l'EDID et réactive la sortie quand l'écran revient. Cela couvre aussi le cas où l'on allume l'écran après la carte, ce que le paramètre seul ne fait pas.

> **Les unités de calcul à chaud.** SkillFishOS n'utilise plus le paramètre `amdgpu.bc250_cc_write_mode=3` (qui fixait 40 CU au démarrage et empêchait tout changement ensuite). Le système démarre maintenant au minimum du pilote (24 CU) et un service met les **40 CU en route à chaud** au démarrage ; vous pouvez les changer sans redémarrer depuis le [Tuner](/fr/docs/app-native). Voir [GPU et overclock](/fr/docs/gpu-overclock).

## Les noyaux à éviter

Tous les noyaux récents ne se comportent pas bien sur ce matériel. Les séries **6.15.0–6.15.6** et **6.17.8–6.17.10** en particulier sont connues comme problématiques et sont à éviter. SkillFishOS livre son propre noyau essayé précisément pour éviter ces régressions — voir [Mises à jour](/fr/docs/aggiornamenti).

## L'IOMMU

Comme indiqué sur la page [matériel](/fr/docs/hardware-bc250), l'**IOMMU ne doit jamais être activée** sur la BC-250 : elle est instable. Le noyau démarre toujours avec l'IOMMU désactivée.

## Pourquoi notre propre noyau plutôt que XanMod ou celui d'origine

- Le **noyau d'origine de Debian** n'a pas les correctifs pour la BC-250 (déverrouillage des fréquences, 40 CU) et suit les régressions citées plus haut.
- **linux-tkg** facilite l'application des correctifs maison et le choix d'ordonnanceurs et d'options tournés vers le jeu.
- Le construire nous-mêmes veut dire que nous ne mettons le noyau à jour **que lorsqu'une version nouvelle apporte quelque chose de réel**, et après l'avoir essayée sur le matériel.

## Sources

- [linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)
- [Les paramètres du pilote amdgpu](https://docs.kernel.org/gpu/amdgpu/module-parameters.html)
- [bc250.info](https://bc250.info) — notes sur le noyau et la ligne de commande
