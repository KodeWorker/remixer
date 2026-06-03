# Remixer

AI-assisted tool that makes English video and audio content accessible to Chinese-speaking audiences — translating, summarizing, and dubbing so your family can enjoy it in their own language.

## What it does

Given any video or audio source, Remixer produces three outputs:

| Output | Audience | Purpose |
|--------|----------|---------|
| **Summary** | Parents / guardians | Quick overview to screen content before sharing |
| **Dubbed audio** | Listeners | Chinese narration so viewers can follow along naturally |
| **Subtitles** | Everyone | Full translated transcript (SRT/VTT) for detailed reading |

All three outputs are optional. Language simplification (rewriting for younger audiences) is also optional — the default preserves the original tone and style.

## Why

The internet is full of exceptional educational content, but most of it is in English. For Chinese-speaking families, the language barrier puts that content out of reach — especially for young children who can't yet read subtitles fast enough to keep up.

Remixer bridges that gap without stripping the content of its depth or character.

## Quickstart

```bash
# Install
uv pip install -r requirements.txt

# Run the full pipeline on a URL or local file
python main.py run https://www.youtube.com/watch?v=...
python main.py run path/to/video.mp4
```

After processing, outputs are saved to `./output`:

```
output/
├── transcript.json     # Raw transcript with timestamps
├── translated.json     # Translated transcript
├── summary.md          # Content summary
├── subtitles.srt       # Translated subtitles
├── subtitles.vtt       # Translated subtitles (WebVTT)
├── dubbed.mp3          # Chinese dubbed audio
└── dubbed.mp4          # Final dubbed video
```

## Running steps individually

Each step can be run on its own, which is useful for testing or reprocessing without redoing the full pipeline:

```bash
python main.py download   https://www.youtube.com/watch?v=...           # → output/video.mp4
python main.py transcribe output/video.mp4                              # → output/transcript.json
python main.py translate  output/transcript.json                        # → output/translated.json
python main.py summarize  output/transcript.json                        # → output/summary.md
python main.py subtitles  output/translated.json                                     # → output/subtitles.srt/.vtt
python main.py separate   output/video.mp4                                           # → output/htdemucs/.../no_vocals.wav
python main.py dub        output/translated.json --background path/to/no_vocals.wav  # → output/dubbed.mp3
python main.py merge      output/video.mp4 output/dubbed.mp3                         # → output/dubbed.mp4
```

## Options

All subcommands accept these shared flags:

| Flag | Description |
|------|-------------|
| `--output` | Output directory (default: `./output`) |
| `--lang` | Target language (default: `zh-TW`) |
| `--whisper-model` | Whisper model size: `tiny`, `base`, `small`, `medium`, `large` (default: `medium`) |
| `--llm-model` | Model name passed to the llama.cpp server (default: `qwen`) |
| `--quality` | Max video height in pixels, e.g. `720`, `480`, `360` (default: best available) |
| `--llm-host` | llama.cpp server URL (default: `http://127.0.0.1:8080`) |
| `--tts-host` | Fish-Speech server URL (default: `http://127.0.0.1:8888`) |
| `--voice` | Fish-Speech reference voice ID (default: server picks randomly) |

The `run` subcommand also accepts:

| Flag | Description |
|------|-------------|
| `--simplify` | Rewrite content for younger audiences |
| `--simplify-age` | Target age for simplification (default: `4`) |
| `--no-summary` | Skip summary |
| `--no-dub` | Skip dubbed audio |
| `--no-subtitles` | Skip subtitle generation |

## Tech stack

- **Transcription** — [Whisper](https://github.com/openai/whisper) · [setup guide](doc/whisper.md)
- **Translation & summarization** — [Qwen](https://huggingface.co/Qwen) via [llama.cpp](https://github.com/ggml-org/llama.cpp) · [setup guide](doc/llama-cpp.md); Claude API support planned
- **TTS (dubbing)** — [Fish-Speech](https://github.com/fishaudio/fish-speech) · [setup guide](doc/fish-speech.md) or [Edge-TTS](https://github.com/rany2/edge-tts) (no GPU)
- **Source separation** — [Demucs](https://github.com/facebookresearch/demucs) (background audio extraction)
- **Video download** — [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Roadmap

- [ ] Child-friendly language simplification
- [ ] Claude API support for translation & summarization
- [ ] Web UI for non-technical family members
- [x] Dubbing: mix original background audio (music, ambience) under dubbed clips using Demucs source separation
- [x] Dubbing: time-stretch TTS clips to fit segment duration (pitch-preserved via librosa) to prevent overlap

## License

[The "For My Family" License](LICENSE)
