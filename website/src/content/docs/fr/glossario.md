---
title: Glossaire
description: Les termes techniques de SkillFishOS et de la BC-250, expliqués brièvement.
group: Référence
order: 5
---

Les termes qui reviennent dans toute la documentation, chacun expliqué en une ligne. Par ordre alphabétique.

## Matériel et APU

**APU** — *Accelerated Processing Unit* : une puce qui réunit le CPU et le GPU sur le même morceau de silicium. La BC-250 en porte une semi-personnalisée d'AMD.

**BC-250** — la carte sur laquelle tourne SkillFishOS : APU Zen 2 + RDNA 2, 16 Go de GDDR6, faite à l'origine pour le minage.

**Cyan Skillfish** — le nom de code de la partie **graphique** (le GPU) de l'APU de la BC-250. D'où le nom « SkillFish ».

**Oberon** — le nom de code de la partie **CPU** (Zen 2) du même APU.

**Unité de calcul (CU)** — les blocs de calcul du GPU. La BC-250 en a 40, mais en montre moins par défaut : SkillFishOS **les déverrouille toutes** (voir [noyau](/fr/docs/kernel)).

**gfx1013** — l'identifiant de l'architecture graphique de la BC-250 (famille RDNA 2). Il compte parce que **ROCm ne la prend pas en charge** → on utilise Vulkan à la place.

**RDNA 2** — l'architecture graphique d'AMD de ce GPU (la même famille que les consoles actuelles).

**Zen 2** — l'architecture CPU d'AMD de cet APU (**8 cœurs / 16 fils** : la carte en montre 6, SkillFishOS déverrouille les deux autres par la SMU).

**GDDR6** — le type de mémoire de la carte : rapide, et ici **partagée** entre le CPU et le GPU.

**UMA** — *Unified Memory Architecture* : le CPU et le GPU utilisent le **même** réservoir de mémoire (les 16 Go de GDDR6).

**GTT** — *Graphics Translation Table* : le mécanisme qui permet au GPU d'utiliser de la mémoire système au-delà de sa mémoire graphique dédiée. SkillFishOS l'agrandit pour que Vulkan voie environ 13 Gio (utile pour l'IA).

## Fréquences, tensions, chaleur

**SMU** — *System Management Unit* : le micro-contrôleur à l'intérieur de l'APU qui gère les fréquences et les tensions. Sur la BC-250 la commande passe **uniquement** par lui, pas par le sysfs habituel d'amdgpu.

**Gouverneur SMU** — le service (`cyan-skillfish-governor`) qui fixe les *points sûrs* de fréquence et de tension du GPU.

**sclk / mclk** — la fréquence du **cœur graphique** (sclk) et celle de la **mémoire** (mclk). Sur la BC-250 le mclk n'est **pas** réglable.

**Undervolt** — abaisser la tension à fréquence égale : le même travail, **moins de chaleur et moins de consommation**. Voir [GPU et overclock](/fr/docs/gpu-overclock).

**Overclock (OC)** — monter les fréquences au-delà de l'origine pour gagner en performance.

**Vid** — la tension que la puce demande à une fréquence donnée. Sur la BC-250 la limite dure est de **1,325 V**.

**Garde thermique** — le veilleur du système qui baisse les fréquences dès que 85 °C sont dépassés.

**Chaleur accumulée (heat-soak)** — la chaleur qui s'accumule et fausse des mesures enchaînées : laissez la carte refroidir entre les essais.

**Loterie du silicium** — le fait que chaque puce supporte un overclock et un undervolt différents : c'est pour cela que SkillFishOS vérifie les profils **sur votre** carte.

## Logiciel système

**Debian sid** — la branche *unstable* de Debian, toujours à jour mais sujette aux régressions : la base de SkillFishOS (voir [Mises à jour](/fr/docs/aggiornamenti)).

**KDE Plasma 6** — l'environnement de bureau utilisé, habillé d'un thème steampunk.

**linux-tkg** — la recette de compilation du noyau (Frogging-Family) sur laquelle repose le noyau sur mesure de SkillFishOS.

**Mesa / RADV** — les pilotes graphiques libres ; **RADV** est le pilote **Vulkan** qu'utilise le GPU de la BC-250.

**ROCm** — la pile de calcul « officielle » d'AMD : elle ne prend **pas** en charge gfx1013, elle n'est donc pas utilisée.

**Vulkan** — l'interface de graphisme et de calcul qui sert sur la BC-250 aussi bien à jouer qu'à l'**IA** (Unsloth Studio).

**Btrfs** — le système de fichiers en copie sur écriture, avec instantanés, qui fournit le « filet de sécurité » (voir [Stockage et instantanés](/fr/docs/storage-snapshot)).

**Snapper** — l'outil qui crée tout seul des instantanés Btrfs avant et après les mises à jour.

**grub-btrfs** — fait apparaître les instantanés dans le menu GRUB, pour revenir en arrière dès le démarrage.

**Épinglage APT** — retenir un paquet à une version vérifiée, pour les composants fragiles sur ce matériel.

**reprepro** — l'outil qui gère le dépôt APT signé de SkillFishOS.

**HPD** — *Hot-Plug Detect* : la détection du branchement de l'écran. Sur la BC-250 elle est **cassée** → d'où le service `skillfish-dp-hotswap`.

**s2idle / mise en veille** — les états de veille d'ACPI : **cassés** sur la BC-250, donc désactivés.

**IOMMU** — l'unité de gestion de mémoire pour la virtualisation des entrées-sorties : instable sur la BC-250, elle n'est **jamais** activée.

## Jeu et IA

**Proton** — la couche de compatibilité de Valve qui fait tourner les jeux Windows sous Linux, par Steam.

**gamescope** — le micro-compositeur de Valve pour le jeu (session « console », rehaussement FSR1/NIS).

**EmuDeck / ES-DE** — l'installateur d'émulateurs et l'interface d'émulation.

**FSR / OptiScaler** — des techniques de **rehaussement de définition**. FSR 4 n'existe pas ici (il demande du RDNA 4) ; on utilise FSR1/NIS ou OptiScaler.

**Unsloth Studio** — le moteur et l'interface de l'IA locale : il exécute des modèles GGUF sur le GPU et offre une interface compatible OpenAI.

**qwen3:14b** — le modèle d'IA de référence, qui tourne entièrement sur le GPU.

**Tuner** — l'application native de SkillFishOS pour régler le matériel avec test et retour en arrière (voir [Applications natives](/fr/docs/app-native)).

## Sources

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [La documentation d'amdgpu](https://docs.kernel.org/gpu/amdgpu/) · [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)
