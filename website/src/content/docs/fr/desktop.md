---
title: Bureau, thème et accès à distance
description: KDE Plasma 6, le thème steampunk, l'affichage système, la veille désactivée et l'accès à distance.
group: Système
order: 4
---

SkillFishOS utilise **[KDE Plasma 6](https://kde.org/plasma-desktop/)** comme environnement de bureau, habillé d'un thème steampunk cohérent et d'une série de réglages propres à la BC-250.

## Les sessions

À la connexion (gérée par **SDDM**, avec connexion automatique) plusieurs sessions sont disponibles :

- **KDE Plasma X11** — *par défaut*. Choisir X11 rend l'accès à distance immédiat (voir plus bas) ;
- **KDE Plasma Wayland** — au choix ;
- **Jeu** — une session [gamescope](https://github.com/ValveSoftware/gamescope) façon Big Picture (voir [Jeu](/fr/docs/gaming)).

## **Attention :** veille désactivée (essentiel)

La BC-250 a une **mise en veille ACPI cassée** : si elle s'endort, elle **ne se réveille pas** et il faut la réinitialiser (voir [matériel](/fr/docs/hardware-bc250)). C'est pourquoi SkillFishOS **désactive pour de bon** tous les états de veille :

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

À cela s'ajoutent une règle `logind` (`IdleAction=ignore`), le verrouillage automatique de l'écran désactivé et une gestion de l'énergie au repos « infini ». C'est une mesure **obligatoire** : une machine en veille est aussi une machine injoignable à distance.

## Le thème « SkillFish Steampunk »

L'allure est une palette coordonnée de laiton et de cuivre (accent **`#d8a849`**, surfaces sombres), cohérente **du démarrage au bureau** : thème GRUB, écran Plymouth, accueil SDDM, fond d'écran au poisson. Le paquet du thème contient :

- des **icônes** (`SkillFishSteampunk`, avec `breeze-dark` en secours) et des **curseurs** dédiés ;
- un style **Kvantum** pour les applications Qt et un jeu de **couleurs** KDE ;
- un **thème plasma**, un thème **Konsole**, des boutons de fenêtre et une **apparence globale** (`org.skillfish.steampunk`) ;
- des avatars assortis et une galerie au choix.

> Les thèmes **Breeze** d'origine restent installés comme secours porteur (ils fournissent notamment la fenêtre de déconnexion et d'extinction). Il ne faut pas les retirer.

## L'affichage système (Conky)

En haut à droite se trouve un **affichage** en laiton bâti avec **[Conky](https://github.com/brndnmtthws/conky)**, qui montre en temps réel : des barres par cœur du CPU avec les MHz, les °C et les watts, les MHz, la température et la mémoire du GPU, la mémoire vive, le disque, le ventilateur et les **appareils Bluetooth connectés** avec leur niveau de batterie (manettes, casques…). Les valeurs viennent d'assistants dédiés qui lisent directement les capteurs du matériel.

## L'accès à distance (x11vnc)

Comme la session par défaut est en X11, l'accès à distance est simple : SkillFishOS démarre **[x11vnc](https://github.com/LibVNC/x11vnc)** sur l'affichage actif et partage le vrai écran. Sur le réseau local, n'importe quel client VNC peut s'y connecter. Cela permet d'aider et de configurer depuis un autre PC, sans clavier ni souris physiques sur la carte.

## Réseau, son et applications

- **Réseau** : l'ethernet est géré par **NetworkManager**, donc visible et réglable depuis l'interface de Plasma.
- **Son** : toute la chaîne **[PipeWire](https://pipewire.org/)** (avec le Bluetooth). À noter : les adaptateurs DP→HDMI *actifs* peuvent casser le son — voir [Dépannage](/fr/docs/risoluzione-problemi).
- **Applications de base** : le gestionnaire de fichiers Dolphin, le terminal Konsole, le lecteur de PDF Okular, la visionneuse Gwenview, l'archiveur Ark, les captures Spectacle, la logithèque Discover (avec flatpak), le navigateur **Google Chrome**, **OnlyOffice**.
- **Applications natives de SkillFishOS** (regroupées sous le menu **« SkillFishOS »**, chacune installable et actualisable en `.deb` depuis le dépôt signé) : le **Tuner** (overclock, undervolt, ventilateur et CU de la BC-250), l'**IA** (LLM local à la demande sur le GPU intégré), le **Monitor** (courbes de température, fréquence, tension et ventilateur en direct), le **Gestionnaire de noyaux** (choisir le noyau de démarrage et désinstaller les anciens), **ISO Mount**, le **Hub** — la logithèque façon Discover (APT + Flatpak + Snap) avec fiches d'applications, carrousel de captures et gestion des sources — ainsi que **Base** (chien de garde matériel et détecteur de blocage avec notification) et **Console**, une session **« SkillFishOS Console (Big Picture) »** façon SteamOS, à choisir depuis l'écran de connexion.
- **Affichage** : un service (`skillfish-dp-hotswap`) s'occupe de la détection de l'écran, nécessaire parce que le HPD du DisplayPort est cassé.

## Sources

- [KDE Plasma](https://kde.org/plasma-desktop/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [Conky](https://github.com/brndnmtthws/conky) · [x11vnc](https://github.com/LibVNC/x11vnc)
- [PipeWire](https://pipewire.org/) · [SDDM](https://github.com/sddm/sddm)
- [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/) · [NetworkManager](https://networkmanager.dev/)
