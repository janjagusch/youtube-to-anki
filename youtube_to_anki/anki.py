"""
This module contains functions to make Anki notes and packages.
"""


from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Iterable

from genanki import Deck, Model, Note, Package
from pydub import AudioSegment

_MODEL = Model(
    1607392319,
    "Youtube",
    fields=[
        {"name": "TL-Audio"},
        {"name": "NL-Transcript"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{TL-Audio}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{NL-Transcript}}',
        },
    ],
)


def _make_note(nl_transcript: str, tl_audio_file: str) -> Note:
    """
    Creates an Anki note from a native langauge transcript and a target language audio file.
    """
    return Note(model=_MODEL, fields=[f"[sound:{tl_audio_file}]", nl_transcript])


def make_package(
    audio_chunks: Iterable[AudioSegment],
    transcript_chunks: Iterable[Dict],
    deck_name: str,
    deck_id: str,
    filepath: str,
) -> Package:
    """
    Creates an Anki deck, packages it and writes it to file path.
    """
    deck = Deck(deck_id=deck_id, name=deck_name)
    with TemporaryDirectory() as tempdir:
        for i, (audio_chunk, transcript_chunk) in enumerate(
            zip(audio_chunks, transcript_chunks)
        ):
            audio_chunk.export(f"{tempdir}/{i}_{deck_id}.mp3")
            note = _make_note(transcript_chunk["text"], f"{i}_{deck_id}.mp3")
            deck.add_note(note)
        package = Package(deck)
        package.media_files = Path(tempdir).glob("*.mp3")
        package.write_to_file(filepath)
