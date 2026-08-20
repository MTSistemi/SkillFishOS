---
title: GPU, CPU, overclock et undervolt
description: Comment SkillFishOS pilote les fréquences, les tensions et les températures de la BC-250 — avec les vrais chiffres mesurés sur le matériel.
group: Système
order: 2
---

Sur un APU ordinaire on règle les fréquences par le sysfs d'`amdgpu`. Sur la BC-250 **cela ne marche pas** : la commande passe par la **SMU** (System Management Unit) et demande des outils dédiés. SkillFishOS les rassemble tous, préréglés avec des profils sûrs et un système de protection thermique.

> **Attention :** **loterie du silicium.** Chaque chiffre de cette page est **mesuré sur notre BC-250**. Chaque carte est différente : l'une acceptera un undervolt plus profond, l'autre moins. C'est pourquoi SkillFishOS **démarre toujours sur le profil Stock** et vous laisse monter par le [Tuner](/fr/docs/app-native), qui vérifie chaque profil **sur votre carte** avec un essai automatique et un retour en arrière.

## Les quatre profils

Le [Tuner](/fr/docs/app-native) propose **quatre profils**. L'image démarre en **Stock** ; les autres sont à un clic après l'essai.

| Profil | CPU | GPU | Notes |
|---|---|---|---|
| **Stock** *(par défaut dans l'image)* | 3500 MHz | 1500 MHz | Compatibilité maximale sur n'importe quelle BC-250 |
| **Performance** | 3700 MHz · ~1106 mV | 2000 MHz | Équilibré et avec undervolt |
| **Turbo** | 3900 MHz · ~1199 mV | 2230 MHz | Montée forte, validée sous le plafond de 85 °C |
| **Crazy** | 4,0 GHz · ~1224 mV | 2230 MHz | Le maximum validé (~83 °C en charge) |

Tous les profils respectent le même **plafond thermique de 85 °C** et laissent le **ventilateur en automatique**.

## Le gouverneur SMU du GPU

Les fréquences du GPU sont conduites par le **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (écrit en Rust), un service du système qui se règle dans `/etc/cyan-skillfish-governor/config.toml`. Il définit des *points sûrs* de fréquence et de tension : **350 MHz / 700 mV** au repos, et la valeur du profil en charge (par exemple 1500/900 en Stock, 2230/1000 en Turbo).

> Le sysfs habituel d'amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) ne commande **rien** sur la BC-250 — seul le gouverneur SMU le fait. Le GPU ne monte à sa fréquence maximale que sous une vraie **saturation graphique**.

## Overclock et undervolt du CPU

Le CPU (**8 cœurs / 16 fils** Zen 2 « Oberon », dont deux déverrouillés par SkillFishOS via la SMU) est pris en charge par un service à passage unique, **`bc250-smu-oc.service`**, qui applique les valeurs de `/etc/bc250-smu-oc.conf` grâce au projet [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Après application il apparaît comme *inactive* — c'est normal (il ne passe qu'une fois).

Ce que nous avons mesuré en poussant **notre** carte :

- **3700 MHz** (profil *Performance*) avec undervolt à environ **1106 mV** (`scale −16`) ;
- **3900 MHz** (profil *Turbo*) à environ **1199 mV** (`scale −24`) ;
- **4,0 GHz** (profil *Crazy*) validés à environ **1224 mV** (`scale −36`) sur 120 s de charge continue, avec une pointe à **83 °C** — le maximum utilisable sur cet exemplaire ;
- **plafond dur de Vid : 1,325 V** (jamais dépassé).

L'**undervolt** n'est pas une manière de « pousser » : c'est faire le même travail avec **moins de chaleur et moins de consommation**. À une fréquence donnée, baisser la tension jusqu'à la limite de la stabilité fait tomber la température et laisse de la marge thermique au reste de l'APU.

### Le couplage thermique entre CPU et GPU

Le CPU et le GPU partagent le **même morceau de silicium** et le **même budget de puissance**. Sous une charge **mixte** (un jeu exigeant : CPU et GPU ensemble) l'APU se protège et le CPU redescend de lui-même vers **3450 MHz** pour rester dans le budget et sous 85 °C. **Ce n'est pas un défaut** : la puce se protège en abandonnant les mégahertz les moins utiles. Pour la même raison, un undervolt du CPU laisse plus de « place » thermique au GPU, et réciproquement.

## Les 40 unités de calcul — à chaud

La BC-250 a **40 CU** (20 WGP, 1 WGP = 2 CU), mais le pilote n'en active que **24** par défaut. SkillFishOS les mène jusqu'à 40 **à chaud, sans redémarrage** : le système démarre au minimum du pilote (24 CU) et un service le porte à 40 au lancement ; depuis le [Tuner](/fr/docs/app-native) vous ajustez le nombre **en direct**, avec une grille de cases et les profils 24/32/40. Les 24 premières CU sont fixées par le pilote et restent toujours allumées.

Avec les 40 CU actives le GPU mesure **11385 GFLOPS** FP32 (vkpeak) à froid, contre environ **6141** avec les 24 de départ : **+85 %**. Sous charge continue (à chaud) il se stabilise vers **10214 GFLOPS**. La bande passante mémoire mesurée (clpeak) est d'environ **350–367 Go/s**.

> **Loterie du silicium.** Sur des puces récupérées ou « d'écart de tri », certaines CU peuvent être fragiles. Le [Tuner](/fr/docs/app-native) a un **« Test des CU »** qui met chaque paire sous charge et signale les erreurs et les blocages du GPU, pour que vous soyez sûr que votre puce tient bien les 40. (Le mécanisme passe par `umr` et l'écriture des masques WGP — merci à [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), notre réécriture est indépendante.)

