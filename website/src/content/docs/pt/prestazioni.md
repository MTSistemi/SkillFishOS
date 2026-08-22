---
title: Desempenho e testes
description: Todos os testes reais da BC-250 no SkillFishOS — capturas, ajustes completos, frequências, tensões, temperaturas e consumo.
group: Referência
order: 3
---

Esta é a **seção completa de medições**: cada passada foi feita na **nossa própria BC-250** com o SkillFishOS, com capturas reais, **todos os ajustes usados** e o registro de **frequências, tensões, temperaturas, consumo e ventoinha** durante a passada.

> **Aviso:** **loteria do silício mais refrigeração.** Os números valem para *este* chip com refrigeração suficiente. O dissipador de fábrica é limitado: comparar testes “em sequência” sem pausa distorce os resultados por causa do *calor acumulado* — deixe a placa esfriar alguns minutos entre as passadas.

## Condições do teste (bancada)

Valem para **todos** os testes abaixo, salvo indicação contrária.

| Item | Valor |
|---|---|
| Placa | **AMD BC-250** — APU Zen 2 “Oberon” + RDNA 2 “Cyan Skillfish” (`gfx1013`) |
| Memória | **16 GB GDDR6** unificada (UMA) |
| Unidades de computação | **40 / 40 ativas** (comutadas em tempo real, veja [GPU](/pt/docs/gpu-overclock)) |
| Kernel | **7.0.10-skillfishos** (linux-tkg) — a versão com que estes números foram tirados; hoje entregamos o **7.2.0**; o 7.1.7 foi remedido com menos de 2 % de diferença |
| Driver | **Mesa 26.0.8** — RADV (Vulkan) / radeonsi (OpenGL), ACO; hoje entregamos a **26.1.6** |
| Governador da GPU | cyan-skillfish — repouso **350 MHz / 700 mV**, carga **2230 MHz / ~1000 mV** |
| Perfil de OC | **Turbo/Crazy** (teto de GPU 2230 MHz, CPU 3,9–4,0 GHz) |
| Teto térmico | **85 °C** (SMU e thermal-guard), ventoinha no **automático** |
| Resolução | **1920×1080** |

> Lembrete de arquitetura: CPU e GPU dividem **o mesmo chip** e **o mesmo orçamento de energia**. Sob carga mista a CPU cede frequência sozinha (≈3,4–3,5 GHz) para caber no orçamento e ficar abaixo de 85 °C — não é defeito, é o chip se protegendo.

---

## Black Myth: Wukong — 112 FPS (1080p)

![Black Myth: Wukong — 112 FPS de média em 1080p na AMD BC-250](/img/benchmarks/wukong-112fps.jpg)

| Ajuste | Valor |
|---|---|
| Resolução | 1920×1080 |
| Limite de FPS | nenhum |
| Tipo de carga | **limitada pela CPU e pelas chamadas de desenho** |
| Reescalonamento | FSR 4 indisponível (RDNA 4) → gamescope FSR1/NIS ou OptiScaler |

**Resultado:** média de **112 FPS** · máximo **128** · mínimo **92** · 1 % piores **101**.

**Telemetria durante a passada** (~4 min):

| Medida | Valor medido |
|---|---|
| Frequência da GPU | ~1,4–1,6 GHz (*sem saturar*: o jogo é limitado pela CPU) |
| Borda da GPU | 83–86 °C |
| Consumo da GPU | ~90–140 W |
| Tensão da GPU | ~970–987 mV |
| Frequência da CPU | ~3,5 GHz (caiu de 3,9 por causa do orçamento compartilhado) |
| Temperatura da CPU | 85 °C (no teto) |
| VRAM | ~1,9 GB (menu) → ~4,4 GB (em jogo) |
| Ventoinha | ~2950–3140 RPM |

> Lição: em *jogo*, num título limitado pelas chamadas de desenho como o Wukong, o que mais conta é a **estabilidade da CPU** sob carga e uma boa refrigeração.

### Governador Balanced contra Performance (ferramenta de teste)

O *sobrevoo* da ferramenta de teste é **limitado pela GPU**, e ali a frequência conta. Pondo o governador em **Performance** pelo Tuner (ele segura a GPU no ponto seguro mais alto sob carga e cai para 350 MHz em repouso):

| Modo do governador | Média | 5 % piores |
|---|---|---|
| **Balanced** (padrão) | 100 FPS | 92 FPS |
| **Performance** | **111 FPS** | **102 FPS** |

**+11 %** na média e nos quadros mais lentos, só por manter a frequência. Por segurança o Tuner limita a GPU a **2200 MHz a 1000 mV** com uma curva de tensão de vários pontos: 2230 MHz a 1000 mV fica abaixo da tensão necessária e pode travar a máquina de vez.

