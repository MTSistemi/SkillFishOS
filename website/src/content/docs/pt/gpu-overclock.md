---
title: GPU, CPU, overclock e undervolt
description: Como o SkillFishOS controla frequências, tensões e temperaturas da BC-250, com os números reais medidos no hardware.
group: Sistema
order: 2
---

Numa APU comum as frequências se ajustam pelo sysfs do `amdgpu`. Na BC-250 **isso não funciona**: o controle passa pela **SMU** (System Management Unit) e exige ferramentas próprias. O SkillFishOS reúne todas elas, já configuradas com perfis seguros e um sistema de proteção térmica.

> **Aviso:** **loteria do silício.** Todos os números desta página foram **medidos na nossa BC-250**. Cada placa é diferente: uma aceita um undervolt mais profundo, outra menos. Por isso o SkillFishOS **sempre inicia no perfil Stock** e deixa você subir pelo [Tuner](/pt/docs/app-native), que valida cada perfil **na sua placa** com um teste automático e volta atrás.

## Os quatro perfis

O [Tuner](/pt/docs/app-native) oferece **quatro perfis**. A ISO inicia em **Stock**; os demais ficam a um clique depois do teste.

| Perfil | CPU | GPU | Observações |
|---|---|---|---|
| **Stock** *(padrão da ISO)* | 3500 MHz | 1500 MHz | Compatibilidade máxima com qualquer BC-250 |
| **Performance** | 3700 MHz · ~1106 mV | 2000 MHz | Equilibrado e com undervolt |
| **Turbo** | 3900 MHz · ~1199 mV | 2230 MHz | Subida forte, validada sob o teto de 85 °C |
| **Crazy** | 4,0 GHz · ~1224 mV | 2230 MHz | Máximo validado (~83 °C sob esforço) |

Todos os perfis respeitam o mesmo **teto térmico de 85 °C** e mantêm a **ventoinha no automático**.

## O governador SMU da GPU

