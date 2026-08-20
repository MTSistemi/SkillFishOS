---
title: Introdução
description: O que é o SkillFishOS, por que ele existe e para quem é.
group: Introdução
order: 1
---

**SkillFishOS** é uma distribuição Linux projetada e ajustada para uma placa específica e pouco comum: a **AMD BC-250**. É um sistema *PC-console* pronto para usar — jogos, emulação, IA no próprio aparelho e trabalho diário na área de trabalho — construído sobre [Debian](https://www.debian.org/) e [KDE Plasma 6](https://kde.org/plasma-desktop/), com um visual steampunk coerente do boot até a área de trabalho.

## A ideia

A BC-250 nasceu como placa para minerar criptomoedas e acabou no mercado de segunda mão por preços muito baixos. Debaixo do dissipador, porém, há uma **APU semipersonalizada da AMD** da mesma família de silício dos consoles da geração atual: CPU Zen 2, gráficos RDNA 2 e 16 GB de GDDR6. Com o software certo ela vira um PC-console pequeno e surpreendentemente capaz.

O problema é que fazê-la funcionar bem no Linux exige patches de kernel, um governador de frequência próprio, overclock, perfis térmicos e uma longa lista de contornos para o hardware. O SkillFishOS existe para **fazer todo esse trabalho uma vez só** e entregar um sistema que *“liga e roda no máximo”*, sem que o usuário precise abrir o terminal.

> O SkillFishOS não distribui jogos nem ROMs: ele fornece as **ferramentas** (Steam, EmuDeck, emuladores, interfaces). O conteúdo você acrescenta, de forma legal.

## Para quem é

O projeto nasceu de uma necessidade concreta e pessoal: **fazer as crianças usarem e aprenderem Linux enquanto jogam**. Os jogos são a cenoura que atrai, e os **snapshots automáticos** do Btrfs são a rede de segurança que permite mexer sem medo de quebrar o sistema — se algo der errado, você volta com um clique pelo menu de boot.

Então o SkillFishOS combina bem com:

- quem tem uma **BC-250** e quer jogar sem virar especialista no kernel do Linux;
- **famílias** que querem um console barato que também seja um PC educativo;
- **quem gosta de mexer** e prefere partir de uma base já ajustada em vez de refazer tudo do zero.

## O que tem dentro, em resumo

- Um **kernel sob medida** ([linux-tkg](https://github.com/Frogging-Family/linux-tkg)) com os patches da BC-250: 40 unidades de computação destravadas, frequências liberadas, um governador SMU próprio.
- Uma **área de trabalho KDE Plasma 6** com visual steampunk (ícones, cursores, papel de parede, HUD do sistema).
- **Pronto para jogar**: Steam, [gamescope](https://github.com/ValveSoftware/gamescope), [EmuDeck](https://www.emudeck.com/), [ES-DE](https://es-de.org/), [Heroic](https://heroicgameslauncher.com/), Proton.
- **IA no próprio aparelho**: [Unsloth Studio](https://unsloth.ai/) acelerado por Vulkan na GPU integrada — **5,1×** mais rápido que na CPU, medido.
- **Snapshots Btrfs** com [Snapper](http://snapper.io/) e volta atrás pelo menu do GRUB.
- **Aplicativos próprios**: o *Tuner* (controle do hardware sem terminal) e o painel de *IA*.
- **Atualizações próprias e testadas** pelo nosso repositório APT, para que as do Debian não peguem você de surpresa.

As páginas seguintes tratam de cada componente em detalhe.

## Fontes

- Documentação da comunidade BC-250 — [bc250.info](https://bc250.info)
- Documentação da AMD BC-250 (elektricm) — [elektricm.github.io/amd-bc250-docs](https://elektricm.github.io/amd-bc250-docs)
- Debian — [debian.org](https://www.debian.org/)
- KDE Plasma — [kde.org/plasma-desktop](https://kde.org/plasma-desktop/)
