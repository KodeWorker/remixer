# Whisper Setup

Whisper is used for transcribing audio to text.

## Install

```bash
uv pip install openai-whisper
```

Whisper also requires `ffmpeg` on your system:

- **Windows**: `winget install ffmpeg` or download from https://ffmpeg.org/download.html
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Models

Whisper comes in several sizes. For most videos, `medium` or `large` gives the best accuracy:

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | 75 MB | fastest | lowest |
| `base` | 145 MB | fast | low |
| `small` | 466 MB | moderate | moderate |
| `medium` | 1.5 GB | slow | good |
| `large` | 2.9 GB | slowest | best |

Models are downloaded automatically on first use.

## Verify

```python
import whisper
model = whisper.load_model("medium")
result = model.transcribe("audio.mp3")
print(result["text"])
```

## Note

For faster inference on CPU, consider [faster-whisper](https://github.com/SYSTRAN/faster-whisper) as a drop-in alternative — same models, significantly faster.
