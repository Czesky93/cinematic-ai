# Cinematic AI - Video Generation from Scripts

Ubuntu-ready Python application that generates up to 5-minute videos from scripts, character photos, and location photos.

## Features

- 📝 **Script Parsing**: Automatically splits scripts into scenes
- 🎭 **Character Consistency**: Uses reference images to maintain character appearance
- 🎬 **Frame Generation**: Creates frames using slideshow mode (AI mode optional)
- 🎤 **TTS Voiceover**: Generates natural-sounding voice narration
- 🎵 **Audio Mixing**: Combines voiceover with background music
- 🎥 **Auto-Editing**: Uses FFmpeg/MoviePy for professional video assembly
- 💾 **MP4 Export**: Outputs standard MP4 videos
- ⚙️ **Configurable**: YAML-based configuration system
- 📊 **Logging**: Comprehensive logging for debugging
- 🔌 **Offline Fallback**: Works offline when AI services unavailable

## Installation

### System Requirements

- Ubuntu 18.04+ (or compatible Linux distribution)
- Python 3.8+
- FFmpeg

### Install FFmpeg

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install the package:

```bash
pip install -e .
```

## Quick Start

### 1. Prepare Your Assets

Create the following structure:

```
project/
├── script.txt           # Your script
├── characters/          # Character reference images
│   ├── SARAH/
│   │   ├── sarah_1.jpg
│   │   └── sarah_2.jpg
│   └── JOHN/
│       └── john_1.jpg
└── locations/           # Location images
    ├── coffee_shop.jpg
    ├── park.jpg
    └── apartment.jpg
```

### 2. Run the Generator

Using the CLI:

```bash
cinematic-ai -s script.txt -c ./characters -l ./locations -o video.mp4
```

With background music:

```bash
cinematic-ai -s script.txt -c ./characters -l ./locations -o video.mp4 -m music.mp3
```

### 3. Run Demo Test

```bash
python demo/run_demo.py
```

## Script Format

The script parser supports two formats:

### Formal Screenplay Format

```
INT. COFFEE SHOP - DAY

SARAH sits at a corner table, nervously checking her phone.

JOHN enters, spotting Sarah.

JOHN
Sorry I'm late. Traffic was terrible.

EXT. PARK - DAY

SARAH and JOHN walk along a tree-lined path.
```

### Simple Format

Just separate scenes with blank lines:

```
Sarah waits in the coffee shop, checking her phone nervously.

John arrives and apologizes for being late.

They walk together through the park, talking.
```

## Configuration

Edit `config/default_config.yaml` to customize:

- **Video Settings**: Resolution, FPS, duration limits
- **Audio Settings**: TTS language, volume levels
- **Scene Settings**: Duration, transitions
- **Frame Generation**: Slideshow or AI mode
- **Output Settings**: Directories, formats

Example configuration:

```yaml
video:
  max_duration: 300  # 5 minutes
  fps: 24
  resolution:
    width: 1920
    height: 1080

audio:
  tts_language: "en"
  background_music_volume: 0.3
  voiceover_volume: 1.0

frame_generation:
  mode: "slideshow"  # or "ai" if available
```

## CLI Usage

```
cinematic-ai [OPTIONS]

Options:
  -s, --script PATH       Path to script file [required]
  -c, --characters PATH   Directory containing character images [required]
  -l, --locations PATH    Directory containing location images [required]
  -o, --output PATH       Output video path [required]
  -m, --music PATH        Background music file (optional)
  --config PATH           Custom configuration file (optional)
  --help                  Show this message and exit
```

## Python API

```python
from cinematic_ai.core.video_generator import CinematicAI

# Initialize generator
generator = CinematicAI()

# Generate video
output_video = generator.generate_video(
    script_path="script.txt",
    characters_dir="./characters",
    locations_dir="./locations",
    output_path="output.mp4",
    background_music="music.mp3"  # optional
)

print(f"Video created: {output_video}")
```

## Architecture

```
src/cinematic_ai/
├── core/
│   ├── config.py              # Configuration management
│   ├── script_parser.py       # Script parsing and scene extraction
│   ├── character_manager.py   # Character image management
│   ├── frame_generator.py     # Frame generation (slideshow/AI)
│   ├── audio_generator.py     # TTS and audio processing
│   ├── video_assembler.py     # FFmpeg video assembly
│   └── video_generator.py     # Main orchestrator
├── utils/
│   └── logger.py              # Logging utilities
└── cli.py                      # Command-line interface
```

## Logging

Logs are saved to `logs/cinematic_ai.log` by default. Set log level in config:

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: "logs/cinematic_ai.log"
```

## Troubleshooting

### FFmpeg not found

```bash
sudo apt-get install -y ffmpeg
```

### Permission denied on demo

```bash
chmod +x demo/run_demo.py
```

### Out of memory

Reduce video resolution in config:

```yaml
video:
  resolution:
    width: 1280
    height: 720
```

### TTS not working

The app uses Google TTS (gTTS) which requires internet. For offline operation, ensure you have audio files pre-generated or use the fallback silent audio mode.

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.