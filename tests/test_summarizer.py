import pytest
import httpx
from unittest.mock import patch, MagicMock
from remixer.summarizer import summarize


SEGMENTS = [
    {"start": 0.0, "end": 3.5, "text": "Black holes are regions of spacetime."},
    {"start": 3.5, "end": 7.0, "text": "Nothing can escape their gravity."},
]


def _mock_response(text):
    mock = MagicMock()
    mock.json.return_value = {"choices": [{"message": {"content": text}}]}
    mock.raise_for_status = MagicMock()
    return mock


def test_returns_string():
    with patch("remixer.summarizer.httpx.post", return_value=_mock_response("黑洞摘要")):
        result = summarize(SEGMENTS)
    assert isinstance(result, str)
    assert result == "黑洞摘要"


def test_calls_api_once():
    with patch("remixer.summarizer.httpx.post", return_value=_mock_response("摘要")) as mock_post:
        summarize(SEGMENTS)
    assert mock_post.call_count == 1


def test_full_transcript_sent():
    with patch("remixer.summarizer.httpx.post", return_value=_mock_response("摘要")) as mock_post:
        summarize(SEGMENTS)
    body = mock_post.call_args.kwargs["json"]
    user_message = next(m["content"] for m in body["messages"] if m["role"] == "user")
    assert "Black holes are regions of spacetime." in user_message
    assert "Nothing can escape their gravity." in user_message


def test_raises_on_http_error():
    mock = MagicMock()
    mock.raise_for_status.side_effect = httpx.HTTPStatusError(
        "error", request=MagicMock(), response=MagicMock()
    )
    with patch("remixer.summarizer.httpx.post", return_value=mock):
        with pytest.raises(httpx.HTTPStatusError):
            summarize(SEGMENTS)
