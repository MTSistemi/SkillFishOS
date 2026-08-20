---
title: Comandos úteis
description: Uma cola de terminal para diagnosticar e ajustar o SkillFishOS.
group: Referência
order: 4
---

O SkillFishOS foi feito para **não** exigir o terminal: para o uso normal bastam o [Tuner](/pt/docs/app-native) e os aplicativos gráficos. Esta página é para quem quer **mexer** ou diagnosticar. Os comandos com privilégio usam `sudo`.

> Antes de experiências arriscadas, lembre-se da rede de segurança: snapshots Btrfs e volta atrás pelo menu do GRUB (veja [Armazenamento e snapshots](/pt/docs/storage-snapshot)).

## Sistema e kernel

```bash
uname -r                      # kernel em execução (deve terminar em -skillfishos)
cat /proc/cmdline             # parâmetros de boot em vigor
journalctl -b -p err          # erros do boot atual
inxi -Fxxxz                   # resumo completo do hardware
```

## GPU, frequências e temperaturas

```bash
# temperatura da GPU pelo sysfs do amdgpu
cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input   # °C ×1000
# estado do governador SMU
systemctl status cyan-skillfish-governor
cat /etc/cyan-skillfish-governor/config.toml               # pontos seguros de frequência e tensão
# acompanhamento da GPU em tempo real
nvtop        # ou: radeontop
```

> Na BC-250 o controle da frequência **não** passa pelo sysfs padrão do amdgpu, e sim pelo **governador SMU**. Mude os valores pelo [Tuner](/pt/docs/app-native), não na mão.

## CPU — overclock e undervolt

```bash
systemctl status bc250-smu-oc.service   # ficar “inactive” depois de aplicar é normal (é de uma passada só)
cat /etc/bc250-smu-oc.conf              # frequência e tensão aplicadas
lscpu | grep MHz                        # frequências atuais dos núcleos
sensors                                 # temperaturas e tensões (nct6686, k10temp)
```

## Unidades de computação em tempo real (skillfish-cu)

```bash
skillfish-cu get          # estado em JSON: CU ativas e máscara por linha (SE/SH)
sudo skillfish-cu max     # colocar todas as CU em uso (40)
sudo skillfish-cu stock   # voltar para 24 (mínimo do driver)
sudo skillfish-cu set 0x1f   # máscara WGP para todas as linhas (0x07=24 … 0x1f=40)
cat /run/skillfish/cu_active # “40/40” (o HUD lê o mesmo)
vulkaninfo | grep -i "deviceName\|driverName"   # a GPU como o Vulkan a vê (RADV)
```

As CU são mais bem manejadas pela **grade** do [Tuner](/pt/docs/app-native) (clique e perfis, com o “Teste de CU”). As primeiras 24 são travadas pelo driver e ficam sempre ligadas.

Medições rápidas (as mesmas que o Tuner usa):

```bash
vkpeak                # desempenho FP32 (GFLOPS)
clpeak                # banda de memória (GB/s)
sysbench cpu run      # carga e medição da CPU
```

## Memória unificada (VRAM e GTT)

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'ttm\.'   # parâmetros de GTT/TTM
glxinfo | grep -i "memory"                                 # memória vista pelo driver
free -h                                                     # RAM/GDDR6 compartilhada
```

## Jogos

```bash
flatpak list                         # aplicativos Flatpak (Steam, emuladores do EmuDeck…)
flatpak update                        # atualizar os aplicativos Flatpak
gamescope -- %command%               # (colocar nas opções de inicialização da Steam)
# controles por Bluetooth
bluetoothctl                         # scan on / pair / connect / trust
```

## IA local

```bash
# um único serviço nativo, sem contêineres: o Docker não está instalado
systemctl status skillfish-unsloth   # estado do motor de IA
sudo systemctl start skillfish-unsloth   # iniciar
sudo systemctl stop skillfish-unsloth    # parar e liberar GPU e memória
curl -s localhost:8888/              # a interface do Unsloth Studio (só loopback)
```

## Snapshots e volta atrás (Btrfs)

```bash
sudo snapper list                    # listar snapshots
sudo snapper create -d "antes de X"  # snapshot manual
sudo btrfs subvolume list /          # subvolumes (@, @home, @log, @cache, @games)

# voltar a um snapshot de verdade (vale a partir do próximo boot)
sudo skillfish-rollback --list       # quais snapshots existem
sudo skillfish-rollback 12           # tornar o snapshot 12 o sistema em uso
sudo skillfish-rollback --undo       # mudou de ideia: devolver o anterior
sudo skillfish-rollback --clean      # descartar os sistemas postos de lado por voltas anteriores

# pelo menu do GRUB → “SkillFishOS snapshots” você chega ao mesmo snapshot
# EM SOMENTE LEITURA: serve para olhar e resgatar arquivos; depois rode o comando acima
```

## Atualizações e repositório

```bash
sudo apt update && sudo apt full-upgrade   # atualizar o sistema
apt-mark showhold                          # pacotes travados (inclusive o kernel)
sudo apt install skillfishos-kernel        # instalar ou atualizar o kernel pelo repositório
apt policy <pacote>                         # de qual repositório e versão vem um pacote
```

## Rede e acesso remoto

```bash
nmcli device status                  # estado das interfaces de rede
ip a                                 # endereços IP
systemctl status x11vnc              # servidor VNC para a área de trabalho remota
hostname -I                          # IP para usar com o cliente VNC
```

## Vídeo (HPD do DisplayPort)

```bash
systemctl status skillfish-dp-hotswap   # serviço que contorna o HPD defeituoso
xrandr                                   # saídas e resoluções (sessão X11)
```

## Fontes

- [Wiki do Btrfs](https://btrfs.readthedocs.io/) · [Snapper](http://snapper.io/)
- [Mesa / RADV](https://docs.mesa3d.org/drivers/radv.html) · [vulkaninfo](https://github.com/KhronosGroup/Vulkan-Tools)
- [Arch Wiki](https://wiki.archlinux.org/) — referência para muitos comandos do Linux
