# Fish-Speech Setup

Fish-Speech is used for generating Chinese dubbed audio from translated text.

## Install

```bash
git clone https://github.com/fishaudio/fish-speech
cd fish-speech
uv pip install -e .
```

## Download model weights

```bash
huggingface-cli download fishaudio/fish-speech-1.5 --local-dir ./checkpoints/fish-speech-1.5
```

## Run the server

```bash
python -m tools.api_server \
  --listen 127.0.0.1:8181 \
  --llama-checkpoint-path ./checkpoints/fish-speech-1.5 \
  --decoder-checkpoint-path ./checkpoints/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth
```

The server will be available at `http://127.0.0.1:8181`.

## Verify

```bash
curl http://127.0.0.1:8181/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，世界！",
    "format": "mp3"
  }' \
  --output test.mp3
```

## Note

Fish-Speech runs best on a CUDA GPU but also works on CPU (slower). For reference voice cloning, you can provide a short audio sample to match a specific speaker's voice — see the [Fish-Speech docs](https://speech.fish.audio) for details.
