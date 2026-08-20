---
title: IA en el propio equipo
description: El motor de IA local, acelerado con Vulkan en la GPU de la BC-250 — Unsloth Studio, con modelos GGUF de Hugging Face.
group: Uso
order: 2
---

SkillFishOS trae una **IA local**: modelos de conversación y de programación funcionando enteramente en la GPU de la BC-250, **sin nube**, sin que nada salga fuera. Un clic la enciende y la apaga, así que la GPU y la memoria quedan libres otra vez cuando quieres jugar.

![Panel SkillFishOS AI — enciende y apaga el motor local acelerado con Vulkan](/img/ai-panel.jpg)

## Por qué Vulkan y no ROCm

El conjunto de cómputo «oficial» de AMD es **ROCm**, pero **no soporta el `gfx1013`** de la BC-250. Por eso SkillFishOS usa el motor **Vulkan** con los controladores Mesa/RADV: aprovecha del todo la GPU integrada y la memoria compartida (con el GTT ampliado, ver [GPU](/es/docs/gpu-overclock)).

**Cuánto importa.** Medido en la placa con Qwen3-1.7B Q4_K_M:

| | solo CPU | GPU con Vulkan | |
|---|---:|---:|---|
| Generación | 41,5 tok/s | **210,7 tok/s** | **5,1×** |
| Procesado del texto de entrada | 9,2 tok/s | **157,2 tok/s** | **17×** |

## El motor: Unsloth Studio

Desde la 26.08 el motor es **[Unsloth Studio](https://unsloth.ai/)**, que sustituye al anterior montaje de Ollama + OpenWebUI en Docker. Es **un único servicio propio** que ofrece tanto la ventana de chat como una **API compatible con la de OpenAI**, escuchando en `127.0.0.1:8888`.

Lo que cambia en la práctica:

- **Un servicio en lugar de un montaje de Docker.** Antes hacían falta tres contenedores (Ollama, OpenWebUI, Dockge) más una imagen propia de unos 6,5 GB; ahora es solo `skillfish-unsloth.service`.
- **Los modelos vienen de Hugging Face.** Unsloth descarga archivos **GGUF** directamente del catálogo completo de Hugging Face y no de un registro seleccionado, así que la variedad de modelos y de cuantizaciones es muchísimo mayor — incluidas las compilaciones que publica el propio equipo de Unsloth.
- **Escucha solo en loopback.** Desde fuera se llega a él por el panel de control, que autentica con PAM: no hay ningún puerto de IA expuesto a la red.

> Desde la 26.06.3 el panel de control y el panel de IA manejan **solo** Unsloth: las ramas que mandaban sobre Ollama a través de Docker han desaparecido, y también Docker, que ya no se instala. Quien todavía conserve contenedores de Ollama de una instalación anterior los mantiene funcionando mientras conserve Docker, pero ya no los gestiona desde aquí. No hay que configurar nada.

## Modelos

Los modelos se descargan **dentro de Unsloth Studio**, desde su propia interfaz. Regla práctica en esta placa: los 16 GB de GDDR6 se reparten entre el sistema y la GPU, así que quedarse por debajo de unos 11 GB de pesos deja sitio para todo lo demás.

## Encenderla y apagarla

Un **panel de IA** propio (aplicación nativa, ver [Aplicaciones propias](/es/docs/app-native)) arranca y para el motor con un clic; el mismo interruptor está en el [panel de control](/es/docs/controllo-remoto). Ten en cuenta que:

- **la IA y los juegos no deberían funcionar a la vez**: comparten la misma GPU y la misma memoria;
- con el motor apagado, la GPU y la memoria vuelven a estar enteras para jugar.

## Fuentes

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (controlador Vulkan)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — hardware compatible](https://rocm.docs.amd.com/) (`gfx1013` no está en la lista)
