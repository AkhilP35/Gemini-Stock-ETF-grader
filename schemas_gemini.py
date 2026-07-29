from typing import List, Literal
from pydantic import BaseModel, Field


class StockRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker, e.g. AAPL")


class StockMarketData(BaseModel):
    ticker: str = Field(..., description="Stock ticker, e.g. AAPL")
    moving_average: float = Field(..., description="30-day moving average")
    closing_prices: List[float] = Field(..., min_length=30, max_length=30, description="Last 30 daily closing prices")


class StockAnalysis(BaseModel):
    ticker: str = Field(..., description="Stock ticker that was analyzed")
    risk_score: int = Field(..., ge=1, le=10)
    signal: Literal["BUY", "HOLD", "SELL"]
    analysis: str = Field(..., description="Brief analysis of the price trend")
    reasoning: str
