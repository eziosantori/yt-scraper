import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ticker_analysis.db')

def init_db():
    """Initialize database with updated schema"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS mentions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ticker TEXT,
                 sentiment TEXT,
                 summary TEXT,
                 video_title TEXT,
                 channel TEXT,
                 ai_provider TEXT,
                 timestamp DATETIME,
                 video_published DATETIME)''')
    
    conn.commit()
    conn.close()

def save_analysis(analysis, video_info, ai_provider):
    """Save analysis results with provider information"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for ticker, data in analysis.items():
        # Use video_info['published'] if present, else None
        video_published = video_info.get('published')
        c.execute('''INSERT INTO mentions 
                  (ticker, sentiment, summary, video_title, channel, ai_provider, timestamp, video_published) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (ticker, data['sentiment'], data['summary'], 
                   video_info['title'], video_info['channel'], 
                   ai_provider, datetime.now(), video_published))
    
    conn.commit()
    conn.close()