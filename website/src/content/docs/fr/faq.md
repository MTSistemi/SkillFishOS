---
title: Questions fréquentes (FAQ)
description: Les questions les plus courantes sur SkillFishOS et la BC-250, avec des réponses brèves.
group: Référence
order: 2
---

Des réponses rapides aux questions les plus courantes. Pour aller plus loin, chaque réponse renvoie à la bonne page.

## Généralités

**Qu'est-ce que SkillFishOS ?**
Une distribution Linux (Debian + KDE Plasma 6) pensée et réglée pour la carte **AMD BC-250** : jeu, émulation, IA locale et usage de bureau, tout préconfiguré. Voir [Introduction](/fr/docs/introduzione).

**Sur quel matériel tourne-t-il ?**
La carte pour laquelle il est fait est l'**AMD BC-250** (APU Zen 2 + RDNA 2 « gfx1013 », 16 Go de GDDR6), et c'est là qu'il fait tout ce dont il est capable : 40 unités de calcul déverrouillées, gouverneur SMU, huit cœurs. Il existe aussi une édition **Générique x86-64** qui tourne sur n'importe quel PC ou machine virtuelle — un noyau ordinaire, où les morceaux propres à la carte se cachent au lieu d'échouer. Voir [Matériel BC-250](/fr/docs/hardware-bc250).

**Combien coûte-t-il ? Est-il libre ?**
Il est **gratuit**. Il assemble des logiciels libres venus de nombreuses communautés ; le code du projet est sur [GitHub](https://github.com/MTSistemi/SkillFishOS). Voir [Sources](/fr/docs/fonti).

**Contient-il des jeux, des ROM ou des BIOS ?**
Non. SkillFishOS fournit les **outils** (Steam, EmuDeck, émulateurs, interfaces) ; le contenu, c'est vous qui l'ajoutez, légalement. Voir [Jeu](/fr/docs/gaming).

## Installation

**Comment l'installer ?**
Écrivez l'ISO sur une clé USB et démarrez l'installateur graphique **Calamares**. Tout à la souris. Voir [Installation](/fr/docs/installazione).

**Puis-je l'essayer sans l'installer ?**
Oui : l'image est **live**, vous pouvez explorer le bureau avant d'installer.

**Est-ce qu'il efface mon disque ?**
L'installation automatique (« Effacer le disque ») oui. Pour conserver des données existantes, utilisez le partitionnement manuel. SkillFishOS utilise **Btrfs** avec des sous-volumes séparés : `@` pour le système, `@home` pour vos données, et en plus `@cache`, `@log` et `@games`.

**Faut-il une connexion à Internet ?**
Pas pour installer ; il en faudra une ensuite pour Steam, les mises à jour et l'IA.

## Performances et overclock

**Pourquoi démarre-t-il « lentement », en Stock ?**
Par sécurité : chaque BC-250 est différente (*loterie du silicium*). On monte de profil depuis le **[Tuner](/fr/docs/app-native)**, qui vérifie tout sur votre carte. Voir [GPU et overclock](/fr/docs/gpu-overclock).

**L'overclock est-il dangereux ?**
Le Tuner applique un profil, le **teste** et **revient en arrière** si la carte ne tient pas ; le plafond de 85 °C et la garde thermique sont toujours actifs. C'est conçu pour être sûr.

**Combien d'images par seconde dans le jeu X ?**
Ça dépend : certains jeux sont **limités par le CPU** (par exemple *Black Myth: Wukong*) et ne suivent pas le GPU. Voir [Performances et mesures](/fr/docs/prestazioni).

**Puis-je utiliser FSR 4 ?**
Non, il demande du matériel RDNA 4. Utilisez gamescope (FSR1/NIS) ou OptiScaler. Voir [Jeu](/fr/docs/gaming).

## Au quotidien

**Pourquoi l'écran est-il parfois noir ?**
Le **HPD du DisplayPort est cassé** sur la BC-250 : SkillFishOS le contourne avec un service dédié. Utilisez un écran DP ou un adaptateur **passif**. Voir [Dépannage](/fr/docs/risoluzione-problemi).

**Pourquoi n'y a-t-il pas de son sur la télé ?**
C'est souvent un adaptateur DP→HDMI **actif** : prenez-en un passif, un écran DP, un convertisseur audio USB ou du son en Bluetooth.

**Puis-je mettre le PC en veille ?**
Non. La **mise en veille est cassée** au niveau matériel et la carte ne se réveille pas : SkillFishOS la désactive exprès. **Ne la réactivez pas.** Voir [Bureau](/fr/docs/desktop).

**Puis-je m'en servir depuis un autre ordinateur ?**
Oui : la session par défaut est en X11 et **x11vnc** tourne, vous pouvez donc piloter le bureau en VNC sur le réseau local. Voir [Bureau](/fr/docs/desktop).

## IA locale

**Quel modèle d'IA puis-je utiliser ?**
Le moteur est **Unsloth Studio** sur **Vulkan** (pas ROCm, qui ne prend pas en charge gfx1013), et les modèles sont des fichiers GGUF venus de Hugging Face. Mesuré sur la carte : **210,7 jetons/s** en génération contre 41,5 sur le CPU. Voir [IA sur la machine](/fr/docs/ai-locale).

**Puis-je jouer pendant que l'IA tourne ?**
Non : l'IA et les jeux lourds se partagent le GPU et la mémoire. Éteignez l'IA avant de jouer.

## Mises à jour

**Comment mettre le système à jour ?**
`sudo apt update && sudo apt full-upgrade` ou l'application **Discover**. Un instantané est pris tout seul avant et après chaque mise à jour. Voir [Mises à jour](/fr/docs/aggiornamenti).

**Une mise à jour a cassé quelque chose — et maintenant ?**
Redémarrez et choisissez un instantané dans **GRUB → « SkillFishOS snapshots »**. Voir [Stockage et instantanés](/fr/docs/storage-snapshot).

**Est-ce que Debian met le noyau à jour ?**
Non : le noyau de SkillFishOS est **retenu** (`apt-mark hold`) et n'est mis à jour que depuis notre dépôt, après essais. Voir [Noyau](/fr/docs/kernel).

## Le projet

**Puis-je contribuer ou signaler un bogue ?**
Oui, par les **Issues** sur [GitHub](https://github.com/MTSistemi/SkillFishOS/issues).

**Où télécharger l'ISO ?**
Depuis la page [Téléchargement](/fr/download) (hébergée sur SourceForge).
