#!/bin/bash
# Aggiunge la guardia hardware ai servizi specifici della BC-250.
#
# Senza guardia, su un PC che non e' una BC-250 questi servizi partono, non
# trovano l'hardware, muoiono e systemd li fa ripartire all'infinito. Misurato
# in VM sulla 26.06.3-rc2: cyan-skillfish-governor era al riavvio numero 231.
# Il desktop funziona lo stesso, quindi il difetto passa inosservato mentre
# brucia CPU e riempie il journal - proprio sull'edizione Generic, che e'
# quella pensata per i PC normali.
#
# ExecCondition diverso da zero fa SALTARE l'unita', non fallire: nessuno
# stato failed, nessun riavvio. E' esattamente la semantica che serve.
#
# Idempotente: si puo' rieseguire senza duplicare nulla.
set -u

GUARD=/usr/local/bin/skillfish-is-bc250
UNITS="
cyan-skillfish-governor.service
skillfish-core-unlock.service
skillfish-cu.service
skillfish-gpu-freq.service
skillfish-gpu-util.service
skillfish-thermal-guard.service
skillfish-dp-hotswap.service
"

if [ ! -x "$GUARD" ]; then
    echo "FATAL: manca $GUARD (lo spedisce skillfish-base)" >&2
    exit 1
fi

echo "guardia: $GUARD"
if "$GUARD"; then
    echo "  questa macchina E' una BC-250: i servizi partiranno normalmente"
else
    echo "  questa macchina NON e' una BC-250: i servizi verranno saltati"
fi
echo

changed=0
for u in $UNITS; do
    f=""
    for d in /etc/systemd/system /usr/lib/systemd/system /lib/systemd/system; do
        [ -f "$d/$u" ] && { f="$d/$u"; break; }
    done
    if [ -z "$f" ]; then
        printf "  %-38s non presente, salto\n" "$u"
        continue
    fi
    if grep -q "ExecCondition=$GUARD" "$f"; then
        printf "  %-38s guardia gia' presente\n" "$u"
        continue
    fi
    [ -f "$f.skfbak" ] || cp "$f" "$f.skfbak"
    # la riga va nella sezione [Service], subito prima di ExecStart
    if grep -q '^ExecStart=' "$f"; then
        sed -i "0,/^ExecStart=/s##ExecCondition=$GUARD\nExecStart=#" "$f"
        printf "  %-38s guardia aggiunta\n" "$u"
        changed=$((changed + 1))
    else
        printf "  %-38s nessun ExecStart, salto\n" "$u"
    fi
done

echo
echo "unita' modificate: $changed"
if [ "$changed" -gt 0 ] && [ -d /run/systemd/system ]; then
    systemctl daemon-reload && echo "systemd ricaricato"
fi

echo
echo "verifica:"
for u in $UNITS; do
    for d in /etc/systemd/system /usr/lib/systemd/system /lib/systemd/system; do
        [ -f "$d/$u" ] || continue
        printf "  %-38s %s\n" "$u" \
            "$(grep -q "ExecCondition=$GUARD" "$d/$u" && echo protetta || echo SENZA GUARDIA)"
        break
    done
done
