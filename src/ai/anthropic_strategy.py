import os 
import anthropic
from .base_strategy import AnalysisStrategy

class AnthropicStrategy(AnalysisStrategy):
    """Implementation using Anthropic's Claude API"""
    
    def __init__(self):
        self.client = anthropic.Client(os.getenv("ANTHROPIC_API_KEY"))
    
    def analyze(self, transcript: str) -> dict:
        """Analyze transcript using Claude API"""
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": self._create_prompt(transcript)
                }]
            )
            return self._validate_response(response.content[0].text)
        except Exception as e:
            print(f"Anthropic API error: {str(e)}")
            return {}
    
    def _create_prompt(self, transcript: str) -> str:
        """Construct the analysis prompt for OpenAI"""
        return f"""
        Analyze this financial video transcript and extract:
        1. Stock tickers mentioned (e.g., AAPL, TSLA)
        2. Market sentiment for each (bullish/bearish/neutral) use always lower case to express sentiment
        3. Brief contextual summary per ticker
        
        Return ONLY valid JSON formatted like this:
        {{
            "TICKER": {{
                "sentiment": "...", 
                "summary": "..."
            }}
        }}
        
        Transcript:
        {transcript}
        """