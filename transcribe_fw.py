# transcribe_fw.py
from faster_whisper import WhisperModel
from pathlib import Path
import json

AUDIO_DIR = Path("audio")
OUT_DIR = Path("transcripts")
OUT_DIR.mkdir(exist_ok=True)

MODEL_SIZE = "medium"   # or small / large-v3
DEVICE = "cpu"          # GitHub Actions 預設
COMPUTE_TYPE = "int8"   # 關鍵：CI 友善

model = WhisperModel(
    MODEL_SIZE,
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)

for audio_path in AUDIO_DIR.glob("*.mp3"):
    video_id = audio_path.stem
    out_txt = OUT_DIR / f"{video_id}.txt"

    if out_txt.exists():
        continue

    segments, info = model.transcribe(
        str(audio_path),
        language="zh",
        beam_size=5,
        vad_filter=True
    )

    with open(out_txt, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"[{seg.start:.2f}-{seg.end:.2f}] {seg.text}\n")
