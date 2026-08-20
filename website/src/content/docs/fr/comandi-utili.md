---
title: Commandes utiles
description: Un aide-mémoire du terminal pour examiner et régler SkillFishOS.
group: Référence
order: 4
---

SkillFishOS est fait pour **ne pas** avoir besoin du terminal : pour l'usage courant, le [Tuner](/fr/docs/app-native) et les applications graphiques suffisent. Cette page est pour qui veut **bricoler** ou chercher la panne. Les commandes privilégiées passent par `sudo`.

> Avant les expériences risquées, souvenez-vous du filet : les instantanés Btrfs et le retour en arrière depuis le menu GRUB (voir [Stockage et instantanés](/fr/docs/storage-snapshot)).

## Système et noyau

```bash
uname -r                      # le noyau en cours (doit finir par -skillfishos)
cat /proc/cmdline             # les paramètres de démarrage en vigueur
journalctl -b -p err          # les erreurs du démarrage actuel
inxi -Fxxxz                   # le récapitulatif complet du matériel
```

## GPU, fréquences et températures

```bash
# la température du GPU depuis le sysfs d'amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# l'état du gouverneur SMU
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # les points sûrs fréquence/tension
# suivre le GPU en temps réel
nvtop        # ou : radeontop
```

> Sur la BC-250 la commande de la fréquence ne passe **pas** par le sysfs habituel d'amdgpu, mais par le **gouverneur SMU**. Changez les valeurs depuis le [Tuner](/fr/docs/app-native), pas à la main.

## CPU — overclock et undervolt

```bash
systemctl status bc250-smu-oc.service   # qu'il soit « inactive » après application est normal (il ne passe qu'une fois)
cat /etc/bc250-smu-oc.conf              # la fréquence et la tension appliquées
lscpu | grep MHz                        # les fréquences actuelles des cœurs
sensors                                 # températures et tensions (nct6686, k10temp)
```

## Les unités de calcul à chaud (skillfish-cu)

```bash
skillfish-cu get          # l'état en JSON : CU actives et masque par rangée (SE/SH)
sudo skillfish-cu max     # mettre toutes les CU en service (40)
sudo skillfish-cu stock   # revenir à 24 (le minimum du pilote)
sudo skillfish-cu set 0x1f   # masque WGP pour toutes les rangées (0x07=24 … 0x1f=40)
cat /run/skillfish/cu_active # « 40/40 » (c'est ce que lit aussi l'affichage du bureau)
vulkaninfo | grep -i "deviceName\|driverName"   # le GPU tel que Vulkan le voit (RADV)
```

Les CU se manient plus commodément depuis la **grille** du [Tuner](/fr/docs/app-native) (clic et profils, avec le « Test des CU »). Les 24 premières sont fixées par le pilote et toujours allumées.

Des mesures rapides (les mêmes que celles du Tuner) :

```bash
vkpeak                # la performance FP32 (GFLOPS)
clpeak                # la bande passante mémoire (Go/s)
sysbench cpu run      # charge et mesure du CPU
```

## Mémoire unifiée (mémoire graphique et GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'ttm\.'   # les paramètres du GTT et de TTM
glxinfo | grep -i "memory"                                 # la mémoire vue par le pilote
free -h                                                     # la RAM/GDDR6 partagée
```

## Jeux

```bash
flatpak list                         # les applications Flatpak (Steam, émulateurs d'EmuDeck…)
flatpak update                        # mettre à jour les applications Flatpak
gamescope -- %command%               # (à mettre dans les options de lancement de Steam)
# manettes en Bluetooth
bluetoothctl                         # scan on / pair / connect / trust
```

## IA locale

```bash
# un seul service natif, pas de conteneurs : Docker n'est pas installé
systemctl status skillfish-unsloth   # l'état du moteur d'IA
sudo systemctl start skillfish-unsloth   # le démarrer
sudo systemctl stop skillfish-unsloth    # l'arrêter et libérer le GPU et la mémoire
curl -s localhost:8888/              # l'interface d'Unsloth Studio (interface locale seulement)
```

## Instantanés et retour en arrière (Btrfs)

```bash
sudo snapper list                    # lister les instantanés
sudo snapper create -d "avant X"     # un instantané à la main
sudo btrfs subvolume list /          # les sous-volumes (@, @home, @log, @cache, @games)

# revenir vraiment à un instantané (effectif dès le prochain démarrage)
sudo skillfish-rollback --list       # quels instantanés existent
sudo skillfish-rollback 12           # faire de l'instantané 12 le système en service
sudo skillfish-rollback --undo       # vous avez changé d'avis : remettre le précédent
sudo skillfish-rollback --clean      # enlever les systèmes mis de côté par les retours précédents

# depuis le menu GRUB → « SkillFishOS snapshots » vous atteignez le même instantané
# EN LECTURE SEULE : bon pour regarder et sauver des fichiers, ensuite lancez la commande ci-dessus
```

## Mises à jour et dépôt

```bash
sudo apt update && sudo apt full-upgrade   # mettre le système à jour
apt-mark showhold                          # les paquets retenus (noyau compris)
sudo apt install skillfishos-kernel        # installer ou mettre à jour le noyau depuis le dépôt
apt policy <paquet>                         # de quel dépôt et en quelle version vient un paquet
```

## Réseau et accès à distance

```bash
nmcli device status                  # l'état des interfaces réseau
ip a                                 # les adresses IP
systemctl status x11vnc              # le serveur VNC pour le bureau à distance
hostname -I                          # l'adresse à donner au client VNC
```

## Affichage (le HPD du DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # le service qui contourne le HPD cassé
xrandr                                   # sorties et définitions (session X11)
```

## Sources

- [Le wiki de Btrfs](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — une référence pour beaucoup de commandes Linux
