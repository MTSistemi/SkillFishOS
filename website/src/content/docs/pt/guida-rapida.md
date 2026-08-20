---
title: Início rápido
description: Seus primeiros 10 minutos com o SkillFishOS — do primeiro boot ao primeiro jogo.
group: Introdução
order: 3
---

Você instalou o SkillFishOS (veja [Instalação](/pt/docs/installazione)) e está no primeiro boot. Esta página é uma **lista rápida** para começar já: todo o resto já está configurado e funcionando.

## Em uma linha

> Liga → você já está na área de trabalho ajustada → conecta um controle → adiciona seus jogos → joga. Sem terminal e sem configuração.

## 1. Primeiro boot (está tudo pronto)

No primeiro boot você encontra uma área de trabalho **KDE Plasma 6** com visual steampunk, um kernel otimizado, o governador SMU, o perfil **Stock**, o conjunto para jogos e os snapshots **já ativos**. No canto superior direito, o **HUD** mostra em tempo real CPU, GPU, temperaturas, memória, ventoinha e dispositivos Bluetooth conectados.

Não é preciso instalar drivers, definir frequências nem ativar nada: o sistema dá boot “na compatibilidade máxima”.

## 2. Conecte-se à rede

A rede por cabo é gerenciada pelo NetworkManager e já está pronta. Para Wi-Fi e Bluetooth use o ícone de rede no painel. A conexão é necessária para a Steam, as atualizações e a IA local.

## 3. Conecte um controle

| Controle | Como |
|---|---|
| **DualShock 4** | Por Bluetooth: segure **Share + PS** até piscar e pareie pelo ícone do Bluetooth. Ele tem **giroscópio**. |
| **Controle genérico** | Por **USB** com um cabo **de dados** (não só de carga): aparece como um controle de Xbox 360. |

Detalhes e solução de problemas → [Jogos](/pt/docs/gaming) e [Solução de problemas](/pt/docs/risoluzione-problemi).

## 4. Adicione seus jogos

- A **Steam** já vem instalada e integrada ao gamescope e ao MangoHud. Entre na sua conta e instale seus jogos: os títulos de Windows rodam pelo **Proton**.
- **Epic / GOG** → [Heroic](/pt/docs/gaming).
- **Emulação** → abra o **EmuDeck**, escolha os emuladores e jogue pela interface **ES-DE**. As ROMs, as BIOS e as chaves são você quem coloca (veja a nota legal em [Jogos](/pt/docs/gaming)).

## 5. (Opcional) Espremer o hardware

O SkillFishOS dá boot no perfil **Stock** para ficar seguro em qualquer placa. Quando quiser mais desempenho, abra o **[Tuner](/pt/docs/app-native)** e suba um perfil:

**Stock → Performance → Turbo → Crazy**

O Tuner **testa cada perfil na sua própria BC-250** e **volta atrás sozinho** se a placa não aguentar. É o jeito seguro de achar o limite do seu chip (veja [GPU e overclock](/pt/docs/gpu-overclock)).

## 6. (Opcional) Ligar a IA local

Quando precisar de um assistente que funcione sem internet, abra o **painel de IA** e inicie o [Unsloth Studio](/pt/docs/ai-locale). Lembre-se: IA e jogos pesados **não** combinam ao mesmo tempo (dividem GPU e memória). Com o motor desligado, a GPU volta inteira para os jogos.

## Coisas para saber desde já

- **Não reative a suspensão**: na BC-250 ela está quebrada e a placa não acorda (veja [Área de trabalho](/pt/docs/desktop)).
- Use um monitor com **DisplayPort** ou um adaptador **passivo**; adaptadores DP→HDMI **ativos** quebram o áudio.
- Você tem uma **rede de segurança**: um snapshot Btrfs é tirado antes e depois de cada atualização; se algo der errado, volte pelo menu do GRUB → *SkillFishOS snapshots* (veja [Armazenamento e snapshots](/pt/docs/storage-snapshot)).

## E agora?

- Quer entender **o que** está usando? → [Hardware BC-250](/pt/docs/hardware-bc250)
- Quer os **números** reais de desempenho? → [Desempenho e testes](/pt/docs/prestazioni)
- Tem uma **dúvida** rápida? → [Perguntas frequentes](/pt/docs/faq)
- Um **termo** que não conhece? → [Glossário](/pt/docs/glossario)
