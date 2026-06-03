import os
import yt_dlp


def download(source: str, output_dir: str) -> str:
    """Download audio from a URL, or pass through a local file path.

    Returns the path to the audio file.
    """
    if os.path.isfile(source):
        return source

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download=True)
        filename = ydl.prepare_filename(info)
        # postprocessor changes extension to mp3
        return os.path.splitext(filename)[0] + ".mp3"
