import io
import os
import subprocess
import httpx
from pydub import AudioSegment


def dub(
    segments: list[dict],
    output_path: str,
    host: str = "http://127.0.0.1:8888",
    format: str = "mp3",
    reference_id: str | None = None,
) -> None:
    """Generate dubbed audio from translated segments via Fish-Speech server.

    Each segment is placed at its original timestamp so the dub stays in sync
    with the source video. Gaps between segments are filled with silence.
    reference_id: a pre-registered Fish-Speech voice ID. None lets the server pick randomly.
    """
    if not segments:
        return

    total_ms = int(segments[-1]["end"] * 1000)
    dubbed = AudioSegment.silent(duration=total_ms)

    for segment in segments:
        text = segment.get("translation", segment["text"])
        start_ms = int(segment["start"] * 1000)

        payload = {"text": text, "format": format}
        if reference_id:
            payload["reference_id"] = reference_id

        response = httpx.post(
            f"{host}/v1/tts",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

        clip = AudioSegment.from_file(io.BytesIO(response.content), format=format)
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
