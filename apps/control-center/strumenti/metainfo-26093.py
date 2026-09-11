#!/usr/bin/env python3
"""The 26.09.3 entry in the Control Center's metainfo: it is what the Hub
shows when it offers the update.

    metainfo-26093.py <repo>
"""
import os
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
p = os.path.join(repo, "apps", "control-center", "os.skillfish.control-center.metainfo.xml")

T = [
 (None, "The AI section drives Unsloth Studio instead of only switching it on: version and update in one click, the first sign-in and the API key done from here, the models on disk, GGUF downloads from the Hugging Face Hub, a chat test with the measured tokens per second, memory and local network. The Tuner gains the 512 MB and 1 GB VRAM presets, and 2048 MB is a valid split again."),
 ("it", "La sezione AI pilota Unsloth Studio invece di limitarsi ad accenderlo: versione e aggiornamento in un clic, primo accesso e chiave API fatti da qui, i modelli sul disco, il download dei GGUF dall'Hub di Hugging Face, una chat di prova con i token al secondo misurati, memoria e rete locale. Il Tuner guadagna i preset VRAM da 512 MB e 1 GB, e i 2048 MB tornano un valore buono."),
 ("fr", "La section IA pilote Unsloth Studio au lieu de se contenter de l'allumer : version et mise à jour en un clic, première connexion et clé API faites ici, les modèles sur le disque, le téléchargement des GGUF depuis le Hub Hugging Face, un essai de chat avec les tokens par seconde mesurés, mémoire et réseau local. Le Tuner gagne les préréglages VRAM 512 Mo et 1 Go, et 2048 Mo redevient une valeur valable."),
 ("es", "La sección IA pilota Unsloth Studio en vez de solo encenderlo: versión y actualización en un clic, primer acceso y clave API hechos desde aquí, los modelos en disco, la descarga de GGUF del Hub de Hugging Face, una prueba de chat con los tokens por segundo medidos, memoria y red local. El Tuner gana los preajustes de VRAM de 512 MB y 1 GB, y 2048 MB vuelve a ser un valor válido."),
 ("pt", "A secção IA pilota o Unsloth Studio em vez de apenas o ligar: versão e atualização num clique, primeiro acesso e chave API feitos aqui, os modelos em disco, a transferência de GGUF do Hub da Hugging Face, um teste de chat com os tokens por segundo medidos, memória e rede local. O Tuner ganha as predefinições de VRAM de 512 MB e 1 GB, e 2048 MB volta a ser um valor válido."),
 ("de", "Der KI-Bereich steuert Unsloth Studio, statt ihn nur einzuschalten: Version und Aktualisierung in einem Klick, erste Anmeldung und API-Schlüssel von hier aus, die Modelle auf der Platte, GGUF-Downloads aus dem Hugging-Face-Hub, ein Chat-Test mit den gemessenen Token pro Sekunde, Speicher und lokales Netz. Der Tuner bekommt die VRAM-Vorgaben 512 MB und 1 GB, und 2048 MB ist wieder ein gültiger Wert."),
 ("pl", "Sekcja AI steruje Unsloth Studio, a nie tylko go włącza: wersja i aktualizacja jednym kliknięciem, pierwsze logowanie i klucz API zrobione stąd, modele na dysku, pobieranie GGUF z Hubu Hugging Face, próbny czat ze zmierzonymi tokenami na sekundę, pamięć i sieć lokalna. Tuner dostaje presety VRAM 512 MB i 1 GB, a 2048 MB znów jest dobrą wartością."),
 ("ru", "Раздел ИИ управляет Unsloth Studio, а не просто включает его: версия и обновление в один клик, первый вход и ключ API сделаны отсюда, модели на диске, загрузка GGUF из Hub Hugging Face, проба чата с измеренными токенами в секунду, память и локальная сеть. Тюнер получает пресеты VRAM 512 МБ и 1 ГБ, а 2048 МБ снова допустимое значение."),
 ("uk", "Розділ ШІ керує Unsloth Studio, а не лише вмикає його: версія й оновлення в один клік, перший вхід і ключ API зроблені звідси, моделі на диску, завантаження GGUF з Hub Hugging Face, проба чату з виміряними токенами за секунду, пам'ять і локальна мережа. Тюнер отримує пресети VRAM 512 МБ і 1 ГБ, а 2048 МБ знову допустиме значення."),
]

with open(p, encoding="utf-8") as f:
    s = f.read()
if '26.09.3' in s:
    raise SystemExit("la voce 26.09.3 c'e' gia'")

righe = ['    <release version="26.09.3" date="2026-09-12">', '      <description>']
for lingua, testo in T:
    testo = testo.replace("&", "&amp;").replace("<", "&lt;")
    righe.append('        <p%s>%s</p>' % ((' xml:lang="%s"' % lingua) if lingua else "", testo))
righe += ['      </description>', '    </release>']
s = s.replace("  <releases>\n", "  <releases>\n" + "\n".join(righe) + "\n", 1)
with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
print("voce 26.09.3 aggiunta")
