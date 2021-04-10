"""
This module contains functions to retrieve metadata from a YouTube video.
"""


import json
import urllib.parse
import urllib.request


def retrieve_info(video_id: str) -> str:
    """
    Retrives video author and title from video id.

    Thanks to: https://stackoverflow.com/a/52664178/7380270
    """
    params = {"format": "json", "url": f"https://www.youtube.com/watch?v={video_id}"}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = f"{url}?{query_string}"
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return f"{data['author_name']} - {data['title']}"
