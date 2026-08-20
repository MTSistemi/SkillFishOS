---
title: Mises à jour et dépôt
description: Comment SkillFishOS se met à jour sans se faire casser par Debian sid.
group: Utilisation
order: 4
---

SkillFishOS repose sur **Debian sid** (*unstable*), la branche de développement de Debian : toujours à jour, mais par nature sujette à des régressions de temps en temps. Sur un matériel aussi particulier que la BC-250, une mauvaise mise à jour (de Mesa, du micrologiciel ou du noyau) peut casser le système. SkillFishOS répond à cela avec deux outils.

## 1. Nos propres composants, depuis un dépôt dédié

Les parties les plus délicates sont construites et distribuées par **nous**, depuis **notre propre dépôt APT signé** :

- le **[noyau](/fr/docs/kernel)** optimisé (image et en-têtes) ;
- le **gouverneur SMU** et les outils d'overclock ;
- les **applications natives** [Tuner et IA](/fr/docs/app-native) ;
- le **thème steampunk** et l'identité visuelle ;
- la configuration du système.

Publier un composant depuis notre dépôt veut dire que nous pouvons l'**essayer d'abord** sur le vrai matériel et ne le mettre à jour **que lorsqu'il apporte quelque chose** — pas chaque fois qu'il change en amont.

## 2. « Retenir » les paquets fragiles

Pour les paquets qui viennent de Debian mais sont délicats sur ce matériel, SkillFishOS utilise l'**épinglage APT** : il les garde à une version **vérifiée** jusqu'à ce que nous en ayons essayé une plus récente. Les principaux candidats sont :

- **Mesa et les pilotes Vulkan (RADV)** — une mise à jour peut faire régresser `gfx1013` ;
- **le micrologiciel AMD et `linux-firmware`** — le microcode du GPU ;
- **le noyau d'origine de Debian** — pour bloquer les versions connues comme problématiques (voir [noyau](/fr/docs/kernel)) ;
- **KDE Plasma** — pour éviter les versions instables.

Ainsi les mises à jour « ordinaires » (la plus grande partie du système) continuent d'arriver régulièrement, tandis que la poignée de paquets qui pourraient tout casser restent figés sur des versions dont nous savons qu'elles marchent.

## Comment mettre à jour

Comme sur n'importe quel système Debian, depuis le terminal :

```bash
sudo apt update && sudo apt full-upgrade
```

…ou depuis l'application graphique **Discover**, ou depuis le **SkillFishOS Hub** — notre logithèque façon Discover, qui installe, retire et met à jour au même endroit à travers **APT, Flatpak et Snap**, avec la navigation par catégorie, des fiches d'applications avec carrousel de captures et un « Tout mettre à jour » en un clic. Grâce aux accrochages de [Snapper](/fr/docs/storage-snapshot), un instantané Btrfs est créé **avant et après** chaque mise à jour : si quelque chose tourne mal, le retour en arrière depuis le menu GRUB rétablit l'état précédent.

> En résumé : **nous** vous donnons un noyau, des applications et des thèmes essayés ; **Debian** vous donne le reste des logiciels à jour ; l'**épinglage** évite les surprises ; **Btrfs** est le filet. Trois couches de protection, pour que mettre à jour ne fasse pas peur.

## Le dépôt officiel

Le dépôt APT de SkillFishOS est **en ligne**, signé en GPG et hébergé sur **GitHub Pages** (suite `aetherium`) :

```bash
# 1. importer la clé de signature
sudo curl -fsSL https://mtsistemi.github.io/SkillFishOS/skillfishos-archive-keyring.gpg \
  -o /usr/share/keyrings/skillfishos-archive-keyring.gpg
# 2. ajouter le dépôt
echo "deb [signed-by=/usr/share/keyrings/skillfishos-archive-keyring.gpg] \
https://mtsistemi.github.io/SkillFishOS aetherium main" \
  | sudo tee /etc/apt/sources.list.d/skillfishos.list
# 3. installer ou mettre à jour le noyau par apt
sudo apt update && sudo apt install skillfishos-kernel
```

Les versions récentes de SkillFishOS l'apportent **déjà configuré** ; sinon les commandes ci-dessus le mettent en place. Le [noyau](/fr/docs/kernel)
(une image de 152 Mo) est publié comme *release asset* sur GitHub : le tout petit paquet
`skillfishos-kernel` le télécharge et l'installe tout seul, si bien que la mise à jour passe
quand même par `apt`. Le dépôt est géré avec **[reprepro](https://salsa.debian.org/debian/reprepro)**
et le client vérifie la signature grâce au *trousseau* dédié.

## Sources

- [Debian unstable (sid)](https://wiki.debian.org/DebianUnstable)
- [L'épinglage APT — manuel Debian](https://wiki.debian.org/AptConfiguration)
- [reprepro](https://salsa.debian.org/debian/reprepro) — gestion du dépôt APT
- [Snapper](http://snapper.io/) — instantanés avant et après APT
