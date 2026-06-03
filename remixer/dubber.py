import io
import httpx
from pydub import AudioSegment


def dub(
    segments: list[dict],
    output_path: str,
    host: str = "http://127.0.0.1:8181",
    format: str = "mp3",
) -> None:
    """Generate dubbed audio from translated segments via Fish-Speech server.

    Each segment is placed at its original timestamp so the dub stays in sync
    with the source video. Gaps between segments are filled with silence.
    """
    if not segments:
        return

    total_ms = int(segments[-1]["end"] * 1000)
    dubbed = AudioSegment.silent(duration=total_ms)

    for segment in segments:
        text = segment.get("translation", segment["text"])
        start_ms = int(segment["start"] * 1000)

        response = httpx.post(
            f"{host}/v1/tts",
            json={"text": text, "format": format},
            timeout=60,
        )
        response.raise_for_status()

        clip = AudioSegment.from_file(io.BytesIO(response.content), format=format)
        dubbed = dubbed.overlay(clip, position=start_ms)

    dubbed.export(output_path, format=format)
