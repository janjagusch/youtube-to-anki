from typing import Dict, Iterable

from youtube_transcript_api import YouTubeTranscriptApi


def retrieve_transcript(video_id: str, language) -> Iterable[Dict]:
    return YouTubeTranscriptApi.get_transcript(video_id, languages=(language,))
