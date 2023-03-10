"""
This module contains utility functions.
"""

from typing import Dict, Iterable, Tuple

import cv2
from numpy import ndarray
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

def take_screenshots(video: cv2.VideoCapture, chunks: Tuple[Dict]) -> Iterable[ndarray]:
    """
    Processes a video, for each interval taking a screenshot (ndarray, colors last) at around the middle of the interval
    """
    screenshots = []
    for chunk in chunks:
        # 30 ms offset to account for the average delay until the next frame
        ms_target = (chunk["start"] + chunk["end"]) // 2 - 30
        while video.isOpened():
            success, frame = video.read()
            if success:
                if video.get(cv2.CAP_PROP_POS_MSEC) >= ms_target:
                    screenshots.append(frame)
                    break
            else:
                break

    video.release()
    return screenshots
