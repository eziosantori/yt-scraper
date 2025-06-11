from youtube_scraper import fetch_new_videos
from transcript_extractor import get_transcript
from analyzer_factory import AnalyzerFactory
from db_manager import init_db, save_analysis
import time

def daily_job():
    """Execution flow for daily analysis
        Main daily job that coordinates the workflow:
        1. Fetches new videos
        2. Extracts transcripts
        3. Analyzes content
        4. Saves results to database
    """   
    # Initialize database
    init_db()
    
    # Create analyzer instance
    analyzer = AnalyzerFactory.create_analyzer()
    provider_name = analyzer.__class__.__name__.replace("Strategy", "").upper()
    print(f"Using analyzer: {provider_name}")
    
    # Fetch new videos
    videos = fetch_new_videos()
    print(f"Found {len(videos)} new videos to analyze")
    
    # Process each video
    for video in videos:
        print(f"Processing: {video['title']}")
        transcript = get_transcript(video['video_id'])
        #transcript = get_transcript_yt_dlp(video['video_id'], languages=['en'])
        
        if transcript:
            analysis = analyzer.analyze(transcript)
            if analysis:
                print(f"Found {len(analysis)} ticker mentions")
                save_analysis(analysis, video, provider_name)
    
    print("Daily analysis completed")

if __name__ == "__main__":
    # Run daily analysis on continuous loop
    while True:
        daily_job()
        time.sleep(86400)  # 24-hour interval
