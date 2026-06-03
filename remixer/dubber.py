import asyncio
import io
import os
import subprocess
import tempfile
import httpx
import librosa
import numpy as np
from pydub import AudioSegment
from tqdm import tqdm

EDGE_TTS_DEFAULT_VOICE = "zh-TW-HsiaoChenNeural"


def _fish_speech_clip(text: str, host: str, format: str, reference_id: str | None) -> AudioSegment:
    payload = {"text": text, "format": format}
    if reference_id:
        payload["reference_id"] = reference_id
    response = httpx.post(f"{host}/v1/tts", json=payload, timeout=60)
    response.raise_for_status()
    return AudioSegment.from_file(io.BytesIO(response.content), format=format)


def _edge_tts_clip(text: str, voice: str) -> AudioSegment:
    import edge_tts

    async def _synthesize():
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name
        await edge_tts.Communicate(text, voice).save(tmp_path)
        return tmp_path

    tmp_path = asyncio.run(_synthesize())
    try:
        return AudioSegment.from_file(tmp_path, format="mp3")
    finally:
        os.unlink(tmp_path)


def _fit_clip(clip: AudioSegment, segment_duration_ms: float) -> AudioSegment:
    """Time-stretch clip to fit within segment duration using librosa (pitch-preserved)."""
    clip_ms = len(clip)
    if clip_ms <= segment_duration_ms:
        return clip

    rate = clip_ms / segment_duration_ms
    sr = clip.frame_rate
    dtype = np.int16

    samples = np.array(clip.get_array_of_samples(), dtype=np.float32)
    samples /= np.iinfo(dtype).max

    if clip.channels == 2:
        samples = samples.reshape(-1, 2).T
        stretched = np.stack([librosa.effects.time_stretch(ch, rate=rate) for ch in samples], axis=1).flatten()
    else:
        stretched = librosa.effects.time_stretch(samples, rate=rate)

    stretched = (stretched * np.iinfo(dtype).max).astype(dtype)
    return clip._spawn(stretched.tobytes(), overrides={"frame_rate": sr})


def dub(
    segments: list[dict],
    output_path: str,
    engine: str = "fish-speech",
    host: str = "http://127.0.0.1:8888",
    format: str = "mp3",
    reference_id: str | None = None,
    voice: str = EDGE_TTS_DEFAULT_VOICE,
    background_path: str | None = None,
) -> None:
    """Generate dubbed audio from translated segments.

    engine: 'fish-speech' (local server) or 'edge-tts' (Microsoft, no GPU needed).
    Each segment is placed at its original timestamp. Clips longer than their segment
    are time-stretched to fit (pitch-preserved). Gaps are filled with silence or
    background audio if background_path is provided.
    """
    if not segments:
        return

    if background_path:
        dubbed = AudioSegment.from_file(background_path)
    else:
        total_ms = int(segments[-1]["end"] * 1000)
        dubbed = AudioSegment.silent(duration=total_ms)

    for segment in tqdm(segments, desc="Dubbing", unit="seg"):
        text = segment.get("translation", segment["text"])
        start_ms = int(segment["start"] * 1000)
        segment_duration_ms = (segment["end"] - segment["start"]) * 1000

        if engine == "edge-tts":
            clip = _edge_tts_clip(text, voice)
        else:
            clip = _fish_speech_clip(text, host, format, reference_id)

        clip = _fit_clip(clip, segment_duration_ms)
        dubbed = dubbed.overlay(clip, position=start_ms)

    dubbed.export(output_path, format=format)


def merge(video_path: str, audio_path: str, output_path: str) -> None:
    """Merge dubbed audio into the original video, replacing the original audio track."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path,
        ],
        check=True,
        capture_output=True,
    )
