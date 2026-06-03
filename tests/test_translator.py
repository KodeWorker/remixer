import pytest
import httpx
from unittest.mock import patch, MagicMock
from remixer.translator import translate


SEGMENTS = [
    {"start": 0.0, "end": 3.5, "text": "Hello world"},
    {"start": 3.5, "end": 7.0, "text": "How are you"},
]


def _mock_response(text):
    mock = MagicMock()
    mock.json.return_value = {"choices": [{"message": {"content": text}}]}
    mock.raise_for_status = MagicMock()
    return mock


def test_adds_translation_field():
    responses = [_mock_response("你好世界"), _mock_response("你好嗎")]
    with patch("remixer.translator.httpx.post", side_effect=responses):
        result = translate(SEGMENTS)
    assert result[0]["translation"] == "你好世界"
    assert result[1]["translation"] == "你好嗎"


def test_preserves_original_fields():
    responses = [_mock_response("你好世界"), _mock_response("你好吗")]
    with patch("remixer.translator.httpx.post", side_effect=responses):
        result = translate(SEGMENTS)
    assert result[0]["start"] == 0.0
    assert result[0]["end"] == 3.5
    assert result[0]["text"] == "Hello world"


def test_calls_api_once_per_segment():
    responses = [_mock_response("你好世界"), _mock_response("你好嗎")]
    with patch("remixer.translator.httpx.post", side_effect=responses) as mock_post:
        translate(SEGMENTS)
    assert mock_post.call_count == 2


def test_raises_on_http_error():
    mock = MagicMock()
    mock.raise_for_status.side_effect = httpx.HTTPStatusError(
        "error", request=MagicMock(), response=MagicMock()
    )
    with patch("remixer.translator.httpx.post", return_value=mock):
        with pytest.raises(httpx.HTTPStatusError):
            translate(SEGMENTS)
