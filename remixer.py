import argparse
import os

from remixer.downloader import download
from remixer.transcriber import transcribe
from remixer.translator import translate
from remixer.summarizer import summarize
from remixer.subtitles import export_srt, export_vtt
from remixer.dubber import dub


def parse_args():
    parser = argparse.ArgumentParser(
        description="Remix English video content for Chinese-speaking audiences."
    )
    parser.add_argument("source", help="Video URL or local file path")
    parser.add_argument("--lang", default="zh-TW", help="Target language (default: zh-TW)")
    parser.add_argument("--whisper-model", default="medium", help="Whisper model size (default: medium)")
    parser.add_argument("--llm-host", default="http://127.0.0.1:8080", help="llama.cpp server URL")
    parser.add_argument("--tts-host", default="http://127.0.0.1:8888", help="Fish-Speech server URL")
    parser.add_argument("--output", default="./output", help="Output directory (default: ./output)")
    parser.add_argument("--simplify", action="store_true", help="Rewrite content for younger audiences")
    parser.add_argument("--simplify-age", type=int, default=4, help="Target age for simplification (default: 4)")
    parser.add_argument("--no-summary", action="store_true", help="Skip summary")
    parser.add_argument("--no-subtitles", action="store_true", help="Skip subtitle generation")
    parser.add_argument("--no-dub", action="store_true", help="Skip dubbed audio")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)

    print(f"[1/4] Downloading: {args.source}")
    audio_path = download(args.source, args.output)

    print(f"[2/4] Transcribing: {audio_path}")
    segments = transcribe(audio_path, model_size=args.whisper_model)

    print(f"[3/4] Translating {len(segments)} segments → {args.lang}")
    segments = translate(segments, target_lang=args.lang, host=args.llm_host)

    print("[4/4] Generating outputs")

    if not args.no_summary:
        print("  · summary")
        summary = summarize(segments, target_lang=args.lang, host=args.llm_host)
        with open(os.path.join(args.output, "summary.md"), "w", encoding="utf-8") as f:
            f.write(summary)

    if not args.no_subtitles:
        print("  · subtitles")
        export_srt(segments, os.path.join(args.output, "subtitles.srt"))
        export_vtt(segments, os.path.join(args.output, "subtitles.vtt"))

    if not args.no_dub:
        print("  · dubbed audio")
        dub(segments, os.path.join(args.output, "dubbed.mp3"), host=args.tts_host)

    print(f"\nDone. Outputs saved to: {args.output}")


if __name__ == "__main__":
    main()
