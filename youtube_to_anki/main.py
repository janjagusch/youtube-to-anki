"""
This module contains the main function for converting YouTube videos to Anki decks.
"""

from typing import Dict, Iterable

import click
import cv2
from pydub import AudioSegment

from youtube_to_anki.anki import make_package as _make_package
from youtube_to_anki.utils import process_audio_chunk, take_screenshots, process_transcript_chunk
from youtube_to_anki.youtube import retrieve_audio, retrieve_video, retrieve_info, retrieve_transcript


def make_package(
        transcript: Iterable[Dict], audio: AudioSegment, video: cv2.VideoCapture, deck_name: str, filepath: str
):
    """
    Creates an Anki package from audio and transcript.
    """
    transcript_chunks = tuple(process_transcript_chunk(chunk) for chunk in transcript)
    screenshots = take_screenshots(video, transcript_chunks) if video is not None else [-1] * len(transcript_chunks)
    audio_chunks = tuple(
        process_audio_chunk(audio, chunk) for chunk in transcript_chunks
    )
    _make_package(audio_chunks, screenshots, transcript_chunks, deck_name, hash(deck_name), filepath)


# pylint: disable=no-value-for-parameter
@click.command()
@click.option(
    "--out",
    default=None,
    help="Where to export the deck. Defaults to '<deck_name>.apgk'.",
)
@click.option(
    "--screenshot-resolution",
    default=-1,
    help="Experimental. Adds screenshots with the specified resolution in pixel height, e.g. 360. Defaults to no screenshots being taken.",
)
@click.option(
    "--transcript-language",
    default="en",
    help="Which transcript language to use. Defaults to 'en'.",
)
@click.argument("video-id")
def main(
        video_id: str,
        transcript_language: str,
        screenshot_resolution: int,
        out: str,
):
    """
    Converts a YouTube video into an Anki deck.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    transcript = retrieve_transcript(video_id, transcript_language)
    video = retrieve_video(url, screenshot_resolution) if screenshot_resolution != -1 else None
    audio = retrieve_audio(url)
    deck_name = retrieve_info(video_id)
    out = out or f"{deck_name}.apkg"
    make_package(transcript, audio, video, deck_name, out)


if __name__ == "__main__":
    main()
