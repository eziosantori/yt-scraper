from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    """
    Fetches and concatenates the transcript for a YouTube video
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Full transcript as a single string, or None if unavailable
    """
    try:
        # Fetch English transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        # Concatenate all text segments
        return " ".join([t['text'] for t in transcript_list])
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {e}")
        return None