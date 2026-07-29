from typing import Dict, Any

import requests
import yfinance as yf

from schemas_gemini import StockMarketData, StockRequest


class MarketDataError(Exception):
    pass


def normalize_input(payload: Dict[str, Any]) -> StockRequest:
    """
    Validates and normalizes incoming dictionary payloads
    into a strongly typed StockRequest model.
    """
    return StockRequest(**payload)


def fetch_stock_market_data(ticker: str, window: int = 30, period: str = "3mo") -> StockMarketData:
    symbol = ticker.strip().upper()
    if not symbol:
        raise MarketDataError("Please enter a stock ticker symbol.")

    try:
        history = yf.Ticker(symbol).history(period=period)
    except requests.exceptions.RequestException as exc:
        raise MarketDataError("Unable to reach market data service. Please try again.") from exc
    except Exception as exc:
        raise MarketDataError(
            f"Unable to fetch market data for '{symbol}'. Please verify the ticker and try again."
        ) from exc

    if history.empty or "Close" not in history:
        raise MarketDataError(f"No market data found for ticker '{symbol}'. Please check the symbol and try again.")

    closes = history["Close"].dropna().tolist()
    if len(closes) < window:
        raise MarketDataError(
            f"Not enough recent data for '{symbol}' to compute a 30-day moving average."
        )

    closing_prices = [round(float(price), 2) for price in closes[-window:]]
    moving_average = round(sum(closing_prices) / len(closing_prices), 2)

    return StockMarketData(
        ticker=symbol,
        moving_average=moving_average,
        closing_prices=closing_prices,
    )


def sample_payload() -> Dict[str, Any]:
    """
    Optional helper sample for testing.
    """
    return {
        "ticker": "AAPL",
    }