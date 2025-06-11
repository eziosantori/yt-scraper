import pytest
from src.strategies.gemini_strategy import GeminiStrategy
from src.strategies.openai_strategy import OpenAIStrategy
from unittest.mock import patch, MagicMock

@patch('src.strategies.gemini_strategy.genai.GenerativeModel')
def test_gemini_strategy_success(mock_model, mock_env, sample_transcript):
    """Test Gemini strategy success path"""
    # Mock Gemini response
    mock_response = MagicMock()
    mock_response.text = '{"AAPL": {"sentiment": "bullish", "summary": "Positive outlook"}}'
    mock_model.return_value.generate_content.return_value = mock_response
    
    strategy = GeminiStrategy()
    result = strategy.analyze(sample_transcript)
    
    assert "AAPL" in result
    assert result["AAPL"]["sentiment"] == "bullish"

@patch('src.strategies.gemini_strategy.genai.GenerativeModel')
def test_gemini_strategy_invalid_json(mock_model, mock_env, sample_transcript):
    """Test Gemini strategy with invalid JSON response"""
    mock_response = MagicMock()
    mock_response.text = "Invalid response"
    mock_model.return_value.generate_content.return_value = mock_response
    
    strategy = GeminiStrategy()
    result = strategy.analyze(sample_transcript)
    
    assert result == {}

@patch('src.strategies.openai_strategy.openai.OpenAI')
def test_openai_strategy_success(mock_client, mock_env, sample_transcript):
    """Test OpenAI strategy success path"""
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"TSLA": {"sentiment": "bearish", "summary": "Challenges ahead"}}'
    mock_client.return_value.chat.completions.create.return_value = mock_response
    
    strategy = OpenAIStrategy()
    result = strategy.analyze(sample_transcript)
    
    assert "TSLA" in result
    assert result["TSLA"]["sentiment"] == "bearish"

@patch('src.strategies.openai_strategy.openai.OpenAI')
def test_openai_strategy_error(mock_client, mock_env, sample_transcript):
    """Test OpenAI strategy error handling"""
    mock_client.return_value.chat.completions.create.side_effect = Exception("API error")
    
    strategy = OpenAIStrategy()
    result = strategy.analyze(sample_transcript)
    
    assert result == {}