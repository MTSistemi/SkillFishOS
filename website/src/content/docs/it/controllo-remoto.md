---
title: Controllo remoto — Remote Manager
description: La dashboard web di SkillFishOS per controllare la BC-250 dal browser o dal telefono — telemetria, KVM, terminale, Tuner, app store e AI.
group: Uso
order: 4
---

**SkillFishOS Remote Manager** è una dashboard web modulare che ti permette di controllare la BC-250 **da un altro PC o dal telefono**, sulla stessa rete locale o — tramite ZeroTier — da qualsiasi parte del mondo. Login con le credenziali di sistema, tutto su HTTPS.

## Installazione

```bash
sudo apt update
sudo apt install skillfish-dashboard
```

Il pacchetto installa il demone, l'app nativa **Remote Manager** (per accendere/spegnere la dashboard e scegliere i moduli) e tutte le pagine web. Le dipendenze opzionali (KVM, terminale, Wake-on-LAN) sono *Recommends*: vengono installate in automatico se disponibili.

## Attivazione

Apri **SkillFishOS Remote Manager** dal menu applicazioni:

- **Interruttore principale** — accende il servizio (persistente, via systemd).
- **Spunte dei moduli** — scegli cosa esporre (telemetria, Tuner, Hub, KVM, terminale, AI…).
- Mostra **URL, QR code e credenziali** per collegarti.

In alternativa, da terminale: `sudo systemctl enable --now skillfish-dashboard`.

> Per scelta di sicurezza la dashboard **non si avvia da sola** dopo l'installazione: la attivi tu quando vuoi.

## Accesso

Apri nel browser **`https://<ip-della-board>:8443`** (oppure `https://BC-250.local:8443`). Essendo un certificato self-signed, il browser mostrerà un avviso la prima volta: è normale, procedi.

Accedi con **utente e password di sistema** (gli stessi del login di SkillFishOS): l'autenticazione usa PAM.

## I moduli

La dashboard si compone in automatico in base ai moduli che hai attivato:

- **Telemetria** — grafici live di temperature, frequenze, Watt e carichi CPU/GPU.
- **Stato sistema** — host, IP, kernel, uptime, RAM, disco, CU attive, freeze rilevati.
- **Controlli (Tuner)** — preset rapidi + il **Tuner completo** in versione web: CPU (frequenza/undervolt/temperatura), GPU (frequenza/voltaggio/governor), **controllo delle Compute Unit a caldo** (griglia WGP, senza riavvio), ventola, VRAM, *Test* e wizard **"Trova il massimo"**.
- **App e pacchetti (Hub)** — un vero **app store** (AppStream + Flatpak + Snap): sfoglia per categorie, cerca, installa/rimuovi, aggiorna. Le **app SkillFishOS** sono messe in evidenza in cima.
- **Desktop (KVM)** — vedi e controlli il desktop reale della board dal browser (noVNC), niente hardware aggiuntivo.
- **Terminale** — una shell web (ttyd) dentro la dashboard.
- **AI / OpenWebUI** — stato del motore, modelli installati e chat con l'LLM locale, sulla GPU della BC-250.
- **AI-Ops** — l'LLM locale legge log e telemetria e ti diagnostica eventuali problemi.
- **Log**, **Regole automatiche** (auto-throttle oltre soglia °C), **Wake-on-LAN** e accensione/spegnimento programmati.
- **ZeroTier** — per raggiungere la dashboard **da ovunque** (vedi sotto).

I pulsanti **Riavvia** e **Spegni** sono sempre disponibili nella barra in alto. Puoi **chiudere, riaprire e trascinare** le schede e **salvare la disposizione**.

## Accesso da remoto (ZeroTier)

La dashboard è pensata per la **rete locale**. Per usarla da fuori casa, attiva il modulo **ZeroTier**: unisciti a una tua rete, autorizza la board su [my.zerotier.com](https://my.zerotier.com) e poi raggiungi la dashboard all'indirizzo ZeroTier della board — senza aprire porte sul router.

## Sicurezza

- **HTTPS** con certificato self-signed (TLS 1.2+), generato al primo avvio.
- **Login PAM** con le credenziali dell'utente, **sessioni firmate** (HMAC) e **rate-limit** sui tentativi.
- Pensata per **rete locale**; per l'accesso da remoto usa ZeroTier, non l'esposizione diretta su internet.
