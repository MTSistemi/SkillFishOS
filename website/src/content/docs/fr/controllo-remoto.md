---
title: Commande à distance — Remote Manager
description: Le tableau de bord web de SkillFishOS pour piloter la BC-250 depuis un navigateur ou un téléphone — télémétrie, KVM, terminal, Tuner, logithèque et IA.
group: Utilisation
order: 4
---

**SkillFishOS Remote Manager** est un tableau de bord web modulaire qui permet de piloter la BC-250 **depuis un autre PC ou depuis votre téléphone**, sur le même réseau local ou — par ZeroTier — depuis n'importe où dans le monde. Vous vous connectez avec vos identifiants système, le tout en HTTPS.

## Installer

```bash
sudo apt update
sudo apt install skillfish-dashboard
```

Le paquet installe le service, l'application native **Remote Manager** (pour allumer ou éteindre le tableau de bord et choisir les modules) et toutes les pages web. Les dépendances facultatives (KVM, terminal, Wake-on-LAN) sont des *Recommends* et arrivent d'elles-mêmes quand elles sont disponibles.

## Activer

Ouvrez **SkillFishOS Remote Manager** depuis le menu des applications :

- **Interrupteur principal** — démarre le service (durable, par systemd).
- **Cases des modules** — choisissez ce que vous exposez (télémétrie, Tuner, Hub, KVM, terminal, IA…).
- Affiche l'**adresse, un QR code et les identifiants** pour se connecter.

Ou depuis un terminal : `sudo systemctl enable --now skillfish-dashboard`.

> Par prudence le tableau de bord **ne démarre pas tout seul** après l'installation — vous l'activez quand vous le voulez.

## Accéder

Ouvrez **`https://<adresse-de-la-carte>:8443`** dans votre navigateur (ou `https://BC-250.local:8443`). Comme le certificat est autosigné, le navigateur vous avertira la première fois — c'est normal, continuez.

Connectez-vous avec votre **nom d'utilisateur et votre mot de passe système** (les mêmes que pour SkillFishOS) : l'authentification passe par PAM.

## Les modules

Le tableau de bord se compose lui-même à partir des modules que vous avez activés :

- **Télémétrie** — courbes en direct des températures, des fréquences, des watts et de la charge du CPU et du GPU, avec les valeurs sur l'axe vertical et un panneau de barres montrant la **fréquence par cœur et par fil** (les 16 fils, ceux qui sont garés bien signalés).
- **État du système** — machine, adresse IP, noyau, temps de fonctionnement, mémoire, disque, CU actives, blocages détectés.
- **Commandes (Tuner)** — les profils rapides et le **Tuner complet** sur le web : CPU (fréquence, undervolt, température), GPU (fréquence, tension, gouverneur), **commande des unités de calcul à chaud** (grille de WGP, sans redémarrer), ventilateur, mémoire graphique, *Test* et les assistants **« Trouver mon maximum »**.
- **Applications et paquets (Hub)** — une vraie **logithèque** (AppStream + Flatpak + Snap) : parcourir par catégorie, chercher, installer, retirer, mettre à jour. Les **applications SkillFishOS** sont mises en avant en haut.
- **Bureau (KVM)** — voir et piloter le vrai bureau de la carte depuis le navigateur (noVNC), sans matériel en plus.
- **Terminal** — une ligne de commande web (ttyd) à l'intérieur du tableau de bord.
- **IA sur la machine** — l'état du moteur Unsloth, l'accélération Vulkan et une discussion avec le modèle local, qui tourne sur le GPU de la BC-250.
- **AI-Ops** — le modèle local lit les journaux et la télémétrie et pose le diagnostic à votre place.
- **Journaux**, **règles automatiques** (retour automatique en arrière au-delà d'un seuil de °C), **Wake-on-LAN** et allumage ou extinction programmés.
- **ZeroTier** — pour atteindre le tableau de bord **de n'importe où** (voir plus bas).

Les boutons **Redémarrer** et **Éteindre** sont toujours là, dans la barre du haut. Vous pouvez **fermer, rouvrir et déplacer** les cartes, et **enregistrer la disposition**.

## L'accès à distance (ZeroTier)

Le tableau de bord est prévu pour le **réseau local**. Pour vous en servir de l'extérieur, activez le module **ZeroTier** : rejoignez un de vos réseaux, autorisez la carte sur [my.zerotier.com](https://my.zerotier.com), puis atteignez le tableau de bord à l'adresse ZeroTier de la carte — sans ouvrir de port sur votre box.

## La sécurité

- **HTTPS** avec un certificat autosigné (TLS 1.2 et plus), créé au premier démarrage.
- **Connexion PAM** avec vos identifiants, **sessions signées** (HMAC) et **limitation du nombre d'essais**.
- Pensé pour le **réseau local** ; pour l'accès à distance, utilisez ZeroTier plutôt que de l'exposer directement sur Internet.