## La protection thermique — le plafond de 85 °C

La limite thermique est de **85 °C**, tenue à deux niveaux :

1. **du côté de la SMU** : la valeur `max_temperature` dans la configuration fait baisser les fréquences à la puce *avant* de franchir 85 °C (sans bridage brutal) ;
2. **du côté du système** : un veilleur, le **thermal-guard**, qui descend les fréquences par pas de 100 MHz si le plafond est dépassé, jusqu'au retour dans les clous.

Ce qu'il faut savoir sur le refroidissement d'origine (voir aussi [Matériel BC-250](/fr/docs/hardware-bc250) pour les **boîtiers imprimables en 3D et les ventilateurs conseillés**) :

- le dissipateur d'origine est **juste** : comparer des mesures faites « à la suite » est faussé par la *chaleur accumulée* — laissez la carte refroidir quelques minutes entre les essais ;
- il n'y a que le capteur de *bord* du GPU ; **il n'existe pas de capteur de température pour la mémoire graphique** ;
- la bande passante mémoire est bonne, mais le `mclk` n'est **pas** réglable.

## Un cas réel : les jeux limités par le CPU

Certains titres — comme *Black Myth: Wukong* **en jeu** — sont limités par le **CPU et les appels de dessin** : les images par seconde ne dépendent presque ni de la définition ni de la fréquence du GPU. Là, ce qui aide c'est l'overclock du **CPU** et un bon refroidissement. Pour le rehaussement de définition, FSR 4 **n'est pas disponible** (il demande du matériel RDNA 4) ; utilisez gamescope (FSR1/NIS) ou [OptiScaler](https://github.com/optiscaler/OptiScaler) jeu par jeu.

Quand la charge est **vraiment** limitée par le GPU (par exemple le *survol de caméra* de la mesure Wukong), la fréquence compte : dans le **Tuner** vous pouvez mettre le **gouverneur en « Performance »**, qui maintient le GPU à son point sûr le plus haut en charge (au repos il redescend quand même à 350 MHz). Mesuré sur le test Wukong : **100 → 111 images par seconde en moyenne (+11 %)**, 92 → 102 sur les images les plus lourdes. Par prudence le Tuner limite le GPU à **2200 MHz sous 1000 mV** (le maximum stable avec le refroidissement d'origine) avec une courbe de tension à plusieurs points : 2230 MHz sous 1000 mV, c'est déjà en dessous de la tension nécessaire, et la machine peut se figer complètement.

## Tout cela, sans terminal

Les fréquences, l'undervolt, le ventilateur et les unités de calcul se règlent depuis la fenêtre du **Tuner**, avec les quatre profils prêts et un **essai automatique suivi d'un retour en arrière** si votre carte ne tient pas une valeur — voir [Applications natives](/fr/docs/app-native). C'est la voie conseillée : commencez en Stock, passez à Performance, essayez Turbo ou Crazy, et le Tuner vérifie tout sur **votre** BC-250.

## Sources

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — le gouverneur SMU du GPU
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock et undervolt du CPU par la SMU
- [bc250.info](https://bc250.info) — les points sûrs et les notes thermiques de la communauté
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — mesures de FP32 et de bande passante mémoire
