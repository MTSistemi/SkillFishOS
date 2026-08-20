---
title: Dépannage
description: Les problèmes les plus courants de la BC-250 et comment SkillFishOS les prend en charge.
group: Référence
order: 1
---

Beaucoup des « problèmes » de la BC-250 sont en réalité des défauts matériels connus que SkillFishOS contourne tout seul. Voici les plus courants.

## L'écran reste noir, l'écran n'est pas détecté

Le **Hot-Plug Detect (HPD) du DisplayPort est cassé** : la carte ne détecte pas le branchement d'un écran. SkillFishOS s'en occupe avec le service `skillfish-dp-hotswap` (qui force la détection au démarrage et à chaque changement d'écran) et le paramètre de noyau `video=DP-1:e`.

Ce qu'il faut vérifier :

- utilisez un **écran DisplayPort** ou un adaptateur DP→HDMI **passif** ;
- évitez les adaptateurs DP→HDMI **actifs** : en plus des soucis de détection, ils **cassent le son** (voir plus bas) ;
- si l'écran a changé, attendez quelques secondes : la détection est automatique mais pas immédiate.

## La carte ne se réveille pas de la veille

La mise en veille est **cassée au niveau matériel**. SkillFishOS la désactive complètement pour cette raison même (voir [Bureau](/fr/docs/desktop)). Si la carte paraît « morte » après un moment d'inactivité et que la gestion de l'énergie avait été modifiée, la seule sortie est une **réinitialisation physique**. Ne réactivez pas les états de veille.

## Pas de son depuis l'écran ou la télé

Le son par DisplayPort fonctionne, mais :

- les **adaptateurs DP→HDMI actifs** cassent le son : prenez des adaptateurs passifs, un écran DP natif, un **convertisseur audio USB** ou du son en **Bluetooth** ;
- la partie son repose sur **PipeWire** : la sortie par défaut se choisit dans les réglages audio de KDE.

## Les manettes ne marchent pas

- Les manettes **DualShock 4** passent en **Bluetooth** (avec le gyroscope). Pour appairer : maintenez *Share + PS* jusqu'au clignotement, puis appairez depuis l'interface Bluetooth.
- Une manette **en USB** doit être branchée avec un câble de **données** (pas seulement de charge) : elle est reconnue comme une Xbox 360.
- Les manettes clones partagent parfois mal l'adaptateur Bluetooth avec les DS4 : dans ce cas, utilisez-les **en USB**.

## Le GPU semble lent, les températures sont hautes

- Vérifiez dans le [Tuner](/fr/docs/app-native) que les **40 CU** et le gouverneur SMU sont actifs.
- Rappelez-vous que le refroidissement est juste : après une charge prolongée la **garde thermique** (85 °C) entre en jeu. Pour des mesures valables, laissez la carte refroidir entre les essais (voir [GPU](/fr/docs/gpu-overclock)).
- Pour les jeux **limités par le CPU**, baisser la définition ne fera pas monter les images par seconde.

## La carte s'est figée (blocage complet)

La BC-250 peut se **figer complètement**, souvent à cause d'un **undervolt trop agressif** : l'instabilité se manifeste surtout **à faible charge**, si bien qu'un blocage peut survenir même au repos. SkillFishOS s'y attaque sur deux fronts :

- **Chien de garde matériel** — le compteur **SP5100 TCO** du chipset est actif (`RuntimeWatchdogSec=2min`) : si le système se bloque complètement, la carte **redémarre d'elle-même** en moins de deux minutes, sans avoir à couper le courant.
- **Détecteur de blocage** — au démarrage un service remarque si l'arrêt précédent a été anormal (pas de marque d'arrêt propre) et l'**inscrit** dans `/var/log/skillfish-freeze.log`, avec une notification sur le bureau. Le compteur apparaît aussi dans le panneau **« Mon silicium »** du Tuner.

Si les blocages reviennent, **descendez d'un profil** (par exemple de Crazy ou Turbo à Performance) dans le Tuner : la valeur moins agressive est presque toujours la solution. Tous les profils sont **à l'épreuve des plantages** — un blocage en plein essai ne laisse jamais la carte sur un profil instable au redémarrage. Si cela persiste même en Stock, soupçonnez l'**alimentation**.

## Une mise à jour a cassé quelque chose

Redémarrez et, depuis le menu **GRUB → « SkillFishOS snapshots »**, choisissez un instantané précédent qui fonctionnait. Voir [Stockage et instantanés](/fr/docs/storage-snapshot). Les instantanés avant et après mise à jour sont automatiques.

## L'IA ne démarre pas, ou sort n'importe quoi

- L'IA tourne sur Vulkan (pas ROCm) et **ne doit pas s'utiliser en même temps que les jeux** (même GPU, même mémoire).
- Si la sortie est abîmée, assurez-vous d'utiliser le cache KV en **f16** (`q4_0` corrompt la sortie sur RADV). Voir [IA sur la machine](/fr/docs/ai-locale).

## Sources

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Arch Wiki — Gamepad](https://wiki.archlinux.org/title/Gamepad)
- [PipeWire — dépannage](https://docs.pipewire.org/)
