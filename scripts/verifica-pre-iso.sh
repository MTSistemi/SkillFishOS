#!/bin/bash
# Controllo completo prima di generare le ISO.
#
# Verifica gli ARTEFATTI VERI sulla board (file installati, contenuto dei .deb,
# testo reso dalle app), non quello che il repo dice che dovrebbe esserci.
# Oggi tre controlli su quattro erano verdi su roba rotta, sempre perche'
# guardavano la cosa sbagliata: flatpak come root invece che come utente, le
# icone con il tema sbagliato, il servizio conky lanciato a mano invece che dal
# login. Qui si guarda il risultato.
PASS=0; FAIL=0; WARN=0
ok()   { printf '  \033[32mOK\033[0m   %s\n' "$1"; PASS=$((PASS+1)); }
ko()   { printf '  \033[31mNO\033[0m   %s\n' "$1"; FAIL=$((FAIL+1)); }
warn() { printf '  \033[33m??\033[0m   %s\n' "$1"; WARN=$((WARN+1)); }
sec()  { printf '\n\033[1m== %s\033[0m\n' "$1"; }

U=skillfish; UID_N=$(id -u $U 2>/dev/null || echo 1000)
# QT_QPA_PLATFORM=offscreen: senza, Qt prova xcb, non trova il display e
# ABORTISCE — il test moriva invece di dare un risultato.
AS="sudo -u $U env XDG_RUNTIME_DIR=/run/user/$UID_N QT_QPA_PLATFORM=offscreen"

sec "1. Le app compilano e sono tradotte"
python3 - <<'PY'
import ast, io, re, sys
ph = lambda s: re.findall(r'%(?:\d+\$)?[-+ #0]*[\d.*]*[a-zA-Z%]', s)
apps = ["tuner", "hub", "ai-panel", "kernel-manager", "monitor", "remote-manager"]
paths = {"ai-panel": "/usr/local/bin/skillfish-ai-panel",
         "remote-manager": "/usr/local/bin/skillfish-remote-manager"}
for a in apps:
    p = paths.get(a, "/usr/local/bin/skillfish-" + a)
    try:
        src = io.open(p, encoding="utf-8").read(); t = ast.parse(src)
    except FileNotFoundError:
        print("  \033[33m??\033[0m   %s: non installato" % a); continue
    except SyntaxError as e:
        print("  \033[31mNO\033[0m   %s: NON COMPILA (%s)" % (a, e)); continue
    D = {}
    for n in ast.walk(t):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict):
            for tg in n.targets:
                if isinstance(tg, ast.Name) and tg.id in ("PL", "UK"):
                    D[tg.id] = {k.value: v.value for k, v in zip(n.value.keys, n.value.values)
                                if isinstance(k, ast.Constant) and isinstance(v, ast.Constant)}
    C = [n for n in ast.walk(t) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
         and n.func.id == "L" and len(n.args) == 2]
    dyn = [n.lineno for n in C if not all(isinstance(x, ast.Constant) for x in n.args)]
    ks = {n.args[1].value for n in C if isinstance(n.args[1], ast.Constant)}
    miss = [k for k in ks for d in ("PL", "UK") if k not in D.get(d, {})]
    bad  = [k for k in ks for d in ("PL", "UK") if k in D.get(d, {}) and ph(D[d][k]) != ph(k)]
    if dyn or miss or bad:
        print("  \033[31mNO\033[0m   %-16s formattate=%s  senza pl/uk=%d  segnaposto errati=%d"
              % (a, dyn or "-", len(miss), len(bad)))
    else:
        print("  \033[32mOK\033[0m   %-16s %3d chiavi, pl+uk complete, nessuna formattata" % (a, len(ks)))
PY

sec "2. Voci di menu: base in inglese, traduzioni presenti"
for f in /usr/share/applications/os.skillfish.*.desktop /usr/share/applications/skillfish-info.desktop; do
    [ -f "$f" ] || continue
    b=$(basename "$f")
    if ! desktop-file-validate "$f" >/dev/null 2>&1; then
        ko "$b non valido: $(desktop-file-validate "$f" 2>&1 | head -1 | cut -c1-110)"; continue
    fi
    it=$(grep -c '^\(Name\|Comment\|GenericName\)\[it\]=' "$f")
    pl=$(grep -c '^\(Name\|Comment\|GenericName\)\[pl\]=' "$f")
    uk=$(grep -c '^\(Name\|Comment\|GenericName\)\[uk\]=' "$f")
    itl=$(grep -E '^(Name|Comment|GenericName)=' "$f" | grep -cE '\b(Regola|Mostra|Accendi|Monta|Grafici|Sfoglia|Scegli|Installa|Attiva)\b')
    if [ "$itl" -gt 0 ]; then ko "$b ha il campo BASE in italiano"
    elif [ "$pl" -eq 0 ] || [ "$uk" -eq 0 ]; then warn "$b senza pl/uk (it=$it pl=$pl uk=$uk)"
    else ok "$b (it=$it pl=$pl uk=$uk)"; fi
