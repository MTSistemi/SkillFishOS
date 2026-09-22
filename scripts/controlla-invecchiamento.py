# -*- coding: utf-8 -*-
u"""I testi dicono ancora la verita'? Confronto con quello che l'archivio serve.

PERCHE' ESISTE. Il 23/08/2026 Mattia ha sfogliato GitHub e ha trovato la wiki
ferma a due mesi e mezzo prima: kernel 7.0.11 quando ne spedivamo 7.2.0, il
motore AI ancora Ollama, quattro applicazioni non nominate. Nessuno l'aveva
notato perche' la wiki, lavorando, non la apre nessuno. La regola «GitHub va
tenuto aggiornato» e' giusta ma vive nella testa di qualcuno; qui vive su una
macchina.

COSA CONTROLLA, e perche' proprio questo
Non tutti i numeri: solo quelli che, se sbagliati, dicono una bugia a chi legge.
  1. la versione del kernel citata nei testi contro quella pubblicata;
  2. i link alle release del kernel: puntano a un tag che esiste?
  3. la tabella delle versioni supportate in SECURITY.md contro l'archivio;
  4. i nomi di pezzi che non spediamo piu' (Ollama, OpenWebUI, Docker), fuori
     dai punti dove sono scritti apposta come «superato»;
  5. l'elenco delle applicazioni nella wiki contro quello che l'archivio serve;
  6. dove portano davvero i pulsanti di download del sito, contro l'ultima
     immagine pubblicata su SourceForge.

⚠️ Il punto 6 e' nato il 15/09/2026, quando il sito ha annunciato la 26.06.5 e
consegnato la 26.06.4 per tre giorni. I testi erano stati aggiornati tutti; il
passaggio dei download no. Cercare il numero nei sorgenti risponde a «lo
diciamo?», non a «lo consegniamo?»: quel giorno le due risposte erano diverse,
e solo la seconda si prova con una richiesta.

⚠️ NON FALLISCE PER RUMORE. Un CHANGELOG deve nominare le versioni vecchie, e
una sezione «superseded» deve nominare Ollama: quei posti sono esclusi apposta.
Un controllo che grida sempre viene spento dopo tre giorni.

Uso:
    python3 scripts/controlla-invecchiamento.py            # solo guarda
    python3 scripts/controlla-invecchiamento.py --rapporto # scrive rapporto.md
"""
from __future__ import unicode_literals, print_function

import io
import os
import re
import sys
import urllib.error
import urllib.request

# ⚠️ OVH non serve piu' l'archivio dal 13/09/2026: si guarda Pages.
ARCHIVIO = "https://mtsistemi.github.io/SkillFishOS"
WIKI = "https://raw.githubusercontent.com/wiki/MTSistemi/SkillFishOS"
SITO = "https://skillfishos.com"
SORGENTE_IMMAGINI = "https://sourceforge.net/projects/skillfishos/rss?path=/"

# I pulsanti della pagina di download. Sono scritti per esteso perche' sono
# esattamente quelli che go.php conosce: se un giorno ne aggiungiamo uno e qui
# non compare, il controllo lo ignora invece di sbagliare da solo.
PULSANTI = ["bc250", "generic", "sha-bc250", "sha-generic",
            "note", "tutti", "tor-bc250", "tor-generic"]
RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# I file dove un numero sbagliato inganna chi legge. Il CHANGELOG NO: la' le
# versioni vecchie ci vanno, e' il suo mestiere.
TESTI = ["README.md", "SECURITY.md", "CONTRIBUTING.md",
         "docs/AI.md", "docs/BUILD.md", "docs/DESKTOP.md",
         "docs/GAMING.md", "docs/OPTIMIZATIONS.md"]

PAGINE_WIKI = ["Home", "Installation", "Kernel", "Apps", "APT-Repository",
               "On-device-AI", "SkillFishOS-Control-Center", "SkillFishOS-Hub",
               "Building-from-Source", "Troubleshooting"]

# ⚠️ NON basta cercare parole-scusa riga per riga: al primo giro questo
# controllo ha dato dodici segnalazioni di cui UNA vera. Quello che conta e'
# DOVE sta la riga.
#
# 1. Un titolo che parla del passato vale per tutta la sua sezione, fino al
#    titolo successivo: dentro «## Superseded: the Ollama stack» ogni riga puo'
#    nominare Ollama, e infatti lo fa.
TITOLI_STORICI = re.compile(r"superseded|history|no longer|used to be|"
                            r"what changed|previously", re.I)
