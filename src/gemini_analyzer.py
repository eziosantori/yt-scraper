import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def analyze_content(transcript):
    """
    Analyzes transcript using Google Gemini API to extract stock tickers, sentiment, and summaries
    
    Args:
        transcript (str): Video transcript text
        
    Returns:
        dict: Analysis results with tickers as keys
    """
    # Configure Gemini API
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Gemini API key not found in environment variables")
    genai.configure(api_key=gemini_api_key)
    
    # Initialize Gemini model (using the efficient Gemini 1.5 Flash)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct the analysis prompt
    prompt = f"""
    You are an expert financial analyst. Analyze the provided YouTube video transcript 
    and identify mentioned stock tickers along with the sentiment and a brief summary.
    
    INSTRUCTIONS:
    1. Identify all stock tickers mentioned (e.g., AAPL, TSLA, MSFT). 
    2. For each ticker, determine the sentiment: bullish, bearish, or neutral.
    3. Provide a one-sentence summary of what was said about the ticker.
    4. Format your response as a valid JSON object without any extra text:
    {{
        "ticker1": {{
            "sentiment": "bullish/bearish/neutral",
            "summary": "Summary here"
        }},
        "ticker2": {{
            ...
        }}
    }}
    
    TRANSCRIPT (truncated to 15000 characters for efficiency):
    {transcript[:15000]}
    """
    
    try:
        # Generate content with Gemini
        response = model.generate_content(prompt)
        # Extract JSON string from the response
        json_str = extract_json(response.text)
        # Parse the JSON string into a Python dictionary
        return json.loads(json_str)
    except Exception as e:
        print(f"Gemini analysis error: {e}")
        return {}

def extract_json(text):
    """
    Extracts a JSON string from text using regex
    
    Args:
        text (str): Text response from Gemini
        
    Returns:
        str: Extracted JSON string, or empty JSON if not found
    """
    # Regex to find the first JSON object in the string
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        return match.group(0)
    return "{}"  # Return empty JSON if not found