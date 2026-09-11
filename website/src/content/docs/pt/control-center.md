---
title: "Control Center"
description: "Todas as ferramentas do SkillFishOS numa janela: Tuner, Ventoinha, Monitor, Jogos, Perfis, Kernel, Snapshots, IA, Emuladores, Consola, ISO."
group: Uso
order: 4
---

Todas as ferramentas do SkillFishOS estão numa janela. Abre-se pelo menu (SkillFishOS → Control Center) ou com `skillfish-control-center`. Também se conduz com o comando: cruz ou alavanca para mover, A confirma, B volta, LB e RB mudam de secção.

## As secções

- **Estado**: um número por cartão: frequência e teto da GPU, CPU, unidades de cálculo, ventoinha, kernel, governor, driver Vulkan, se o último arranque seguiu um encerramento limpo. Aqui não se define nada.
- **Tuner**: a curva tensão/frequência do governor da GPU, a CPU, os núcleos, as unidades de cálculo, a VRAM.
- **Ventoinha**: a curva da ventoinha com o avanço, os sensores de origem, os limites de segurança, o teste PWM.
- **Monitor**: todas as leituras, um gráfico por unidade, mais as barras de frequência por thread. REC grava, CSV exporta.
- **Jogos**: a nossa Mesa por lançador ou para todo o sistema, o escalonador scx_bpfland, FSR 4, instalação e predefinição do GE-Proton.
- **Perfis**: teto, CPU, ventoinha e escalonador num clique; guarde os seus.
- **Kernel**: os kernels instalados, o predefinido, arrancar uma vez, desinstalar.
- **Snapshots**: os snapshots do sistema e a manutenção btrfs agendada.
- **IA**: Unsloth Studio em Vulkan: ligado/desligado, hardware, o limite GTT.
- **Emuladores**: EmuDeck, ou os emuladores um a um a partir do Flathub.
- **Consola**: Steam Big Picture dentro do gamescope, agora ou a partir do ecrã de início de sessão.
- **ISO**: imagens de disco montadas através do udisks.

## Tuner

A curva é o gráfico: MHz na horizontal, milivolts na vertical. Arraste um ponto, duplo clique para acrescentar um, clique direito para o retirar, ou escreva os números na tabela ao lado do gráfico (+ e − acrescentam e retiram pontos). A linha vertical a tracejado é o teto, o ponto azul é a GPU neste momento. Três presets: **Cautious 1850** (o ponto ideal com o dissipador de série, quase os mesmos fotogramas e dez graus a menos), **Balanced 2000**, **Performance 2100** (a curva de quinze pontos medida na placa de desenvolvimento, a que enviamos).

**Aplicar é uma prova.** Uma curva que pede pouca tensão bloqueia a placa, e na BC-250 um bloqueio resolve-se a tirar a ficha. Por isso Aplicar arranca a candidata com a curva anterior ainda no disco e conta 25 segundos: carregue em Manter e a candidata fica escrita de vez; não faça nada, ou a placa morre e volta, e arranca a curva anterior.

Os painéis abrem-se quando são precisos:

- **CPU**: frequência, degrau de undervolt (6,25 mV cada) e limite térmico, cada um com um cursor e uma caixa numérica de passo 1. *Sugerir UV* desce o undervolt dois degraus de cada vez com doze segundos de carga por degrau; *Encontrar o máximo* sobe de 3600 a 4000 MHz; *Teste 60 s* carrega os valores atuais. Cada prova mostra uma contagem decrescente e um botão Stop; os valores em prova nunca são escritos no disco, por isso um bloqueio arranca com os anteriores. Acima de 3500 MHz com oito núcleos o ganho é nulo: manda o calor.
- **Núcleos**: que núcleos estão ativos, SMT, o desbloqueio dos 8 núcleos (6c/12t passa a 8c/16t, +20 % medido) e *Antes do arranque (EFI)*: o desbloqueio feito antes do GRUB num só arranque, em vez do reinício extra do serviço dentro do sistema.
- **CU**: as 40 unidades de cálculo em 20 células (pares): verde ligada, vermelha desligada, cinzenta mantida ligada pelo driver. Escreva quantas CU quer (de 24 a 40, aos pares) ou clique nas células; *Teste CU* liga os pares extra um a um sob o vkpeak e reporta erros, para a lotaria do silício.
- **VRAM**: a divisão UMA no CMOS, aplicada no próximo arranque. Com os 512 MB dinâmicos alguns jogos escolhem texturas baixas: se estiverem desfocadas, experimente 4 ou 6 GB fixos.
- **Avançado**: os botões do próprio governor: margem a subir, degrau, confirmações a descer, limiares térmicos e de potência, droop.
- **Teste**: vkpeak e o registo do assistente.

## Monitor

Um gráfico por grandeza, cada um com a sua escala real: temperaturas (CPU, GPU, VRM, sistema, NVMe), frequências (CPU média, mínima, máxima, GPU e o seu teto), carga, potência, tensões, ventoinha e memória (RAM, VRAM, GTT), mais uma barra por thread. Clique numa entrada da legenda para esconder uma linha; passe o rato para ler todos os gráficos no mesmo instante. REC escreve um ficheiro `.sfmon` (CSV) que Abrir recarrega com um cursor; CSV exporta-o para uma folha de cálculo.

## Jogos

- **Driver Vulkan**: a nossa Mesa abre as filas de cálculo que o driver de série mantém fechadas nesta GPU: +4 % no Cyberpunk 2077, +12 % com FSR 4. Por lançador (Steam, Heroic) com um override flatpak, ou para todo o sistema. Precisa do kernel do SkillFishOS: noutro kernel essas filas bloqueiam a GPU, e o interruptor de sistema recusa-se a arrancar aí. O cartão mostra o kernel em execução.
- **Escalonador**: scx_bpfland, carregado só enquanto corre um jogo (o GameMode lança-o e retira-o): +1,5-2 % no Cyberpunk e fotogramas mais regulares. Se o kernel o expulsar duas vezes, o serviço pára até repor o contador a zero: é a linha «Expulso pelo kernel».
- **FSR 4**: através do OptiScaler no caminho DLSS do jogo. O GE-Proton 11 descarrega o OptiScaler sozinho quando encontra `PROTON_USE_OPTISCALER=1`, o jogo tem de ficar em DLSS, e a biblioteca FSR 4 da AMD (`amdxcffx64.dll`, do driver Windows da AMD) vai ao lado do jogo. O XeSS, onde um jogo o traz de série, custa o mesmo que o FSR 3 a 1080p.
- **Proton**: as versões GE-Proton 11; Instalar descarrega uma (cerca de 500 MB) para as pastas do Steam e do Heroic, Predefinida escolhe-a. O Steam tem de estar fechado para que a sua predefinição seja escrita.

## Ventoinha, perfis e o resto

A página **Ventoinha** desenha a curva dentro do gráfico dos sensores: a esta temperatura a ventoinha roda assim, com um avanço para que a velocidade suba antes da temperatura. Os **Perfis** movem o teto dentro da curva que já existe e definem em conjunto CPU, preset da ventoinha e escalonador. Os **Snapshots** são fotografias do sistema, os seus ficheiros não são tocados. **IA** retém a memória da GPU enquanto está ligada: desligue-a antes de jogar. **Consola** arranca o Steam Big Picture dentro do gamescope por cima do ambiente de trabalho, ou como sessão a partir do ecrã de início. O **Remote Manager** replica as páginas Tuner, Jogos e Perfis num navegador.
