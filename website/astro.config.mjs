// @ts-check
import { defineConfig } from 'astro/config';
import os from 'node:os';
import path from 'node:path';

// Keep Vite's dep-optimizer cache OUTSIDE the Dropbox-synced project folder:
// on Windows, Dropbox/AV locking node_modules/.vite causes EBUSY rename errors.
const viteCacheDir = path.join(os.tmpdir(), 'skillfishos-website-vite');
// Same reason for the build output: Dropbox locking dist/ causes EBUSY rmdir
// during Astro's post-build cleanup. Build outside the synced folder.
const outDir = path.join(os.tmpdir(), 'skillfishos-website-dist');
const cacheDir = path.join(os.tmpdir(), 'skillfishos-website-cache');

// SkillFishOS website — static output, bilingual IT/EN.
// IT is the default locale served at "/", EN under "/en/".
export default defineConfig({
  site: 'https://skillfishos.com',
  outDir,
  cacheDir,
  i18n: {
    defaultLocale: 'it',
    locales: ['it', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  build: {
    // Emit /page/index.html so URLs work on plain Apache (OVH) without rewrites
    format: 'directory',
  },
  redirects: {
    // Senza queste voci /<lang>/docs non genera un index.html e il server
    // risponde con l'elenco delle cartelle. PL e UK hanno l'interfaccia
    // tradotta ma i documenti in inglese, quindi puntano alle stesse pagine.
    '/docs': '/docs/introduzione',
    '/en/docs': '/en/docs/introduzione',
    '/pl/docs': '/pl/docs/introduzione',
    '/uk/docs': '/uk/docs/introduzione',
    // ⚠️ Aggiungendo una lingua questa riga si dimentica facilmente, e il
    // sintomo non e' una pagina rotta ma l'elenco delle cartelle di Apache:
    // sembra un problema del server, invece manca qui. Successo con il russo.
    '/ru/docs': '/ru/docs/introduzione',
    '/es/docs': '/es/docs/introduzione',
    '/pt/docs': '/pt/docs/introduzione',
    '/de/docs': '/de/docs/introduzione',
    '/fr/docs': '/fr/docs/introduzione',
  },
  vite: {
    cacheDir: viteCacheDir,
  },
});
