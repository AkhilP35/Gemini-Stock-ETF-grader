import argparse
import sys
import requests


def main():
    parser = argparse.ArgumentParser(description="Test /analyze endpoint with ticker-only input")
    parser.add_argument("ticker", help="Stock/ETF ticker, e.g. AAPL, TSLA, SPY")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/analyze",
        help="Analyze endpoint URL (default: http://localhost:8000/analyze)",
    )
    args = parser.parse_args()

    print("[INFO] Sending payload:")
    print(f"       ticker={args.ticker.upper()}")

    try:
        resp = requests.post(args.url, json={"ticker": args.ticker}, timeout=30)
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
