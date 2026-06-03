"""Launch the Fish-Speech API server from anywhere.

Usage:
    uv run scripts/start_fish_speech.py --dir /path/to/fish-speech
    uv run scripts/start_fish_speech.py --dir /path/to/fish-speech --checkpoint /path/to/checkpoints/s2-pro
    uv run scripts/start_fish_speech.py --dir /path/to/fish-speech --listen 127.0.0.1:8888
"""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Start the Fish-Speech API server.",
        # pass unrecognised flags straight through to api_server.py
        add_help=False,
    )
    parser.add_argument("--dir", required=True, help="Path to the fish-speech cloned directory")
    parser.add_argument("--listen", default="0.0.0.0:8888", help="Host and port to listen on (default: 0.0.0.0:8888)")
    parser.add_argument("--checkpoint", default=None, help="Path to the model checkpoint directory (e.g. /path/to/checkpoints/s2-pro)")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    args, extra = parser.parse_known_args()

    fish_speech_dir = Path(args.dir).resolve()
    server_script = fish_speech_dir / "tools" / "api_server.py"

    if not fish_speech_dir.exists():
        print(f"Error: directory not found: {fish_speech_dir}")
        sys.exit(1)

    if not server_script.exists():
        print(f"Error: api_server.py not found at {server_script}")
        sys.exit(1)

    cmd = [sys.executable, str(server_script), "--listen", args.listen]

    if args.checkpoint:
        checkpoint = Path(args.checkpoint).resolve()
        cmd += ["--llama-checkpoint-path", str(checkpoint)]
        cmd += ["--decoder-checkpoint-path", str(checkpoint / "codec.pth")]

    cmd += extra

    subprocess.run(cmd, cwd=fish_speech_dir)


if __name__ == "__main__":
    main()
