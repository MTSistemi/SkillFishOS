# -*- coding: utf-8 -*-
u"""Dizionario condiviso delle traduzioni di SkillFishOS.

PERCHE' ESISTE
Fino a oggi ogni applicazione si portava dentro i propri dizionari, uno per
lingua. Con sei app e quattro lingue erano ventiquattro dizionari incollati nel
codice; arrivando a otto lingue diventerebbero quarantotto, e ogni stringa
nuova andrebbe toccata in otto punti diversi. Prima o poi divergono - e' solo
questione di quando.

C'e' un motivo piu' importante del nostro comodo, pero'. Il polacco delle app
lo ha scritto Cyryl Sochacki, che non aveva il permesso di scrittura sul
repository: ha dovuto tenere un fork e riscrivere le stesse modifiche a ogni
nostro rilascio. Con le traduzioni in un file di dati per lingua, chi vuole
aiutare manda UN FILE, non una modifica dentro sei sorgenti Python che non ha
mai visto. Con la Spagna diventata il nostro primo paese non anglofono, e la
Russia subito dietro, la differenza fra "possiamo tradurre" e "possono
tradurci" e' tutta qui.

COME FUNZIONA
Le chiavi sono le stringhe INGLESI, esattamente come gia' erano nei dizionari
delle app: `L(it, en)` cerca `en`. Un file per lingua, comune a tutte le app,
in /usr/share/skillfish/i18n/<lingua>.json.

⚠️ PER POLACCO E UCRAINO L'APP RESTA L'AUTORITA', QUESTO E' SOLO UN RIPIEGO.
Unendo i dizionari e' saltato fuori che "off" in polacco compare tradotto in
due modi diversi - "wył." su un interruttore e "wyłączona" riferito a una
ventola - e hanno ragione entrambi. Un dizionario unico appiattirebbe quel
genere di sfumature su una scelta sola, cancellando lavoro fatto bene. Quindi
l'app cerca PRIMA nel proprio dizionario e solo dopo qui.

Il ripiego serve perche' ogni traduzione viveva dentro una sola app: il Tuner
traduce "Apply", il Monitor usa la stessa stringa senza averla nel proprio
dizionario, e l'utente polacco leggeva "Apply" nel Monitor. La traduzione
c'era gia', era solo nel file sbagliato.

⚠️ NON DEVE MAI FAR MORIRE UNA APP. Se il file manca, e' rotto o illeggibile,
si torna all'inglese e basta: una traduzione assente e' un fastidio, una app
che non parte e' un guasto.
"""
import io
import json
import os

CARTELLA = "/usr/share/skillfish/i18n"

# L'italiano non passa mai di qui: e' la lingua sorgente, la stringa arriva
# gia' scritta nel codice come primo argomento di L().
INTERNE = ("it",)

_cache = {}


def _pulisci(codice):
    u"""Da 'ru_RU.UTF-8', 'ru-RU' o 'ru' ricava 'ru'."""
    if not codice:
        return ""
    c = str(codice).replace("-", "_").split(".")[0].split("@")[0]
    c = c.split("_")[0].strip().lower()
    # ⚠️ Nei locale scritti a mano capita il PAESE al posto della lingua
    # ("UA" invece di "uk"): due lettere maiuscole non sono una lingua.
    return c if c.isalpha() and len(c) == 2 else ""


def lingua(ambiente=None):
    u"""La lingua dell'utente, con l'ordine standard dei locale."""
    env = ambiente if ambiente is not None else os.environ
    for chiave in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        c = _pulisci((env.get(chiave) or "").split(":")[0])
        if c:
            return c
    return "en"


def carica(codice):
    u"""Il dizionario di una lingua, o vuoto se non c'e' o non si legge."""
    c = _pulisci(codice)
    if not c or c in INTERNE or c == "en":
        return {}
    if c in _cache:
        return _cache[c]
    d = {}
    percorso = os.path.join(CARTELLA, c + ".json")
    try:
        with io.open(percorso, encoding="utf-8") as f:
            dati = json.load(f)
        if isinstance(dati, dict):
            # Si accetta sia il file piatto sia quello con un'intestazione:
            # {"_meta": {...}, "voci": {...}}
            d = dati.get("voci") if isinstance(dati.get("voci"), dict) else dati
            d = dict((k, v) for k, v in d.items()
                     if isinstance(k, str) and isinstance(v, str) and v)
    except Exception:
        d = {}
    _cache[c] = d
    return d


def disponibili():
    u"""Le lingue per cui esiste un file, in ordine."""
    try:
        return sorted(n[:-5] for n in os.listdir(CARTELLA) if n.endswith(".json"))
    except Exception:
        return []


def traduttore(codice=None):
    u"""Restituisce una funzione tr(en) -> testo tradotto (o l'inglese).

    Si usa cosi', dentro l'app:

        import sys; sys.path.insert(0, "/usr/share/skillfish")
        from i18n import traduttore
        _tr = traduttore(LANG)
        def L(it, en):
            if LANG == "it": return it
            if LANG == "pl": return PL.get(en, en)
            if LANG == "uk": return UK.get(en, en)
            return _tr(en)
    """
    d = carica(codice if codice is not None else lingua())

    def tr(en):
        return d.get(en, en) if d else en
    return tr