---

## Unigine Superposition — 1080p HIGH: 12938

![Unigine Superposition 1080p High — 12938 pontos na BC-250](/img/benchmarks/superposition-high.jpg)

| Ajuste | Valor |
|---|---|
| Versão | 1.1 |
| Interface gráfica | **OpenGL** |
| Resolução | 1920×1080, tela cheia |
| Sombreadores | **High** |
| Texturas | High |
| Profundidade de campo | ativada |
| Borrão de movimento | ativado |

**Resultado:** **12 938** pontos · FPS mínimo **75,59** · média **96,77** · máximo **127,16**.
**Configuração lida pela ferramenta:** CPU AMD BC-250 **a 3894 MHz**, RAM 7 GB, GPU AMD BC-250 8 GB (Cyan Skillfish), kernel 7.0.10-skillfishos.

---

## Unigine Superposition — 1080p EXTREME: 5513

![Unigine Superposition 1080p Extreme — 5513 pontos na BC-250](/img/benchmarks/superposition-extreme.jpg)

| Ajuste | Valor |
|---|---|
| Versão | 1.1 |
| Interface gráfica | **OpenGL** |
| Resolução | 1920×1080, tela cheia |
| Sombreadores | **Extreme** |
| Texturas | High |
| Profundidade de campo | ativada |
| Borrão de movimento | ativado |

**Resultado:** **5513** pontos · média de **41,25** FPS (mínimo ~32,8 · máximo ~49).

![Unigine Superposition — cena desenhada em tempo real](/img/benchmarks/superposition-scene.jpg)
*Uma cena do Superposition desenhada em tempo real na BC-250.*

---

## Unigine Heaven 4.0 — 113,7 FPS · 2865 pontos

![Unigine Heaven 4.0 — 113,7 FPS, 2865 pontos na BC-250](/img/benchmarks/heaven-113fps.jpg)

| Ajuste | Valor |
|---|---|
| Interface gráfica | **OpenGL** |
| Resolução | 1920×1080, em janela |
| Suavização de bordas | **8×** |
| Qualidade | **Ultra** |
| Tesselação | **Extreme** |

**Resultado:** **113,7 FPS** · **2865** pontos · mínimo **54,8** · máximo **219,5**.
**Plataforma lida pela ferramenta:** Linux 7.0.10-skillfishos x86_64 · CPU AMD BC-250 ×12 · GPU gfx1013.

![Unigine Heaven — cena desenhada em tempo real](/img/benchmarks/heaven-scene.jpg)
*A cena do Heaven desenhada em tempo real na BC-250 durante a passada.*

---

## Computação na GPU — vkpeak (sintético)

Vazão de computação Vulkan na **mesma** placa, antes e depois de liberar as 40 CU.

| Medida | Base 24 CU | SkillFishOS 40 CU |
|---|---|---|
| **FP32** escalar | 6141 GFLOPS | **11 329** GFLOPS *(11 385 a frio)* |
| FP16 vec4 | 12 260 | **22 685** |
| produto escalar int8 | 24 550 GIOPS | **45 495** GIOPS |
| FP64 escalar | 385 | ~640 |
| copy d2d (banda interna) | — | 191 GBPS |

Com as 40 CU ativas: **+85 %** em FP32 sobre a base (≈**11,3 TFLOPS**). A quente, sob esforço contínuo, fica em torno de **10 214 GFLOPS**. Em repouso o governador cai para 350 MHz, com a borda a cerca de 54 °C depois da carga.

## Banda de memória — clpeak

| Medida | Valor |
|---|---|
| Banda GDDR6 medida | **~350–367 GB/s** |
| `mclk` ajustável | **Não** (frequência de memória fixa) |
| Memória vista pelo Vulkan | ~13 GiB (com o GTT ampliado) |

---

## Perfis do Tuner — frequências, tensões, temperaturas

| Perfil | CPU | Tensão da CPU | GPU | Temperatura de pico |
|---|---|---|---|---|
| **Stock** *(padrão da ISO)* | 3500 MHz | — | 1500 MHz | a mais baixa |
| **Performance** | 3700 MHz | ~1106 mV (`scale −16`) | 2000 MHz | equilibrada |
| **Turbo** | 3900 MHz | ~1199 mV (`scale −24`) | 2230 MHz | < 85 °C (teto) |
| **Crazy** | 4,0 GHz | ~1224 mV (`scale −36`) | 2230 MHz | ~83 °C em 120 s de esforço |

- **Máximo rígido de Vid: 1,325 V** (nunca ultrapassado).
- Teto térmico de 85 °C em todos os perfis; ventoinha no automático; em repouso a GPU fica em **350 MHz / 700 mV**.

