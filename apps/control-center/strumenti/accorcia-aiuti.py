#!/usr/bin/env python3
"""Shorten the help texts of the Control Center pages to one sentence each
(2026-09-12, Mattia: "le descrizioni dei ? sono troppo prolisse"). The long
explanations live in the documentation, linked from every page.

    accorcia-aiuti.py <apps/control-center dir>

Each entry: file, a snippet that identifies the Italian text of an L(...) call,
and the new (it, en) pair. The whole L(...) call is replaced. Idempotent.
"""
import os
import re
import sys

base = os.path.join(sys.argv[1], "sfcc", "pagine")
STR = r'(?:"(?:[^"\\]|\\.)*"\s*)+'
L_CALL = re.compile(r'L\(\s*(' + STR + r'),\s*(' + STR + r')\)', re.S)

CAMBI = [
    ("stato.py", "La frequenza che il governor sta forzando",
     "Frequenza forzata dal governor e tetto: sotto carico sale al tetto, che scende se la scheda scalda o tira troppo.",
     "Clock forced by the governor and its ceiling: under load it jumps to the ceiling, which drops when the board gets hot or draws too much."),
    ("stato.py", "La BC-250 nasce con 24 unita' attive",
     "24 unita' attive di serie: le altre 16 le accendiamo noi all'avvio.",
     "24 units on by default: we turn the other 16 on at boot."),
    ("stato.py", "Il sistema lascia un segno quando si spegne",
     "Se manca il segno dello spegnimento in ordine, l'ultima volta e' andato giu' da solo: con l'overclock e' il sintomo che conta.",
     "If the orderly-shutdown mark is missing, the last time it went down on its own: with an overclock that is the symptom that counts."),
    ("ventola.py", "Un grafico solo con dentro tutto",
     "I sensori degli ultimi cinque minuti e la curva della ventola nel riquadro: trascina i punti, doppio clic per aggiungerne uno.",
     "The sensors of the last five minutes and the fan curve in the box: drag the knots, double-click to add one."),
    ("ventola.py", "ACCESO: il controllo si prende la ventola",
     "Acceso: la curva comanda la ventola. Spento: torna al firmware, e non c'e' nemmeno l'emergenza.",
     "On: the curve drives the fan. Off: back to the firmware, with no emergency either."),
    ("ventola.py", "Il segnale che arriva prima di tutti",
     "Un gioco pesante scalda venti secondi dopo l'avvio: la ventola parte prima.",
     "A heavy game heats up twenty seconds after launch: the fan starts before."),
    ("ventola.py", "Scrivere su un'uscita PWM non vuol dire",
     "Ventola al massimo, poi al 35%, poi di nuovo al massimo: se i giri seguono, il PWM comanda davvero. Trenta secondi.",
     "Fan to full, then 35%, then full again: if the speed follows, the PWM really drives it. Thirty seconds."),
    ("giochi.py", "La nostra Mesa apre le code compute",
     "La nostra Mesa apre le code compute: +4% in Cyberpunk, +12% con FSR 4. Serve il nostro kernel.",
     "Our Mesa opens the compute queues: +4% in Cyberpunk, +12% with FSR 4. It needs our kernel."),
    ("giochi.py", "scx_bpfland, lo schedulatore di CachyOS",
     "scx_bpfland solo mentre gira un gioco (lo alza GameMode): +1,5-2% in Cyberpunk. Espulso due volte dal kernel, si ferma finche' non azzeri.",
     "scx_bpfland only while a game runs (GameMode raises it): +1.5-2% in Cyberpunk. Ejected twice by the kernel, it stops until you reset."),
    ("giochi.py", "FSR 4 gira sulla BC-250 attraverso OptiScaler",
     "Via OptiScaler sul percorso DLSS: GE-Proton 11 lo scarica da solo e il gioco va messo su DLSS. Serve amdxcffx64.dll dal driver AMD.",
     "Through OptiScaler on the DLSS path: GE-Proton 11 downloads it and the game must be set to DLSS. Needs amdxcffx64.dll from the AMD driver."),
    ("giochi.py", "Le versioni GE-Proton 11 pubblicate",
     "Le GE-Proton 11 di GloriousEggroll: Installa scarica 500 MB per Steam e Heroic, Predefinita la sceglie. Steam va chiuso.",
     "GloriousEggroll's GE-Proton 11: Install downloads 500 MB for Steam and Heroic, Default picks it. Steam must be closed."),
    ("ai.py", "Unsloth Studio con llama.cpp su Vulkan",
     "Unsloth Studio con llama.cpp su Vulkan. Acceso tiene la memoria della GPU: spegnilo prima di giocare.",
     "Unsloth Studio with llama.cpp on Vulkan. On, it holds GPU memory: turn it off before gaming."),
    ("ai.py", "Sulla BC-250 la memoria e' condivisa",
     "Quota di RAM che il modello puo' usare oltre alla VRAM. Parametro del kernel: serve un riavvio.",
     "Share of RAM the model may use on top of VRAM. Kernel parameter: a reboot is needed."),
    ("emulatori.py", "Installa e configura quasi tutti gli emulatori",
     "Installa e configura emulatori, cartelle ROM, BIOS e controlli, tutto nella tua home.",
     "Installs and configures emulators, ROM folders, BIOS files and controls, all in your home."),
    ("emulatori.py", "Flatpak da Flathub, perche' i pacchetti Debian",
     "Flatpak da Flathub: i pacchetti Debian sono vecchi e su questa GPU rendono male. Spuntati i consigliati.",
     "Flatpaks from Flathub: the Debian packages are old and run badly on this GPU. The recommended ones are ticked."),
    ("console.py", "Parte sopra al desktop che sta girando",
     "Parte sopra al desktop: gamescope prende lo schermo e Steam si apre in modalita' console.",
     "Starts on top of the desktop: gamescope takes the screen and Steam opens in console mode."),
    ("console.py", "Nella schermata di accesso, in basso",
     "Nella schermata di accesso scegli la sessione «SkillFishOS Console»: la scheda parte in Steam senza desktop.",
     "On the login screen pick the «SkillFishOS Console» session: the board starts into Steam, no desktop."),
    ("profili.py", "Prende tetto, CPU, preset della ventola",
     "Salva tetto, CPU, ventola e schedulatore come sono adesso in un profilo tuo.",
     "Saves ceiling, CPU, fan and scheduler as they are now in a profile of yours."),
]


def sostituisci(testo, pezzo, it, en):
    for m in L_CALL.finditer(testo):
        if pezzo in m.group(1):
            nuovo = 'L("%s",\n            "%s")' % (it.replace('"', '\\"'), en.replace('"', '\\"'))
            return testo[:m.start()] + nuovo + testo[m.end():], True
    return testo, False


tot = 0
for f, pezzo, it, en in CAMBI:
    p = os.path.join(base, f)
    with open(p, encoding="utf-8") as fp:
        t = fp.read()
    if it in t:
        continue
    t, ok = sostituisci(t, pezzo, it, en)
    if not ok:
        print("NON TROVATO:", f, pezzo)
        continue
    with open(p, "w", encoding="utf-8") as fp:
        fp.write(t)
    tot += 1
print("accorciati:", tot)
