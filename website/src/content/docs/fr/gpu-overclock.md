---
title: GPU, CPU, overclock et undervolt
description: Comment SkillFishOS pilote les fréquences, les tensions et les températures de la BC-250 — avec les vrais chiffres mesurés sur le matériel.
group: Système
order: 2
---

Sur un APU ordinaire on règle les fréquences par le sysfs d'`amdgpu`. Sur la BC-250 **cela ne marche pas** : la commande passe par la **SMU** (System Management Unit) et demande des outils dédiés. SkillFishOS les rassemble tous, préréglés avec une courbe sûre d'usine et un système de protection thermique.

> **Attention :** **loterie du silicium.** Chaque chiffre de cette page est **mesuré sur notre BC-250**. Chaque carte est différente : l'une acceptera une courbe plus poussée, l'autre moins. C'est pourquoi SkillFishOS **démarre avec la courbe d'usine** (profil **Performance**, plafond à 2100 MHz) et vous laisse la changer depuis le [Tuner](/fr/docs/control-center), qui vérifie chaque courbe **sur votre carte** avec un essai automatique de 25 secondes et revient en arrière tout seul si elle ne tient pas.

## La courbe tension/fréquence et les trois profils

![la courbe tension/fréquence dans le Tuner, avec le tableau des points et les trois profils](/img/control-center-tuner.png)

Le [Tuner](/fr/docs/control-center) pilote le GPU avec une **courbe tension/fréquence** : MHz à l'horizontale, millivolts à la verticale, des points qu'on tire sur le graphique ou qu'on saisit dans le tableau à côté. Trois profils déplacent le **plafond** de la courbe :

| Profil | Plafond GPU | Notes |
|---|---|---|
| **Cautious** | 1850 MHz | Le point d'équilibre avec le refroidissement d'origine : presque les mêmes images, dix degrés de moins |
| **Balanced** | 2000 MHz | Compromis entre fréquence et chaleur |
| **Performance** | 2100 MHz | La courbe à quinze points mesurée sur la carte de développement — celle que nous livrons par défaut |

**Appliquer est un essai, pas une écriture immédiate.** Une courbe qui demande trop peu de tension bloque la carte, et sur la BC-250 un blocage ne se résout qu'en coupant l'alimentation. C'est pourquoi Appliquer garde l'ancienne courbe sur le disque, essaie la candidate pendant **25 secondes** et attend une confirmation : appuyez sur Garder pour l'écrire pour de bon ; sinon — ou si la carte se bloque et redémarre toute seule — l'ancienne courbe revient au démarrage.

## Le gouverneur V/F du GPU

Les fréquences du GPU sont conduites par **skillfish-vf-governor**, notre service qui retire l'horloge et la tension au gouverneur d'usine et les pilote directement par la SMU, en tenant un **plafond de fréquence** que la chaleur et la consommation peuvent abaisser et, une fois la carte calmée, rendre. Un processus à part, **skillfish-vf-watchdog**, prend la main si le gouverneur plante avec l'horloge forcée.

Mesuré sur *Black Myth: Wukong*, même session, mêmes 84 °C dans les deux passages : **+4,5 %** sur carte froide, **+11 %** sur carte chaude, face au gouverneur d'usine. L'avantage grandit avec la température parce que le gouverneur d'usine cède de l'horloge en chauffant, et le nôtre non.

> Le sysfs habituel d'amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) ne commande **rien** sur la BC-250 — seul skillfish-vf-governor le fait. Le GPU ne monte au plafond que sous une vraie **saturation graphique**.

## Overclock et undervolt du CPU

