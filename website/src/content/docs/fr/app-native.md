---
title: Applications natives — Tuner et IA
description: Les outils graphiques de SkillFishOS pour piloter le matériel et l'IA sans terminal.
group: Utilisation
order: 3
---

SkillFishOS comprend deux applications natives (écrites en **PyQt6**, habillées avec Kvantum) qui mettent la commande du matériel et de l'IA entre les mains de l'utilisateur **sans toucher au terminal**.

## SkillFishOS Tuner

Le **Tuner** est le tableau de commande du matériel. Il permet de régler :

- l'**overclock et l'undervolt du CPU** ;
- les **points sûrs du GPU** (par le gouverneur SMU, voir [GPU et overclock](/fr/docs/gpu-overclock)) ;
- le **ventilateur** (commande PWM) ;
- la **mémoire graphique UMA** (demande un redémarrage) ;
- les **unités de calcul, à chaud** — voir plus bas.

### Les unités de calcul à chaud (la grille)

Le Tuner montre les CU du GPU comme une **grille de cases** (4 rangées SE/SH × 5 WGP) : **vert = active, rouge = éteinte**. On les bascule **à chaud, sans redémarrer** — en cliquant sur les paires (1 WGP = 2 CU) ou en utilisant les **profils 24 / 32 / 40 CU** — puis *Appliquer*. Les 24 premières CU sont le minimum du pilote et restent toujours allumées (voir [GPU et overclock](/fr/docs/gpu-overclock)).

![Le Tuner de SkillFishOS — la grille des unités de calcul à chaud, les profils et le test des CU](/img/tuner.jpg)

### Le test des CU (loterie du silicium)

Le bouton **« Tester les CU »** contrôle la santé des CU supplémentaires : il allume chaque paire seule, la met sous charge avec **vkpeak** et guette les **erreurs et les blocages du GPU**, puis termine par une charge sur les 40. Il est là pour repérer les **CU défectueuses** sur les APU récupérés ou « d'écart de tri », pour que vous sachiez si votre puce tient bien les 40 CU.

![Résultat du test des CU — toutes les paires correctes, 40 CU stables à 11380 GFLOPS, aucun défaut](/img/cu-test.jpg)

### Le déroulement d'un « Test » et le suivi en direct

