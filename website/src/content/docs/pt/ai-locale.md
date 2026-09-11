---
title: IA no próprio aparelho
description: O motor de IA local, acelerado por Vulkan na GPU da BC-250 — Unsloth Studio, com modelos GGUF do Hugging Face.
group: Uso
order: 2
---

O SkillFishOS traz uma **IA local**: modelos de conversa e de programação rodando inteiramente na GPU da BC-250, **sem nuvem**, sem nada saindo para fora. Um clique liga e desliga, então a GPU e a memória ficam livres de novo quando você quer jogar.

![Secção IA do Control Center: motor, modelos, memória e um teste de chat](/img/control-center-ai.png)

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


## Os modelos

Os modelos são ficheiros **GGUF** do catálogo da Hugging Face, e chegam de dois sítios: a secção **IA** do [Control Center](/pt/docs/control-center), onde escreves o nome do repositório (por exemplo `unsloth/Qwen3-4B-GGUF`) e escolhes a variante da lista, com os tamanhos; ou o Hub dentro do Unsloth Studio, que tem a pesquisa e as fichas completas.

Regra prática nesta placa: os 16 GB de GDDR6 são partilhados entre sistema e GPU, por isso convém ficar abaixo dos ~11 GB de pesos para deixar espaço ao resto.

## Ligar, atualizar e a chave

A secção **IA** do [Control Center](/pt/docs/control-center) liga e desliga o motor, ativa-o no arranque e mostra a versão com a atualização num clique. O mesmo está no [Remote Manager](/pt/docs/controllo-remoto), pelo navegador.

O Unsloth gera uma senha ao acaso quando se instala, e **desliga-se sozinho ao fim de uma hora** se essa senha não for mudada. Esse passo é feito pela secção IA: escolhes a senha do Studio e a chave API é criada com ela. A chave é como a janela e o Remote Manager falam com o motor; os modelos em disco, a memória (VRAM, GTT, RAM, swap) e um teste de chat com os tokens por segundo medidos ficam ao lado.

Tem em conta que:

- **IA e jogos não se usam juntos**: partilham a mesma GPU e a mesma memória;
- com o motor desligado, GPU e RAM voltam a estar totalmente disponíveis para jogar.

## Fontes

- [Unsloth](https://unsloth.ai/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Hugging Face](https://huggingface.co/)
- [Mesa / RADV (driver Vulkan)](https://docs.mesa3d.org/drivers/radv.html)
- [ROCm — hardware suportado](https://rocm.docs.amd.com/) (o `gfx1013` não está na lista)
