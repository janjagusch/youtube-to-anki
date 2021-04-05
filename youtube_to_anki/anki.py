from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Iterable

from genanki import Deck, Model, Note, Package
from pydub import AudioSegment

_MODEL = Model(
    1607392319,
    "Youtube",
    fields=[
        {"name": "JP-Audio"},
        {"name": "EN-Transcript"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{JP-Audio}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{EN-Transcript}}',
        },
    ],
)


def _make_note(en_transcript, jp_audio_file):
    return Note(model=_MODEL, fields=[f"[sound:{jp_audio_file}]", en_transcript])


def make_package(
    audio_chunks: Iterable[AudioSegment],
    transcript_chunks: Iterable[Dict],
    deck_name: str,
    deck_id: str,
    filepath: str,
) -> Package:
    deck = Deck(deck_id=deck_id, name=deck_name)
    with TemporaryDirectory() as tempdir:
        for i, (audio_chunk, transcript_chunks) in enumerate(zip(audio_chunks, transcript_chunks)):
            audio_chunk.export(f"{tempdir}/{i}_{deck_id}.mp3")
            note = _make_note(transcript_chunks["text"], f"{i}_{deck_id}.mp3")
            deck.add_note(note)
        package = Package(deck)
        package.media_files = Path(tempdir).glob("*.mp3")
        package.write_to_file(filepath)
