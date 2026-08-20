---
title: O kernel sob medida
description: O kernel linux-tkg com patches para a BC-250, os parâmetros de boot e os kernels a evitar.
group: Sistema
order: 1
---

O coração das otimizações do SkillFishOS é um **kernel compilado sob medida** para a BC-250, baseado no [linux-tkg](https://github.com/Frogging-Family/linux-tkg) — uma receita de compilação da *Frogging Family* que aplica patches voltados a desempenho e jogos.

## Versão e patches

O kernel do SkillFishOS é a versão **`7.1.7-skillfishos`** (a série 7.0 saiu de manutenção). Além dos patches padrão do linux-tkg, ele inclui:

- o patch de **liberação de frequência** da BC-250 (faixa de 350 a 2230 MHz);
- o patch de **40 CU**, que ativa todas as unidades de computação da GPU;
- um patch próprio **RDSEED-quiet**, que cala uma mensagem barulhenta do kernel neste hardware.

O pacote do kernel (imagem e cabeçalhos) é publicado como entrega e fica **travado** (`apt-mark hold`), para que uma atualização do Debian não o troque por um kernel inadequado. É o kernel padrão no GRUB.

## Parâmetros de boot (cmdline)

A linha de comando do kernel está assim, e cada parâmetro tem um motivo preciso:

```
mitigations=off
split_lock_detect=off
ttm.pages_limit=1572864
ttm.page_pool_size=1572864
```

| Parâmetro | O que faz |
|---|---|
| `mitigations=off` | desliga as proteções contra Spectre e Meltdown para espremer o desempenho (uma escolha aceitável num console de casa) |
| `ttm.pages_limit` / `ttm.page_pool_size` | o teto do GTT, contado em páginas de 4 KiB: 1572864 = 6 GiB, então o Vulkan enxerga uns 13 GiB somando VRAM e GTT (útil para a IA). Antes era o `amdgpu.gttsize`, em desuso desde o kernel 7.x: com os dois definidos, o driver obedece a este e avisa a cada boot |
| `split_lock_detect=off` | desliga o detector de *split lock*, que do contrário sufoca processos que fazem acessos atômicos desalinhados (jogos e emuladores fazem) |

> **E o DisplayPort?** O HPD da BC-250 é defeituoso (veja [hardware](/pt/docs/hardware-bc250)), mas o SkillFishOS **não** usa o parâmetro `video=DP-1:e`: o serviço `skillfish-dp-hotswap` acompanha o EDID e reativa a saída quando o monitor volta. Isso cobre também o caso de ligar o monitor depois da placa, que o parâmetro sozinho não resolve.

> **Unidades de computação em tempo real.** O SkillFishOS não usa mais o parâmetro `amdgpu.bc250_cc_write_mode=3` (que cravava 40 CU no boot e impedia mudanças em tempo real). Agora o sistema dá boot no mínimo do driver (24 CU) e um serviço **leva a 40 em tempo real** na inicialização; dá para mudar sem reiniciar pelo [Tuner](/pt/docs/app-native). Veja [GPU e overclock](/pt/docs/gpu-overclock).

## Kernels a evitar

Nem todo kernel recente se dá bem com este hardware. Em especial, as séries **6.15.0–6.15.6** e **6.17.8–6.17.10** são conhecidas por dar problema e é melhor desviar delas. O SkillFishOS traz o próprio kernel testado justamente para escapar dessas regressões — veja [Atualizações](/pt/docs/aggiornamenti).

## IOMMU

Como diz a página de [hardware](/pt/docs/hardware-bc250), **a IOMMU nunca deve ser ativada** na BC-250: ela é instável. O kernel sempre dá boot com a IOMMU desligada.

## Por que um kernel próprio e não o XanMod ou o padrão

- Ao **kernel padrão do Debian** faltam os patches da BC-250 (liberação de frequência, 40 CU) e ele segue as regressões citadas acima.
- O **linux-tkg** facilita aplicar os patches próprios e escolher escalonadores e opções pensados para jogos.
- Compilar por conta própria significa que atualizamos o kernel **só quando uma versão nova traz benefício de verdade** e depois de testá-la no hardware.

## Fontes

- [linux-tkg (Frogging-Family)](https://github.com/Frogging-Family/linux-tkg)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock)
- [Parâmetros do driver amdgpu](https://docs.kernel.org/gpu/amdgpu/module-parameters.html)
- [bc250.info](https://bc250.info) — notas sobre o kernel e a linha de comando
