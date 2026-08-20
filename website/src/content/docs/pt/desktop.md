---
title: Área de trabalho, visual e acesso remoto
description: KDE Plasma 6, o visual steampunk, o HUD do sistema, o bloqueio da suspensão e o acesso à distância.
group: Sistema
order: 4
---

O SkillFishOS usa o **[KDE Plasma 6](https://kde.org/plasma-desktop/)** como ambiente de trabalho, vestido com um visual steampunk coerente e um conjunto de ajustes próprios da BC-250.

## Sessões

Na tela de acesso (cuidada pelo **SDDM**, com entrada automática) há várias sessões disponíveis:

- **KDE Plasma X11** — *padrão*. Escolher X11 deixa o acesso remoto trivial (veja abaixo);
- **KDE Plasma Wayland** — dá para escolher;
- **Gaming** — uma sessão do [gamescope](https://github.com/ValveSoftware/gamescope) no estilo Big Picture (veja [Jogos](/pt/docs/gaming)).

## **Atenção:** bloqueio da suspensão (crítico)

A BC-250 tem a **suspensão ACPI quebrada**: se ela dormir, **não acorda** e é preciso um reset (veja [hardware](/pt/docs/hardware-bc250)). Por isso o SkillFishOS **desativa em definitivo** todos os estados de sono:

```bash
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

A isso soma uma regra do `logind` (`IdleAction=ignore`), o bloqueio automático de tela desligado e um gerenciamento de energia com inatividade “infinita”. É uma medida **obrigatória**: uma máquina suspensa também fica inalcançável à distância.

## Visual “SkillFish Steampunk”

O visual é uma paleta combinada de latão e cobre (destaque **`#d8a849`**, superfícies escuras) e se mantém **do boot até a área de trabalho**: tema do GRUB, tela do Plymouth, saudação do SDDM, papel de parede com o peixe. O pacote do visual traz:

- **ícones** (`SkillFishSteampunk`, com `breeze-dark` como reserva) e **cursores** próprios;
- um estilo **Kvantum** para os aplicativos Qt e um **esquema de cores** do KDE;
- um **tema do Plasma**, um tema do **Konsole**, botões de janela e um **aspecto e comportamento** global (`org.skillfish.steampunk`);
- avatares de usuário no mesmo estilo e uma galeria para escolher.

> Os temas **Breeze** de fábrica continuam instalados como reserva estrutural (em especial, são eles que dão a janela de sair e desligar). Não devem ser removidos.

## HUD do sistema (Conky)

No canto superior direito há um **HUD** em latão feito com o **[Conky](https://github.com/brndnmtthws/conky)**, mostrando em tempo real: barras de CPU por núcleo com MHz, °C e watts, frequência, temperatura e VRAM da GPU, memória, disco, ventoinha e os **dispositivos Bluetooth conectados** com o nível de bateria (controles, fones…). Os valores vêm de auxiliares próprios que leem os sensores do hardware diretamente.

## Acesso à distância (x11vnc)

Como a sessão padrão é X11, o acesso remoto é simples: o SkillFishOS inicia o **[x11vnc](https://github.com/LibVNC/x11vnc)** na tela ativa e compartilha a imagem real. Na rede local qualquer cliente VNC consegue conectar. Assim dá para dar suporte e configurar de outro PC sem teclado e mouse ligados na placa.

## Rede, áudio e aplicativos

- **Rede**: a conexão por cabo é cuidada pelo **NetworkManager**, então aparece e se configura pelas janelas do Plasma.
- **Áudio**: um conjunto completo de **[PipeWire](https://pipewire.org/)** (com suporte a Bluetooth). Atenção: adaptadores DP→HDMI *ativos* podem quebrar o áudio — veja [Solução de problemas](/pt/docs/risoluzione-problemi).
- **Aplicativos básicos**: gerenciador de arquivos Dolphin, terminal Konsole, leitor de PDF Okular, visualizador de imagens Gwenview, compactador Ark, capturas Spectacle, loja Discover (com flatpak), navegador **Google Chrome**, **OnlyOffice**.
- **Aplicativos próprios do SkillFishOS** (reunidos no menu **“SkillFishOS”**, cada um instalável e atualizável como `.deb` pelo repositório assinado): **Tuner** (controle de overclock, undervolt, ventoinha e CU da BC-250), **AI** (modelo de linguagem local na GPU integrada, quando você quiser), **Monitor** (gráficos ao vivo de temperatura, frequência, tensão e ventoinha), **Kernel Manager** (escolher o kernel de boot e desinstalar os antigos), **ISO Mount**, **Hub** — a central de programas no estilo Discover (APT + Flatpak + Snap) com páginas de aplicativo, carrossel de capturas e gestão das fontes — além do **Base** (vigia por hardware e detector de travamentos com aviso na área de trabalho) e do **Console**, uma sessão **“SkillFishOS Console (Big Picture)”** no estilo SteamOS, escolhida na tela de acesso.
- **Vídeo**: um serviço (`skillfish-dp-hotswap`) cuida da detecção do monitor, necessário porque o HPD do DisplayPort é defeituoso.

## Fontes

- [KDE Plasma](https://kde.org/plasma-desktop/) · [Kvantum](https://github.com/tsujan/Kvantum)
- [Conky](https://github.com/brndnmtthws/conky) · [x11vnc](https://github.com/LibVNC/x11vnc)
- [PipeWire](https://pipewire.org/) · [SDDM](https://github.com/sddm/sddm)
- [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/) · [NetworkManager](https://networkmanager.dev/)
