import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("YOUTUBE_API_KEY", "test_yt_key")
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key")
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("AI_PROVIDER", "gemini")

@pytest.fixture
def sample_video_data():
    """Sample video data for testing"""
    return [
        {
            'channel': 'CNBC',
            'title': 'Market Analysis Today',
            'video_id': 'abc123',
            'published': '2023-10-01T12:00:00Z'
        }
    ]

@pytest.fixture
def sample_transcript():
    """Sample transcript text"""
    return "Apple stock is looking strong. AAPL is bullish according to analysts. Meanwhile, TSLA faces challenges."

@pytest.fixture
def sample_analysis():
    """Sample analysis result"""
    return {
        "AAPL": {
            "sentiment": "bullish",
            "summary": "Apple stock is performing well"
        },
        "TSLA": {
            "sentiment": "bearish",
            "summary": "Tesla faces challenges"
        }
    }