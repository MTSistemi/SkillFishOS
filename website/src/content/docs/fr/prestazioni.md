---
title: Performances et mesures
description: Toutes les vraies mesures de la BC-250 sous SkillFishOS — captures, réglages complets, fréquences, tensions, températures et consommation.
group: Référence
order: 3
---

Voici la **section complète des mesures** : chaque essai a été fait sur **notre propre BC-250** sous SkillFishOS, avec de vraies captures d'écran, **tous les réglages employés** et le relevé des **fréquences, tensions, températures, consommation et vitesse du ventilateur** pendant l'essai.

> **Attention :** **loterie du silicium et refroidissement.** Les chiffres valent pour *cette* puce avec un refroidissement suffisant. Le dissipateur d'origine est juste : comparer des mesures « à la suite » sans pause est faussé par la *chaleur accumulée* — laissez la carte refroidir quelques minutes entre les essais.

## Les conditions de l'essai (le banc)

Elles valent pour **toutes** les mesures ci-dessous, sauf mention contraire.

| Élément | Valeur |
|---|---|
| Carte | **AMD BC-250** — APU Zen 2 « Oberon » + RDNA 2 « Cyan Skillfish » (`gfx1013`) |
| Mémoire | **16 Go de GDDR6** unifiés (UMA) |
| Unités de calcul | **40 / 40 actives** (basculées à chaud, voir [GPU](/fr/docs/gpu-overclock)) |
| Noyau | **7.0.10-skillfishos** (linux-tkg) — la version avec laquelle ces chiffres ont été pris ; nous livrons aujourd'hui le **7.2.0** ; le 7.1.7 avait été remesuré à moins de 2 % près |
| Pilote | **Mesa 26.0.8** — RADV (Vulkan) / radeonsi (OpenGL), ACO ; nous livrons aujourd'hui la **26.1.6** |
| Gouverneur du GPU | cyan-skillfish — au repos **350 MHz / 700 mV**, en charge **2230 MHz / ~1000 mV** |
| Profil d'overclock | **Turbo/Crazy** (plafond GPU 2230 MHz, CPU 3,9–4,0 GHz) |
| Plafond thermique | **85 °C** (SMU et thermal-guard), ventilateur en **automatique** |
| Définition | **1920×1080** |

> Rappel sur l'architecture : le CPU et le GPU partagent **le même morceau de silicium** et **le même budget de puissance**. Sous charge mixte le CPU cède de la fréquence de lui-même (environ 3,4–3,5 GHz) pour rester dans le budget et sous 85 °C — ce n'est pas un défaut, c'est la puce qui se protège.

---

## Black Myth: Wukong — 112 images/s (1080p)

