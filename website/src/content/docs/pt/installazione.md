---
title: Instalação
description: Como gravar a ISO, dar boot no instalador e terminar a configuração.
group: Instalação
order: 1
---

O SkillFishOS é instalado a partir de uma **ISO ao vivo** que traz o instalador gráfico [Calamares](https://calamares.io/). Todo o processo é feito com o mouse, sem terminal.

> A ISO **26.06.4 “Aetherium”** está disponível — baixe na página de [Download](/pt/download). Ela dá boot em **inglês** para ser universal e deixa você escolher idioma e teclado durante a instalação.

## Requisitos

- uma placa **AMD BC-250** (veja [hardware](/pt/docs/hardware-bc250));
- um **SSD ou NVMe** para instalar;
- um monitor ligado por **DisplayPort** (um adaptador DP→HDMI *passivo* pode funcionar, mas veja as notas sobre imagem e áudio em [Solução de problemas](/pt/docs/risoluzione-problemi));
- um **pendrive de pelo menos 8 GB** para o instalador;
- teclado e mouse para a instalação.

## 1. Grave a ISO no pendrive

Baixe a ISO na página de [Download](/pt/download) e grave num pendrive com uma destas ferramentas:

- **[balenaEtcher](https://etcher.balena.io/)** (Windows/macOS/Linux, com janela, recomendado);
- **[Ventoy](https://www.ventoy.net/)** (permite guardar várias ISOs no mesmo pendrive);
- pelo terminal do Linux com o `dd`:

```bash
sudo dd if=SkillFishOS_amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

> Troque `/dev/sdX` pelo dispositivo certo do seu pendrive. **Atenção**: o `dd` grava sem perguntar e apaga tudo o que houver no destino.

## 2. Dê boot na BC-250 pelo pendrive

Coloque o pendrive, ligue a placa e entre no menu de boot ou na UEFI para escolher o USB como dispositivo de inicialização. O ambiente **ao vivo** do SkillFishOS (KDE Plasma) vai subir: dá para passear pelo sistema antes de instalar.

## 3. Instale com o Calamares

Na área de trabalho ao vivo abra o instalador (ícone *Install SkillFishOS*). O Calamares conduz passo a passo:

1. **Idioma e fuso horário.**
2. **Teclado.**
3. **Particionamento.** O SkillFishOS usa **Btrfs** com subvolumes separados: `@` (sistema), `@home` (seus dados), `@cache` e `@log` (fora dos snapshots), `@games` (a biblioteca de jogos). Assim dá para *voltar atrás* no sistema sem mexer nos seus arquivos. Uma pequena partição **EFI** completa o quadro, e o swap é um **arquivo**, não uma partição. Para a maioria, a opção automática (“Apagar disco”) já serve.
4. **Usuário.** Crie sua conta (ela entra nos grupos certos para jogos, áudio, renderização e afins).
5. **Resumo e instalação.**

Quando terminar, reinicie e tire o pendrive.

## 4. Primeiro boot

No primeiro boot **está tudo configurado**: kernel otimizado, governador, overclock, visual, jogos e snapshots ativos. Não é preciso ajustar nada na mão.

Daqui você pode:

- parear seus [controles](/pt/docs/gaming) (DualShock 4 por Bluetooth ou um controle por USB);
- adicionar seus jogos à [Steam ou ao EmuDeck](/pt/docs/gaming);
- ligar a [IA local](/pt/docs/ai-locale) quando precisar;
- ajustar o hardware com o [Tuner](/pt/docs/app-native), se quiser.

## Divisão do disco

| Partição | Sistema de arquivos | Conteúdo |
|---|---|---|
| `nvme0n1p1` | FAT32 (EFI) | gerenciador de boot GRUB |
| `nvme0n1p2` | **Btrfs** | `@` (sistema) · `@home` (dados) · `@cache` · `@log` · `@games` · `@swap` |

Não há partição de swap: o swap é um **arquivo** dentro do subvolume `@swap`. No Btrfs ele muda de tamanho sem mexer na tabela de partições, e fica fora dos snapshots.

## Fontes

- [Calamares](https://calamares.io/) — o instalador universal
- [balenaEtcher](https://etcher.balena.io/) · [Ventoy](https://www.ventoy.net/)
- [Wiki do Btrfs](https://btrfs.readthedocs.io/) — subvolumes e snapshots
