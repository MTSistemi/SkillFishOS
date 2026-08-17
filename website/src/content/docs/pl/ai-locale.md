---
title: Lokalna AI
description: Lokalny silnik AI, przyspieszany Vulkanem na grafice BC-250 — Unsloth Studio z modelami GGUF z Hugging Face.
group: Używanie
order: 2
---

SkillFishOS ma w zestawie **lokalną AI**: modele do rozmowy i do kodu działające w całości na grafice BC-250, **bez chmury**, bez wysyłania czegokolwiek na zewnątrz. Jedno kliknięcie włącza je i wyłącza, więc grafika i pamięć wracają do dyspozycji, gdy chcesz zagrać.

![Panel SkillFishOS AI — włącza i wyłącza lokalny silnik modeli przyspieszany Vulkanem](/img/ai-panel.jpg)

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

> Od 26.06.3 panel sterowania i panel AI obsługują **wyłącznie** Unsloth: gałęzie kodu sterujące Ollamą przez Dockera zniknęły, a razem z nimi sam Docker, który nie jest już instalowany. Kto trzyma jeszcze kontenery Ollamy z wcześniejszej instalacji, może je uruchamiać, dopóki zostawi sobie Dockera, ale nie zarządza nimi już stąd. Nic nie trzeba konfigurować.

## Modele

Modele pobiera się **wewnątrz Unsloth Studio**, z jego własnego interfejsu. Praktyczna zasada na tej płycie: 16 GB GDDR6 dzieli się między system i grafikę, więc trzymanie się poniżej ~11 GB samych wag zostawia miejsce na całą resztę.

## Włączanie i wyłączanie

Osobny **panel AI** (własna aplikacja, zobacz [Własne aplikacje](/pl/docs/app-native)) uruchamia i zatrzymuje silnik jednym kliknięciem; ten sam przełącznik jest w [panelu webowym](/pl/docs/controllo-remoto). Pamiętaj:

- **AI i gry nie powinny chodzić razem**: dzielą tę samą grafikę i tę samą pamięć;
- przy wyłączonym silniku grafika i pamięć są znowu w pełni dostępne do grania.

## Źródła

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (sterownik Vulkana)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — obsługiwany sprzęt](https://rocm.docs.amd.com/) (`gfx1013` nie ma na liście)
