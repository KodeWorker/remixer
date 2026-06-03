import argparse
import json
import os

from remixer.downloader import download
from remixer.transcriber import transcribe
from remixer.translator import translate
from remixer.summarizer import summarize
from remixer.subtitles import export_srt, export_vtt
from remixer.dubber import dub, merge


def cmd_download(args):
    os.makedirs(args.output, exist_ok=True)
    video_path = download(args.source, args.output, quality=args.quality)
    print(f"Video saved: {video_path}")


def cmd_transcribe(args):
    os.makedirs(args.output, exist_ok=True)
    segments = transcribe(args.audio, model_size=args.whisper_model)
    out = os.path.join(args.output, "transcript.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    print(f"Transcript saved: {out} ({len(segments)} segments)")


def cmd_translate(args):
    os.makedirs(args.output, exist_ok=True)
    with open(args.transcript, encoding="utf-8") as f:
        segments = json.load(f)
    segments = translate(segments, target_lang=args.lang, host=args.llm_host, model=args.llm_model)
    out = os.path.join(args.output, "translated.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    print(f"Translation saved: {out}")


def cmd_summarize(args):
    os.makedirs(args.output, exist_ok=True)
    with open(args.transcript, encoding="utf-8") as f:
        segments = json.load(f)
    summary = summarize(segments, target_lang=args.lang, host=args.llm_host, model=args.llm_model)
    out = os.path.join(args.output, "summary.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary saved: {out}")


def cmd_subtitles(args):
    os.makedirs(args.output, exist_ok=True)
    with open(args.translated, encoding="utf-8") as f:
        segments = json.load(f)
    export_srt(segments, os.path.join(args.output, "subtitles.srt"))
    export_vtt(segments, os.path.join(args.output, "subtitles.vtt"))
    print(f"Subtitles saved: {args.output}/subtitles.srt and .vtt")


def cmd_dub(args):
    os.makedirs(args.output, exist_ok=True)
    with open(args.translated, encoding="utf-8") as f:
        segments = json.load(f)
    audio_out = os.path.join(args.output, "dubbed.mp3")
    dub(segments, audio_out, host=args.tts_host, reference_id=args.voice)
    if args.video:
        video_out = os.path.join(args.output, "dubbed.mp4")
        merge(args.video, audio_out, video_out)
        print(f"Dubbed video saved: {video_out}")
    else:
        print(f"Dubbed audio saved: {audio_out}")


def cmd_run(args):
    os.makedirs(args.output, exist_ok=True)

    print(f"[1/4] Downloading: {args.source}")
    video_path = download(args.source, args.output, quality=args.quality)

    print(f"[2/4] Transcribing: {video_path}")
    segments = transcribe(video_path, model_size=args.whisper_model)

    print(f"[3/4] Translating {len(segments)} segments → {args.lang}")
    segments = translate(segments, target_lang=args.lang, host=args.llm_host, model=args.llm_model)

    print("[4/4] Generating outputs")

    if not args.no_summary:
        print("  · summary")
        summary = summarize(segments, target_lang=args.lang, host=args.llm_host, model=args.llm_model)
        with open(os.path.join(args.output, "summary.md"), "w", encoding="utf-8") as f:
            f.write(summary)

    if not args.no_subtitles:
        print("  · subtitles")
        export_srt(segments, os.path.join(args.output, "subtitles.srt"))
        export_vtt(segments, os.path.join(args.output, "subtitles.vtt"))

    if not args.no_dub:
        print("  · dubbed audio")
        audio_out = os.path.join(args.output, "dubbed.mp3")
        dub(segments, audio_out, host=args.tts_host, reference_id=args.voice)
        print("  · merging video")
        merge(video_path, audio_out, os.path.join(args.output, "dubbed.mp4"))

    print(f"\nDone. Outputs saved to: {args.output}")


def main():
    parser = argparse.ArgumentParser(
        description="Remix English video content for Chinese-speaking audiences."
    )
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--output", default="./output", help="Output directory (default: ./output)")
    shared.add_argument("--lang", default="zh-TW", help="Target language (default: zh-TW)")
    shared.add_argument("--llm-host", default="http://127.0.0.1:8080", help="llama.cpp server URL")
    shared.add_argument("--tts-host", default="http://127.0.0.1:8888", help="Fish-Speech server URL")
    shared.add_argument("--voice", default=None, help="Fish-Speech reference voice ID (default: server picks randomly)")
    shared.add_argument("--whisper-model", default="medium", help="Whisper model size: tiny, base, small, medium, large (default: medium)")
    shared.add_argument("--llm-model", default="qwen", help="Model name to pass to the llama.cpp server (default: qwen)")
    shared.add_argument("--quality", type=int, default=None, metavar="HEIGHT", help="Max video height in pixels, e.g. 720, 480, 360 (default: best available)")

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("download", parents=[shared], help="Download audio from a URL")
    p.add_argument("source", help="Video URL")

    p = sub.add_parser("transcribe", parents=[shared], help="Transcribe audio or video to transcript.json")
    p.add_argument("audio", help="Path to audio or video file")

    p = sub.add_parser("translate", parents=[shared], help="Translate transcript.json → translated.json")
    p.add_argument("transcript", help="Path to transcript.json")

    p = sub.add_parser("summarize", parents=[shared], help="Summarize transcript.json → summary.md")
    p.add_argument("transcript", help="Path to transcript.json")

    p = sub.add_parser("subtitles", parents=[shared], help="Export translated.json → subtitles.srt/.vtt")
    p.add_argument("translated", help="Path to translated.json")

    p = sub.add_parser("dub", parents=[shared], help="Generate dubbed video (or audio) from translated.json")
    p.add_argument("translated", help="Path to translated.json")
    p.add_argument("--video", default=None, help="Original video to merge dubbed audio into (produces dubbed.mp4)")

    p = sub.add_parser("run", parents=[shared], help="Run the full pipeline")
    p.add_argument("source", help="Video URL or local file path")
    p.add_argument("--simplify", action="store_true", help="Rewrite content for younger audiences")
    p.add_argument("--simplify-age", type=int, default=4, help="Target age for simplification (default: 4)")
    p.add_argument("--no-summary", action="store_true", help="Skip summary")
    p.add_argument("--no-subtitles", action="store_true", help="Skip subtitle generation")
    p.add_argument("--no-dub", action="store_true", help="Skip dubbed audio")

    args = parser.parse_args()
    {
        "download":   cmd_download,
        "transcribe": cmd_transcribe,
        "translate":  cmd_translate,
        "summarize":  cmd_summarize,
        "subtitles":  cmd_subtitles,
        "dub":        cmd_dub,
        "run":        cmd_run,
    }[args.command](args)


if __name__ == "__main__":
    main()
