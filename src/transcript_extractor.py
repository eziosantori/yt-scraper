from supadata import Supadata
import os
from functools import lru_cache

@lru_cache(maxsize=100)
def get_supa_transcript(video_id):
    """
    Example function to get a YouTube transcript using Supadata.
    Replace {your_api_key} with your actual Supadata API key.
    """

    print(f"Recupero transcript per il video {video_id}")
    # Initialize Supadata client with your API key
    supadata = Supadata(api_key=os.getenv("SUPADATA_API_KEY"))

    transcript = supadata.youtube.transcript(video_id=video_id, text=True)
    print(f"{transcript.content}")

    return transcript.content    