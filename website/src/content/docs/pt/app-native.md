---
title: Aplicativos próprios — Tuner e AI
description: As ferramentas gráficas do SkillFishOS para controlar o hardware e a IA sem terminal.
group: Uso
order: 3
---

O SkillFishOS traz dois aplicativos próprios (escritos em **PyQt6**, com o visual do Kvantum) que colocam o controle do hardware e do conjunto de IA nas mãos do usuário **sem passar pelo terminal**.

## SkillFishOS Tuner

O **Tuner** é o painel de controle do hardware. Ele permite ajustar:

- **overclock e undervolt da CPU**;
- os **pontos seguros da GPU** (pelo governador SMU, veja [GPU e overclock](/pt/docs/gpu-overclock));
- a **ventoinha** (controle PWM);
- a **VRAM UMA** (exige reiniciar);
- as **unidades de computação, em tempo real** — veja abaixo.

### Unidades de computação em tempo real (grade)

O Tuner mostra as CU da GPU como uma **grade de quadrados** (4 linhas SE/SH × 5 WGP): **verde = ativa, vermelho = desligada**. Dá para alternar **em tempo real, sem reiniciar**: clique nos pares (1 WGP = 2 CU) ou use os **perfis de 24 / 32 / 40 CU**, e então *Aplicar*. As primeiras 24 CU são o mínimo do driver e ficam sempre ligadas (veja [GPU e overclock](/pt/docs/gpu-overclock)).

![SkillFishOS Tuner — a grade de unidades de computação em tempo real, os perfis e o teste de CU](/img/tuner.jpg)

### Teste de CU (loteria do silício)

O botão **“Teste de CU”** confere a saúde das CU extras: liga cada par sozinho, exige dele com o **vkpeak** e fica de olho em **erros e travamentos da GPU**, com uma carga final sobre as 40. Ele existe para pegar **CU defeituosas** em APUs de descarte, para você saber se o seu chip aguenta as quarenta.

![Resultado do teste de CU — todos os pares em ordem, 40 CU estáveis a 11380 GFLOPS, sem defeitos](/img/cu-test.jpg)

### O fluxo de “Teste” e o monitor ao vivo

