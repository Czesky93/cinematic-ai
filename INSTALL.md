# Installation Guide

## Prerequisites

- **Operating System**: Ubuntu 18.04+ (or compatible Linux distribution)
- **Python**: 3.8 or higher
- **FFmpeg**: Required for video processing

## Step 1: Install System Dependencies

### Ubuntu/Debian

```bash
# Update package list
sudo apt-get update

# Install FFmpeg
sudo apt-get install -y ffmpeg

# Verify installation
ffmpeg -version
```

### Other Linux Distributions

**Fedora/RHEL:**
```bash
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

## Step 2: Install Python Dependencies

### Option A: Using pip (Recommended)

```bash
# Install from PyPI (once published)
pip install cinematic-ai

# Or install from source
git clone https://github.com/Czesky93/cinematic-ai.git
cd cinematic-ai
pip install -e .
```

### Option B: Install requirements manually

```bash
pip install -r requirements.txt
```

## Step 3: Verify Installation

### Test the CLI

```bash
cinematic-ai --help
```

You should see:
```
Usage: cinematic-ai [OPTIONS]

  Cinematic AI - Generate videos from scripts, character photos, and location
  photos.
  ...
```

### Run the Demo

```bash
python demo/run_demo.py
```

This will:
1. Parse the sample script
2. Generate frames from character and location images
3. Create TTS voiceovers (or fallback to silent audio if offline)
4. Assemble a complete MP4 video at `demo/output/demo_video.mp4`

## Troubleshooting

### FFmpeg not found

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution:**
```bash
sudo apt-get install -y ffmpeg
```

### Permission denied

**Error:** `Permission denied: demo/run_demo.py`

**Solution:**
```bash
chmod +x demo/run_demo.py
```

### Import errors

**Error:** `ModuleNotFoundError: No module named 'cinematic_ai'`

**Solution:**
```bash
# Make sure you're in the project directory
cd /path/to/cinematic-ai

# Install in editable mode
pip install -e .
```

### TTS not working (offline)

**Info:** TTS requires internet connection. The application will automatically fall back to silent audio when offline.

**Alternative:** Pre-generate voiceovers when online, or use custom audio files.

### Out of memory

**Error:** System runs out of memory during video generation

**Solution:** Reduce video resolution in `config/default_config.yaml`:

```yaml
video:
  resolution:
    width: 1280  # Instead of 1920
    height: 720  # Instead of 1080
```

## Development Setup

For developers who want to contribute:

```bash
# Clone the repository
git clone https://github.com/Czesky93/cinematic-ai.git
cd cinematic-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e .

# Run tests
python -m unittest discover tests
```

## Uninstallation

```bash
pip uninstall cinematic-ai
```

## Next Steps

After installation, see the [README.md](README.md) for:
- Quick start guide
- Script format documentation
- Configuration options
- Python API usage
- CLI examples
