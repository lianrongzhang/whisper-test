from faster_whisper import WhisperModel
from pathlib import Path
from tqdm import tqdm

AUDIO_DIR = Path("audio")
OUT_DIR = Path("transcripts")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_SIZE = "medium"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"   # ⭐ GitHub Actions 必選

model = WhisperModel(
    MODEL_SIZE,
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)

audio_files = sorted(
    list(AUDIO_DIR.glob("*.mp3")) +
    list(AUDIO_DIR.glob("*.wav"))
)

print(f"🔊 Found {len(audio_files)} audio files")

for audio_path in tqdm(audio_files, desc="Transcribing"):
    video_id = audio_path.stem
    out_txt = OUT_DIR / f"{video_id}.txt"

    if out_txt.exists() and out_txt.stat().st_size > 0:
        continue

    try:
        segments, info = model.transcribe(
            str(audio_path),
            language="zh",
            beam_size=5,
            vad_filter=True
        )

        with open(out_txt, "w", encoding="utf-8") as f:
            for seg in segments:
                f.write(f"[{seg.start:.2f}-{seg.end:.2f}] {seg.text}\n")

    except Exception as e:
        print(f"❌ Failed {video_id}: {e}")
