"""
This module contains functions to make Anki notes and packages.
"""


from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Iterable

import cv2
from genanki import Deck, Model, Note, Package
from pydub import AudioSegment

style = """
.card {text-align:center;}
.card {font-family: myfont; font-size: 30px}
"""

_MODEL = Model(
    1601234219,
    "YoutubeWithScreenshot",
    fields=[
        {"name": "TL-Audio"},
        {"name": "NL-Transcript"},
        {"name": "Screenshot"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Screenshot}}<br>{{TL-Audio}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{NL-Transcript}}',
        },
    ],
    css=style
)


def _make_note(nl_transcript: str, tl_audio_file: str, screenshot: str) -> Note:
    """
    Creates an Anki note from a native langauge transcript and a target language audio file.
    """
    return Note(model=_MODEL, fields=[f"[sound:{tl_audio_file}]", nl_transcript, f'<img src="{screenshot}">'])


def make_package(
    audio_chunks: Iterable[AudioSegment],
    screenshots: Iterable[str],
    transcript_chunks: Iterable[Dict],
    deck_name: str,
    deck_id: int,
    filepath: str,
) -> Package:
    """
    Creates an Anki deck, packages it and writes it to file path.
    """
    deck = Deck(deck_id=deck_id, name=deck_name)
    with TemporaryDirectory() as tempdir:
        for i, (audio_chunk, transcript_chunk, screenshot) in enumerate(
            zip(audio_chunks, transcript_chunks, screenshots)
        ):
            audio_chunk.export(f"{tempdir}/{i}_{deck_id}.mp3")
            cv2.imwrite(f"{tempdir}/{i}_{deck_id}.png", screenshot)
            note = _make_note(transcript_chunk["text"], f"{i}_{deck_id}.mp3", f"{i}_{deck_id}.png")
            deck.add_note(note)
        package = Package(deck)
        package.media_files = list(Path(tempdir).glob("*.mp3")) + list(Path(tempdir).glob("*.png"))
        package.write_to_file(filepath)
