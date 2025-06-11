from youtube_scraper import fetch_new_videos
from transcript_extractor import get_text_reliable
from transcript_extractor import get_supa_transcript
from analyzer_factory import AnalyzerFactory
from db_manager import init_db, save_analysis
import time
import argparse
from datetime import datetime, timezone

def daily_job(date_from=None):
    """Execution flow for daily analysis
        Main daily job that coordinates the workflow:
        1. Fetches new videos
        2. Extracts transcripts
        3. Analyzes content
        4. Saves results to database
        date_from: if provided, only process videos newer than this date (YYYY-MM-DD)
    """   
    # Initialize database
    init_db()
    
    # Create analyzer instance
    analyzer = AnalyzerFactory.create_analyzer()
    provider_name = analyzer.__class__.__name__.replace("Strategy", "").upper()
    print(f"Using analyzer: {provider_name}")
    
    # Fetch new videos
    if date_from:
        try:
            date_obj = datetime.strptime(date_from, "%Y-%m-%d").date()
            print(f"Processing videos from date: {date_obj}")
        except Exception as e:
            print(f"Invalid date_from format: {date_from}. Use YYYY-MM-DD. Using today as fallback.")
            date_obj = datetime.now(timezone.utc).date()
    else:
        date_obj = datetime.now(timezone.utc).date()

    videos = fetch_new_videos(date=date_obj)
    print(f"Found {len(videos)} new videos to analyze")
    
    # Process each video
    for video in videos:
        print(f"Processing: {video['title']}")
        transcript = get_supa_transcript(video['video_id'])
        
        if transcript:
            analysis = analyzer.analyze(transcript)
            if analysis:
                print(f"Found {len(analysis)} ticker mentions")
                save_analysis(analysis, video, provider_name)
    
    print("Daily analysis completed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run daily video analysis job.")
    parser.add_argument('--date_from', type=str, default=None, help='Process only videos published on or after this date (YYYY-MM-DD)')
    parser.add_argument('--once', action='store_true', help='Run the job only once and exit')
    args = parser.parse_args()

    if args.once:
        print(f"Running daily job once... Processing videos from {args.date_from if args.date_from else 'today'}")
        daily_job(date_from=args.date_from)
    else:
        # Run daily analysis on continuous loop
        while True:
            daily_job(date_from=args.date_from)
            time.sleep(86400)  # 24-hour interval
