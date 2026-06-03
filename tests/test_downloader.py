import os
from unittest.mock import patch, MagicMock
from remixer.downloader import download


def test_local_file_passthrough(tmp_path):
    f = tmp_path / "audio.mp3"
    f.write_bytes(b"fake audio")
    result = download(str(f), str(tmp_path))
    assert result == str(f)


def test_url_download(tmp_path):
    fake_info = {"title": "test video", "ext": "webm"}

    mock_ydl = MagicMock()
    mock_ydl.extract_info.return_value = fake_info
    mock_ydl.prepare_filename.return_value = str(tmp_path / "test video.webm")
    mock_ydl.__enter__ = lambda s: mock_ydl
    mock_ydl.__exit__ = MagicMock(return_value=False)

    with patch("remixer.downloader.yt_dlp.YoutubeDL", return_value=mock_ydl):
        result = download("https://youtube.com/watch?v=test", str(tmp_path))

    assert result == str(tmp_path / "test video.mp3")


def test_url_download_creates_output_dir(tmp_path):
    output_dir = str(tmp_path / "new_dir")
    fake_info = {"title": "test", "ext": "webm"}

    mock_ydl = MagicMock()
    mock_ydl.extract_info.return_value = fake_info
    mock_ydl.prepare_filename.return_value = os.path.join(output_dir, "test.webm")
    mock_ydl.__enter__ = lambda s: mock_ydl
    mock_ydl.__exit__ = MagicMock(return_value=False)

    with patch("remixer.downloader.yt_dlp.YoutubeDL", return_value=mock_ydl):
        download("https://youtube.com/watch?v=test", output_dir)

    assert os.path.isdir(output_dir)
