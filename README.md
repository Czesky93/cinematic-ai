# Cinematic AI - Generowanie wideo na podstawie scenariuszy

Ubuntu-kompatybilna aplikacja w Pythonie, która generuje do 5 minut wideo na podstawie scenariuszy, zdjęć postaci oraz lokalizacji.

## Funkcje

- **📜 Parsowanie scenariuszy**: Automatycznie dzieli scenariusze na sceny.
- **🎭 Spójność postaci**: Używa zdjęć referencyjnych do utrzymania wyglądu postaci.
- **🎬 Generowanie kadrów**: Tworzy kadry w trybie pokazu slajdów (opcjonalnie tryb AI).
- **🎤 Lektor TTS**: Generuje narrację głosową o naturalnym brzmieniu.
- **🎵 Mikser audio**: Łączy lektor z muzyką w tle.
- **🎥 Automatyczna edycja**: Wykorzystuje FFmpeg/MoviePy do profesjonalnego montażu wideo.
- **💾 Eksport MP4**: Eksportuje standardowe wideo MP4.
- **⚙️ Konfigurowalne**: System konfiguracji oparty na YAML.
- **📊 Raportowanie logów**: Kompleksowe logowanie do celów debugowania.
- **🔌 Tryb offline**: Działa w trybie offline, gdy usługi AI są niedostępne.

## Instalacja

### Wymagania systemowe

- Ubuntu 18.04+ (lub kompatybilna dystrybucja Linuksa)
- Python 3.8+
- FFmpeg

### Instalacja FFmpeg

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### Instalacja zależności Python

```bash
pip install -r requirements.txt
```

Lub instalacja całego pakietu:

```bash
pip install -e .
```

## Szybki start

### 1. Przygotuj swoje materiały

Struktura katalogu:

```
project/
├── script.txt           # Twój scenariusz
├── characters/          # Zdjęcia postaci referencyjnych
│   ├── SARAH/
│   │   ├── sarah_1.jpg
│   │   └── sarah_2.jpg
│   └── JOHN/
│       └── john_1.jpg
└── locations/           # Zdjęcia lokalizacji
    ├── coffee_shop.jpg
    ├── park.jpg
    └── apartment.jpg
```

### 2. Uruchom generator

Za pomocą CLI:

```bash
cinematic-ai -s script.txt -c ./characters -l ./locations -o video.mp4
```

Z muzyką w tle:

```bash
cinematic-ai -s script.txt -c ./characters -l ./locations -o video.mp4 -m music.mp3
```

### 3. Test demo

```bash
python demo/run_demo.py
```