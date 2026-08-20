---
title: IA no próprio aparelho
description: O motor de IA local, acelerado por Vulkan na GPU da BC-250 — Unsloth Studio, com modelos GGUF do Hugging Face.
group: Uso
order: 2
---

O SkillFishOS traz uma **IA local**: modelos de conversa e de programação rodando inteiramente na GPU da BC-250, **sem nuvem**, sem nada saindo para fora. Um clique liga e desliga, então a GPU e a memória ficam livres de novo quando você quer jogar.

![Painel SkillFishOS AI — liga e desliga o motor local acelerado por Vulkan](/img/ai-panel.jpg)

## Por que Vulkan e não ROCm

O conjunto de computação “oficial” da AMD é o **ROCm**, mas ele **não dá suporte ao `gfx1013`** da BC-250. Por isso o SkillFishOS usa o motor **Vulkan** com os drivers Mesa/RADV: ele aproveita por completo a GPU integrada e a memória compartilhada (com o GTT ampliado, veja [GPU](/pt/docs/gpu-overclock)).

**O quanto isso pesa.** Medido na placa com o Qwen3-1.7B Q4_K_M:

| | só CPU | GPU por Vulkan | |
|---|---:|---:|---|
| Geração | 41,5 tok/s | **210,7 tok/s** | **5,1×** |
| Processamento do texto de entrada | 9,2 tok/s | **157,2 tok/s** | **17×** |

## O motor: Unsloth Studio

Desde a 26.08 o motor é o **[Unsloth Studio](https://unsloth.ai/)**, no lugar do antigo conjunto Ollama + OpenWebUI em Docker. É **um único serviço nativo** que oferece tanto a janela de conversa quanto uma **API compatível com a da OpenAI**, escutando em `127.0.0.1:8888`.

O que muda na prática:

- **Um serviço em vez de um conjunto de Docker.** Antes eram três contêineres (Ollama, OpenWebUI, Dockge) mais uma imagem própria de uns 6,5 GB; agora é só o `skillfish-unsloth.service`.
- **Os modelos vêm do Hugging Face.** O Unsloth baixa arquivos **GGUF** direto do catálogo completo do Hugging Face, e não de um registro selecionado, então a variedade de modelos e quantizações é muito maior — incluindo as compilações que a própria equipe do Unsloth publica.
- **Ele escuta só em loopback.** De fora chega-se a ele pelo painel de controle, que autentica por PAM: nenhuma porta de IA fica exposta à rede.

> Desde a 26.06.3 o painel de controle e o painel de IA falam **só** com o Unsloth: os ramos que comandavam o Ollama pelo Docker foram embora, e o Docker também, que não é mais instalado. Quem ainda tem contêineres do Ollama de uma instalação anterior continua com eles funcionando enquanto mantiver o Docker, mas não os gerencia mais por aqui. Não há nada para configurar.

## Modelos

Os modelos são baixados **dentro do Unsloth Studio**, pela interface dele. Regra prática nesta placa: os 16 GB de GDDR6 são divididos entre o sistema e a GPU, então ficar abaixo de uns 11 GB de pesos deixa espaço para todo o resto.

## Ligar e desligar

Um **painel de IA** próprio (aplicativo nativo, veja [Aplicativos próprios](/pt/docs/app-native)) inicia e para o motor com um clique; o mesmo interruptor está no [painel de controle](/pt/docs/controllo-remoto). Lembre-se:

- **IA e jogos não devem rodar juntos**: dividem a mesma GPU e a mesma memória;
- com o motor desligado, a GPU e a memória voltam inteiras para os jogos.

## Fontes

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (driver Vulkan)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — hardware suportado](https://rocm.docs.amd.com/) (o `gfx1013` não está na lista)
