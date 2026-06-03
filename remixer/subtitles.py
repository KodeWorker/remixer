import os


def _format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def export_srt(segments: list[dict], output_path: str) -> None:
    """Export translated segments as an SRT subtitle file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = _format_timestamp(segment["start"])
            end = _format_timestamp(segment["end"])
            text = segment.get("translation", segment["text"])
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def export_vtt(segments: list[dict], output_path: str) -> None:
    """Export translated segments as a WebVTT subtitle file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, segment in enumerate(segments, start=1):
            start = _format_timestamp(segment["start"]).replace(",", ".")
            end = _format_timestamp(segment["end"]).replace(",", ".")
            text = segment.get("translation", segment["text"])
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
