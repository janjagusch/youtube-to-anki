"""
This module contains utility functions.
"""

from typing import Dict

from pydub import AudioSegment


def process_transcript_chunk(chunk: Dict) -> Dict:
    """
    Calculates end timestamp from start timestamp and duration and converts timestamp from seconds
    to milliseconds.
    """
    return {
        "text": chunk["text"],
        "start": int(chunk["start"] * 1000),
        "end": int((chunk["start"] + chunk["duration"]) * 1000),
    }


def process_audio_chunk(audio: AudioSegment, chunk: Dict) -> AudioSegment:
    """
    Indexes an audio segment by the start and end timestamp provided in the transcript chunk.
    """
    return audio[chunk["start"] : chunk["end"]]
