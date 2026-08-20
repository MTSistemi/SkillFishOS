---
title: IA sur la machine
description: Le moteur d'IA local, accéléré en Vulkan sur le GPU de la BC-250 — Unsloth Studio, avec des modèles GGUF venus de Hugging Face.
group: Utilisation
order: 2
---

SkillFishOS embarque une **IA locale** : des modèles de discussion et de programmation qui tournent entièrement sur le GPU de la BC-250, **sans nuage**, sans rien envoyer dehors. Un clic l'allume et l'éteint, si bien que le GPU et la mémoire redeviennent libres quand vous voulez jouer.

![Le panneau d'IA de SkillFishOS — allume et éteint le moteur LLM local accéléré en Vulkan](/img/ai-panel.jpg)

## Pourquoi Vulkan et pas ROCm

La pile de calcul « officielle » d'AMD est **ROCm**, mais elle **ne prend pas en charge le `gfx1013`** de la BC-250. SkillFishOS utilise donc le moteur **Vulkan** avec les pilotes Mesa/RADV : il exploite pleinement le GPU intégré et la mémoire partagée (avec le GTT agrandi, voir [GPU](/fr/docs/gpu-overclock)).

**Ce que cela change.** Mesuré sur la carte avec Qwen3-1.7B Q4_K_M :

| | CPU seul | GPU par Vulkan | |
|---|---:|---:|---|
| Génération | 41,5 jetons/s | **210,7 jetons/s** | **5,1×** |
| Traitement de l'invite | 9,2 jetons/s | **157,2 jetons/s** | **17×** |

## Le moteur : Unsloth Studio

Depuis la 26.08 le moteur est **[Unsloth Studio](https://unsloth.ai/)**, à la place de l'ancien assemblage Docker Ollama + OpenWebUI. C'est **un seul service natif** qui fournit à la fois l'interface de discussion et une **interface compatible OpenAI**, à l'écoute sur `127.0.0.1:8888`.

Ce qui change en pratique :

- **Un service au lieu d'un assemblage Docker.** Il fallait avant trois conteneurs (Ollama, OpenWebUI, Dockge) plus une image sur mesure d'environ 6,5 Go ; maintenant c'est juste `skillfish-unsloth.service`.
- **Les modèles viennent de Hugging Face.** Unsloth récupère les fichiers **GGUF** directement dans tout le catalogue Hugging Face plutôt que dans un registre restreint, si bien que le choix de modèles et de quantifications est bien plus large — y compris les versions que l'équipe Unsloth publie elle-même.
- **Il n'écoute que sur l'interface locale.** De l'extérieur on l'atteint par le tableau de bord, qui vérifie les comptes par PAM : aucun port d'IA n'est ouvert sur le réseau.

> Depuis la 26.06.3 le tableau de bord et le panneau d'IA ne pilotent **que** Unsloth : les branches qui commandaient Ollama par Docker ont disparu, et Docker aussi, qui n'est plus installé. Qui garde encore des conteneurs Ollama d'une installation plus ancienne les conserve tant qu'il garde Docker, mais ne les gère plus depuis ici. Rien à configurer.

## Les modèles

Les modèles se téléchargent **dans Unsloth Studio**, depuis sa propre interface. Repère utile sur cette carte : les 16 Go de GDDR6 sont partagés entre le système et le GPU, donc rester sous environ 11 Go de poids laisse de la place pour tout le reste.

## L'allumer et l'éteindre

Un **panneau d'IA** dédié (application native, voir [Applications natives](/fr/docs/app-native)) démarre et arrête le moteur en un clic ; le même interrupteur se trouve dans le [tableau de bord web](/fr/docs/controllo-remoto). Gardez en tête que :

- **l'IA et les jeux ne doivent pas tourner ensemble** : ils partagent le même GPU et la même mémoire ;
- le moteur éteint, le GPU et la mémoire redeviennent entièrement disponibles pour le jeu.

## Sources

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (le pilote Vulkan)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — matériel pris en charge](https://rocm.docs.amd.com/) (`gfx1013` n'y figure pas)