Le déroulement d'un **« Test »** (CPU, GPU, CU, ventilateur) : appliquer un changement → lancer une mesure → **vérifier** la stabilité et, si quelque chose ne va pas, **revenir en arrière** tout seul. Dès qu'un test démarre, la fenêtre **[SkillFishOS Télémétrie](#skillfishos-télémétrie)** s'ouvre avec les courbes en direct de la **température, de la fréquence, de la tension et du ventilateur** (on peut la fermer à volonté).

![SkillFishOS Télémétrie pendant un test du Tuner — courbes en direct de température, fréquence, tension du GPU et ventilateur](/img/monitor.jpg)

Comment c'est bâti : une interface côté utilisateur plus un petit **service root** qui exécute les opérations privilégiées. Sur un PC personnel il est réglé pour ne pas demander de mot de passe à chaque opération. L'affichage sur le bureau montre lui aussi les **CU actives** en direct.

### Les modes du gouverneur : Équilibré et Performance

Le GPU de la BC-250 est piloté par un **gouverneur SMU** qui monte et descend la fréquence selon la charge. Le Tuner propose deux modes par un interrupteur :

- **Équilibré** *(par défaut)* — la fréquence redescend au repos (jusqu'à 350 MHz) et monte en charge : moins de consommation et de température à l'usage courant.
- **Performance** — le GPU **reste accroché à sa fréquence la plus haute** dès qu'il y a de la charge, ce qui supprime les petites oscillations. Sur notre mesure de *Black Myth: Wukong* cela vaut **+11 % d'images par seconde** (d'environ 100 à 111 de moyenne) et un **1 % bas** plus élevé (92 → 102), tout le reste égal.

Les deux restent sous le **plafond thermique de 85 °C** : le mode Performance pousse plus fort, il ne désactive pas les protections.

### Trouver mon maximum (les assistants CPU et GPU)

Chaque BC-250 est différente ([loterie du silicium](/fr/docs/gpu-overclock)). Le Tuner comprend deux assistants **« Trouver mon maximum »** qui dressent le portrait de **votre** carte :

- **GPU** — il monte marche après marche (2000 → 2200 MHz, par pas de 50 MHz), applique et **teste** chaque marche, et s'arrête à la dernière qui tient.
- **CPU** — il parcourt les marches de fréquence et d'undervolt (de 3600 MHz jusqu'à 4000 MHz à l'échelle −36) avec le même principe de **test et retour en arrière** : si une marche ne tient pas, il revient à la dernière bonne valeur.

Tout est **à l'épreuve des plantages** : la valeur inscrite sur le disque est toujours la dernière stable, si bien qu'un blocage en plein essai ne laisse jamais la carte sur un profil instable au démarrage suivant.

### Mon silicium

Le panneau **« Mon silicium »** résume le portrait de votre carte — meilleur CPU et meilleur GPU trouvés, CU en bonne santé, compteur de blocages détectés — et permet de **partager le résultat de façon anonyme** dans la base de la loterie du silicium (il ouvre une issue GitHub déjà remplie). Plus nous rassemblons de données, meilleurs deviennent les profils conseillés pour tout le monde.

## SkillFishOS Télémétrie

**Télémétrie** montre en temps réel la température, la fréquence, la charge du CPU et du GPU, les tensions, la consommation et le ventilateur. Elle s'ouvre d'elle-même pendant les tests du Tuner, mais c'est aussi une application à part entière. Le bouton **ENR** enregistre une séance de mesure dans un fichier **`.sfmon`** (dans `~/SkillFishOS-benchmarks/`) : rouvrez-le et Télémétrie devient un **analyseur** avec une barre de temps pour repasser la séance seconde par seconde.

![SkillFishOS Télémétrie — les courbes avec un axe gradué et le panneau de fréquence par cœur et par fil](/img/telemetry-percore.jpg)

### La fréquence par cœur et par fil

Avec [8 cœurs déverrouillés](/fr/docs/hardware-bc250) un seul chiffre de « fréquence du CPU » ne dit pas grand-chose : au repos les seize fils peuvent être à 800, 1775 et 3990 MHz **en même temps**, si bien que la valeur affichée dépend seulement du cœur qui a été relevé.

Le panneau du bas dessine **une barre par fil**, appariées par cœur physique et étiquetées `cœur·fil`. La couleur va du laiton à la braise à mesure que le fil monte, les MHz sont écrits sur chaque barre, et l'en-tête résume le **minimum, la moyenne, le maximum et le nombre de fils en service**. Les fils que vous avez garés depuis le Tuner ne disparaissent pas : ils restent en pointillé, marqués **« éteint »**, pour que la vraie configuration se voie d'un coup d'œil.

### Des axes lisibles

Chaque courbe a désormais une **grille avec les valeurs sur l'axe vertical**, calées sur des nombres ronds (`0 / 1000 / 2000 / 3000`, pas `-160 / 1394 / 2948`). Le zéro devient le plancher quand les données s'en approchent, si bien qu'une courbe de MHz ou de tours par minute ne montre jamais de base négative ; et une ligne plate n'est plus grossie au point de faire ressembler le bruit à une montagne.

## SkillFishOS IA

Le **panneau d'IA** allume et éteint le moteur LLM local en un clic, ce qui rend le GPU et la mémoire aux jeux quand on n'en a pas besoin. C'est la façade « facile » de ce qui est décrit dans [IA sur la machine](/fr/docs/ai-locale).

![Le panneau d'IA de SkillFishOS — moteur LLM local (Qwen3 14B) sur le GPU Vulkan, allumé et éteint en un clic](/img/ai-panel.jpg)

## Pourquoi elles existent

Le but de SkillFishOS est que **n'importe qui** — les plus jeunes compris — puisse utiliser et régler le système sans avoir à apprendre des commandes de terminal. Ces applications traduisent des opérations compliquées (gouverneur SMU, paramètres du noyau, instantanés et retour en arrière) en quelques clics, tout en gardant les **garde-fous** (garde thermique, test et retour en arrière) toujours actifs.

## Sources

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Le dépôt du projet — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)
