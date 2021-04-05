from typing import Dict

from pydub import AudioSegment


def process_transcript_chunk(chunk: Dict) -> Dict:
    return {
        "text": chunk["text"],
        "start": int(chunk["start"] * 1000),
        "end": int((chunk["start"] + chunk["duration"]) * 1000),
    }


def process_audio_chunk(audio: AudioSegment, chunk: Dict) -> AudioSegment:
    return audio[chunk["start"] : chunk["end"]]