![Black Myth: Wukong — 112 images/s en moyenne en 1080p sur l'AMD BC-250](/img/benchmarks/wukong-112fps.jpg)

| Réglage | Valeur |
|---|---|
| Définition | 1920×1080 |
| Limite d'images | aucune |
| Type de charge | **limitée par le CPU et les appels de dessin** |
| Rehaussement | FSR 4 indisponible (RDNA 4) → gamescope FSR1/NIS ou OptiScaler |

**Résultat :** en moyenne **112 images/s** · maximum **128** · minimum **92** · 1 % les plus basses **101**.

**Les relevés pendant l'essai** (environ 4 min) :

| Grandeur | Valeur mesurée |
|---|---|
| Fréquence du GPU | ~1,4–1,6 GHz (*non saturé* : le jeu est limité par le CPU) |
| Bord du GPU | 83–86 °C |
| Consommation du GPU | ~90–140 W |
| Tension du GPU | ~970–987 mV |
| Fréquence du CPU | ~3,5 GHz (descendue de 3,9 à cause du budget partagé) |
| Température du CPU | 85 °C (au plafond) |
| Mémoire graphique | ~1,9 Go (menu) → ~4,4 Go (en jeu) |
| Ventilateur | ~2950–3140 tr/min |

> La leçon : *en jeu*, sur un titre limité par les appels de dessin comme Wukong, ce qui compte le plus, c'est la **stabilité du CPU** en charge et un bon refroidissement.

### Gouverneur Balanced contre Performance (l'outil de mesure)

Le *survol de caméra* de l'outil de mesure est, lui, **limité par le GPU** : là, la fréquence compte. En mettant le gouverneur sur **Performance** depuis le Tuner (il maintient le GPU à son point sûr le plus haut en charge, tout en redescendant à 350 MHz au repos) :

| Mode du gouverneur | Moyenne | 5 % les plus basses |
|---|---|---|
| **Balanced** (par défaut) | 100 images/s | 92 images/s |
| **Performance** | **111 images/s** | **102 images/s** |

**+11 %** sur la moyenne comme sur les images les plus lourdes, rien qu'en tenant la fréquence. Par prudence le Tuner limite le GPU à **2200 MHz sous 1000 mV** avec une courbe de tension à plusieurs points : 2230 MHz sous 1000 mV est en dessous de la tension nécessaire et peut figer la machine.

---

## Unigine Superposition — 1080p HIGH : 12938

![Unigine Superposition 1080p High — 12938 points sur la BC-250](/img/benchmarks/superposition-high.jpg)

| Réglage | Valeur |
|---|---|
| Version | 1.1 |
| Interface graphique | **OpenGL** |
| Définition | 1920×1080, plein écran |
| Nuanceurs | **High** |
| Textures | High |
| Profondeur de champ | activée |
| Flou de mouvement | activé |

**Résultat :** **12 938** points · images/s minimum **75,59** · moyenne **96,77** · maximum **127,16**.
**Ce que l'outil a lu :** CPU AMD BC-250 **à 3894 MHz**, 7 Go de mémoire vive, GPU AMD BC-250 8 Go (Cyan Skillfish), noyau 7.0.10-skillfishos.

---

## Unigine Superposition — 1080p EXTREME : 5513

![Unigine Superposition 1080p Extreme — 5513 points sur la BC-250](/img/benchmarks/superposition-extreme.jpg)

| Réglage | Valeur |
|---|---|
| Version | 1.1 |
| Interface graphique | **OpenGL** |
| Définition | 1920×1080, plein écran |
| Nuanceurs | **Extreme** |
| Textures | High |
| Profondeur de champ | activée |
| Flou de mouvement | activé |

**Résultat :** **5513** points · moyenne **41,25** images/s (minimum ~32,8 · maximum ~49).

![Unigine Superposition — une scène calculée en temps réel](/img/benchmarks/superposition-scene.jpg)
*Une scène de Superposition calculée en temps réel sur la BC-250.*

---

## Unigine Heaven 4.0 — 113,7 images/s · 2865 points

![Unigine Heaven 4.0 — 113,7 images/s, 2865 points sur la BC-250](/img/benchmarks/heaven-113fps.jpg)

| Réglage | Valeur |
|---|---|
| Interface graphique | **OpenGL** |
| Définition | 1920×1080, en fenêtre |
| Anticrénelage | **8×** |
| Qualité | **Ultra** |
| Tessellation | **Extreme** |

**Résultat :** **113,7 images/s** · **2865** points · minimum **54,8** · maximum **219,5**.
**Ce que l'outil a lu :** Linux 7.0.10-skillfishos x86_64 · CPU AMD BC-250 ×12 · GPU gfx1013.

![Unigine Heaven — une scène calculée en temps réel](/img/benchmarks/heaven-scene.jpg)
*La scène de Heaven calculée en temps réel sur la BC-250 pendant l'essai.*

---

## Le calcul sur le GPU — vkpeak (synthétique)

Le débit de calcul Vulkan sur la **même** carte, avant et après le déverrouillage des 40 CU.

| Grandeur | Départ 24 CU | SkillFishOS 40 CU |
|---|---|---|
| **FP32** scalaire | 6141 GFLOPS | **11 329** GFLOPS *(11 385 à froid)* |
| FP16 vec4 | 12 260 | **22 685** |
| produit scalaire int8 | 24 550 GIOPS | **45 495** GIOPS |
| FP64 scalaire | 385 | ~640 |
| copy d2d (bande passante interne) | — | 191 GBPS |

Avec les 40 CU actives : **+85 %** en FP32 par rapport au départ (environ **11,3 TFLOPS**). À chaud, sous charge continue, cela se stabilise vers **10 214 GFLOPS**. Au repos le gouverneur redescend à 350 MHz, le bord à environ 54 °C après la charge.

## La bande passante mémoire — clpeak

| Grandeur | Valeur |
|---|---|
| Bande passante GDDR6 mesurée | **~350–367 Go/s** |
| `mclk` réglable | **Non** (fréquence mémoire figée) |
| Mémoire vue par Vulkan | ~13 Gio (avec le GTT agrandi) |

---

## Les profils du Tuner — fréquences, tensions, températures

| Profil | CPU | Tension du CPU | GPU | Température de pointe |
|---|---|---|---|---|
| **Stock** *(par défaut dans l'image)* | 3500 MHz | — | 1500 MHz | la plus basse |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | équilibrée |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (le plafond) |
| **Crazy** | 4,0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C sur 120 s de charge |

- **Maximum dur de Vid : 1,325 V** (jamais dépassé).
- Plafond thermique de 85 °C sur tous les profils ; ventilateur en automatique ; au repos le GPU se tient à **350 MHz / 700 mV**.

## Le déverrouillage des 8 cœurs — de vrais +20 %

La BC-250 arrive avec **deux cœurs éteints par le logiciel** : le masque des cœurs autorisés de la SMU montre 3 sur 4 par CCX. SkillFishOS le réécrit et porte le CPU à **8 cœurs / 16 fils**, sans BIOS modifié.

Mesuré sur un même démarrage, en éteignant et en rallumant les deux cœurs supplémentaires à chaud :

| Charge | 6c/12f | 8c/16f | |
|---|---|---|---|
| Compression `xz -T` | 6,41 s | **5,11 s** | **+20 %** |
| Modèle de langue sur le CPU | 34,0 jetons/s | **40,8 jetons/s** | **+20 %** |
| Température | 66 °C | 68 °C | +2 °C |

C'est +20 % et non les +33 % théoriques : la bande passante mémoire et le coût des fils mangent la différence. Cela reste **un cinquième de performance en plus, gratuitement**.

### L'overclock avec les 8 cœurs

Remesuré marche après marche, chaque marche **stable, 0 erreur machine** :

| Cible | Atteint en charge | Score | Température | Ventilateur |
|---|---|---|---|---|
| 3500 (témoin) | 3475 | 5118 év/s | 57 °C | — |
| 3700 | 3673 | 5410 | 62 °C | 50 % |
| 3900 | 3872 | 5704 | 71 °C | 68 % |
| **4000** | **3971** | **5849** | **81 °C** | **93 %** |

**Maximum stable : 4000 MHz**, +14 % sur le score par rapport à 3500 — et atteignable seulement une fois la commande du ventilateur réparée. **Attention :** sous une charge **combinée CPU et GPU** la fréquence se pose à 3375–3492 MHz à 86 °C : au-delà d'environ 3900, c'est le dissipateur qui limite, pas le silicium.

---

## La validation thermique (essai en charge)

Les données relevées pendant la vérification automatique du Tuner (essai avec retour en arrière).

| Phase | Fréquence | Température | Notes |
|---|---|---|---|
| Repos | CPU ~2,5 GHz · GPU 350 MHz | k10 46 °C · GPU 45 °C | sans charge |
| **Charge CPU** (12 fils, 120 s) | CPU **3,68–3,69 GHz** | k10 **85 °C** (au plafond) | chiffre historique, pris **avant** le déverrouillage des 8 cœurs |
| **Charge GPU** (vkpeak en boucle, 120 s) | GPU **2000 MHz** | bord jusqu'à **86 °C** | à 86 °C le gouverneur redescend à 1819–1900 MHz (thermal-guard) ; le CPU tombe à ~2,2–2,4 GHz à cause du budget partagé |

---

## Comparaisons

**Le même matériel, en ne changeant que le système** — Superposition 1080p Extreme sur la **même** BC-250 :

| Système | Score |
|---|---|
| **SkillFishOS** (GPU 2230 · CPU 3900, 40 CU) | **5513** |
| Autre distribution (Bazzite, fréquences d'origine) | 4102 |

→ **+34 % de performances réelles** tirées exactement de la même puce, grâce aux 40 CU déverrouillées, à un gouverneur qui pousse à 2230 MHz et à l'overclock du CPU avec undervolt.

**Face aux Radeon de bureau** (Superposition 1080p High) : la BC-250 sous SkillFishOS (**12 938**) fait jeu égal avec une **RX 6600 / 6600 XT** à plus de 200 €, avec la puissance de calcul brute d'une **RX 6700** (environ 11,3 TFLOPS) — sur une carte à environ 50 €.

---

## Les outils et la méthode

| Outil | Ce qu'il mesure |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | le débit FP32/FP16/int8 par Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | la bande passante mémoire et le débit OpenCL |
| [sysbench](https://github.com/akopytov/sysbench) | la charge et la mesure du CPU (le Tuner s'en sert aussi) |
| [Unigine Superposition / Heaven](https://benchmark.unigine.com/) | les mesures graphiques en OpenGL |
| MangoHud en jeu | les images par seconde et le temps par image dans de vrais jeux |
| notre propre télémétrie | fréquence, température, consommation et ventilateur par le sysfs d'`amdgpu`, `k10temp`, `nct6686` |

## Sources

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench) · [Unigine](https://benchmark.unigine.com/)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — le déverrouillage des CU
- [bc250.info](https://bc250.info) — les points sûrs et les notes thermiques de la communauté
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — le rehaussement jeu par jeu
