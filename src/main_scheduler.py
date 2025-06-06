from youtube_scraper import fetch_new_videos
from transcript_extractor import get_transcript
from gemini_analyzer import analyze_content
from db_manager import init_db, save_analysis
import time

def daily_job():
    """
    Main daily job that coordinates the workflow:
    1. Fetches new videos
    2. Extracts transcripts
    3. Analyzes content
    4. Saves results to database
    """
    # Initialize database
    init_db()
    
    # Fetch new videos published today
    videos = fetch_new_videos()
    print(f"Found {len(videos)} new videos.")
    
    # Process each video
    for video in videos:
        print(f"Processing video: {video['title']}")
        transcript = get_transcript(video['video_id'])
        if transcript:
            # Analyze transcript using Gemini
            analysis = analyze_content(transcript)
            if analysis:
                print(f"Found {len(analysis)} ticker mentions. Saving to database...")
                save_analysis(analysis, video)
    
    print("Daily job completed.")

if __name__ == "__main__":
    # Run immediately and then every 24 hours
    while True:
        daily_job()
        time.sleep(86400)  # 24 hours in seconds