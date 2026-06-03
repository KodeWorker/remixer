# llama.cpp Setup

llama.cpp runs Qwen locally and exposes an OpenAI-compatible HTTP server that Remixer uses for translation and summarization.

## Install

### Option A — Pre-built binaries (recommended)

Download the latest release for your platform from https://github.com/ggml-org/llama.cpp/releases and extract it.

### Option B — Build from source

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

## Download a Qwen model

Remixer uses Qwen for Chinese translation. Download a GGUF quantized model from Hugging Face:

```bash
# Example: Qwen3-8B at Q4 quantization (good balance of quality and speed)
huggingface-cli download Qwen/Qwen3-8B-GGUF qwen3-8b-q4_k_m.gguf --local-dir ./models
```

Larger models produce better translations. Recommended minimums:

| Model | VRAM / RAM | Quality |
|-------|-----------|---------|
| Qwen3-4B Q4 | ~3 GB | decent |
| Qwen3-8B Q4 | ~5 GB | good |
| Qwen3-14B Q4 | ~9 GB | great |

## Run the server

```bash
llama-server \
  --model ./models/qwen3-8b-q4_k_m.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 8192
```

The server exposes an OpenAI-compatible API at `http://127.0.0.1:8080`.

## Verify

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen",
    "messages": [{"role": "user", "content": "Translate to Chinese: Hello, world!"}]
  }'
```
