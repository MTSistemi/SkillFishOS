---
title: Prise en main
description: Vos 10 premières minutes avec SkillFishOS — du premier démarrage à la première partie.
group: Introduction
order: 3
---

Vous avez installé SkillFishOS (voir [Installation](/fr/docs/installazione)) et vous en êtes au premier démarrage. Cette page est une **liste rapide** pour partir tout de suite : tout le reste est déjà configuré et fonctionne.

## En une ligne

> On allume → on est déjà sur le bureau réglé → on branche une manette → on ajoute ses jeux → on joue. Pas de terminal, pas de réglages.

## 1. Le premier démarrage (tout est prêt)

Au premier démarrage vous arrivez sur un bureau **KDE Plasma 6** en thème steampunk, avec un noyau optimisé, le gouverneur SMU, le profil **Stock**, tout le nécessaire pour jouer et les instantanés **déjà actifs**. En haut à droite, l'**affichage système** montre en temps réel le CPU, le GPU, les températures, la mémoire, le ventilateur et les appareils Bluetooth connectés.

Vous n'avez pas de pilotes à installer, pas de fréquences à régler, rien à activer : le système démarre « à compatibilité maximale ».

## 2. Se connecter au réseau

L'Ethernet est géré par NetworkManager et fonctionne tout de suite. Pour le Wi-Fi et le Bluetooth, passez par l'icône du réseau dans le panneau. Une connexion est nécessaire pour Steam, les mises à jour et l'IA locale.

## 3. Brancher une manette

| Manette | Comment |
|---|---|
| **DualShock 4** | En Bluetooth : maintenez **Share + PS** jusqu'au clignotement, puis appairez depuis l'icône Bluetooth. Elle a le **gyroscope**. |
| **Manette générique** | En **USB** avec un câble de **données** (pas un câble de charge seule) : vue comme une manette Xbox 360. |

Détails et dépannage → [Jeu](/fr/docs/gaming) et [Dépannage](/fr/docs/risoluzione-problemi).

## 4. Ajouter vos jeux

- **Steam** est déjà installé et relié à gamescope et MangoHud. Connectez-vous et installez vos jeux : les titres Windows tournent avec **Proton**.
- **Epic / GOG** → [Heroic](/fr/docs/gaming).
- **Émulation** → lancez **EmuDeck**, choisissez vos émulateurs, puis jouez depuis l'interface **ES-DE**. Les ROM, les BIOS et les clés, c'est vous qui les ajoutez (voir la note légale dans [Jeu](/fr/docs/gaming)).

## 5. (Facultatif) Pousser le matériel

SkillFishOS démarre sur le profil **Stock** pour être sûr sur n'importe quelle carte. Quand vous voulez plus de performances, ouvrez le **[Tuner](/fr/docs/app-native)** et montez d'un profil :

**Stock → Performance → Turbo → Crazy**

Le Tuner **essaie chaque profil sur votre propre BC-250** et **revient en arrière** tout seul si la carte ne tient pas. C'est la façon sûre de trouver la limite de votre puce (voir [GPU et overclock](/fr/docs/gpu-overclock)).

## 6. (Facultatif) Allumer l'IA locale

Quand vous avez besoin d'un assistant d'IA hors ligne, ouvrez le **panneau d'IA** et démarrez [Unsloth Studio](/fr/docs/ai-locale). À retenir : l'IA et les jeux lourds ne s'utilisent **pas** en même temps (même GPU, même mémoire). Le moteur éteint, le GPU repart entièrement au jeu.

## À savoir tout de suite

- **Ne réactivez pas la mise en veille** : sur la BC-250 elle est cassée et la carte ne se réveille pas (voir [Bureau](/fr/docs/desktop)).
- Utilisez un écran **DisplayPort** ou un adaptateur **passif** ; les adaptateurs DP→HDMI **actifs** cassent le son.
- Vous avez un **filet de sécurité** : un instantané Btrfs est pris avant et après chaque mise à jour ; si les choses tournent mal, revenez en arrière depuis le menu GRUB → *SkillFishOS snapshots* (voir [Stockage et instantanés](/fr/docs/storage-snapshot)).

## Et ensuite ?

- Envie de comprendre **ce que** vous utilisez ? → [Matériel BC-250](/fr/docs/hardware-bc250)
- Envie des **chiffres** réels de performance ? → [Performances et mesures](/fr/docs/prestazioni)
- Une **question** rapide ? → [FAQ](/fr/docs/faq)
- Un **terme** inconnu ? → [Glossaire](/fr/docs/glossario)
