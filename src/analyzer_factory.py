from ai import GeminiStrategy, OpenAIStrategy, AnthropicStrategy
import os

class AnalyzerFactory:
    """Factory class to instantiate the appropriate analysis strategy"""
    
    @staticmethod
    def create_analyzer():
        """
        Creates strategy instance based on environment configuration
        Defaults to Gemini if not specified
        """
        provider = os.getenv("AI_PROVIDER", "gemini").lower()
        
        if provider == "gemini":
            return GeminiStrategy()
        elif provider == "openai":
            return OpenAIStrategy()
        elif provider == "antropic":
            return AnthropicStrategy()        
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")