done

sec "3. Icone - con il tema ATTIVO, non con breeze"
TEMA=$($AS grep -m1 '^Theme=' /home/$U/.config/kdeglobals 2>/dev/null | cut -d= -f2)
[ -n "$TEMA" ] && ok "tema attivo: $TEMA" || warn "non leggo il tema attivo"
if [ -e /usr/share/icons/SkillFishSteampunk/icon-theme.cache ]; then
    ko "c'e' una icon-theme.cache nel tema steampunk: svuota le icone della barra, va tolta"
else
    ok "nessuna icon-theme.cache nel tema steampunk (giusto cosi')"
fi
$AS python3 - "$TEMA" <<'PY'
import sys
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
except Exception as e:
    print("  \033[33m??\033[0m   non posso provare le icone: %s" % e); sys.exit()
a = QApplication(["x"]); QIcon.setThemeSearchPaths(["/usr/share/icons"])
QIcon.setThemeName(sys.argv[1] or "SkillFishSteampunk")
def px(n):
    p = QIcon.fromTheme(n).pixmap(48, 48); im = p.toImage()
    return sum(1 for y in range(im.height()) for x in range(im.width())
               if im.pixelColor(x, y).alpha() > 0)
hub, disc, logo = px("skillfish-hub"), px("plasmadiscover"), px("skillfishos")
if hub == 0:            print("  \033[31mNO\033[0m   skillfish-hub non si risolve")
elif hub == disc != 0:  print("  \033[32mOK\033[0m   skillfish-hub identica a plasmadiscover (%d px)" % hub)
else:                   print("  \033[33m??\033[0m   skillfish-hub %d px, plasmadiscover %d px" % (hub, disc))
print("  \033[32mOK\033[0m   il logo skillfishos resta diverso (%d px)" % logo if logo != hub
      else "  \033[31mNO\033[0m   l'Hub usa ancora il logo generico")
PY

sec "4. HUD"
[ -x /usr/local/bin/skillfish-hud ] && ok "skillfish-hud installato ed eseguibile" || ko "skillfish-hud manca"
grep -q 'skillfish-is-bc250' /usr/local/bin/skillfish-hud 2>/dev/null \
    && ok "protetto: non parte fuori dalla BC-250" || ko "manca il controllo sull'hardware"
E=$(grep -m1 '^Exec=' /etc/skel/.config/autostart/skillfish-conky.desktop 2>/dev/null)
case "$E" in
    "Exec=/usr/local/bin/skillfish-hud") ok "autostart: percorso assoluto, niente quoting" ;;
    *'$HOME'*) ko "autostart cita ancora \$HOME: non verra' espanso" ;;
    *) warn "autostart: $E" ;;
esac
/usr/local/bin/skillfish-is-bc250 >/dev/null 2>&1 \
    && ok "questa e' una BC-250: qui il HUD deve partire" \
    || warn "questa non risulta una BC-250"

sec "5. Barra e skel"
L=$(grep -m1 'launchers=' /etc/skel/.config/plasma-org.kde.plasma.desktop-appletsrc 2>/dev/null)
case "$L" in
    *os.skillfish.hub.desktop*) ok "skel: nella barra c'e' il nostro Hub" ;;
    *discover*) ko "skel: nella barra c'e' ancora Discover" ;;
    *) warn "skel: $L" ;;
esac
grep -q 'discover' <<<"$L" && ko "skel: Discover ancora presente" || ok "skel: nessun riferimento a Discover"

sec "6. Emulatori"
for f in /usr/local/share/skillfish/install-emudeck.sh /usr/local/share/skillfish/install-emulators.sh; do
    [ -x "$f" ] && ok "$(basename $f) installato" || ko "$(basename $f) manca"
    bash -n "$f" 2>/dev/null && ok "$(basename $f) sintassi corretta" || ko "$(basename $f) errore di sintassi"
done
for d in emudeck emulators; do
    f=/usr/share/applications/os.skillfish.$d.desktop
    if [ -f "$f" ]; then
        grep -q 'Categories=.*Game' "$f" && ok "os.skillfish.$d nel menu Giochi" || ko "os.skillfish.$d fuori da Giochi"
    else ko "os.skillfish.$d.desktop manca"; fi
done

