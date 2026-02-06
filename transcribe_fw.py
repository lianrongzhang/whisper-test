from faster_whisper import WhisperModel
from pathlib import Path
from tqdm import tqdm
import os

# =========================
# Paths
# =========================

AUDIO_DIR = Path("audio")
OUT_DIR = Path("transcripts")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# Shard config（一定要最前面）
# =========================

SHARD_ID = int(os.environ.get("SHARD_ID", "0"))
TOTAL_SHARDS = int(os.environ.get("TOTAL_SHARDS", "1"))

audio_files = sorted(
    list(AUDIO_DIR.glob("*.mp3")) +
    list(AUDIO_DIR.glob("*.wav"))
)

audio_files = [
    f for i, f in enumerate(audio_files)
    if i % TOTAL_SHARDS == SHARD_ID
]

print(
    f"🔀 Shard {SHARD_ID}/{TOTAL_SHARDS} "
    f"→ {len(audio_files)} audio files"
)

# =========================
# Model
# =========================

MODEL_SIZE = "medium"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"   # GitHub Actions 必選

single_model = WhisperModel(
    MODEL_SIZE,
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)
model = BatchedInferencePipeline(model=single_model)

# =========================
# Transcription
# =========================

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
            vad_filter=True,
            batch_size=16
        )

        with open(out_txt, "w", encoding="utf-8") as f:
            for seg in segments:
                f.write(f"[{seg.start:.2f}-{seg.end:.2f}] {seg.text}\n")

    except Exception as e:
        print(f"❌ Failed {video_id}: {e}")
