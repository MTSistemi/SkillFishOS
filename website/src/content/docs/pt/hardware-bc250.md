---
title: O hardware AMD BC-250
description: A placa, a APU, as especificações e os defeitos conhecidos.
group: Introdução
order: 2
---

A **AMD BC-250** é uma placa compacta baseada numa **APU semipersonalizada** de codinome *Oberon* para a CPU e *Cyan Skillfish* para os gráficos: a mesma família de silício dos consoles da geração atual da AMD. Ela foi feita para sistemas de mineração (normalmente com várias placas por gabinete) e hoje aparece no mercado de segunda mão por preços baixos.

## Especificações principais

| Componente | Detalhe |
|---|---|
| **CPU** | 8 núcleos / 16 threads **Zen 2** (a placa mostra 6; o SkillFishOS destrava os outros dois pelo SMU) (“Oberon”), até **3,9 GHz** (turbo), 4,0 GHz validados |
| **GPU** | **RDNA 2** “Cyan Skillfish” (`gfx1013`), até **40 unidades de computação** destraváveis |
| **Memória** | **16 GB GDDR6** compartilhada (UMA) entre CPU e GPU |
| **Computação** | ~**11,3 TFLOPS** FP32 com 40 CU / 2000 MHz (medido com o vkpeak) |
| **Banda de memória** | ~350–367 GB/s (medido com o clpeak) |
| **Saída de vídeo** | 1× DisplayPort |

A memória é **unificada**: a GDDR6 é dividida entre o sistema e os gráficos. De fábrica cerca de 8 GB ficam como VRAM, mas no Linux o espaço de vídeo pode ser ampliado pelo **GTT** (Graphics Translation Table), fazendo o Vulkan enxergar uns 13 GiB — especialmente útil para os modelos de IA.

## Destravamento dos 8 núcleos da CPU

A placa se apresenta como **6 núcleos / 12 threads**, mas os núcleos físicos são **oito**: os dois que faltam não estão com defeito, estão desligados por configuração do produto. Quem entrega isso é a máscara de presença dos núcleos — em praticamente todas as placas ela vale `0x77`, um valor **simétrico**: quatro núcleos por complexo, com o quarto desativado nos dois. Um descarte real de fabricação deixaria um padrão assimétrico, porque defeitos não se distribuem com tanta arrumação.

O SkillFishOS reescreve essa máscara pelo **SMU** no boot e a placa volta como **8 núcleos / 16 threads**. Sem BIOS modificada e sem ferro de solda.

O serviço traz duas salvaguardas: se a máscara **não** for `0x77`, ele não mexe em nada, porque um padrão diferente pode significar que os núcleos foram mesmo desativados de fábrica; e o reinício a quente só acontece **depois** de a escrita ter sido relida e confirmada, então não há como entrar num laço de reinícios.

> Medido na nossa própria placa: **+20%** em trabalho multithread. Em cargas de poucas threads não muda nada, como era de esperar: dois núcleos a mais não fazem uma thread correr mais rápido.

