"""
This module contains a function to retrieve the transcript from a YouTube video.
"""


from typing import Dict, Iterable

from youtube_transcript_api import YouTubeTranscriptApi


def retrieve_transcript(video_id: str, language: str) -> Iterable[Dict]:
    """
    Retrieves a video transcript in a given language.
    """
    return YouTubeTranscriptApi.get_transcript(video_id, languages=(language,))
