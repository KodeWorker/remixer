# Fish-Speech Setup

Fish-Speech is used for generating Chinese dubbed audio from translated text.

## Requirements

Fish-Speech recommends a GPU with at least **24 GB VRAM** for optimal performance. It can run on CPU but will be significantly slower.

## Install

```bash
git clone https://github.com/fishaudio/fish-speech
cd fish-speech
uv pip install -e .
```

## Download model weights

```bash
huggingface-cli download fishaudio/s2-pro --local-dir checkpoints/s2-pro
```

## Run the server

```bash
python tools/api_server.py --listen 0.0.0.0:8888
```

The server will be available at `http://127.0.0.1:8888`.

## Verify

```bash
curl http://127.0.0.1:8888/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，世界！",
    "format": "mp3"
  }' \
  --output test.mp3
```

## Note

For reference voice cloning, you can provide a short audio sample to match a specific speaker's voice — see the [Fish-Speech docs](https://speech.fish.audio) for details.
