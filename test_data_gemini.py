import unittest
from unittest.mock import patch

import requests

from data_gemini import MarketDataError, fetch_stock_market_data


class _FakeSeries:
    def __init__(self, values):
        self.values = values

    def dropna(self):
        return _FakeSeries([value for value in self.values if value is not None])

    def tolist(self):
        return self.values


class _FakeHistory:
    def __init__(self, closes):
        self._closes = closes
        self.empty = not closes

    def __contains__(self, key):
        return key == "Close" and self._closes is not None

    def __getitem__(self, key):
        if key != "Close":
            raise KeyError(key)
        return _FakeSeries(self._closes)


class FetchStockMarketDataTests(unittest.TestCase):
    @patch("data_gemini.yf.Ticker")
    def test_fetch_stock_market_data_success(self, mock_ticker):
        closes = [100 + i for i in range(35)]
        mock_ticker.return_value.history.return_value = _FakeHistory(closes)

        result = fetch_stock_market_data("aapl")

        self.assertEqual(result.ticker, "AAPL")
        self.assertEqual(len(result.closing_prices), 30)
        self.assertEqual(result.closing_prices[0], 105.0)
        self.assertEqual(result.closing_prices[-1], 134.0)
        self.assertEqual(result.moving_average, 119.5)

    @patch("data_gemini.yf.Ticker")
    def test_fetch_stock_market_data_invalid_ticker(self, mock_ticker):
        mock_ticker.return_value.history.return_value = _FakeHistory([])

        with self.assertRaises(MarketDataError) as context:
            fetch_stock_market_data("INVALID")

        self.assertIn("No market data found", str(context.exception))

    @patch("data_gemini.yf.Ticker")
    def test_fetch_stock_market_data_network_error(self, mock_ticker):
        mock_ticker.return_value.history.side_effect = requests.exceptions.RequestException("boom")

        with self.assertRaises(MarketDataError) as context:
            fetch_stock_market_data("AAPL")

        self.assertIn("Unable to reach market data service", str(context.exception))


if __name__ == "__main__":
    unittest.main()
