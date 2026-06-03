import os
from remixer.subtitles import export_srt, export_vtt


SEGMENTS = [
    {"start": 0.0,    "end": 3.5,   "text": "Hello world",    "translation": "你好世界"},
    {"start": 3.5,    "end": 7.0,   "text": "How are you",    "translation": "你好嗎"},
    {"start": 3661.0, "end": 3665.0,"text": "One hour mark",  "translation": "一小時"},
]

SEGMENTS_NO_TRANSLATION = [
    {"start": 0.0, "end": 3.5, "text": "Hello world"},
]


class TestExportSrt:
    def test_creates_file(self, tmp_path):
        path = str(tmp_path / "subtitles.srt")
        export_srt(SEGMENTS, path)
        assert os.path.isfile(path)

    def test_sequence_numbers(self, tmp_path):
        path = str(tmp_path / "subtitles.srt")
        export_srt(SEGMENTS, path)
        content = open(path, encoding="utf-8").read()
        assert content.startswith("1\n")
        assert "\n2\n" in content
        assert "\n3\n" in content

    def test_srt_timestamp_format(self, tmp_path):
        path = str(tmp_path / "subtitles.srt")
        export_srt(SEGMENTS, path)
        content = open(path, encoding="utf-8").read()
        assert "00:00:00,000 --> 00:00:03,500" in content

    def test_one_hour_timestamp(self, tmp_path):
        path = str(tmp_path / "subtitles.srt")
        export_srt(SEGMENTS, path)
        content = open(path, encoding="utf-8").read()
        assert "01:01:01,000 --> 01:01:05,000" in content

    def test_uses_translation(self, tmp_path):
        path = str(tmp_path / "subtitles.srt")
        export_srt(SEGMENTS, path)
        content = open(path, encoding="utf-8").read()
        assert "你好世界" in content
        assert "Hello world" not in content

    def test_fallback_to_original_text(self, tmp_path):
        path = str(tmp_path / "subtitles.srt")
        export_srt(SEGMENTS_NO_TRANSLATION, path)
        content = open(path, encoding="utf-8").read()
        assert "Hello world" in content


class TestExportVtt:
    def test_creates_file(self, tmp_path):
        path = str(tmp_path / "subtitles.vtt")
        export_vtt(SEGMENTS, path)
        assert os.path.isfile(path)

    def test_webvtt_header(self, tmp_path):
        path = str(tmp_path / "subtitles.vtt")
        export_vtt(SEGMENTS, path)
        content = open(path, encoding="utf-8").read()
        assert content.startswith("WEBVTT\n")

    def test_vtt_uses_dot_separator(self, tmp_path):
        path = str(tmp_path / "subtitles.vtt")
        export_vtt(SEGMENTS, path)
        content = open(path, encoding="utf-8").read()
        assert "00:00:00.000 --> 00:00:03.500" in content
        assert "," not in content.split("WEBVTT")[1]

    def test_uses_translation(self, tmp_path):
        path = str(tmp_path / "subtitles.vtt")
        export_vtt(SEGMENTS, path)
        content = open(path, encoding="utf-8").read()
        assert "你好世界" in content
