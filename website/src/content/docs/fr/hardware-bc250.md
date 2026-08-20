---
title: Le matériel AMD BC-250
description: La carte, l'APU, ses caractéristiques et ses défauts matériels connus.
group: Introduction
order: 2
---

L'**AMD BC-250** est une carte compacte bâtie autour d'un **APU semi-personnalisé** dont le nom de code est *Oberon* pour la partie CPU et *Cyan Skillfish* pour la partie graphique — la même famille de silicium que les consoles AMD de cette génération. Elle a été produite pour des machines de minage (souvent plusieurs cartes par châssis) et se retrouve aujourd'hui sur le marché de l'occasion à bas prix.

## Les caractéristiques principales

| Élément | Détail |
|---|---|
| **CPU** | 8 cœurs / 16 fils **Zen 2** (la carte en montre 6 ; SkillFishOS déverrouille les deux autres par la SMU) (« Oberon »), jusqu'à **3,9 GHz** (Turbo), 4,0 GHz validés |
| **GPU** | **RDNA 2** « Cyan Skillfish » (`gfx1013`), jusqu'à **40 unités de calcul** déverrouillables |
| **Mémoire** | **16 Go de GDDR6** partagés (UMA) entre le CPU et le GPU |
| **Calcul** | environ **11,3 TFLOPS** FP32 à 40 CU / 2000 MHz (mesuré avec vkpeak) |
| **Bande passante mémoire** | environ 350–367 Go/s (mesurée avec clpeak) |
| **Sortie vidéo** | 1× DisplayPort |

La mémoire est **unifiée** : la GDDR6 est partagée entre le système et la partie graphique. Par défaut environ 8 Go sont attribués comme mémoire graphique, mais sous Linux l'espace vidéo peut être agrandi par le **GTT** (Graphics Translation Table), ce qui fait voir à Vulkan environ 13 Gio de mémoire — particulièrement utile pour les modèles d'IA.

## Le déverrouillage des 8 cœurs du CPU

La carte se présente avec **6 cœurs / 12 fils**, mais il y a **huit** cœurs physiques : les deux qui manquent ne sont pas défectueux, ils sont éteints par la configuration du produit. Le masque de présence des cœurs le trahit — sur pratiquement toutes les cartes il vaut `0x77`, une valeur **symétrique** : quatre cœurs par complexe avec le quatrième désactivé des deux côtés. Un vrai tri de fabrication laisserait un motif asymétrique, parce que les défauts ne se répartissent pas aussi proprement.

SkillFishOS réécrit ce masque par la **SMU** au démarrage et la carte revient en **8 cœurs / 16 fils**. Pas de BIOS modifié, pas de soudure.

Deux garde-fous sont dans le service : si le masque n'est **pas** `0x77` il ne touche à rien, car un autre motif peut vouloir dire que des cœurs ont vraiment été désactivés en usine ; et le redémarrage à chaud n'arrive **qu'après** que l'écriture a été relue et confirmée, si bien qu'il ne peut pas partir en boucle de redémarrage.

> Mesuré sur notre propre carte : **+20 %** sur les charges multifils. Sur les charges qui n'utilisent que quelques fils cela ne change rien, comme on pouvait s'y attendre — deux cœurs de plus ne font pas courir un fil unique plus vite.

La rétro-ingénierie est celle de [bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock) : sans ce travail, cette fonction n'existerait pas.

## Le déverrouillage des 40 CU

Le GPU a 40 CU mais le pilote n'en active que **24** par défaut. SkillFishOS les **met en route jusqu'à 40 à chaud** (sans redémarrage) : il démarre au minimum du pilote et un service passe à 40 au démarrage, réglable depuis le [Tuner](/fr/docs/app-native). La rétro-ingénierie du déverrouillage est documentée par [bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock) ; la commande à chaud par `umr` s'inspire de [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager) (réécriture indépendante).

> Avec 40 CU actives, SkillFishOS mesure **11385 GFLOPS** FP32 (vkpeak) à froid, contre environ 6141 pour une configuration de départ à 24 CU : environ **+85 %**.

## Les défauts matériels à connaître

La BC-250 est du matériel de « minage » détourné : elle a quelques limites que SkillFishOS contourne par le logiciel. Les connaître explique beaucoup des choix du système.

### Le Hot-Plug Detect (HPD) du DisplayPort cassé

La détection du branchement d'un écran sur le connecteur DisplayPort **ne marche pas** : la carte ne « voit » pas qu'on branche un écran. SkillFishOS règle cela avec un service dédié (`skillfish-dp-hotswap`) qui force la détection au démarrage et guette les changements d'écran ensuite, plus le paramètre de noyau `video=DP-1:e` en secours. Voir [Bureau](/fr/docs/desktop) et [Dépannage](/fr/docs/risoluzione-problemi).

