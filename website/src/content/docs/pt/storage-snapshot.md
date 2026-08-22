---
title: Armazenamento e snapshots Btrfs
description: "A rede de segurança do SkillFishOS: snapshots automáticos e volta atrás pelo boot."
group: Sistema
order: 3
---

Uma das ideias centrais do SkillFishOS é poder **mexer sem medo**. Quem torna isso possível é o sistema de arquivos **[Btrfs](https://btrfs.readthedocs.io/)** com snapshots automáticos: cada mudança importante fica registrada e, se algo quebrar, você volta com um clique.

## Subvolumes separados

O disco tem uma só partição Btrfs, dividida em subvolumes distintos:

- **`@`** — o sistema operacional;
- **`@home`** — os dados do usuário;
- **`@cache`** e **`@log`** — caches e registros, deixados fora dos snapshots para que uma volta atrás não traga junto os registros de ontem;
- **`@games`** — a biblioteca de jogos, que senão deixaria cada snapshot enorme;
- **`@swap`** — o arquivo de swap.

Mantê-los separados é essencial: voltar atrás no sistema **não toca nos arquivos pessoais**. Dá para regressar a um sistema de “ontem” mantendo os documentos, os saves e as configurações de hoje.

## Snapshots automáticos com o Snapper

O SkillFishOS usa o **[Snapper](http://snapper.io/)** com uma configuração `root` e **ganchos de antes e depois no APT**: toda vez que você instala ou atualiza pacotes, um snapshot é criado sozinho *antes* e *depois*. Assim, se uma atualização der problema, o snapshot de “antes” já está lá.

Da configuração vale destacar:

- um limite de snapshots guardados para o disco não encher;
- snapshots preservados nos *marcos* importantes do sistema;
- gestão a partir de uma janela com **SkillFishOS Snapshots**, a aplicação que escrevemos nós.

## Quantos ficam guardados

**Cinco**, de fábrica: três comuns (o par antes/depois em torno de cada operação do `apt`) e dois “importantes” — as atualizações que mexem no kernel ou no systemd, justamente as que você mais provavelmente vai querer de volta. Acima deles fica o ponto *“SkillFishOS - clean install”*, que nunca expira: o caminho de volta ao sistema como ele saiu da caixa.

A linha de hora em hora está **desligada**. Num console de casa ela só come disco sem que ninguém olhe aqueles snapshots. Os snapshots que você cria **na mão** não entram na conta dos cinco e nunca são apagados sozinhos: se você fez um de propósito, ele fica até você remover.

## Volta atrás pelo menu de boot

Graças ao **[grub-btrfs](https://github.com/Antynea/grub-btrfs)**, os snapshots aparecem direto no menu do **GRUB**, em *“SkillFishOS snapshots”*. Reinicie, escolha o snapshot de antes do problema e você estará dentro dele.

Duas coisas que vale saber antes de contar com isso:

- **O que você inicia é somente leitura.** É um ambiente de resgate: olhe em volta, confira se o estado antigo estava mesmo bom, tire os arquivos de que precisa. Alguns serviços vão acusar erro ao subir — eles simplesmente não conseguem escrever. É o esperado, não um defeito.
- **O menu de boot é atualizado depois de cada operação do `apt`**, então o snapshot tirado *antes* de uma atualização está na lista exatamente quando você precisa.

## Como tornar a volta definitiva

Iniciar um snapshot não muda nada por si só, e o `snapper rollback` aqui não ajuda: ele troca o subvolume padrão, enquanto a nossa entrada do GRUB fixa `subvol=@` e ganha. O comando que resolve é:

```bash
sudo skillfish-rollback --list    # quais snapshots existem
sudo skillfish-rollback 12        # o snapshot 12 vira o sistema a partir do próximo boot
```

Ele põe o sistema atual de lado — não apaga, transforma em `@-rotto-<data>` — e constrói a partir do snapshot escolhido um `@` novo e gravável, levando junto todo o histórico de snapshots. Se o estado antigo também não for a resposta, `sudo skillfish-rollback --undo` devolve tudo, e `--clean` libera o espaço quando você tiver certeza.

Funciona pelo sistema normal e de dentro de um snapshot iniciado em somente leitura, que é o caso que importa quando a máquina não sobe mais.

> **Sua pasta pessoal nunca é tocada.** O `@home` é um subvolume à parte: o sistema viaja no tempo, seus arquivos ficam como estão. É bom saber, e lembrar antes de contar com uma volta atrás para recuperar um documento apagado — ela não vai.

> Essa é a rede de segurança que deixa até os mais novos explorarem o sistema sem medo de quebrá-lo sem volta.

## Por que Btrfs e não Timeshift

O SkillFishOS escolheu **Btrfs + Snapper + grub-btrfs** em vez de soluções como o Timeshift porque:

- a integração com o APT é automática (um snapshot a cada operação de pacotes);
- os snapshots são nativos do sistema de arquivos (instantâneos, *copy-on-write*, baratos);
- a volta atrás está disponível **já no boot**, mesmo que o sistema não suba mais do jeito normal.

## Fontes

- [Documentação do Btrfs](https://btrfs.readthedocs.io/)
- [Snapper](http://snapper.io/)
- [grub-btrfs (Antynea)](https://github.com/Antynea/grub-btrfs)
