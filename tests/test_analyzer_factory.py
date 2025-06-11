import pytest
from src.analyzer_factory import AnalyzerFactory
from src.ai.gemini_strategy import GeminiStrategy
from src.ai.openai_strategy import OpenAIStrategy
from src.ai.anthropic_strategy import AnthropicStrategy

def test_create_analyzer_gemini(mock_env):
    """Test Gemini analyzer creation"""
    analyzer = AnalyzerFactory.create_analyzer()
    assert isinstance(analyzer, GeminiStrategy)

def test_create_analyzer_openai(monkeypatch):
    """Test OpenAI analyzer creation"""
    monkeypatch.setenv("AI_PROVIDER", "openai")
    analyzer = AnalyzerFactory.create_analyzer()
    assert isinstance(analyzer, OpenAIStrategy)


def test_create_analyzer_anthropic(monkeypatch):
    """Test Anthropic analyzer creation"""
    monkeypatch.setenv("AI_PROVIDER", "anthropic")
    analyzer = AnalyzerFactory.create_analyzer()
    assert isinstance(analyzer, AnthropicStrategy)

def test_create_analyzer_invalid(monkeypatch):
    """Test invalid provider handling"""
    monkeypatch.setenv("AI_PROVIDER", "invalid")
    with pytest.raises(ValueError):
        AnalyzerFactory.create_analyzer()