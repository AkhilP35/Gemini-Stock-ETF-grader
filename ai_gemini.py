import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas_gemini import StockAnalysis, StockRequest

from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_asset(stock_data: StockRequest) -> StockAnalysis:
    prompt = f"""
You are an expert financial analyst. Analyze the following 30-day stock data for {stock_data.ticker}:
- 30-Day Moving Average: {stock_data.moving_average}
- Daily Closing Prices: {stock_data.closing_prices}

Provide a brief analysis of the trend.
Assign a risk_score from 1 (lowest risk) to 10 (highest risk).
Assign a signal of strictly "BUY", "HOLD", or "SELL".
Provide a 2-3 sentence reasoning for your decision based on the price trend versus the moving average.
"""
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StockAnalysis,
            temperature=0.2,
        ),
    )
    parsed = json.loads(response.text)
    return StockAnalysis(**parsed)