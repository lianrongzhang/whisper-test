#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
從 videos JSON 讀取 YouTube URL
使用 yt-dlp 下載音訊
使用 ffprobe 驗證音訊檔
"""

import json
import subprocess
from pathlib import Path
from tqdm import tqdm

# =========================
# 設定
# =========================

INPUT_JSON = "CTWANT_videos.json"
OUTPUT_DIR = Path("audio")
AUDIO_FORMAT = "mp3"
FFPROBE_TIMEOUT = 10

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# 工具函式
# =========================

def run_cmd(cmd, timeout=None):
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout
    )

def ffprobe_ok(path: Path) -> bool:
    """確認音訊檔是否可被 ffprobe 解析"""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        str(path)
    ]
    try:
        r = run_cmd(cmd, timeout=FFPROBE_TIMEOUT)
        return r.returncode == 0
    except Exception:
        return False

def download_audio(url: str, video_id: str, out_dir: Path) -> Path | None:
    out_path = out_dir / f"{video_id}.{AUDIO_FORMAT}"

    # 已存在且可用就跳過
    if out_path.exists() and ffprobe_ok(out_path):
        return out_path

    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", AUDIO_FORMAT,
        "--audio-quality", "0",
        "-o", str(out_dir / f"{video_id}.%(ext)s"),
        url
    ]


    r = run_cmd(cmd)
    if r.returncode != 0:
        return None

    if out_path.exists() and ffprobe_ok(out_path):
        return out_path

    return None

# =========================
# 主流程
# =========================

def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    videos = data.get("videos", [])
    print(f"📦 讀取影片數量: {len(videos)}")

    manifest = []
    failed = []

    for v in tqdm(videos, desc="下載音訊"):
        video_id = v["video_id"]
        url = v["url"]

        audio_path = download_audio(url, video_id, OUTPUT_DIR)

        if audio_path:
            manifest.append({
                "video_id": video_id,
                "url": url,
                "audio_path": str(audio_path),
                "channel": v.get("channel"),
                "published_at": v.get("published_at"),
                "view_count": v.get("view_count"),
                "comment_count": v.get("comment_count"),
            })
        else:
            failed.append({
                "video_id": video_id,
                "url": url
            })

    # =========================
    # 輸出結果
    # =========================

    with open("manifest_audio.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    with open("failed_downloads.json", "w", encoding="utf-8") as f:
        json.dump(failed, f, ensure_ascii=False, indent=2)

    print("\n✅ 完成")
    print(f"成功音訊: {len(manifest)}")
    print(f"失敗影片: {len(failed)}")

if __name__ == "__main__":
    main()
