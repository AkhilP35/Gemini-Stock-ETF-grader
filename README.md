# Gemini Stock ETF Grader

The app now uses a **ticker-only input flow**.

## How analysis input works

1. Enter a stock/ETF ticker symbol (for example, `AAPL` or `SPY`).
2. The backend fetches recent historical prices from `yfinance` (3 months).
3. The backend derives:
   - Last 30 daily closing prices
   - 30-day moving average (computed from those closes)
4. The existing Gemini grading/analysis flow runs using this auto-fetched data.

If the ticker is invalid, history is incomplete, or market data cannot be fetched, the API returns a user-friendly error message.
