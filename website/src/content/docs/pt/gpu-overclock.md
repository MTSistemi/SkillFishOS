---
title: GPU, CPU, overclock e undervolt
description: Como o SkillFishOS controla frequências, tensões e temperaturas da BC-250, com os números reais medidos no hardware.
group: Sistema
order: 2
---

Numa APU comum as frequências se ajustam pelo sysfs do `amdgpu`. Na BC-250 **isso não funciona**: o controle passa pela **SMU** (System Management Unit) e exige ferramentas próprias. O SkillFishOS reúne todas elas, com uma curva segura de fábrica e um sistema de proteção térmica.

> **Aviso:** **loteria do silício.** Todos os números desta página foram **medidos na nossa BC-250**. Cada placa é diferente: uma aceita uma curva mais puxada, outra menos. Por isso o SkillFishOS **inicia com a curva de fábrica** (perfil **Performance**, teto de 2100 MHz) e deixa você trocá-la pelo [Tuner](/pt/docs/control-center), que testa cada curva **na sua placa** com um teste automático de 25 segundos e volta sozinho se ela não aguentar.

## A curva tensão/frequência e os três perfis

![a curva de tensão e frequência no Tuner, com a tabela de pontos e os três perfis](/img/control-center-tuner.png)

O [Tuner](/pt/docs/control-center) governa a GPU com uma **curva tensão/frequência**: MHz na horizontal, milivolts na vertical, pontos que você arrasta no gráfico ou escreve na tabela ao lado. Três perfis movem o **teto** da curva:

| Perfil | Teto da GPU | Observações |
|---|---|---|
| **Cautious** | 1850 MHz | O ponto ideal com a refrigeração de fábrica: quase os mesmos quadros, dez graus a menos |
| **Balanced** | 2000 MHz | Equilíbrio entre frequência e calor |
| **Performance** | 2100 MHz | A curva de quinze pontos medida na placa de desenvolvimento: a que enviamos por padrão |

**Aplicar é um teste, não uma gravação imediata.** Uma curva que pede tensão de menos trava a placa, e na BC-250 uma travada só se resolve tirando a energia. Por isso Aplicar mantém a curva anterior no disco, testa a candidata por **25 segundos** e espera confirmação: aperte Manter para gravá-la de verdade; caso contrário — ou se a placa travar e reiniciar sozinha — a curva anterior volta na inicialização.

## O governador V/F da GPU

As frequências da GPU são conduzidas pelo **skillfish-vf-governor**, nosso serviço que tira o clock e a tensão do governador de fábrica e os controla direto pela SMU, mantendo um **teto de frequência** que o calor e o consumo podem baixar e, quando a placa se acalma, devolver. Um processo separado, o **skillfish-vf-watchdog**, assume o controle se o governador travar com o clock forçado.

Medido em *Black Myth: Wukong*, mesma sessão, mesmos 84 °C nas duas passadas: **+4,5%** com a placa fria, **+11%** com a placa quente, frente ao governador de fábrica. A vantagem cresce com a temperatura porque o governador de fábrica perde clock à medida que a placa esquenta, e o nosso não.

> O sysfs padrão do amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **não** controla a BC-250 — só o skillfish-vf-governor controla. A GPU só sobe até o teto com **saturação gráfica** de verdade.

## Overclock e undervolt da CPU

