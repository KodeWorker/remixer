from unittest.mock import patch, MagicMock
from remixer.transcriber import transcribe


FAKE_SEGMENTS = [
    {"start": 0.0, "end": 3.5, "text": "  Hello world  "},
    {"start": 3.5, "end": 7.0, "text": "  How are you  "},
]


def _mock_whisper(segments):
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"segments": segments}
    return mock_model


def test_returns_segments():
    with patch("remixer.transcriber.whisper.load_model", return_value=_mock_whisper(FAKE_SEGMENTS)):
        result = transcribe("audio.mp3")
    assert len(result) == 2


def test_segment_fields():
    with patch("remixer.transcriber.whisper.load_model", return_value=_mock_whisper(FAKE_SEGMENTS)):
        result = transcribe("audio.mp3")
    for seg in result:
        assert "start" in seg
        assert "end" in seg
        assert "text" in seg


def test_text_is_stripped():
    with patch("remixer.transcriber.whisper.load_model", return_value=_mock_whisper(FAKE_SEGMENTS)):
        result = transcribe("audio.mp3")
    assert result[0]["text"] == "Hello world"
    assert result[1]["text"] == "How are you"


def test_timestamps_preserved():
    with patch("remixer.transcriber.whisper.load_model", return_value=_mock_whisper(FAKE_SEGMENTS)):
        result = transcribe("audio.mp3")
    assert result[0]["start"] == 0.0
    assert result[0]["end"] == 3.5


def test_model_size_passed():
    mock_load = MagicMock(return_value=_mock_whisper(FAKE_SEGMENTS))
    with patch("remixer.transcriber.whisper.load_model", mock_load):
        transcribe("audio.mp3", model_size="large")
    mock_load.assert_called_once_with("large")