# 2. Una MISURA si riferisce a quello con cui e' stata fatta. Riscriverla per
#    farla combaciare con l'ultima versione sarebbe falsificarla.
MISURE = re.compile(r"measured|benchmark|tested on|as measured", re.I)
# 3. Una riga di tabella che porta un verdetto sta facendo il suo mestiere: la
#    tabella delle versioni supportate DEVE nominare le vecchie, se no non dice
#    fino a dove arriviamo.
VERDETTI = re.compile(r"previous series|best effort|\|\s*no\s*\||superseded|"
                      r"upgrade to|pre-release", re.I)
# 4. E una riga che descrive il contenuto di un'immagine gia' pubblicata dice
#    cosa c'e' dentro quella, non cosa spediamo oggi.
IMMAGINI = re.compile(r"\.iso|/files/|download", re.I)

SCUSANTI = re.compile(r"used to be|was here until|earlier releases|"
                      r"until 26\.|were here|it used to", re.I)


def righe_da_guardare(testo):
    u"""Le righe su cui ha senso pretendere che sia tutto attuale.

    Salta le sezioni storiche per intero, le misure, i verdetti di tabella e le
    righe che descrivono un'immagine gia' pubblicata.
    """
    dentro_storia = False
    for n_, riga in enumerate(testo.split("\n"), 1):
        if riga.startswith("#"):
            dentro_storia = bool(TITOLI_STORICI.search(riga))
            continue
        if dentro_storia:
            continue
        if (SCUSANTI.search(riga) or MISURE.search(riga)
                or VERDETTI.search(riga) or IMMAGINI.search(riga)):
            continue
        yield n_, riga


def scarica(url):
    try:
        with urllib.request.urlopen(url, timeout=40) as f:
            return f.read().decode("utf-8", "replace")
    except Exception as e:
        sys.stderr.write("non riesco a leggere %s: %s\n" % (url, e))
        return None


def versioni_pubblicate():
    u"""Cosa serve l'archivio adesso: {pacchetto: versione}."""
    t = scarica(ARCHIVIO + "/dists/aetherium/main/binary-amd64/Packages")
    if t is None:
        return None
    fuori = {}
    for blocco in t.split("\n\n"):
        n = re.search(r"^Package: (.+)$", blocco, re.M)
        v = re.search(r"^Version: (.+)$", blocco, re.M)
        if n and v:
            fuori[n.group(1)] = v.group(1).strip()
    return fuori


def immagine_pubblicata():
    u"""L'ultima release che su SourceForge ha davvero una immagine BC-250.

    ⚠️ Non basta guardare l'ultima cartella: 26.06.1, .2 e .3 esistono ancora
    con dentro le sole note di rilascio. Una cartella non e' una release
    scaricabile, e il confronto va fatto con quello che uno puo' scaricare.
    """
    t = scarica(SORGENTE_IMMAGINI)
    if t is None:
        return None
    viste = re.findall(
        r"/files/(\d+\.\d+\.\d+)-Aetherium/"
        r"SkillFishOS-\1-Aetherium-BC250-amd64\.iso", t)
    if not viste:
        return None
    return max(viste, key=lambda v: [int(x) for x in v.split(".")])


def dove_porta(percorso):
    u"""Dove manda il sito, senza seguire il rimando.

    Il Location e' la risposta: seguirlo vorrebbe dire scaricare tre gigabyte
    per sapere una cosa che sta in una intestazione.
    """
    class NonSeguire(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    try:
        r = urllib.request.build_opener(NonSeguire).open(SITO + percorso, timeout=40)
        return r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "")
    except Exception as e:
        sys.stderr.write("non riesco a chiedere a %s%s: %s\n" % (SITO, percorso, e))
        return None, None


def testi_locali():
    for rel in TESTI:
        p = os.path.join(RADICE, rel)
        if os.path.isfile(p):
            yield rel, io.open(p, encoding="utf-8").read()


def testi_wiki():
    for nome in PAGINE_WIKI:
        t = scarica("%s/%s.md" % (WIKI, nome))
        if t is not None:
            yield "wiki/%s" % nome, t


