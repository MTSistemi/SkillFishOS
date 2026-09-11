---
title: Lokalna AI
description: Lokalny silnik AI, przyspieszany Vulkanem na grafice BC-250 — Unsloth Studio z modelami GGUF z Hugging Face.
group: Używanie
order: 2
---

SkillFishOS ma w zestawie **lokalną AI**: modele do rozmowy i do kodu działające w całości na grafice BC-250, **bez chmury**, bez wysyłania czegokolwiek na zewnątrz. Jedno kliknięcie włącza je i wyłącza, więc grafika i pamięć wracają do dyspozycji, gdy chcesz zagrać.

![Sekcja SI w Control Center: silnik, modele, pamięć i próbny czat](/img/control-center-ai.png)

## Dlaczego Vulkan, a nie ROCm

„Oficjalnym” stosem obliczeniowym AMD jest **ROCm**, ale **nie obsługuje on `gfx1013` z BC-250**. SkillFishOS używa więc backendu **Vulkan** ze sterownikami Mesa/RADV: wykorzystuje w pełni zintegrowaną grafikę i współdzieloną pamięć (z rozszerzonym GTT, zobacz [GPU](/pl/docs/gpu-overclock)).

**Ile to znaczy w praktyce.** Zmierzone na płycie z Qwen3-1.7B Q4_K_M:

| | Sam procesor | Grafika przez Vulkan | |
|---|---:|---:|---|
| Generowanie | 41,5 tok/s | **210,7 tok/s** | **5,1×** |
| Przetwarzanie zapytania | 9,2 tok/s | **157,2 tok/s** | **17×** |

## Silnik: Unsloth Studio

Od wydania 26.08 silnikiem jest **[Unsloth Studio](https://unsloth.ai/)**, który zastąpił wcześniejszy dockerowy zestaw Ollama + OpenWebUI. To **jedna natywna usługa** dająca zarówno interfejs rozmowy, jak i **API zgodne z OpenAI**, nasłuchująca na `127.0.0.1:8888`.

Co się przez to zmienia:

- **Jedna usługa zamiast zestawu kontenerów.** Wcześniej potrzeba było trzech kontenerów (Ollama, OpenWebUI, Dockge) plus własnego obrazu na ~6,5 GB; teraz jest to po prostu `skillfish-unsloth.service`.
- **Modele przychodzą z Hugging Face.** Unsloth pobiera pliki **GGUF** wprost z pełnego katalogu Hugging Face, a nie z wybranego rejestru, więc wachlarz dostępnych modeli i kwantyzacji jest nieporównanie szerszy — łącznie z tym, co publikuje sam zespół Unsloth.
- **Nasłuchuje tylko lokalnie.** Z zewnątrz dociera się przez panel sterowania, który uwierzytelnia przez PAM: żaden port AI nie jest wystawiony do sieci.


## Modele

Modele to pliki **GGUF** z katalogu Hugging Face i pochodzą z dwóch miejsc: z sekcji **SI** [Control Center](/pl/docs/control-center), gdzie wpisujesz nazwę repozytorium (na przykład `unsloth/Qwen3-4B-GGUF`) i wybierasz wariant z listy, z rozmiarami; albo z Hubu w Unsloth Studio, który ma wyszukiwarkę i pełne karty modeli.

Praktyczna zasada na tej płycie: 16 GB GDDR6 dzieli system z GPU, więc lepiej zostać poniżej ~11 GB wag, żeby reszcie zostało miejsce.

## Włączanie, aktualizacja i klucz

Sekcja **SI** w [Control Center](/pl/docs/control-center) włącza i wyłącza silnik, włącza go przy starcie i pokazuje wersję z aktualizacją jednym kliknięciem. To samo jest w [Remote Managerze](/pl/docs/controllo-remoto), z przeglądarki.

Unsloth przy instalacji tworzy losowe hasło i **wyłącza się sam po godzinie**, jeśli hasło nie zostanie zmienione. Ten krok wykonuje sekcja SI: wybierasz hasło do Studio, a klucz API powstaje razem z nim. Kluczem okno i Remote Manager rozmawiają z silnikiem; modele na dysku, pamięć (VRAM, GTT, RAM, swap) i próbny czat ze zmierzonymi tokenami na sekundę są obok.

Pamiętaj, że:

- **SI i gry nie chodzą razem**: dzielą to samo GPU i tę samą pamięć;
- przy wyłączonym silniku GPU i RAM wracają w całości do grania.

## Źródła

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (sterownik Vulkana)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — obsługiwany sprzęt](https://rocm.docs.amd.com/) (`gfx1013` nie ma na liście)
