# Whisper Test - Audio Transcription

This repository contains tools for transcribing audio files using Faster-Whisper.

## Setup

### Prerequisites
- Python 3.10 or later
- FFmpeg (for audio processing)

### Installation

1. Install system dependencies:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y ffmpeg
   
   # macOS
   brew install ffmpeg
   ```

2. Install Python dependencies:
   ```bash
   pip install faster-whisper ffmpeg-python
   ```

## Usage

### Local Transcription

1. Create an `audio` directory and add your MP3 files:
   ```bash
   mkdir audio
   cp your-audio-file.mp3 audio/
   ```

2. Run the transcription script:
   ```bash
   python transcribe_fw.py
   ```

3. Find transcripts in the `transcripts/` directory

### GitHub Actions

The repository includes a GitHub Actions workflow for transcription:

1. Go to the "Actions" tab in your GitHub repository
2. Select "Faster-Whisper Transcription" workflow
3. Click "Run workflow"

**Note**: Make sure you have audio files in the `audio` directory before running the workflow.

## Configuration

You can adjust transcription settings in `transcribe_fw.py`:

- `MODEL_SIZE`: Choose from "tiny", "base", "small", "medium", "large-v3"
- `DEVICE`: "cpu" or "cuda" (GPU)
- `COMPUTE_TYPE`: "int8" (for CPU), "float16" (for GPU)

## Files

- `transcribe_fw.py` - Main transcription script using faster-whisper
- `batch_transcribe_all_videos.py` - Batch processing script
- `download_audio_from_json.py` - Download audio from JSON metadata
- `youtube_transcribe.py` - YouTube transcription tool
- `.github/workflows/transcribe.yml` - GitHub Actions workflow

## Troubleshooting

### "No MP3 files found"
Make sure you have MP3 files in the `audio/` directory.

### FFmpeg errors
Ensure FFmpeg is properly installed on your system.

### Out of memory
Try using a smaller model size like "small" or "base".