A engenharia reversa é a [bc250-core-unlock (rw-r-r-0644)](https://github.com/rw-r-r-0644/bc250-core-unlock): sem esse trabalho o recurso não existiria.

## Destravamento das 40 CU

A GPU tem 40 CU, mas o driver ativa só **24** por padrão. O SkillFishOS **leva a 40 em tempo real** (sem reiniciar): dá boot com o mínimo do driver e um serviço sobe para 40 na inicialização, ajustável pelo [Tuner](/pt/docs/app-native). A engenharia reversa do destravamento está documentada no [bc250-40cu-unlock](https://github.com/duggasco/bc250-40cu-unlock); o controle em tempo real via `umr` é inspirado no [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager) (reescrito do zero).

> Com as 40 CU ativas, o SkillFishOS mede **11385 GFLOPS** FP32 (vkpeak) a frio, contra cerca de 6141 de uma configuração base de 24 CU: aproximadamente **+85%**.

## Defeitos do hardware que vale conhecer

A BC-250 é hardware de “mineração” reaproveitado: tem limitações que o SkillFishOS contorna por software. Conhecê-las explica muitas escolhas do sistema.

### Hot-Plug Detect (HPD) do DisplayPort defeituoso

A detecção do monitor no conector DisplayPort **não funciona**: a placa não “vê” quando você liga uma tela. O SkillFishOS resolve com um serviço próprio (`skillfish-dp-hotswap`) que força a detecção no boot e fica de olho nas trocas de monitor durante o uso, mais o parâmetro de kernel `video=DP-1:e` como reserva. Veja [Área de trabalho](/pt/docs/desktop) e [Solução de problemas](/pt/docs/risoluzione-problemi).

### Suspensão ACPI quebrada

A suspensão (**o s2idle está quebrado**): a placa dorme mas **não acorda** e precisa de um reset. Além disso, uma máquina suspensa fica inalcançável à distância. Por isso o SkillFishOS **desativa em definitivo** todos os estados de sono (veja [Área de trabalho](/pt/docs/desktop)). É uma medida obrigatória.

### IOMMU inutilizável

A IOMMU da BC-250 é instável: **nunca deve ser ativada**. O sistema sempre dá boot sem IOMMU.

### Sensores térmicos

Só está disponível o sensor de temperatura da *borda* da GPU; **não existe sensor de temperatura da VRAM**. A refrigeração de fábrica é justa, então comparar testes rodados um atrás do outro não vale (efeito de calor acumulado): deixe a placa esfriar alguns minutos entre as passadas.

## Refrigeração, gabinetes imprimíveis e ventoinhas

A BC-250 chega **nua**, pensada para prateleiras de mineração com cinco ventoinhas “gritonas” de 80 mm alimentadas pelo conector de distribuição. Para uso em mesa é preciso refrigeração própria. É preciso esfriar **duas coisas**: o dissipador da APU **e** os chips de **GDDR6**, que esquentam muito e não têm sensor de temperatura (veja [GPU e overclock](/pt/docs/gpu-overclock)).

**O que funciona (dicas da comunidade):**

- **2 ventoinhas de 120 mm** de pressão estática apontadas para o dissipador é o arranjo de mesa mais comum; sem gabinete dá para apoiá-las direto sobre o dissipador (com abraçadeiras pelas aletas).
- Uma **ventoinha dedicada à VRAM** é muito recomendada se você faz overclock: os módulos GDDR6 são o ponto mais quente.
- A ventoinha se liga ao conector **PWM de 4 pinos** da placa — o SkillFishOS a controla pelo `nct6686` (sensores) e a deixa em **automático**.

**Gabinetes e dutos (STL gratuitos, para imprimir em 3D):**

| Modelo | Autor | Observações |
|---|---|---|
| [Console Style Case](https://www.thingiverse.com/thing:7172528) | Arthrimus | Gabinete “console” com espaço para a fonte, duto para **1× 120 mm** |
| [ASRock BC-250 Shell Case](https://www.printables.com/model/1228207-asrock-amd-bc-250-shell-case) | onemorecap | Casca de encaixe, montagem rápida de uma ventoinha |
| [Yet Another BC-250 Fan Shroud](https://www.printables.com/model/1339540-yet-another-bc-250-fan-shroud) | ViRazY | Entrada de **140 mm** e saída de **120 mm** |
| [Case ATX PSU & Fan Duct](https://www.printables.com/model/1616167-amd-bc-250-case-atx-psu-fan-duct) | ZMASLO | Usa uma fonte ATX comum, duto que não danifica o dissipador |
| [Standard ATX PSU case](https://www.thingiverse.com/thing:7269520) | CatSiewDai | Gabinete completo para fontes ATX |
| [OC vRAM Fan Kit (remix)](https://www.thingiverse.com/thing:7271946) | marccyberwiz | Kit de ventoinha **dedicada à VRAM** para overclock |
| [NexGen3D — DIY Steam Machine (Bazzite)](https://www.printables.com/model/1499974-nexgen3d-diy-steam-machine-powered-by-bazzite) | NexGen3D | Gabinete completo no estilo **Steam Machine** para a BC-250 |
| [NexGen3D — Steam Machine PRO (refrigeração líquida)](https://www.printables.com/model/1614131-nexgen3d-diy-steam-machine-pro-liquid-cooled-bc-25/files) | NexGen3D | Versão **PRO com líquida** (AIO) — refrigeração máxima |
| [NexGen3D — suporte AIO para a BC-250](https://www.printables.com/model/1554003-nexgen3d-aio-mount-for-the-bc-250) | NexGen3D | Suporte para montar um **AIO** (refrigeração líquida) na BC-250 |

> Guia de referência sobre refrigeração: [Cooling Solutions — amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/).

## Fontes

- [bc250.info](https://bc250.info) — wiki da comunidade
- [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs) — documentação técnica (inclusive a de [refrigeração](https://elektricm.github.io/amd-bc250-docs/hardware/cooling/))
- [mothenjoyer69/bc250-documentation](https://github.com/mothenjoyer69/bc250-documentation) — notas de hardware e refrigeração
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — destravamento das unidades de computação
- [bc250_memcfg (fanoush)](https://github.com/fanoush/bc250_memcfg) — configuração da memória
- Driver do kernel Linux `amdgpu` — [docs.kernel.org/gpu/amdgpu](https://docs.kernel.org/gpu/amdgpu/)
