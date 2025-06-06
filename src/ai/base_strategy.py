from abc import ABC, abstractmethod
import json

class AnalysisStrategy(ABC):
    """Abstract base class for all analysis strategies"""
    
    @abstractmethod
    def analyze(self, transcript: str) -> dict:
        """Analyze the transcript and return ticker data"""
        pass
    
    def _validate_response(self, response: str) -> dict:
        """Helper method to validate and clean JSON responses"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print("Invalid JSON response from AI provider")
            return {}