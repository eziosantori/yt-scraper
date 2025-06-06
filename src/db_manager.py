import sqlite3
from datetime import datetime
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ticker_analysis.db')

def init_db():
    """
    Initializes SQLite database and creates table if it doesn't exist
    """
    # Create data directory if needed
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create table schema
    c.execute('''CREATE TABLE IF NOT EXISTS mentions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ticker TEXT,
                 sentiment TEXT,
                 summary TEXT,
                 video_title TEXT,
                 channel TEXT,
                 timestamp DATETIME)''')
    conn.commit()
    conn.close()

def save_analysis(analysis, video_info):
    """
    Saves analysis results to the database
    
    Args:
        analysis (dict): Analysis results from Gemini
        video_info (dict): Video metadata
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Save each ticker mention
    for ticker, data in analysis.items():
        c.execute("""INSERT INTO mentions 
                  (ticker, sentiment, summary, video_title, channel, timestamp) 
                  VALUES (?, ?, ?, ?, ?, ?)""",
                  (ticker, data['sentiment'], data['summary'], 
                   video_info['title'], video_info['channel'], datetime.now()))
    
    conn.commit()
    conn.close()