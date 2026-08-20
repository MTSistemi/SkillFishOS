---
title: KI auf dem Gerät
description: Der lokale KI-Motor, mit Vulkan auf der GPU der BC-250 beschleunigt — Unsloth Studio, mit GGUF-Modellen von Hugging Face.
group: Benutzung
order: 2
---

SkillFishOS bringt eine **lokale KI** mit: Modelle zum Chatten und zum Programmieren laufen vollständig auf der GPU der BC-250, **ohne Cloud**, nichts verlässt das Gerät. Ein Klick schaltet sie ein und aus, damit GPU und Arbeitsspeicher wieder frei sind, wenn du spielen willst.

![SkillFishOS-KI-Fenster — schaltet den lokalen, mit Vulkan beschleunigten Motor ein und aus](/img/ai-panel.jpg)

## Warum Vulkan und nicht ROCm

Der „offizielle“ Rechenunterbau von AMD ist **ROCm**, aber er **unterstützt das `gfx1013`** der BC-250 **nicht**. Deshalb verwendet SkillFishOS den **Vulkan**-Unterbau mit den Mesa/RADV-Treibern: er nutzt die eingebaute GPU und den gemeinsamen Speicher voll aus (mit erweiterter GTT, siehe [GPU](/de/docs/gpu-overclock)).

**Wie viel das ausmacht.** Auf der Platine mit Qwen3-1.7B Q4_K_M gemessen:

| | nur CPU | GPU über Vulkan | |
|---|---:|---:|---|
| Erzeugung | 41,5 Token/s | **210,7 Token/s** | **5,1×** |
| Verarbeitung der Eingabe | 9,2 Token/s | **157,2 Token/s** | **17×** |

## Der Motor: Unsloth Studio

Seit 26.08 ist der Motor **[Unsloth Studio](https://unsloth.ai/)**, an Stelle des früheren Gespanns aus Ollama und OpenWebUI in Docker. Es ist **ein einziger nativer Dienst**, der sowohl das Chatfenster als auch eine **zu OpenAI kompatible Schnittstelle** bereitstellt und auf `127.0.0.1:8888` lauscht.

Was sich in der Praxis ändert:

- **Ein Dienst statt eines Docker-Gespanns.** Früher brauchte es drei Container (Ollama, OpenWebUI, Dockge) und ein eigenes Abbild von rund 6,5 GB; jetzt ist es nur noch `skillfish-unsloth.service`.
- **Die Modelle kommen von Hugging Face.** Unsloth holt **GGUF**-Dateien unmittelbar aus dem vollständigen Katalog von Hugging Face statt aus einer ausgewählten Liste, die Auswahl an Modellen und Quantisierungen ist damit ungleich größer — samt der Fassungen, die das Unsloth-Team selbst veröffentlicht.
- **Er lauscht nur auf dem Loopback.** Von außen erreicht man ihn über die Fernsteuerung, die sich über PAM anmeldet: kein KI-Port ist zum Netz hin offen.

> Seit 26.06.3 steuern die Fernsteuerung und das KI-Fenster **nur** Unsloth: die Zweige, die Ollama über Docker befehligten, sind verschwunden, und Docker selbst ebenso — es wird nicht mehr installiert. Wer noch Ollama-Container aus einer früheren Installation hat, behält sie laufend, solange er Docker behält, verwaltet sie aber nicht mehr von hier aus. Einzurichten ist nichts.

## Modelle

Die Modelle werden **innerhalb von Unsloth Studio** geladen, aus dessen eigener Oberfläche. Faustregel auf dieser Platine: die 16 GB GDDR6 teilen sich System und GPU, unter rund 11 GB Gewichten zu bleiben lässt also Platz für alles andere.

## Ein- und ausschalten

Ein eigenes **KI-Fenster** (native Anwendung, siehe [Eigene Anwendungen](/de/docs/app-native)) startet und stoppt den Motor mit einem Klick; derselbe Schalter steckt in der [Fernsteuerung](/de/docs/controllo-remoto). Bedenke dabei:

- **KI und Spiele sollten nicht gleichzeitig laufen**: sie teilen sich dieselbe GPU und denselben Speicher;
- ist der Motor aus, stehen GPU und Speicher wieder vollständig zum Spielen bereit.

## Quellen

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (Vulkan-Treiber)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — unterstützte Hardware](https://rocm.docs.amd.com/) (`gfx1013` steht nicht auf der Liste)
