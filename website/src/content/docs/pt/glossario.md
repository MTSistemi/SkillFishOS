---
title: Glossário
description: Os termos técnicos do SkillFishOS e da BC-250, explicados em poucas palavras.
group: Referência
order: 5
---

Os termos que se repetem por toda a documentação, cada um explicado em uma linha. Em ordem alfabética.

## Hardware e APU

**APU** — *Accelerated Processing Unit*: um chip que reúne CPU e GPU na mesma pastilha. A BC-250 traz uma semipersonalizada da AMD.

**BC-250** — a placa em que o SkillFishOS roda: APU Zen 2 + RDNA 2, 16 GB GDDR6, feita originalmente para mineração.

**Cyan Skillfish** — o codinome da parte **gráfica** (GPU) da APU da BC-250. Daí o nome “SkillFish”.

**Oberon** — o codinome da parte de **CPU** (Zen 2) dessa mesma APU.

**Unidade de computação (CU)** — os blocos de cálculo da GPU. A BC-250 tem 40, mas de fábrica mostra menos: o SkillFishOS **destrava todas** (veja [kernel](/pt/docs/kernel)).

**gfx1013** — o identificador da arquitetura gráfica da BC-250 (família RDNA 2). Importa porque **o ROCm não a suporta** → no lugar dele se usa o Vulkan.

**RDNA 2** — a arquitetura gráfica da AMD desta GPU (a mesma família dos consoles atuais).

**Zen 2** — a arquitetura de CPU da AMD desta APU (**8 núcleos / 16 threads**: a placa mostra 6, o SkillFishOS destrava os outros dois pelo SMU).

**GDDR6** — o tipo de memória da placa: rápida e aqui **compartilhada** entre CPU e GPU.

**UMA** — *Unified Memory Architecture*: CPU e GPU usam **o mesmo** conjunto de memória (os ~16 GB de GDDR6).

**GTT** — *Graphics Translation Table*: o mecanismo que deixa a GPU usar memória do sistema além da VRAM dedicada. O SkillFishOS o amplia para o Vulkan enxergar uns 13 GiB (útil para a IA).

## Frequências, tensões, temperatura

**SMU** — *System Management Unit*: o microcontrolador dentro da APU que comanda frequências e tensões. Na BC-250 o controle passa **só** por ele, e não pelos arquivos padrão do amdgpu no sysfs.

**Governador SMU** — o serviço (`cyan-skillfish-governor`) que define os *pontos seguros* de frequência e tensão da GPU.

**sclk / mclk** — frequência do **núcleo** gráfico (sclk) e da **memória** (mclk). Na BC-250 a mclk **não** pode ser ajustada.

**Undervolt** — baixar a tensão mantendo a frequência: o mesmo trabalho, **menos calor e menos consumo**. Veja [GPU e overclock](/pt/docs/gpu-overclock).

**Overclock (OC)** — subir as frequências acima das de fábrica para ganhar desempenho.

**Vid** — a tensão que o chip pede numa dada frequência. Na BC-250 o máximo absoluto é **1,325 V**.

**Proteção térmica** — o vigia do sistema que baixa as frequências se passar de 85 °C.

**Calor acumulado (heat-soak)** — o calor que se acumula e distorce testes rodados um atrás do outro: deixe a placa esfriar entre as passadas.

**Loteria do silício** — o fato de cada chip aguentar um overclock e um undervolt diferentes; por isso o SkillFishOS valida os perfis **na sua** placa.

## Software de sistema

**Debian sid** — o ramo *unstable* do Debian, sempre atualizado mas sujeito a regressões: a base do SkillFishOS (veja [Atualizações](/pt/docs/aggiornamenti)).

**KDE Plasma 6** — o ambiente de trabalho usado, vestido com o visual steampunk.

**linux-tkg** — a receita de compilação do kernel (Frogging-Family) em que se baseia o kernel sob medida do SkillFishOS.

**Mesa / RADV** — os drivers gráficos de código aberto; o **RADV** é o driver **Vulkan** usado pela GPU da BC-250.

**ROCm** — o conjunto de computação “oficial” da AMD: **não** dá suporte ao gfx1013, então não é usado.

**Vulkan** — a interface de gráficos e computação usada tanto para jogar quanto para a **IA** (Unsloth Studio) na BC-250.

**Btrfs** — o sistema de arquivos copy-on-write com snapshots que dá a “rede de segurança” (veja [Armazenamento e snapshots](/pt/docs/storage-snapshot)).

**Snapper** — a ferramenta que cria snapshots Btrfs automáticos antes e depois das atualizações.

**grub-btrfs** — faz os snapshots aparecerem no menu do GRUB, para voltar atrás já no boot.

**Fixação do APT (pinning)** — manter um pacote numa versão verificada, para os componentes frágeis neste hardware.

**reprepro** — a ferramenta com que se gerencia o repositório APT assinado do SkillFishOS.

**HPD** — *Hot-Plug Detect*: a detecção do monitor conectado. Na BC-250 é **defeituosa** → o serviço `skillfish-dp-hotswap`.

**s2idle / suspensão** — os estados de sono do ACPI: **quebrados** na BC-250 e por isso desligados.

**IOMMU** — a unidade de gestão de memória para virtualizar entrada e saída: instável na BC-250, **nunca** é ativada.

## Jogos e IA

**Proton** — a camada de compatibilidade da Valve que roda jogos de Windows no Linux pela Steam.

**gamescope** — o microcompositor da Valve para jogos (sessão “console”, escalonamento FSR1/NIS).

**EmuDeck / ES-DE** — o instalador de emuladores e a interface para emulação.

**FSR / OptiScaler** — tecnologias de **escalonamento**. O FSR 4 não está disponível (precisa de RDNA 4); usam-se FSR1/NIS ou OptiScaler.

**Unsloth Studio** — motor e interface da IA local: roda modelos GGUF na GPU e oferece uma API compatível com a da OpenAI.

**qwen3:14b** — o modelo de IA de referência, rodando inteiramente na GPU.

**Tuner** — o aplicativo próprio do SkillFishOS para ajustar o hardware com teste e retorno (veja [Aplicativos próprios](/pt/docs/app-native)).

## Fontes

- [bc250.info](https://bc250.info) · [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- [Documentação do amdgpu](https://docs.kernel.org/gpu/amdgpu/) · [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html)
