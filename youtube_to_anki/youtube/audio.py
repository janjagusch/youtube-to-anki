from tempfile import TemporaryDirectory

from pydub import AudioSegment
from youtube_dl import YoutubeDL


def _download_audio(url: str, filepath: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": filepath,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def retrieve_audio(url: str) -> AudioSegment:
    with TemporaryDirectory() as tempdir:
        _download_audio(url, f"{tempdir}/temp.%(ext)s")
        return AudioSegment.from_mp3(f"{tempdir}/temp.mp3")
