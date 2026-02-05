# transcribe_fw.py
from faster_whisper import WhisperModel
from pathlib import Path
import json
import sys

AUDIO_DIR = Path("audio")
OUT_DIR = Path("transcripts")
OUT_DIR.mkdir(exist_ok=True)

# Check if audio directory exists
if not AUDIO_DIR.exists():
    print(f"Warning: Audio directory '{AUDIO_DIR}' does not exist.")
    print("Please create the 'audio' directory and add MP3 files to transcribe.")
    sys.exit(0)

# Check if there are any audio files
audio_files = list(AUDIO_DIR.glob("*.mp3"))
if not audio_files:
    print(f"Warning: No MP3 files found in '{AUDIO_DIR}' directory.")
    print("Please add MP3 files to transcribe.")
    sys.exit(0)

print(f"Found {len(audio_files)} audio file(s) to transcribe")

MODEL_SIZE = "medium"   # or small / large-v3
DEVICE = "cpu"          # GitHub Actions 預設
COMPUTE_TYPE = "int8"   # 關鍵：CI 友善

model = WhisperModel(
    MODEL_SIZE,
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)

for audio_path in audio_files:
    video_id = audio_path.stem
    out_txt = OUT_DIR / f"{video_id}.txt"

    if out_txt.exists():
        print(f"Skipping {video_id} (already transcribed)")
        continue

    print(f"Transcribing {video_id}...")
    segments, info = model.transcribe(
        str(audio_path),
        language="zh",
        beam_size=5,
        vad_filter=True
    )

    with open(out_txt, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"[{seg.start:.2f}-{seg.end:.2f}] {seg.text}\n")
    
    print(f"✓ Completed {video_id}")

print(f"\nTranscription complete! Check the '{OUT_DIR}' directory for results.")
