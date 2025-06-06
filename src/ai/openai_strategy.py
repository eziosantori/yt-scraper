import os
import openai
from dotenv import load_dotenv
from .base_strategy import AnalysisStrategy

load_dotenv()

class OpenAIStrategy(AnalysisStrategy):
    """Concrete strategy implementation using OpenAI API"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in .env file")
        
        self.client = openai.OpenAI(api_key=api_key)
    
    def analyze(self, transcript: str) -> dict:
        """Analyze transcript using OpenAI API"""
        prompt = self._create_prompt(transcript[:12000])  # Token limit consideration
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}]
            )
            return self._validate_response(response.choices[0].message.content)
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return {}

    def _create_prompt(self, transcript: str) -> str:
        """Construct the analysis prompt for OpenAI"""
        return f"""
        Analyze this financial video transcript and extract:
        1. Stock tickers mentioned (e.g., AAPL, TSLA)
        2. Market sentiment for each (bullish/bearish/neutral)
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