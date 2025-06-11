import pytest
from src.main_scheduler import daily_job
from unittest.mock import patch, MagicMock

@patch('src.main_scheduler.fetch_new_videos')
@patch('src.main_scheduler.get_transcript')
@patch('src.analyzer_factory.AnalyzerFactory.create_analyzer')
@patch('src.db_manager.save_analysis')
def test_daily_job_success(
    mock_save, mock_analyzer, mock_transcript, mock_fetch, 
    mock_env, sample_video_data, sample_transcript, sample_analysis
):
    """Test successful daily job execution"""
    # Mock dependencies
    mock_fetch.return_value = sample_video_data
    mock_transcript.return_value = sample_transcript
    mock_analyzer.return_value.analyze.return_value = sample_analysis
    
    daily_job()
    
    # Verify calls
    mock_fetch.assert_called_once()
    mock_transcript.assert_called_once()
    mock_analyzer.return_value.analyze.assert_called_once_with(sample_transcript)
    mock_save.assert_called_once_with(
        sample_analysis, 
        sample_video_data[0], 
        "GEMINI"  # Default provider
    )

@patch('src.main_scheduler.fetch_new_videos')
def test_daily_job_no_videos(mock_fetch, mock_env, caplog):
    """Test daily job with no new videos"""
    mock_fetch.return_value = []
    
    daily_job()
    
    assert "Found 0 new videos" in caplog.text

@patch('src.main_scheduler.fetch_new_videos')
@patch('src.main_scheduler.get_transcript')
def test_daily_job_no_transcript(mock_transcript, mock_fetch, mock_env, sample_video_data, caplog):
    """Test handling of videos without transcripts"""
    mock_fetch.return_value = sample_video_data
    mock_transcript.return_value = None
    
    daily_job()
    
    assert "No transcript available" in caplog.text