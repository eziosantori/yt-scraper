import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ticker_analysis.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Add column if not exists
try:
    c.execute('ALTER TABLE mentions ADD COLUMN video_published DATETIME')
    print('Colonna video_published aggiunta')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Colonna video_published già esistente')
    else:
        raise

# Update existing records
c.execute('UPDATE mentions SET video_published = timestamp WHERE video_published IS NULL')
print('Aggiornati i record esistenti')

conn.commit()
conn.close()
print('Done.')