As frequências da GPU são conduzidas pelo **[cyan-skillfish-governor](https://github.com/Magnap/cyan-skillfish-governor)** (escrito em Rust), um serviço do sistema configurado em `/etc/cyan-skillfish-governor/config.toml`. Ele define *pontos seguros* de frequência e tensão: **350 MHz / 700 mV** em repouso e o valor do perfil sob carga (por exemplo 1500/900 no Stock, 2230/1000 no Turbo).

> O sysfs padrão do amdgpu (`power_dpm_force_performance_level`, `pp_dpm_sclk`) **não** controla a BC-250 — só o governador SMU controla. A GPU só sobe à frequência máxima com **saturação gráfica** de verdade.

## Overclock e undervolt da CPU

A CPU (**8 núcleos / 16 threads** Zen 2 “Oberon”, dois deles liberados pelo SkillFishOS via SMU) é tratada por um serviço de uma passada só, o **`bc250-smu-oc.service`**, que aplica os valores de `/etc/bc250-smu-oc.conf` pelo projeto [bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc). Depois de aplicar ele aparece como *inactive* — é normal (é de uma passada só).

O que medimos forçando a **nossa** placa:

- **3700 MHz** (perfil *Performance*) com undervolt para cerca de **1106 mV** (`scale −16`);
- **3900 MHz** (perfil *Turbo*) a cerca de **1199 mV** (`scale −24`);
- **4,0 GHz** (perfil *Crazy*) validados a cerca de **1224 mV** (`scale −36`) por 120 s de esforço contínuo, com pico de **83 °C** — o máximo utilizável neste exemplar;
- **teto rígido de Vid: 1,325 V** (nunca ultrapassado).

**Undervolt** não é “forçar”: é fazer o mesmo trabalho com **menos calor e menos consumo**. Numa dada frequência, baixar a tensão até o limite da estabilidade derruba a temperatura e deixa folga térmica para o resto da APU.

### Acoplamento térmico CPU↔GPU

CPU e GPU dividem o **mesmo chip** e o **mesmo orçamento de energia**. Sob carga **mista** (um jogo pesado: CPU e GPU juntas) a APU se protege e a CPU cai sozinha para cerca de **3450 MHz**, para caber no orçamento e ficar abaixo de 85 °C. **Isso não é defeito**: o chip se protege abrindo mão dos megahertz menos úteis. Pelo mesmo motivo, um undervolt na CPU deixa mais “espaço” térmico para a GPU, e vice-versa.

## As 40 unidades de computação, em tempo real

A BC-250 tem **40 CU** (20 WGP, 1 WGP = 2 CU), mas o driver habilita **24** por padrão. O SkillFishOS as leva a 40 **em tempo real, sem reiniciar**: o sistema começa no mínimo do driver (24 CU) e um serviço sobe para 40 na inicialização; pelo [Tuner](/pt/docs/app-native) você ajusta o número **ao vivo**, com uma grade de quadradinhos e perfis de 24/32/40. As primeiras 24 CU são travadas pelo driver e ficam sempre ligadas.

Com as 40 CU a GPU marca **11385 GFLOPS** FP32 (vkpeak) a frio, contra cerca de **6141** com as 24 de partida: **+85%**. Sob esforço contínuo (a quente) fica em torno de **10214 GFLOPS**. A banda de memória medida (clpeak) é de **~350–367 GB/s**.

> **Loteria do silício.** Em chips recuperados ou de “descarte” algumas CU podem ser fracas. O [Tuner](/pt/docs/app-native) tem um **“Teste de CU”** que força cada par e aponta falhas ou travamentos da GPU, para você confirmar que o seu chip aguenta as 40. (Mecanismo via `umr`, escrevendo as máscaras WGP — crédito ao [bc250-cu-live-manager](https://github.com/WinnieLV/bc250-cu-live-manager), reimplementação própria.)

## Proteção térmica — o teto de 85 °C

O limite térmico é de **85 °C**, garantido em dois níveis:

1. **pela SMU**: o valor `max_temperature` da configuração faz o chip reduzir as frequências *antes* de cruzar os 85 °C (evitando o estrangulamento bruto);
2. **pelo sistema**: um vigia **thermal-guard** que, se a temperatura passar do teto, baixa as frequências de 100 em 100 MHz até voltar à faixa.

O que convém saber sobre a refrigeração de fábrica (veja também [Hardware BC-250](/pt/docs/hardware-bc250) para **gabinetes imprimíveis em 3D e ventoinhas recomendadas**):

- o dissipador de fábrica é **limitado**: comparar testes “em sequência” distorce os resultados por causa do *calor acumulado* — deixe a placa esfriar alguns minutos entre as passadas;
- só existe o sensor de *borda* da GPU; **não há sensor de temperatura da VRAM**;
- a banda de memória é boa, mas o `mclk` **não** é ajustável.

## Um caso real: jogos limitados pela CPU

Alguns títulos — como *Black Myth: Wukong* em **jogo** — são limitados pela **CPU e pelas chamadas de desenho**: os FPS quase não dependem da resolução nem da frequência da GPU. Ali ajudam o overclock de **CPU** e uma boa refrigeração. Para reescalonamento, o FSR 4 **não está disponível** (exige hardware RDNA 4); use gamescope (FSR1/NIS) ou o [OptiScaler](https://github.com/optiscaler/OptiScaler) por jogo.

Quando a carga **está mesmo** limitada pela GPU (por exemplo o *sobrevoo* do benchmark de Wukong), a frequência conta: no **Tuner** dá para pôr o **governador em “Performance”**, que segura a GPU no ponto seguro mais alto sob carga (em repouso ela ainda cai para 350 MHz). Medido no benchmark de Wukong: **100 → 111 FPS de média (+11%)**, 92 → 102 nos quadros mais lentos. Por segurança o Tuner limita a GPU a **2200 MHz a 1000 mV** (o máximo estável com a refrigeração de fábrica) com uma curva de tensão de vários pontos: forçar 2230 MHz a 1000 mV fica abaixo da tensão necessária e pode travar a máquina de vez.

## Tudo isso sem terminal

Frequências, undervolt, ventoinha e unidades de computação se ajustam pela janela do **Tuner**, com os quatro perfis prontos e **teste automático com volta atrás** se a sua placa não segurar um valor — veja [Aplicativos nativos](/pt/docs/app-native). É o caminho recomendado: comece no Stock, passe para Performance, experimente Turbo ou Crazy, e o Tuner valida tudo na **sua** BC-250.

## Fontes

- [cyan-skillfish-governor (Magnap)](https://github.com/Magnap/cyan-skillfish-governor) — governador SMU da GPU
- [bc250_smu_oc (bc250-collective)](https://github.com/bc250-collective/bc250_smu_oc) — overclock e undervolt da CPU pela SMU
- [bc250.info](https://bc250.info) — pontos seguros e notas térmicas da comunidade
- [vkpeak](https://github.com/nihui/vkpeak) · [clpeak](https://github.com/krrishnarraj/clpeak) — testes de FP32 e de banda de memória