sec "7. Pacchetti .deb"
# ATTENZIONE: questa sezione guardava in /tmp/debs/out e /tmp/newdebs/out, che
# sono le cartelle dei VECCHI script di build. Dopo un riavvio /tmp e' vuoto:
# il ciclo non trovava nessun file, saltava tutto e il riepilogo diceva
# comunque "nessun errore". Undici controlli spariti in silenzio.
# Adesso le cartelle si cercano, e se non c'e' NESSUN pacchetto e' un errore,
# non un motivo per stare zitti.
DEBDIR=""
for d in /root/debs-new/out /tmp/sfx-debs/out /tmp/debs/out /tmp/newdebs/out; do
    [ -d "$d" ] && ls "$d"/*.deb >/dev/null 2>&1 && { DEBDIR="$d"; break; }
done
if [ -z "$DEBDIR" ]; then
    ko "nessun .deb trovato: ricostruisci con scripts/build-debs-ci.sh prima di generare le ISO"
else
    ok "pacchetti in $DEBDIR"
    for d in "$DEBDIR"/*.deb; do
        n=$(basename "$d")
        dpkg-deb -I "$d" >/dev/null 2>&1 && ok "$n leggibile ($(du -h "$d" | cut -f1))" || ko "$n corrotto"
    done
    # l'elenco va su file: con `dpkg-deb -c | grep -q` grep chiude la pipe al
    # primo riscontro e dpkg-deb muore di SIGPIPE, dando falsi negativi
    T=$(ls "$DEBDIR"/skillfish-tuner_*.deb 2>/dev/null | head -1)
    if [ -n "$T" ]; then
        dpkg-deb -c "$T" > /tmp/vpi.$$ 2>/dev/null
        grep -qF 'usr/local/bin/skillfish-hud' /tmp/vpi.$$ \
            && ok "skillfish-hud e' dentro skillfish-tuner" || ko "skillfish-hud NON e' nel pacchetto"
        grep -qF 'tuner-presets.json' /tmp/vpi.$$ \
            && ok "tuner-presets.json e' nel pacchetto" || ko "tuner-presets.json manca"
        grep -qF 'Wydajność' <(dpkg-deb --fsys-tarfile "$T" | tar -xO ./usr/share/skillfish/tuner-presets.json 2>/dev/null) \
            && ok "diacritici polacchi nei preset" || ko "diacritici polacchi persi"
        rm -f /tmp/vpi.$$
    else ko "skillfish-tuner non costruito"; fi

    H=$(ls "$DEBDIR"/skillfish-hub_*.deb 2>/dev/null | head -1)
    if [ -n "$H" ]; then
        dpkg-deb -c "$H" > /tmp/vpi.$$ 2>/dev/null
        N=$(grep -c 'skillfish-hub\.\(png\|svg\)' /tmp/vpi.$$)
        [ "$N" -ge 4 ] && ok "icone dell'Hub nel pacchetto ($N file)" || ko "solo $N icone dell'Hub nel pacchetto"
        rm -f /tmp/vpi.$$
        # la correzione che faceva fallire ogni installazione flatpak
        dpkg-deb --fsys-tarfile "$H" | tar -xO ./usr/local/bin/skillfish-hub 2>/dev/null \
            | grep -qF '"--system", "flathub"' \
            && ok "Hub: le installazioni flatpak indicano l'ambito" \
            || ko "Hub: manca --system, nessuna installazione flatpak funzionerebbe"
    else ko "skillfish-hub non costruito"; fi

    # changelog e copyright, obbligatori per la Debian Policy
    senza=0
    for d in "$DEBDIR"/*.deb; do
        p=$(dpkg-deb -f "$d" Package)
        dpkg-deb -c "$d" > /tmp/vpi.$$ 2>/dev/null
        grep -qF "usr/share/doc/$p/changelog.Debian.gz" /tmp/vpi.$$ || senza=$((senza+1))
        grep -qF "usr/share/doc/$p/copyright" /tmp/vpi.$$ || senza=$((senza+1))
        rm -f /tmp/vpi.$$
    done
    [ "$senza" = 0 ] && ok "tutti i pacchetti hanno changelog e copyright" \
                     || ko "$senza documenti obbligatori mancanti"
fi

sec "8. Versione e marchio"
grep -m1 PRETTY_NAME /etc/os-release
for f in /etc/os-release /etc/lsb-release /etc/issue; do
    [ -f "$f" ] && printf '  %-20s %s\n' "$(basename $f)" "$(grep -m1 -oE '26\.[0-9.]+' $f | head -1)"
done

sec "9. Calamares"
# Il branding attivo si LEGGE da settings.conf invece di darlo per scontato:
# cercavo in skillfishos/, ma quello in uso e' eggs/ e la cartella skillfish/
# contiene una vecchia versione italiana che non viene mai mostrata.
BR=$(grep -m1 "^branding:" /etc/calamares/settings.conf | cut -d: -f2 | tr -d " ")
ok "branding attivo: $BR"
S=/etc/calamares/branding/$BR/show.qml
if [ -f "$S" ]; then
    grep -q 'Qt.locale()' "$S" && ok "presentazione multilingua (legge la lingua scelta)" || ko "presentazione a lingua fissa"
    for l in it pl uk en; do
        grep -q "\"$l\":" "$S" && ok "  diapositive in $l" || ko "  diapositive in $l mancanti"
    done
else warn "show.qml non trovato in $S"; fi

printf '\n\033[1m== RIEPILOGO ==\033[0m\n'
printf '  superati %d   falliti %d   da guardare %d\n' "$PASS" "$FAIL" "$WARN"
[ "$FAIL" -eq 0 ] && echo "  Nessun errore bloccante." || echo "  CI SONO ERRORI: non generare le ISO prima di averli risolti."
