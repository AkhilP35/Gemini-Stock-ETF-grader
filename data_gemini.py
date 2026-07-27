from typing import Dict, Any
from schemas_gemini import StockRequest


def normalize_input(payload: Dict[str, Any]) -> StockRequest:
    """
    Validates and normalizes incoming dictionary payloads
    into a strongly typed StockRequest model.
    """
    return StockRequest(**payload)


def sample_payload() -> Dict[str, Any]:
    """
    Optional helper sample for testing.
    """
    return {
        "ticker": "AAPL",
        "moving_average": 195.42,
        "closing_prices": [
            193.1, 194.0, 195.2, 196.4, 197.0, 196.2, 195.9, 196.8, 197.3, 198.0,
            197.6, 196.9, 196.1, 195.8, 195.4, 194.9, 194.3, 193.8, 194.5, 195.0,
            195.7, 196.3, 197.1, 197.8, 198.2, 198.9, 199.3, 198.7, 198.1, 197.5
        ]
    }