### La mise en veille ACPI cassée

La mise en veille (**s2idle est cassé**) : la carte s'endort mais **ne se réveille pas** et il faut la réinitialiser. Une machine en veille est aussi une machine injoignable à distance. C'est pourquoi SkillFishOS **désactive pour de bon** tous les états de veille (voir [Bureau](/fr/docs/desktop)). C'est une mesure obligatoire.

### L'IOMMU inutilisable

L'IOMMU de la BC-250 est instable : elle **ne doit jamais être activée**. Le système démarre toujours sans IOMMU.

### Les capteurs de température

Seul le capteur de température de *bord* du GPU est disponible ; **il n'y a pas de capteur pour la mémoire graphique**. Le refroidissement d'origine est juste, si bien que comparer des mesures faites à la suite n'a pas de sens (effet de *chaleur accumulée*) : laissez la carte refroidir quelques minutes entre les essais.

## Refroidissement, boîtiers imprimables en 3D et ventilateurs

La BC-250 arrive **nue**, prévue pour des racks de minage avec cinq ventilateurs *hurleurs* de 80 mm alimentés par le connecteur de distribution. Un usage de bureau demande un refroidissement dédié. **Deux choses sont à refroidir** : le dissipateur de l'APU **et** les puces de **GDDR6**, qui chauffent beaucoup et n'ont aucun capteur de température (voir [GPU et overclock](/fr/docs/gpu-overclock)).

**Ce qui marche (les conseils de la communauté) :**

- **2 ventilateurs de 120 mm à forte pression statique** dirigés sur le dissipateur, c'est le montage de bureau le plus courant ; sans boîtier on peut les poser directement sur le dissipateur (avec des colliers passés dans les ailettes).
- Un **ventilateur dédié à la mémoire graphique** est vivement conseillé si vous overclockez : les modules GDDR6 sont l'endroit le plus chaud.
- Le ventilateur se branche sur le connecteur **PWM 4 broches** de la carte — SkillFishOS le pilote par `nct6686` (les capteurs) et le laisse en **automatique**.

**Boîtiers et conduits (fichiers STL gratuits, imprimables en 3D) :**

| Modèle | Auteur | Notes |
|---|---|---|
| [Console Style Case](https://www.thingiverse.com/thing:7172528) | Arthrimus | Boîtier « console » avec baie d'alimentation, capot pour **1× 120 mm** |
| [ASRock BC-250 Shell Case](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case) | onemorecap | Coque à clipser, montage rapide d'un seul ventilateur |
| [Yet Another BC-250 Fan Shroud](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud) | ViRazY | Entrée en **140 mm** et sortie en **120 mm** |
| [Case ATX PSU & Fan Duct](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct) | ZMASLO | Utilise une alimentation ATX standard, conduit qui n'abîme pas le refroidisseur |
| [Boîtier pour alimentation ATX standard](https://www.thingiverse.com/thing:7269520) | CatSiewDai | Boîtier complet pour alimentations ATX |
| [OC vRAM Fan Kit (remix)](https://www.thingiverse.com/thing:7271946) | marccyberwiz | Ventilateur **dédié à la mémoire graphique** pour l'overclock |
| [NexGen3D — DIY Steam Machine (Bazzite)](https://www.printables.com/model/1499974-nexgen3d-diy-steam-machine-powered-by-bazzite) | NexGen3D | Boîtier complet façon **Steam Machine** pour la BC-250 |
| [NexGen3D — Steam Machine PRO (refroidissement liquide)](https://www.printables.com/model/1614131-nexgen3d-diy-steam-machine-pro-liquid-cooled-bc-25/files) | NexGen3D | Version **PRO en refroidissement liquide** (AIO) — le maximum |
| [NexGen3D — support AIO pour la BC-250](https://www.printables.com/model/1554003-nexgen3d-aio-mount-for-the-bc-250) | NexGen3D | Support pour monter un **AIO** (refroidisseur liquide) sur la BC-250 |

> Guide de référence sur le refroidissement : [Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/).

## Sources

- [bc250.info](https://bc250.info) — le wiki de la communauté
- [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) — documentation technique (dont le [refroidissement](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/))
- [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation) — notes sur le matériel et le refroidissement
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — le déverrouillage des unités de calcul
- [bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg) — la configuration de la mémoire
- Le pilote noyau Linux `amdgpu` — [docs.kernel.org/gpu/amdgpu](https://docs.kernel.org/gpu/amdgpu/)
