import io
from unittest.mock import patch, MagicMock, call
from remixer.dubber import dub


SEGMENTS = [
    {"start": 0.0, "end": 3.5, "text": "Hello", "translation": "哈囉"},
    {"start": 3.5, "end": 7.0, "text": "World", "translation": "世界"},
]


def _mock_tts_response(content=b"fakeaudio"):
    mock = MagicMock()
    mock.content = content
    mock.raise_for_status = MagicMock()
    return mock


def _make_mock_audio_segment():
    mock_segment = MagicMock()
    mock_segment.overlay.return_value = mock_segment
    return mock_segment


def test_calls_tts_per_segment(tmp_path):
    mock_audio = _make_mock_audio_segment()
    responses = [_mock_tts_response(), _mock_tts_response()]

    with patch("remixer.dubber.httpx.post", side_effect=responses) as mock_post, \
         patch("remixer.dubber.AudioSegment.silent", return_value=mock_audio), \
         patch("remixer.dubber.AudioSegment.from_file", return_value=mock_audio):
        dub(SEGMENTS, str(tmp_path / "dubbed.mp3"))

    assert mock_post.call_count == 2


def test_uses_translation_text(tmp_path):
    mock_audio = _make_mock_audio_segment()
    responses = [_mock_tts_response(), _mock_tts_response()]

    with patch("remixer.dubber.httpx.post", side_effect=responses) as mock_post, \
         patch("remixer.dubber.AudioSegment.silent", return_value=mock_audio), \
         patch("remixer.dubber.AudioSegment.from_file", return_value=mock_audio):
        dub(SEGMENTS, str(tmp_path / "dubbed.mp3"))

    texts = [c.kwargs["json"]["text"] for c in mock_post.call_args_list]
    assert texts == ["哈囉", "世界"]


def test_fallback_to_original_text(tmp_path):
    segments = [{"start": 0.0, "end": 3.5, "text": "Hello"}]
    mock_audio = _make_mock_audio_segment()

    with patch("remixer.dubber.httpx.post", return_value=_mock_tts_response()) as mock_post, \
         patch("remixer.dubber.AudioSegment.silent", return_value=mock_audio), \
         patch("remixer.dubber.AudioSegment.from_file", return_value=mock_audio):
        dub(segments, str(tmp_path / "dubbed.mp3"))

    text = mock_post.call_args.kwargs["json"]["text"]
    assert text == "Hello"


def test_overlay_at_correct_position(tmp_path):
    mock_audio = _make_mock_audio_segment()
    responses = [_mock_tts_response(), _mock_tts_response()]

    with patch("remixer.dubber.httpx.post", side_effect=responses), \
         patch("remixer.dubber.AudioSegment.silent", return_value=mock_audio), \
         patch("remixer.dubber.AudioSegment.from_file", return_value=mock_audio):
        dub(SEGMENTS, str(tmp_path / "dubbed.mp3"))

    positions = [c.kwargs["position"] for c in mock_audio.overlay.call_args_list]
    assert positions == [0, 3500]


def test_empty_segments_does_nothing(tmp_path):
    output = str(tmp_path / "dubbed.mp3")
    with patch("remixer.dubber.httpx.post") as mock_post:
        dub([], output)
    mock_post.assert_not_called()
    assert not (tmp_path / "dubbed.mp3").exists()