O fluxo do botão **“Teste”** (CPU, GPU, CU, ventoinha): aplicar uma mudança → rodar uma medição → **verificar** a estabilidade e, se algo der errado, fazer um **retorno** automático. Assim que um teste começa, abre a janela do **[SkillFishOS Telemetry](#skillfishos-telemetry)** com gráficos ao vivo de **temperatura, frequência, tensão e ventoinha** (dá para fechar).

![SkillFishOS Telemetry durante um teste do Tuner — gráficos ao vivo de temperatura, frequência, tensão da GPU e ventoinha](/img/monitor.jpg)

Como é feito: uma janela de usuário mais um pequeno **serviço com poderes de root** que executa as operações privilegiadas. Num PC pessoal ele está configurado para não pedir senha a cada operação. O HUD da área de trabalho também mostra as **CU ativas** ao vivo.

### Modos do governador: Balanced e Performance

A GPU da BC-250 é conduzida por um **governador SMU** que sobe e desce a frequência conforme a carga. O Tuner oferece dois modos num interruptor:

- **Balanced** *(padrão)* — a frequência cai em repouso (até 350 MHz) e sobe com a carga: menos consumo e menos temperatura no uso diário.
- **Performance** — a GPU **fica cravada na frequência máxima** assim que aparece carga, e somem as microoscilações. Na nossa medição de *Black Myth: Wukong* isso vale **+11% de FPS** (de cerca de 100 para cerca de 111 em média) e um **1% low** mais alto (92 → 102), com todo o resto igual.

Os dois continuam sob o **teto térmico de 85 °C**: o modo Performance aperta mais, não desliga as proteções.

### “Encontre meu máximo” (assistentes de CPU e GPU)

Cada BC-250 é diferente ([loteria do silício](/pt/docs/gpu-overclock)). O Tuner tem dois assistentes **“Encontre meu máximo”** que caracterizam a **sua** placa:

- **GPU** — sobe em degraus (2000 → 2200 MHz, de 50 em 50), aplicando e **testando** cada degrau, parando no último estável.
- **CPU** — percorre os degraus de frequência e undervolt (de 3600 MHz até 4000 MHz na escala −36) com o mesmo esquema de **teste e retorno**: se um degrau não aguentar, ele volta ao último valor bom.

Tudo é **à prova de travamento**: o valor de trabalho no disco é sempre o último estável, então um travamento no meio do teste nunca deixa a placa com um perfil instável no próximo boot.

### Meu silício

O painel **“Meu silício”** resume o perfil da sua placa — o melhor valor de CPU e GPU encontrado, as CU sadias, o contador de travamentos detectados — e permite **compartilhar o resultado de forma anônima** na base da loteria do silício (abre uma issue do GitHub já preenchida). Quanto mais dados juntarmos, melhores ficam os perfis recomendados para todo mundo.

## SkillFishOS Telemetry

O **Telemetry** mostra em tempo real temperatura, frequência, carga de CPU e GPU, tensões, consumo e ventoinha. Ele abre sozinho durante os testes do Tuner, mas também é um aplicativo por conta própria. O botão **REC** grava uma sessão de medição num arquivo **`.sfmon`** (em `~/SkillFishOS-benchmarks/`): ao reabrir, o Telemetry vira um **analisador** com uma barra de tempo para rever a passada segundo a segundo.

![SkillFishOS Telemetry — gráficos com eixo rotulado e o painel de frequência por núcleo e thread](/img/telemetry-percore.jpg)

### Frequência por núcleo e thread

Com [oito núcleos destravados](/pt/docs/hardware-bc250), um único número de “frequência da CPU” diz muito pouco: em repouso as dezesseis threads podem estar **ao mesmo tempo** em 800, 1775 e 3990 MHz, então o valor que aparece depende só de qual núcleo foi consultado.

O painel de baixo desenha **uma barra por thread**, agrupadas por núcleo físico e rotuladas `núcleo·thread`. A cor vai do latão à brasa conforme a thread sobe, os MHz ficam impressos em cada barra, e o cabeçalho resume **mínimo, média, máximo e quantas threads estão em atividade**. As threads que você desligou pelo Tuner não somem: ficam como um espaço tracejado marcado **“off”**, assim a configuração real se vê num relance.

### Eixos legíveis

Cada gráfico agora tem uma **escala com linhas e valores no eixo vertical**, ajustada a números humanos (`0 / 1000 / 2000 / 3000`, e não `-160 / 1394 / 2948`). O zero vira o piso quando os dados estão perto dele, então um gráfico de MHz ou de rotações da ventoinha nunca mostra uma base negativa; e uma linha reta não é mais ampliada até o ruído virar montanha.

## SkillFishOS AI

O **painel de IA** liga e desliga a IA local com um clique, liberando GPU e memória para os jogos quando ela não é necessária. É a cara “fácil” do que está descrito em [IA no aparelho](/pt/docs/ai-locale).

![Painel SkillFishOS AI — motor local (Qwen3 14B) na GPU via Vulkan, liga e desliga com um clique](/img/ai-panel.jpg)

## Por que existem

O objetivo do SkillFishOS é que **qualquer pessoa** — inclusive as mais novas — consiga usar e ajustar o sistema sem precisar decorar comandos de terminal. Esses aplicativos traduzem operações complicadas (governador SMU, parâmetros de kernel, snapshots e retorno) em alguns cliques, mantendo sempre ligadas as **proteções** (teto térmico, teste com retorno).

## Fontes

- [PyQt6 / Qt for Python](https://doc.qt.io/qtforpython/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [sysbench](https://github.com/akopytov/sysbench) · [vkpeak](https://github.com/nihui/vkpeak)
- Repositório do projeto — [github.com/MTSistemi/SkillFishOS](https://github.com/MTSistemi/SkillFishOS) (`apps/tuner`, `apps/ai-panel`)
