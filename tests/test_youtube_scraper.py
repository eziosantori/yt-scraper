import pytest
from src.youtube_scraper import fetch_new_videos
from unittest.mock import patch, MagicMock


@patch('src.youtube_scraper.requests.get')
def test_fetch_new_videos_no_items(mock_get, mock_env):
    """Test handling of empty API response"""
    mock_response = MagicMock()
    mock_response.json.return_value = {'items': []}
    mock_get.return_value = mock_response
    
    videos = fetch_new_videos()
    assert videos == []
