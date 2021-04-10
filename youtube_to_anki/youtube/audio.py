"""
This module contains a function to retrieve the audio from a YouTube video.
"""


from tempfile import TemporaryDirectory

from pydub import AudioSegment
from youtube_dl import YoutubeDL


def _download_audio(url: str, filepath: str):
    """
    Downloads the audio from a YouTube url into a file path.
    """
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
    """
    Downloads audio from YouTube URL and returns it as AudioSegment.
    """
    with TemporaryDirectory() as tempdir:
        _download_audio(url, f"{tempdir}/temp.%(ext)s")
        return AudioSegment.from_mp3(f"{tempdir}/temp.mp3")