## A liberação dos 8 núcleos — um +20 % real

A BC-250 vem com **dois núcleos desligados por software**: a máscara de núcleos habilitados da SMU mostra 3 de 4 por CCX. O SkillFishOS a reescreve e leva a CPU a **8 núcleos / 16 threads**, sem BIOS remendada.

Medido no mesmo boot, desligando e ligando os dois núcleos extras em tempo real:

| Carga | 6n/12t | 8n/16t | |
|---|---|---|---|
| Compressão `xz -T` | 6,41 s | **5,11 s** | **+20 %** |
| Inferência de LLM na CPU | 34,0 tok/s | **40,8 tok/s** | **+20 %** |
| Temperatura | 66 °C | 68 °C | +2 °C |

É +20 % e não os +33 % teóricos: a banda de memória e o custo das threads comem a diferença. Ainda assim, **um quinto a mais de desempenho de graça**.

### Overclock com os 8 núcleos

Remedido degrau a degrau, cada um **estável e com 0 MCE**:

| Alvo | Alcançado sob carga | Pontuação | Temperatura | Ventoinha |
|---|---|---|---|---|
| 3500 (referência) | 3475 | 5118 ev/s | 57 °C | — |
| 3700 | 3673 | 5410 | 62 °C | 50 % |
| 3900 | 3872 | 5704 | 71 °C | 68 % |
| **4000** | **3971** | **5849** | **81 °C** | **93 %** |

**Máximo estável: 4000 MHz**, +14 % na pontuação em relação a 3500 — e só alcançável depois de corrigido o controle da ventoinha. **Atenção:** sob carga **combinada de CPU e GPU** a frequência se acomoda em 3375–3492 MHz a 86 °C: passados os ~3900, quem limita é o dissipador, não o silício.

---

## Validação térmica (teste de esforço)

Dados registrados durante a validação automática do Tuner (teste com volta atrás).

| Fase | Frequência | Temperatura | Observações |
|---|---|---|---|
| Repouso | CPU ~2,5 GHz · GPU 350 MHz | k10 46 °C · GPU 45 °C | sem carga |
| **Esforço de CPU** (12 threads, 120 s) | CPU **3,68–3,69 GHz** | k10 **85 °C** (no teto) | número histórico, tirado **antes** da liberação dos 8 núcleos |
| **Esforço de GPU** (laço de vkpeak, 120 s) | GPU **2000 MHz** | borda até **86 °C** | a 86 °C o governador cai para 1819–1900 MHz (thermal-guard); a CPU desce para ~2,2–2,4 GHz por causa do orçamento compartilhado |

---

## Comparações

**O mesmo hardware, mudando só o sistema** — Superposition 1080p Extreme na **mesma** BC-250:

| Sistema | Pontuação |
|---|---|
| **SkillFishOS** (GPU 2230 · CPU 3900, 40 CU) | **5513** |
| Outra distribuição (Bazzite, frequências de fábrica) | 4102 |

→ **+34 % de desempenho real** do mesmíssimo chip, graças às 40 CU liberadas, a um governador que empurra 2230 MHz e ao overclock com undervolt da CPU.

**Contra as Radeon de mesa** (Superposition 1080p High): a BC-250 com SkillFishOS (**12 938**) fica no nível de uma **RX 6600 / 6600 XT** de mais de 200 €, com a computação bruta de uma **RX 6700** (~11,3 TFLOPS) — numa placa de cerca de 50 €.

---

## Ferramentas e método

| Ferramenta | O que mede |
|---|---|
| [vkpeak](https://github.com/nihui/vkpeak) | vazão FP32/FP16/int8 pelo Vulkan |
| [clpeak](https://github.com/krrishnarraj/clpeak) | banda de memória e vazão OpenCL |
| [sysbench](https://github.com/akopytov/sysbench) | esforço e medição da CPU (o Tuner também o usa) |
| [Unigine Superposition / Heaven](https://benchmark.unigine.com/) | testes gráficos OpenGL |
| MangoHud em jogo | FPS e tempo de quadro em jogos reais |
| telemetria própria | frequência, temperatura, consumo e ventoinha pelo sysfs do `amdgpu`, `k10temp`, `nct6686` |

## Fontes

- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) · [sysbench](https://github.com/akopytov/sysbench) · [Unigine](https://benchmark.unigine.com/)
- [bc250-40cu-unlock (duggasco)](https://github.com/duggasco/bc250-40cu-unlock) — liberação das CU
- [bc250.info](https://bc250.info) — pontos seguros e notas térmicas da comunidade
- [OptiScaler](https://github.com/optiscaler/OptiScaler) — reescalonamento por jogo
