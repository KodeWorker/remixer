import os
import yt_dlp


def download(source: str, output_dir: str, quality: int | None = None) -> str:
    """Download video from a URL, or pass through a local file path.

    quality: max height in pixels (e.g. 720, 480, 360). None means best available.
    Returns the path to the video file.
    """
    if os.path.isfile(source):
        return source

    os.makedirs(output_dir, exist_ok=True)

    if quality:
        fmt = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"
    else:
        fmt = "bestvideo+bestaudio/best"

    ydl_opts = {
        "format": fmt,
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.splitext(filename)[0] + ".mp4"