Le CPU (**8 cœurs / 16 fils** Zen 2 « Oberon », dont deux déverrouillés par SkillFishOS via la SMU — aussi avant le démarrage, avec un programme EFI, en un seul redémarrage) est pris en charge pour l'overclock par un service à passage unique, **`bc250-smu-oc.service`**, qui applique les valeurs de `/etc/bc250-smu-oc.conf` grâce au projet [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Après application il apparaît comme *inactive* — c'est normal (il ne passe qu'une fois).

Ce que nous avons mesuré en poussant **notre** carte :

- **3700 MHz** avec undervolt à environ **1106 mV** (`scale −16`) ;
- **3900 MHz** à environ **1199 mV** (`scale −24`) ;
- **4,0 GHz** validés à environ **1224 mV** (`scale −36`) sur 120 s de charge continue, avec une pointe à **83 °C** — le maximum utilisable sur cet exemplaire ;
- **plafond dur de Vid : 1,325 V** (jamais dépassé).

L'**undervolt** n'est pas une manière de « pousser » : c'est faire le même travail avec **moins de chaleur et moins de consommation**. À une fréquence donnée, baisser la tension jusqu'à la limite de la stabilité fait tomber la température et laisse de la marge thermique au reste de l'APU.

### Le couplage thermique entre CPU et GPU

Le CPU et le GPU partagent le **même morceau de silicium** et le **même budget de puissance**. Sous une charge **mixte** (un jeu exigeant : CPU et GPU ensemble) l'APU se protège et le CPU redescend de lui-même vers **3450 MHz** pour rester dans le budget et sous 85 °C. **Ce n'est pas un défaut** : la puce se protège en abandonnant les mégahertz les moins utiles. Pour la même raison, un undervolt du CPU laisse plus de « place » thermique au GPU, et réciproquement.

## Les 40 unités de calcul — à chaud

La BC-250 a **40 CU** (20 paires), mais le pilote n'en active que **24** par défaut. SkillFishOS les mène à 40 **au démarrage, sans étape en plus** ; depuis le [Tuner](/fr/docs/control-center) vous ajustez le nombre **en direct**, en tapant la valeur voulue ou en cliquant sur les 20 cases appariées. Les 24 premières CU sont fixées par le pilote et restent toujours allumées.

Avec les 40 CU actives le GPU mesure **11385 GFLOPS** FP32 (vkpeak) à froid, contre environ **6141** avec les 24 de départ : **+85 %**. Sous charge continue (à chaud) il se stabilise vers **10214 GFLOPS**. La bande passante mémoire mesurée (clpeak) est d'environ **350–367 Go/s**.

> **Loterie du silicium.** Sur des puces récupérées ou « d'écart de tri », certaines CU peuvent être fragiles. Le [Tuner](/fr/docs/control-center) a un **« Test des CU »** qui met chaque paire sous charge avec vkpeak et signale les erreurs et les blocages du GPU, pour que vous soyez sûr que votre puce tient bien les 40. (Le mécanisme passe par `umr` et l'écriture des masques WGP — merci à [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), notre réécriture est indépendante.)

## La protection thermique — le plafond de 85 °C

La limite thermique est de **85 °C**, tenue à deux niveaux :

1. **du côté du gouverneur** : `gradi_max` et `watt_max` dans `/etc/skillfish-vf-governor.json` font baisser le plafond de fréquence *avant* de franchir 85 °C ou la limite de puissance (la nôtre, pas celle du micrologiciel), et le rendent une fois la carte calmée ;
2. **du côté du système** : **skillfish-vf-watchdog**, un processus à part qui prend la main si le gouverneur plante avec l'horloge forcée.

Ce qu'il faut savoir sur le refroidissement d'origine (voir aussi [Matériel BC-250](/fr/docs/hardware-bc250) pour les **boîtiers imprimables en 3D et les ventilateurs conseillés**) :

- le dissipateur d'origine est **juste** : comparer des mesures faites « à la suite » est faussé par la *chaleur accumulée* — laissez la carte refroidir quelques minutes entre les essais ;
- il n'y a que le capteur de *bord* du GPU ; **il n'existe pas de capteur de température pour la mémoire graphique** ;
- la bande passante mémoire est bonne, mais le `mclk` n'est **pas** réglable.

## Un cas réel : les jeux limités par le CPU

Certains titres — comme *Black Myth: Wukong* **en jeu** — sont limités par le **CPU et les appels de dessin** : les images par seconde ne dépendent presque ni de la définition ni de la fréquence du GPU. Là, ce qui aide c'est l'overclock du **CPU** et un bon refroidissement. Pour le rehaussement de définition, FSR 4 passe par [OptiScaler](https://github.com/optiscaler/OptiScaler) sur le chemin DLSS du jeu (voir [Jeux](/fr/docs/gaming)).

Quand la charge est **vraiment** limitée par le GPU (par exemple le *survol de caméra* de la mesure Wukong), le plafond de la courbe compte : dans le [Tuner](/fr/docs/control-center) montez le profil de Cautious ou Balanced vers **Performance** (2100 MHz), ou saisissez votre propre courbe. L'avantage mesuré sur Wukong face à l'ancien gouverneur d'usine est de **+4,5 % sur carte froide et +11 % sur carte chaude** : le gouverneur V/F ne cède pas d'horloge en chauffant, contrairement à celui d'usine. Il reste une limite physique infranchissable : **1129 mV**, le plafond de tension qu'amdgpu déclare pour ce GPU — aucune courbe ne peut le dépasser.

## Tout cela, sans terminal

Les fréquences, la courbe du GPU, le ventilateur et les unités de calcul se règlent depuis la fenêtre du **Tuner**, avec les trois profils du GPU prêts et un **essai automatique de 25 secondes qui revient à la courbe précédente** si votre carte ne la tient pas — voir [Control Center](/fr/docs/control-center). C'est la voie conseillée : commencez en Cautious, passez à Balanced ou Performance, et le Tuner vérifie tout sur **votre** BC-250.

## Sources

- skillfish-vf-governor — notre gouverneur V/F pour le GPU, commande SMU directe avec plafond réglable
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock et undervolt du CPU par la SMU
- [bc250.info](https://bc250.info) — les points sûrs et les notes thermiques de la communauté
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — mesures de FP32 et de bande passante mémoire
