# 使用說明 (Usage Guide)

## 問題已修復 (Issues Fixed)

### 修復的問題 (Fixed Issues)
1. ✅ `transcribe_fw.py` 現在會檢查 `audio/` 目錄是否存在
2. ✅ 當沒有音頻文件時會顯示友好的警告訊息
3. ✅ GitHub Actions 工作流程現在正確安裝 ffmpeg
4. ✅ 上傳步驟只在有轉錄結果時執行

### 如何使用 (How to Use)

#### 本地測試 (Local Testing)

1. 安裝依賴 (Install dependencies):
```bash
pip install faster-whisper ffmpeg-python
```

2. 創建 audio 目錄並添加 MP3 文件 (Create audio directory and add MP3 files):
```bash
mkdir audio
# 將你的 MP3 文件放入 audio 目錄
# Put your MP3 files in the audio directory
```

3. 運行轉錄腳本 (Run transcription script):
```bash
python transcribe_fw.py
```

4. 檢查 transcripts 目錄中的結果 (Check results in transcripts directory):
```bash
ls transcripts/
```

#### GitHub Actions 使用 (Using GitHub Actions)

1. 在存儲庫中創建 `audio` 目錄並提交音頻文件
2. 前往 GitHub 存儲庫的 "Actions" 標籤
3. 選擇 "Faster-Whisper Transcription" 工作流程
4. 點擊 "Run workflow" 按鈕
5. 工作流程完成後，從 Artifacts 下載轉錄結果

#### 重要提示 (Important Notes)

- 腳本支持 MP3 格式的音頻文件
- 使用 medium 模型進行中文轉錄
- 轉錄結果會保存在 `transcripts/` 目錄中
- 已轉錄的文件會被跳過（檢查 .txt 文件是否存在）

### 配置選項 (Configuration Options)

在 `transcribe_fw.py` 中可以調整以下設置：

```python
MODEL_SIZE = "medium"   # 可選: tiny, base, small, medium, large-v3
DEVICE = "cpu"          # CPU 或 cuda (需要 GPU)
COMPUTE_TYPE = "int8"   # int8 適合 CPU, float16 適合 GPU
```

### 故障排除 (Troubleshooting)

**問題: "No MP3 files found"**
- 確保 `audio/` 目錄中有 MP3 文件

**問題: FFmpeg 錯誤**
- 確保已安裝 ffmpeg: `sudo apt-get install ffmpeg`

**問題: 內存不足**
- 嘗試使用較小的模型，如 "small" 或 "base"