def controlla():
    guai = []
    pub = versioni_pubblicate()
    if pub is None:
        return ["Could not read the apt archive: check skipped, not failed."]

    kern = pub.get("skillfishos-kernel", "")
    kern_corto = kern.split("-")[0]                       # 7.2.0-2 -> 7.2.0
    # Only versions in our own YY.MM.N scheme count. Packages that carry an
    # upstream version (skillfish-vkpeak 20260816-1, skillfish-mesa-gfx1013)
    # would otherwise "win" the comparison and make SECURITY.md look stale.
    app = sorted((v for k, v in pub.items()
                  if k.startswith("skillfish-") and re.fullmatch(r"\d{2}\.\d{2}\.\d+", v)),
                 key=lambda s: [int(x) for x in re.findall(r"\d+", s)] or [0])
    app_ultima = app[-1] if app else ""

    tutti = list(testi_locali()) + list(testi_wiki())

    # 1 e 2: versioni del kernel e link alle release
    for nome, t in tutti:
        for n_, riga in righe_da_guardare(t):
            for m in re.finditer(r"\b(\d+\.\d+\.\d+)-skillfishos", riga):
                if m.group(1) != kern_corto:
                    guai.append("**%s:%d** says the kernel is `%s-skillfishos`, "
                                "but the archive serves `%s`."
                                % (nome, n_, m.group(1), kern_corto))
            for m in re.finditer(r"releases/tag/kernel-(\d+\.\d+\.\d+)-skillfishos", riga):
                if m.group(1) != kern_corto:
                    guai.append("**%s:%d** links to release `kernel-%s-skillfishos`, "
                                "which is not the current one (`%s`)."
                                % (nome, n_, m.group(1), kern_corto))

    # 3: la tabella delle versioni supportate
    p = os.path.join(RADICE, "SECURITY.md")
    if os.path.isfile(p) and app_ultima:
        t = io.open(p, encoding="utf-8").read()
        m = re.search(r"\| Apps \| `skillfish-\*` `([0-9.]+)`", t)
        # Only OLDER is stale. The release commit moves SECURITY.md forward
        # before the packages reach the mirrors, and the push runs this check
        # in that gap: a newer version there is a release in progress, and
        # flagging it opened a false issue on three releases (#90, #92, #94).
        def _v(x):
            return [int(n) for n in re.findall(r"\d+", x)]
        if m and _v(m.group(1)) < _v(app_ultima):
            guai.append("**SECURITY.md** claims apps `%s` are supported, "
                        "but the latest published is `%s`." % (m.group(1), app_ultima))

    # 4: pezzi che non spediamo piu'
    morti = ["Ollama", "OpenWebUI", "open-webui", "Dockge"]
    for nome, t in tutti:
        for n_, riga in righe_da_guardare(t):
            for d in morti:
                if re.search(r"\b%s\b" % re.escape(d), riga, re.I):
                    guai.append("**%s:%d** mentions **%s**, which we no longer ship, "
                                "and the line does not present it as history."
                                % (nome, n_, d))

    # 5: applicazioni pubblicate ma non nominate nella wiki
    apps_wiki = scarica(WIKI + "/Apps.md")
    if apps_wiki:
        for pacchetto in sorted(k for k in pub if k.startswith("skillfish-")):
            if pacchetto in ("skillfish-menu", "skillfish-theme"):
                continue          # infrastruttura, non hanno una voce loro
            if pacchetto not in apps_wiki:
                guai.append("**wiki/Apps** does not mention `%s`, which we publish." % pacchetto)

    # 6: i pulsanti consegnano davvero l'ultima immagine?
    # ⚠️ Se il sito o SourceForge non rispondono si SALTA. Un controllo che
    # grida per un problema di rete viene spento, e allora non protegge piu'
    # niente: e' la stessa ragione per cui le regole qui sopra hanno le loro
    # eccezioni.
    iso = immagine_pubblicata()
    if iso:
        sbagliati, muti = [], False
        for chiave in PULSANTI:
            codice, dove = dove_porta("/go.php?f=" + chiave)
            if codice is None:
                muti = True
                break
            if codice not in (301, 302) or not dove:
                sbagliati.append("`%s` answers %s instead of a redirect" % (chiave, codice))
            elif iso not in dove:
                sbagliati.append("`%s` -> %s" % (chiave, dove))
        # Una sola segnalazione, non otto: e' un guasto solo, e otto righe
        # identiche in una issue si leggono come rumore.
        if not muti and sbagliati:
            guai.append("**The download buttons do not hand over `%s`**, which is "
                        "the newest image on SourceForge. The page can say the new "
                        "number and still serve the old file: every button goes "
                        "through `go.php`. %s"
                        % (iso, "; ".join(sbagliati[:4])))

    return guai


def main():
    guai = controlla()
    if not guai:
        print("All aligned: the texts say what the archive serves.")
        return 0

    print("Found %d stale things:\n" % len(guai))
    for g in guai:
        print(" - " + g.replace("**", ""))

    if "--rapporto" in sys.argv:
        with io.open(os.path.join(RADICE, "rapporto-invecchiamento.md"),
                     "w", encoding="utf-8", newline="\n") as f:
            f.write("Some of what we publish no longer matches what we say.\n\n")
            for g in guai:
                f.write("- %s\n" % g)
            f.write("\n---\n_Opened automatically by "
                    "`scripts/controlla-invecchiamento.py`. "
                    "Close it once the texts match again._\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
