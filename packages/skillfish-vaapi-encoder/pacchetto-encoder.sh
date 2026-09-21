#!/bin/bash
# Package the BC-250 VA-API encoder.
#
#     pacchetto-encoder.sh [versione]
#         esempio: pacchetto-encoder.sh 26.09.1
#
# ⚠️ SI ACCENDE SOLO SU UNA BC-250, e non e' pignoleria. Questo driver
# decodifica sul processore, quindi dire a tutto il sistema
# LIBVA_DRIVER_NAME=bc250 significa mettere lui al posto di uno che decodifica
# sulla scheda grafica, e Firefox, mpv e VLC ci rimettono. Sulla BC-250 non si
# perde niente perche' li' un VA-API non c'e': radeonsi_drv_video.so fallisce
# l'init anche forzando --display drm --device /dev/dri/renderD128, misurato.
# Su un PC normale, dove radeonsi o iHD funzionano benissimo, la stessa riga
# sarebbe un danno - e le nostre immagini finiscono anche sui PC.
#
# Quindi la variabile non sta in un file fisso: la scrive un generatore di
# ambiente di systemd, che gira all'apertura della sessione SULLA MACCHINA VERA
# e decide li', chiedendo a skillfish-is-bc250.
set -u
VER="${1:-$(date +%y.%m).1}"
QUI=$(dirname "$(readlink -f "$0")")
RADICE=$(cd "$QUI/../.." && pwd)
LAVORO=~/encoder-bc250
ALBERO=$LAVORO/costruito

[ -f "$ALBERO/bc250_drv_video.so" ] || {
    echo "non trovo $ALBERO: prima compila-encoder.sh" >&2; exit 1; }
COMMIT=$(cat "$LAVORO/commit.txt" 2>/dev/null || echo sconosciuto)

# ⚠️ Si controlla che la libreria sia davvero la nostra, non una v0.4.3 di
# monte: senza le correzioni l'HEVC va in segfault al primo fotogramma, e un
# pacchetto che fa quello e' peggio di nessun pacchetto.
if ! strings "$ALBERO/bc250_drv_video.so" | grep -q 'BC250_HEVC_SLICES'; then
    echo "questa libreria non conosce BC250_HEVC_SLICES: non e' il nostro ramo" >&2
    exit 1
fi

P=~/pkg-encoder
rm -rf "$P"
install -d "$P/DEBIAN" \
           "$P/usr/lib/x86_64-linux-gnu/dri" \
           "$P/usr/share/bc250/shaders" \
           "$P/usr/lib/systemd/user-environment-generators" \
           "$P/usr/share/metainfo" \
           "$P/usr/share/icons/hicolor/scalable/apps" \
           "$P/usr/share/icons/hicolor/48x48/apps" \
           "$P/usr/share/icons/hicolor/128x128/apps" \
           "$P/usr/share/icons/hicolor/256x256/apps" \
           "$P/usr/share/doc/skillfish-vaapi-encoder"

install -m 0644 "$ALBERO/bc250_drv_video.so" "$P/usr/lib/x86_64-linux-gnu/dri/"
install -m 0644 "$ALBERO"/*.spv "$P/usr/share/bc250/shaders/"

# ⚠️ La scheda nell'Hub esiste solo se il pacchetto porta un metainfo.
# Senza, il driver non sta nel catalogo che l'Hub legge e la sua descrizione
# vive solo in `apt show`, solo in inglese.
install -m 0644 "$QUI/os.skillfish.vaapi.metainfo.xml" "$P/usr/share/metainfo/"
ICONE=$RADICE/system/usr/share/icons/hicolor
install -m 0644 "$ICONE/scalable/apps/skillfish-vaapi-encoder.svg" \
        "$P/usr/share/icons/hicolor/scalable/apps/"
for s in 48x48 128x128 256x256; do
    install -m 0644 "$ICONE/$s/apps/skillfish-vaapi-encoder.png" \
            "$P/usr/share/icons/hicolor/$s/apps/"
done
install -m 0755 "$QUI/60-skillfish-vaapi" \
        "$P/usr/lib/systemd/user-environment-generators/60-skillfish-vaapi"
install -m 0644 "$QUI/copyright" "$P/usr/share/doc/skillfish-vaapi-encoder/copyright"

TAGLIA=$(du -sk "$P" | cut -f1)
cat > "$P/DEBIAN/control" <<CTRL
Package: skillfish-vaapi-encoder
Version: $VER
Section: video
Priority: optional
Architecture: amd64
Depends: libva2, libvulkan1, libdrm2, libgomp1
Recommends: skillfish-base
Installed-Size: $TAGLIA
Maintainer: Mattia Tadini <info@mtsistemi.it>
Description: Video encoding and decoding for the AMD BC-250
 The BC-250 has no usable video engine, so recording, streaming and playback
 all fall back to the CPU. This is a VA-API driver that does the work itself:
 encoding with Vulkan compute shaders on the board's 40 compute units, and
 decoding on the CPU with its own H.264 and H.265 decoders.
 .
 Encoding, measured on the board at 1920x1080 at 60 fps: H.264 reaches 129
 frames per second, HEVC 113. Recording a game costs it 13% with H.264 and 35%
 with HEVC, and both hold a full 60 fps.
 .
 Decoding, measured the same way: H.264 reaches 119 frames per second, H.265
 96. Both produce every sample of every picture exactly as the reference
 decoder does - 67 H.264 and 38 H.265 configurations compared byte for byte -
 and both hold 1920x1080 at 60 fps with room to spare. H.265 decodes several
 coding tree block rows at once when the stream allows it; set
 BC250_HEVC_THREAD to use fewer.
 .
 Faster than nothing, not faster than everything: ffmpeg's own threaded
 software decoder reaches 355 frames per second on the same processor. This
 driver is for an application that asks for VA-API and would otherwise be
 told there is none.
 .
 It turns itself on only on a real BC-250, where no other VA-API driver
 initialises at all: on a machine whose own driver works, this one would take
 its place and give back less.
 .
 Built from commit $COMMIT of simpmix/bc250-encoding-decoding-fix with our
 fixes (upstream pull requests 21 and 22).
CTRL

cat > "$P/DEBIAN/postinst" <<'POST'
#!/bin/sh
set -e
if [ "$1" = configure ]; then
    # ⚠️ La cache di ldconfig non c'entra: il driver lo apre libva per nome,
    # dalla cartella dri/. Qui si dice solo che c'e', e a chi.
    if [ -x /usr/local/bin/skillfish-is-bc250 ] && /usr/local/bin/skillfish-is-bc250 >/dev/null 2>&1; then
        echo "skillfish-vaapi-encoder: BC-250 riconosciuta, la codifica hardware si accende al prossimo accesso"
    else
        echo "skillfish-vaapi-encoder: non e' una BC-250, il driver resta installato ma spento"
    fi
fi
exit 0
POST
chmod 0755 "$P/DEBIAN/postinst"

FUORI=~/skillfish-vaapi-encoder_${VER}_amd64.deb
dpkg-deb --build --root-owner-group "$P" "$FUORI" >/dev/null
echo ">>> $FUORI"
dpkg-deb -I "$FUORI" | sed -n '2,12p'
echo ">>> dentro:"
dpkg-deb -c "$FUORI" | awk '{print "   "$6}' | head -20
