import pytest
from src.transcript_extractor import get_transcript
from unittest.mock import patch

@patch('src.transcript_extractor.YouTubeTranscriptApi.get_transcript')
def test_get_transcript_success(mock_get_transcript):
    """Test successful transcript retrieval"""
    mock_get_transcript.return_value = [
        {'text': 'Hello', 'start': 0, 'duration': 1},
        {'text': 'world', 'start': 1, 'duration': 1}
    ]
    
    transcript = get_transcript('test_video_id')
    assert transcript == "Hello world"

@patch('src.transcript_extractor.YouTubeTranscriptApi.get_transcript')
def test_get_transcript_no_transcript(mock_get_transcript):
    """Test handling of unavailable transcript"""
    mock_get_transcript.side_effect = Exception("No transcript")
    
    transcript = get_transcript('test_video_id')
    assert transcript is None

def test_get_transcript_invalid_id():
    """Test handling of invalid video ID"""
    transcript = get_transcript('')
    assert transcript is None