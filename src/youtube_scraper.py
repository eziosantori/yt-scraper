import requests
import json
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube channels to monitor (channel name: channel ID)
CHANNELS = {
    # 'CNBC': 'UCvJJ_dzjViJCoLf5uKUTwoA',
    # 'Bloomberg': 'UCIALMKvObZNtJ6AmdCLP7Lg',
    'IBD Live': 'UC5fZv7bPcF5j2RsfO-9OiLA',
}

def fetch_new_videos(date=datetime.now(timezone.utc).date()):
    """
    Fetches new videos from predefined YouTube channels published today.
    
    Returns:
        list: A list of dictionaries containing video details
    """
    # Get YouTube API key from environment
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YouTube API key not found in environment variables")
    
    results = []
    print(date)
    
    for name, channel_id in CHANNELS.items():
        # Construct API request URL
        url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=20"
        print(url)
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        ## print("Risposta JSON completa:")
        # print(json.dumps(data, indent=2)) # Stampa il JSON in modo leggibile
        
        # Process each item in the response
        for item in data.get('items', []):
            # Skip if not a video
            if item['id']['kind'] != 'youtube#video': 
                continue
            
            video_id = item['id']['videoId']
            published = datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            print(published.date())
            # Check if video was published today
            # if published.date() == datetime(2025,6,6).date():
            if published.date() == date:
                results.append({
                    'channel': name,
                    'title': item['snippet']['title'],
                    'video_id': video_id,
                    'published': published
                })
    return results