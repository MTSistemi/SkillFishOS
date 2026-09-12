---
title: Jogos e emulação
description: Steam, gamescope, EmuDeck, ES-DE, Heroic, Android e controles.
group: Uso
order: 1
---

O SkillFishOS nasceu para jogar. Todo o conjunto de jogos já vem instalado e configurado; você acrescenta **seus** jogos e **suas** ROMs.

## A nossa Mesa (driver Vulkan)

A seção **Jogos** do [Control Center](/pt/docs/control-center) pode ligar a nossa build de **Mesa/RADV**, que abre as filas de computação que o driver de fábrica mantém fechadas nessa GPU: medido **+4% no Cyberpunk 2077**, **+12% com o FSR 4 ligado**. Vale por lançador (Steam, Heroic) por um override flatpak, ou para **o sistema todo** (área de trabalho incluída). Precisa do kernel do SkillFishOS: em outro kernel essas filas de computação travam a GPU e o interruptor do sistema se recusa a iniciar. Programas de 32 bits ficam com o driver do Debian.

## Steam e Proton

A **Steam** (via [Flatpak](https://flatpak.org/)) está integrada ao **[gamescope](https://github.com/ValveSoftware/gamescope)** (o microcompositor da Valve), ao **[gamemode](https://github.com/FeralInteractive/gamemode)** e ao **[MangoHud](https://github.com/flightlessmango/MangoHud)**. Há uma **sessão de console** própria (gamescope, no estilo Big Picture) que se escolhe na tela de acesso. Os jogos de Windows rodam pelo **Proton**: a seção Jogos do Control Center instala e define como padrão o **GE-Proton 11-6** e o **GE-Proton 10-34**, compartilhados entre Steam e Heroic.

## Jogos fora da Steam: Heroic

O **[Heroic Games Launcher](https://heroicgameslauncher.com/)** cuida dos títulos da **Epic Games** e da **GOG**, e dos jogos de Windows pelo **GE-Proton**. Com o **[ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt)** dá para instalar na mão outras versões do Proton e do Wine, além das que o Control Center já instala. Os jogos do Heroic podem ser adicionados à Steam (com as capas).

## Emulação: EmuDeck + ES-DE

O **[EmuDeck](https://www.emudeck.com/)** instala e configura, em alguns cliques, um conjunto completo de emuladores (Flatpak): **RetroArch, Dolphin, PCSX2, PPSSPP, melonDS, PrimeHack, Ryujinx, ScummVM** e outros. A interface é o **[ES-DE](https://es-de.org/)** (EmulationStation Desktop Edition).

No SkillFishOS a pasta `~/Emulation` pode apontar para um **NAS** na rede (BIOS, ROMs e saves compartilhados entre máquinas).

> **Atenção:** o ES-DE reescreve o arquivo de configuração ao sair: edite com o programa **fechado**.
>
> **Atenção:** no **Ryujinx**, o firmware e as chaves são importados pelo usuário: o firmware espera cada NCA como um diretório. **Jogos, ROMs, BIOS e chaves não vêm** no sistema — é uma escolha legal deliberada: o SkillFishOS fornece as ferramentas, o conteúdo é seu.

## Android e mais

- **[Waydroid](https://waydro.id/)** para aplicativos e jogos Android (binder no kernel, suporte a iptables e bibliotecas ARM);
- **[Sober](https://sober.vinegarhq.org/)** como reprodutor do Roblox — não vem instalado, pegue na loja com `flatpak install flathub org.vinegarhq.Sober`. É um aplicativo de 18 MB que arrasta 1,1 GB de bibliotecas do GNOME: é justamente por deixá-lo de fora que a ISO continua pequena.

> Observação: a IA local e o Android não devem ser usados junto com jogos pesados, porque dividem a mesma GPU e a mesma memória.

## Controles

A configuração recomendada e testada:

- **2 DualShock 4 por Bluetooth** — com giroscópio (útil para o controle por movimento em jogos como o Mario Kart), ligados ao adaptador Realtek integrado;
- **controle por USB** — com um cabo **de dados** ele aparece como um Xbox 360 (driver `xpad`, XInput), sem giroscópio.

Os drivers `xpad`, `hid_playstation` e `hid_nintendo` fazem parte do kernel. Para parear um DS4 de novo: segure *Share + PS* até piscar e pareie pela janela do Bluetooth.

## Escalonamento

A nossa Mesa traz o **FSR 4** pelo **[OptiScaler](https://github.com/optiscaler/OptiScaler)** na rota DLSS do jogo: o GE-Proton 11 baixa o OptiScaler sozinho quando encontra `PROTON_USE_OPTISCALER=1`, o jogo precisa estar em DLSS, e a biblioteca FSR 4 da AMD (`amdxcffx64.dll`, tirada do driver Windows da AMD) precisa ir junto do jogo. As alternativas seguem sendo o escalonamento do **gamescope** (FSR1/NIS) e o XeSS, onde um jogo já traz embutido. Em títulos que dependem da *CPU* (por exemplo *Black Myth: Wukong*), não adianta baixar a resolução nem a frequência da GPU — veja [GPU e overclock](/pt/docs/gpu-overclock).

## Fontes

- [Steam](https://store.steampowered.com/) · [gamescope](https://github.com/ValveSoftware/gamescope) · [gamemode](https://github.com/FeralInteractive/gamemode) · [MangoHud](https://github.com/flightlessmango/MangoHud)
- [Heroic](https://heroicgameslauncher.com/) · [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) · [Proton GE](https://github.com/GloriousEggroll/proton-ge-custom)
- [EmuDeck](https://www.emudeck.com/) · [ES-DE](https://es-de.org/) · [RetroArch](https://www.retroarch.com/)
- [Waydroid](https://waydro.id/) · [Sober](https://sober.vinegarhq.org/)
