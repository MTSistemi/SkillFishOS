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
    // The "Native apps" page is gone: those apps are the Control Center now.
    // The old addresses were linked from the forum and from our own posts.
    '/docs/app-native': '/docs/control-center',
    '/en/docs/app-native': '/en/docs/control-center',
    '/pl/docs/app-native': '/pl/docs/control-center',
    '/uk/docs/app-native': '/uk/docs/control-center',
    '/ru/docs/app-native': '/ru/docs/control-center',
    '/es/docs/app-native': '/es/docs/control-center',
    '/pt/docs/app-native': '/pt/docs/control-center',
    '/de/docs/app-native': '/de/docs/control-center',
    '/fr/docs/app-native': '/fr/docs/control-center',
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
