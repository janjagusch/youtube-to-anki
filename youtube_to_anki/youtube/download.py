"""
This module contains a function to retrieve the audio from a YouTube video.
"""


import cv2
from tempfile import TemporaryDirectory

from pydub import AudioSegment
from yt_dlp import YoutubeDL


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

def _download_video(url: str, filepath: str, resolution: int):
    """
    Downloads the best video <= the given resolution from a YouTube url into a file path.
    """
    ydl_opts = {
        "format": f"bestvideo[height<={resolution}]",
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

def retrieve_video(url: str, resolution: int) -> cv2.VideoCapture:
    """
    Downloads audio from YouTube URL and returns it as AudioSegment.
    """
    with TemporaryDirectory() as tempdir:
        path = f"{tempdir}/temp.mp4"
        _download_video(url, path, resolution)
        return cv2.VideoCapture(path)
