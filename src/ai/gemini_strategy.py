import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from .base_strategy import AnalysisStrategy

load_dotenv()

class GeminiStrategy(AnalysisStrategy):
    """Concrete strategy implementation using Gemini API"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze(self, transcript: str) -> dict:
        """Analyze transcript using Gemini API"""
        prompt = self._create_prompt(transcript[:15000])  # Truncate for efficiency
        
        try:
            response = self.model.generate_content(prompt)
            json_str = self._extract_json(response.text)
            return self._validate_response(json_str)
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            return {}

    def _create_prompt(self, transcript: str) -> str:
        """Construct the analysis prompt for Gemini"""
        return f"""
        As a professional financial analyst, analyze this YouTube transcript:
        {transcript}
        
        Requirements:
        1. Identify all mentioned stock tickers (e.g., AAPL, TSLA)
        2. Determine sentiment for each (bullish/bearish/neutral) use always lower case to express sentiment
        3. Provide a concise 1-sentence summary per ticker
        4. Format response as valid JSON exactly like this:
        {{
            "TICKER": {{
                "sentiment": "...",
                "summary": "..."
            }}
        }}
        """
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON string from Gemini's response"""
        match = re.search(r'\{[\s\S]*\}', text)
        return match.group(0) if match else "{}"