---
title: Perguntas frequentes
description: As dúvidas mais comuns sobre o SkillFishOS e a BC-250, com respostas curtas.
group: Referência
order: 2
---

Respostas rápidas para as perguntas mais comuns. Para se aprofundar, cada resposta leva à página certa.

## Geral

**O que é o SkillFishOS?**
Uma distribuição Linux (Debian + KDE Plasma 6) projetada e ajustada para a placa **AMD BC-250**: jogos, emulação, IA local e uso de escritório, tudo já configurado. Veja [Introdução](/pt/docs/introduzione).

**Em que hardware ele roda?**
A placa para a qual ele foi feito é a **AMD BC-250** (APU Zen 2 + RDNA 2 “gfx1013”, 16 GB GDDR6), e é nela que ele faz tudo o que sabe: 40 unidades de computação destravadas, governador SMU, oito núcleos. Existe também a edição **Generic x86-64**, que roda em qualquer PC ou máquina virtual — um kernel comum, com as partes específicas da placa se escondendo em vez de falhar. Veja [Hardware BC-250](/pt/docs/hardware-bc250).

**Quanto custa? É de código aberto?**
É **gratuito**. Ele reúne software livre de muitas comunidades; o código do projeto está no [GitHub](https://github.com/MTSistemi/SkillFishOS). Veja [Fontes](/pt/docs/fonti).

**Ele inclui jogos, ROMs ou BIOS?**
Não. O SkillFishOS fornece as **ferramentas** (Steam, EmuDeck, emuladores, interfaces); o conteúdo você acrescenta, de forma legal. Veja [Jogos](/pt/docs/gaming).

## Instalação

**Como instalo?**
Grave a ISO num pendrive e dê boot no instalador gráfico **Calamares**. Tudo com o mouse. Veja [Instalação](/pt/docs/installazione).

**Dá para experimentar sem instalar?**
Dá: a ISO é **ao vivo**, você pode passear pela área de trabalho antes de instalar.

**Ele apaga meu disco?**
A instalação automática (“Apagar disco”) apaga. Para preservar dados existentes, use o particionamento manual. O SkillFishOS usa **Btrfs** com subvolumes separados `@rootfs` e `@home`.

**Preciso de conexão com a internet?**
Para instalar, não; depois será necessária para a Steam, as atualizações e a IA.

## Desempenho e overclock

**Por que ele começa “devagar”, no Stock?**
Por segurança: cada BC-250 é diferente (*loteria do silício*). Os perfis são elevados pelo **[Tuner](/pt/docs/app-native)**, que valida tudo na sua própria placa. Veja [GPU e overclock](/pt/docs/gpu-overclock).

**Overclock é perigoso?**
O Tuner aplica um perfil, **testa** e **volta atrás** se a placa não aguentar; o teto de 85 °C e a proteção térmica ficam sempre ligados. Foi feito para ser seguro.

**Quantos FPS no jogo X?**
Depende: alguns jogos dependem da **CPU** (por exemplo *Black Myth: Wukong*) e não melhoram com uma GPU mais rápida. Veja [Desempenho e testes](/pt/docs/prestazioni).

**Posso usar FSR 4?**
Não, ele exige hardware RDNA 4. Use o gamescope (FSR1/NIS) ou o OptiScaler. Veja [Jogos](/pt/docs/gaming).

## Uso no dia a dia

**Por que às vezes a tela fica preta?**
O **HPD do DisplayPort é defeituoso** na BC-250: o SkillFishOS contorna isso com um serviço próprio. Use um monitor DP ou um adaptador **passivo**. Veja [Solução de problemas](/pt/docs/risoluzione-problemi).

**Por que não sai áudio pela TV?**
Normalmente é um adaptador DP→HDMI **ativo**: use um passivo, um monitor DP, uma placa de som USB ou áudio por Bluetooth.

**Posso suspender o PC?**
Não. **A suspensão está quebrada** no nível do hardware e a placa não acorda: o SkillFishOS a desativa de propósito. **Não reative.** Veja [Área de trabalho](/pt/docs/desktop).

**Posso usá-lo de outro computador?**
Pode: a sessão padrão é X11 e o **x11vnc** está rodando, então dá para controlar a área de trabalho por VNC na rede local. Veja [Área de trabalho](/pt/docs/desktop).

## IA local

**Qual modelo de IA posso usar?**
O motor é o **Unsloth Studio** sobre **Vulkan** (não ROCm, que não tem suporte no gfx1013), e os modelos são arquivos GGUF baixados do Hugging Face. Medido na placa: **210,7 tok/s** gerando contra 41,5 na CPU. Veja [IA no aparelho](/pt/docs/ai-locale).

**Posso jogar com a IA ligada?**
Não: IA e jogos pesados dividem GPU e memória. Desligue a IA antes de jogar.

## Atualizações

**Como atualizo o sistema?**
`sudo apt update && sudo apt full-upgrade` ou o aplicativo **Discover**. Um snapshot é tirado automaticamente antes e depois de cada atualização. Veja [Atualizações](/pt/docs/aggiornamenti).

**Uma atualização quebrou alguma coisa, e agora?**
Reinicie e escolha um snapshot no **GRUB → “SkillFishOS snapshots”**. Veja [Armazenamento e snapshots](/pt/docs/storage-snapshot).

**O Debian atualiza o kernel?**
Não: o kernel do SkillFishOS está **travado** (`apt-mark hold`) e só é atualizado pelo nosso repositório testado. Veja [Kernel](/pt/docs/kernel).

## Projeto

**Posso contribuir ou relatar um problema?**
Pode, pelas **Issues** no [GitHub](https://github.com/MTSistemi/SkillFishOS/issues).

**Onde baixo a ISO?**
Na página de [Download](/pt/download) (hospedada no SourceForge).
