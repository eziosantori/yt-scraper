# Stock YouTube Monitor with Gemini API

Automated system to monitor financial YouTube channels, extract stock ticker mentions, analyze sentiment, and present results in a dashboard.

## Features

- Daily automated checks for new videos
- Transcript extraction
- Ticker identification and sentiment analysis using Gemini API
- SQLite database storage
- Interactive dashboard for data exploration

## Setup

### Prerequisites

- Python 3.8+
- YouTube Data API Key (from [Google Cloud Console](https://console.cloud.google.com/))
- Gemini API Key (from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. Clone repository:

   ```bash
   git clone https://github.com/tuo_repo/stock_youtube_monitor.git
   cd stock_youtube_monitor
   ```

2. virtual env

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. install
   ```bash
   pip install -r requirements.txt
   ```

## Obtaining API Keys

### YouTube Data API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "YouTube Data API v3":
   - Navigate to **APIs & Services** > **Library**
   - Search for "YouTube Data API v3"
   - Click on it and press **Enable**
4. Create credentials:
   - Go to **APIs & Services** > **Credentials**
   - Click **Create Credentials** > **API Key**
   - Copy your generated API key
5. (Optional) Restrict API key to prevent unauthorized use

### Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on **Get API key** in the left sidebar
4. Choose **Create API key in new project**
5. Copy your generated API key

### Adding Keys to the Project

1. Create a `.env` file in the project root directory
2. Add your keys in the following format:

```env
# .env file
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## Run

```bash
 # collection service
cd src
python main_scheduler.py

 # Terminale 2 - Dashboard
 cd dashboard
 streamlit run main.py
```

Access dashboard at: http://localhost:8501

stock_youtube_monitor/
├── venv/ # Virtual environment
├── src/
│ ├── youtube_scraper.py
│ ├── transcript_extractor.py
│ ├── gemini_analyzer.py
│ ├── db_manager.py
│ └── main_scheduler.py
├── dashboard/
│ └── app.py
├── .env # Environment variables file
├── requirements.txt
└── README.md
