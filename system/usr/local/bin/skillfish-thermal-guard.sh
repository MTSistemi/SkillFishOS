#!/bin/sh
# SkillFishOS - guardia termica della CPU.
#
# COSA FA. Guarda la temperatura del processore. Se supera il limite, toglie
# 100 MHz all'overclock; quando la scheda torna fredda, li rimette.
#
# ⚠️ LA PARTE CHE RIMETTE E' NUOVA, E MANCAVA. Fino al 27/08/2026 questa guardia
# sapeva solo scalare: una volta scesa da 3700 a 3500 non risaliva mai piu', e
# siccome riscrive /etc/bc250-smu-oc.conf col valore nuovo, dopo mezz'ora di
# gioco il file diceva 3500 come se l'avesse scelto l'utente. Nessuno se ne
# accorgeva. Misurato col banco di prova: 1,2% di fotogrammi in meno, per sempre,
# su ogni macchina che avesse giocato una volta con la ventola in affanno.
#
# ⚠️ E NON DEVE RIALZARE QUELLO CHE HA ABBASSATO L'UTENTE. Se rialzasse a
# occhi chiusi fino a un valore ricordato, disferebbe la scelta di chi ha messo
# 3400 apposta perche' a 3700 la sua scheda si pianta. Percio' si tiene il conto
# dell'ultimo valore scritto DA NOI: se il file e' diverso da quello, l'ha
# cambiato qualcun altro, e quel valore diventa il nuovo obiettivo.
#
# La temperatura si legge da k10temp, che e' il sensore del processore.

CONF=/etc/skillfish/thermal-guard.conf
OC=/etc/bc250-smu-oc.conf
STATO=/var/lib/skillfish/thermal-guard
APPLY=/opt/bc250_smu_oc/bc250_apply.py
[ -f "$APPLY" ] || APPLY=/root/bc250_smu_oc/bc250_apply.py

# valori di riserva, se la configurazione non c'e' o e' incompleta
LIMITE=85          # sopra questa temperatura si scala
PASSO=100          # di quanto si scala o si risale, in MHz
MINIMO=3500        # sotto non si scende: e' la frequenza di serie
MARGINE=15         # quanti gradi sotto il limite serve per risalire
ATTESA=6           # letture consecutive fredde prima di risalire (10s l'una)

[ -r "$CONF" ] && . "$CONF" 2>/dev/null
RIPRISTINO=$((LIMITE - MARGINE))

mkdir -p "$(dirname "$STATO")" 2>/dev/null
obiettivo=''
nostro=''
[ -r "$STATO" ] && . "$STATO" 2>/dev/null

freddi=0

leggi_temperatura() {
    t=0
    for h in /sys/class/hwmon/hwmon*; do
        [ "$(cat "$h/name" 2>/dev/null)" = k10temp ] &&
            t=$(awk '{printf "%d",$1/1000}' "$h/temp1_input" 2>/dev/null)
    done
    echo "${t:-0}"
}

frequenza_attuale() {
    awk -F= '/frequency/{print $2}' "$OC" 2>/dev/null | tr -d ' ' | head -1
}

applica() {
    # ⚠️ Il governor della GPU va fermato mentre si riprogramma la SMU, se no i
    # due parlano insieme allo stesso chip e l'applicazione fallisce a meta'.
    sed -i "s/^frequency = .*/frequency = $1/" "$OC"
    systemctl stop cyan-skillfish-governor 2>/dev/null
    python3 "$APPLY" --apply "$OC" >/dev/null 2>&1
    systemctl start cyan-skillfish-governor 2>/dev/null
    nostro=$1
    printf 'obiettivo=%s\nnostro=%s\n' "$obiettivo" "$nostro" > "$STATO"
}

while true; do
    t=$(leggi_temperatura)
    cur=$(frequenza_attuale)

    if [ -n "$cur" ]; then
        # Se il file non contiene il valore che avevamo scritto noi, vuol dire
        # che l'ha cambiato l'utente o il Tuner: quello diventa l'obiettivo, e
        # da li' in poi non si risale mai piu' in alto.
        if [ -z "$obiettivo" ] || [ "$cur" != "$nostro" ]; then
            obiettivo=$cur
            nostro=$cur
            printf 'obiettivo=%s\nnostro=%s\n' "$obiettivo" "$nostro" > "$STATO"
        fi

        if [ "$t" -gt "$LIMITE" ] && [ "$cur" -gt "$MINIMO" ]; then
            nuova=$((cur - PASSO))
            [ "$nuova" -lt "$MINIMO" ] && nuova=$MINIMO
            echo "caldo: ${t}C sopra il limite di ${LIMITE}C, scendo da ${cur} a ${nuova} MHz"
            applica "$nuova"
            freddi=0
        elif [ "$t" -lt "$RIPRISTINO" ] && [ "$cur" -lt "$obiettivo" ]; then
            # ⚠️ Non si risale alla prima lettura fredda: fra un fotogramma e
            # l'altro la temperatura oscilla di parecchi gradi, e una guardia
            # che sale e scende in continuazione riprogramma la SMU ogni dieci
            # secondi durante una partita. Servono ATTESA letture di fila.
            freddi=$((freddi + 1))
            if [ "$freddi" -ge "$ATTESA" ]; then
                nuova=$((cur + PASSO))
                [ "$nuova" -gt "$obiettivo" ] && nuova=$obiettivo
                echo "freddo: ${t}C da $((ATTESA * 10))s, risalgo da ${cur} a ${nuova} MHz (obiettivo ${obiettivo})"
                applica "$nuova"
                freddi=0
            fi
        else
            freddi=0
        fi
    fi

    sleep 10
done
