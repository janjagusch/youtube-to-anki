"""
This module contains the main function for converting YouTube videos to Anki decks.
"""

from typing import Dict, Iterable

import click
from pydub import AudioSegment

from youtube_to_anki.anki import make_package as _make_package
from youtube_to_anki.utils import process_audio_chunk, process_transcript_chunk
from youtube_to_anki.youtube import retrieve_audio, retrieve_info, retrieve_transcript


def make_package(
    transcript: Iterable[Dict], audio: AudioSegment, deck_name: str, filepath: str
):
    """
    Creates an Anki package from audio and transcript.
    """
    transcript_chunks = tuple(process_transcript_chunk(chunk) for chunk in transcript)
    audio_chunks = tuple(
        process_audio_chunk(audio, chunk) for chunk in transcript_chunks
    )
    _make_package(audio_chunks, transcript_chunks, deck_name, hash(deck_name), filepath)


# pylint: disable=no-value-for-parameter
@click.command()
@click.option(
    "--out",
    default=None,
    help="Where to export the deck. Defaults to '<deck_name>.apgk'.",
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
    out: str,
):
    """
    Converts a YouTube video into an Anki deck.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    transcript = retrieve_transcript(video_id, transcript_language)
    audio = retrieve_audio(url)
    deck_name = retrieve_info(video_id)
    out = out or f"{deck_name}.apkg"
    make_package(transcript, audio, deck_name, out)


if __name__ == "__main__":
    main()
