import whisper


def transcribe(audio_path: str, model_size: str = "medium") -> list[dict]:
    """Transcribe audio file using Whisper.

    Returns a list of segments: [{"start": float, "end": float, "text": str}, ...]
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return [
        {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
        for s in result["segments"]
    ]
