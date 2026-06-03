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
pip install -r requirements.txt

# Run on any video URL
python remixer.py https://www.youtube.com/watch?v=...

# Or a local file
python remixer.py path/to/video.mp4
```

## Outputs

After processing, you'll find the following in the output directory:

```
output/
├── summary.md          # Content summary
├── dubbed.mp3          # Chinese dubbed audio
└── subtitles.srt       # Full translated subtitles
```

## Options

| Flag | Description |
|------|-------------|
| `--lang` | Target language (default: `zh`) |
| `--simplify` | Rewrite content for younger audiences |
| `--simplify-age` | Target age for simplification (default: `4`) |
| `--no-summary` | Skip summary |
| `--no-dub` | Skip dubbed audio |
| `--no-subtitles` | Skip subtitle generation |
| `--output` | Output directory (default: `./output`) |

## Tech stack

- **Transcription** — [Whisper](https://github.com/openai/whisper)
- **Translation & summarization** — [Qwen](https://huggingface.co/Qwen) via [llama.cpp](https://github.com/ggml-org/llama.cpp); Claude API support planned
- **TTS (dubbing)** — [Fish-Speech](https://github.com/fishaudio/fish-speech)
- **Video download** — [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Roadmap

- [ ] Core pipeline: transcribe → translate → summarize
- [ ] Dubbed audio generation
- [ ] Subtitle export (SRT + VTT)
- [ ] Child-friendly language simplification
- [ ] Claude API support for translation & summarization
- [ ] Web UI for non-technical family members

## License

[The "For My Family" License](LICENSE)
