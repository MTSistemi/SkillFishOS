# SkillFishOS — Website

Sito ufficiale di SkillFishOS, costruito con [Astro](https://astro.build/) (SSG).
Output **statico puro**, bilingue **IT/EN**, deploy via FTP su OVH.

## Struttura

```
src/
 ├─ i18n.ts                  # dizionario IT/EN + config sito (SITE.isoUrl, repo, github)
 ├─ styles/global.css        # design tokens steampunk + stile docs
 ├─ layouts/Base.astro       # <head>, SEO/OG, Header + Footer
 ├─ components/
 │   ├─ Header.astro         # nav + lang-switch (link alla pagina equivalente)
 │   ├─ Footer.astro
 │   ├─ HomeContent.astro    # contenuto home (condiviso IT/EN)
 │   ├─ DownloadContent.astro
 │   └─ DocsShell.astro      # chrome docs: sidebar + indice pagina + prev/next
 ├─ content.config.ts        # collection "docs" (Markdown)
 ├─ content/docs/*.md        # la documentazione (italiano)
 └─ pages/
     ├─ index.astro              → /              (IT)
     ├─ download/index.astro     → /download
     ├─ docs/[...slug].astro     → /docs/<slug>   (genera le pagine docs)
     └─ en/…                     → /en/, /en/download, /en/docs
```

### i18n
IT è la lingua di default (servita su `/`), EN sotto `/en/`. Le stringhe stanno in
`src/i18n.ts` nella forma `{ it, en }`; si rendono con `t(key, lang)` (e `set:html`
per le stringhe con markup). Il selettore lingua linka la pagina equivalente.

La **documentazione** è in italiano. La pagina `/en/docs` rimanda all'italiano e
alle docs su GitHub finché non viene tradotta.

### Aggiungere una pagina di documentazione
Crea `src/content/docs/mia-pagina.md` con frontmatter:
```yaml
---
title: Titolo
description: "Descrizione (tra virgolette se contiene il carattere :)"
group: Sistema        # Introduzione | Installazione | Sistema | Uso | Riferimenti
order: 5              # ordine nella sidebar dentro al gruppo
---
```
La pagina compare automaticamente in sidebar, con indice e prev/next.

## Build

```powershell
# Windows (consigliato in questo repo, vedi nota Dropbox):
./build.ps1
# oppure direttamente:
npm run build
```

L'output finisce in **`%TEMP%\skillfishos-website-dist`**, non in `./dist`.

> ### Nota Dropbox + Windows (importante)
> Il progetto vive in una cartella sincronizzata da Dropbox. Astro a fine build
> rimuove cartelle di cache vuote (`.astro`, `.astro/img`) e il filtro di Dropbox
> le tiene bloccate → `astro build` esce con codice 1 e `EBUSY ... rmdir '.astro'`
> **dopo** aver però già scritto tutto l'output.
>
> Per questo `astro.config.mjs` redirige **outDir**, **vite.cacheDir** e **cacheDir**
> in `%TEMP%`, e `build.ps1` considera il build riuscito se l'output esiste
> (ignorando l'EBUSY cosmetico). `node_modules`, `dist` e `.astro` sono marcati
> come *Dropbox-ignored*.

## Anteprima locale

```powershell
npm run preview   # serve l'output su http://localhost:4321/
# oppure dev con hot-reload:
npm run dev
```

## Deploy su OVH (FTP)

Caricare il **contenuto** di `%TEMP%\skillfishos-website-dist` nella web-root OVH
(`www/`) via FTP (`ftp.cluster129.hosting.ovh.net`). Essendo statico, non serve
PHP né database. Gli URL usano la forma `/pagina/` (cartella + `index.html`), che
funziona su Apache senza rewrite.

## Configurazione del download ISO
L'URL della ISO è in `src/i18n.ts` → `SITE.isoUrl`. Finché è vuoto, la pagina
Download mostra lo stato "ISO in arrivo". Impostandolo (es. `dl.skillfishos.com`
o un bucket R2), il bottone diventa il link di download reale.
