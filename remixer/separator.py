import os
import subprocess
import sys
from pathlib import Path


def separate(source_path: str, output_dir: str, model: str = "htdemucs") -> str:
    """Separate background audio (no vocals) from a video or audio file using Demucs.

    Returns the path to the no_vocals stem (WAV).
    """
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(
        [
            sys.executable, "-m", "demucs",
            "--two-stems", "vocals",
            "-n", model,
            "-o", output_dir,
            source_path,
        ],
        check=True,
    )
    stem_name = Path(source_path).stem
    background = Path(output_dir) / model / stem_name / "no_vocals.wav"
    return str(background)
