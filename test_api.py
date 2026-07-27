import argparse
import sys
import requests
import yfinance as yf


def build_payload(ticker: str, window: int = 30):
    # Pull extra days to handle weekends/holidays
    hist = yf.Ticker(ticker).history(period="3mo")

    if hist.empty or "Close" not in hist:
        raise ValueError(f"No historical close data found for ticker: {ticker}")

    closes = hist["Close"].dropna().tolist()

    if len(closes) < window:
        raise ValueError(
            f"Not enough close prices for {ticker}. Need at least {window}, got {len(closes)}."
        )

    closing_prices = [round(float(x), 2) for x in closes[-window:]]
    moving_average = round(sum(closing_prices) / len(closing_prices), 2)

    return {
        "ticker": ticker.upper(),
        "moving_average": moving_average,
        "closing_prices": closing_prices,
    }


def main():
    parser = argparse.ArgumentParser(description="Test /analyze endpoint with real stock data")
    parser.add_argument("ticker", help="Stock/ETF ticker, e.g. AAPL, TSLA, SPY")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/analyze",
        help="Analyze endpoint URL (default: http://localhost:8000/analyze)",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=30,
        help="Number of closing prices to send (default: 30)",
    )
    args = parser.parse_args()

    try:
        payload = build_payload(args.ticker, window=args.window)
    except Exception as e:
        print(f"[ERROR] Payload build failed: {e}")
        sys.exit(1)

    print("[INFO] Sending payload:")
    print(f"       ticker={payload['ticker']}")
    print(f"       moving_average={payload['moving_average']}")
    print(f"       closing_prices_count={len(payload['closing_prices'])}")

    try:
        resp = requests.post(args.url, json=payload, timeout=30)
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        sys.exit(1)

    print(f"\n[INFO] Status code: {resp.status_code}")
    try:
        print("[INFO] Response JSON:")
        print(resp.json())
    except Exception:
        print("[INFO] Raw response:")
        print(resp.text)


if __name__ == "__main__":
    main()