A CPU (**8 núcleos / 16 threads** Zen 2 “Oberon”, dois deles liberados pelo SkillFishOS via SMU — também antes de iniciar, com um programa EFI, numa única reinicialização) é tratada, para o overclock, por um serviço de uma passada só, o **`bc250-smu-oc.service`**, que aplica os valores de `/etc/bc250-smu-oc.conf` pelo projeto [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Depois de aplicar ele aparece como *inactive* — é normal (é de uma passada só).

O que medimos forçando a **nossa** placa:

- **3700 MHz** com undervolt para cerca de **1106 mV** (`scale −16`);
- **3900 MHz** a cerca de **1199 mV** (`scale −24`);
- **4,0 GHz** validados a cerca de **1224 mV** (`scale −36`) por 120 s de esforço contínuo, com pico de **83 °C** — o máximo utilizável neste exemplar;
- **teto rígido de Vid: 1,325 V** (nunca ultrapassado).

**Undervolt** não é “forçar”: é fazer o mesmo trabalho com **menos calor e menos consumo**. Numa dada frequência, baixar a tensão até o limite da estabilidade derruba a temperatura e deixa folga térmica para o resto da APU.

### Acoplamento térmico CPU↔GPU

CPU e GPU dividem o **mesmo chip** e o **mesmo orçamento de energia**. Sob carga **mista** (um jogo pesado: CPU e GPU juntas) a APU se protege e a CPU cai sozinha para cerca de **3450 MHz**, para caber no orçamento e ficar abaixo de 85 °C. **Isso não é defeito**: o chip se protege abrindo mão dos megahertz menos úteis. Pelo mesmo motivo, um undervolt na CPU deixa mais “espaço” térmico para a GPU, e vice-versa.

## As 40 unidades de computação, em tempo real

A BC-250 tem **40 CU** (20 pares), mas o driver habilita **24** por padrão. O SkillFishOS as leva a 40 **na inicialização, sem passo extra**; pelo [Tuner](/pt/docs/control-center) você ajusta o número **ao vivo**, escrevendo a quantidade desejada ou clicando nos 20 quadradinhos pareados. As primeiras 24 CU são travadas pelo driver e ficam sempre ligadas.

Com as 40 CU a GPU marca **11385 GFLOPS** FP32 (vkpeak) a frio, contra cerca de **6141** com as 24 de partida: **+85%**. Sob esforço contínuo (a quente) fica em torno de **10214 GFLOPS**. A banda de memória medida (clpeak) é de **~350–367 GB/s**.

> **Loteria do silício.** Em chips recuperados ou de “descarte” algumas CU podem ser fracas. O [Tuner](/pt/docs/control-center) tem um **“Teste de CU”** que força cada par com vkpeak e aponta falhas ou travamentos da GPU, para você confirmar que o seu chip aguenta as 40. (Mecanismo via `umr`, escrevendo as máscaras WGP — crédito ao [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), reimplementação própria.)

## Proteção térmica — o teto de 85 °C

O limite térmico é de **85 °C**, garantido em dois níveis:

1. **pelo governador**: `gradi_max` e `watt_max` em `/etc/skillfish-vf-governor.json` baixam o teto de frequência *antes* de cruzar os 85 °C ou o limite de potência (o nosso, não o do firmware), e o devolvem quando a placa se acalma;
2. **pelo sistema**: **skillfish-vf-watchdog**, um processo separado que assume o controle se o governador travar com o clock forçado.

O que convém saber sobre a refrigeração de fábrica (veja também [Hardware BC-250](/pt/docs/hardware-bc250) para **gabinetes imprimíveis em 3D e ventoinhas recomendadas**):

- o dissipador de fábrica é **limitado**: comparar testes “em sequência” distorce os resultados por causa do *calor acumulado* — deixe a placa esfriar alguns minutos entre as passadas;
- só existe o sensor de *borda* da GPU; **não há sensor de temperatura da VRAM**;
- a banda de memória é boa, mas o `mclk` **não** é ajustável.

## Um caso real: jogos limitados pela CPU

Alguns títulos — como *Black Myth: Wukong* em **jogo** — são limitados pela **CPU e pelas chamadas de desenho**: os FPS quase não dependem da resolução nem da frequência da GPU. Ali ajudam o overclock de **CPU** e uma boa refrigeração. Para reescalonamento, o FSR 4 passa pelo [OptiScaler](https://github.com/optiscaler/OptiScaler) na rota DLSS do jogo (veja [Jogos](/pt/docs/gaming)).

Quando a carga **está mesmo** limitada pela GPU (por exemplo o *sobrevoo* do benchmark de Wukong), o teto da curva conta: no [Tuner](/pt/docs/control-center) suba o perfil de Cautious ou Balanced para **Performance** (2100 MHz), ou escreva sua própria curva. A vantagem medida em Wukong contra o antigo governador de fábrica é de **+4,5% com a placa fria e +11% com a placa quente**: o governador V/F não perde clock ao esquentar, o que o de fábrica faz. Continua havendo um limite físico intransponível: **1129 mV**, o teto de tensão que o amdgpu declara para essa GPU — nenhuma curva pode ultrapassá-lo.

## Tudo isso sem terminal

Frequências, a curva da GPU, ventoinha e unidades de computação se ajustam pela janela do **Tuner**, com os três perfis da GPU prontos e um **teste automático de 25 segundos que volta à curva anterior** se a sua placa não a aguentar — veja [Control Center](/pt/docs/control-center). É o caminho recomendado: comece em Cautious, suba para Balanced ou Performance, e o Tuner valida tudo na **sua** BC-250.

## Fontes

- skillfish-vf-governor — nosso governador V/F da GPU, controle direto pela SMU com teto configurável
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock e undervolt da CPU pela SMU
- [bc250.info](https://bc250.info) — pontos seguros e notas térmicas da comunidade
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — testes de FP32 e de banda de memória
