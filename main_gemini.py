import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from schemas_gemini import StockRequest, StockAnalysis
from ai_gemini import analyze_asset
from data_gemini import MarketDataError, fetch_stock_market_data

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Gemini Stock Analysis API",
    description="Analyzes 30-day stock trend data using Gemini and returns BUY/HOLD/SELL signal.",
    version="1.0.0"
)

# Mount templates and static files
templates = Jinja2Templates(directory="templates")

import os
static_dir = "static"
if not os.path.isdir(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/health")
def health():
    has_key = bool(os.getenv("GEMINI_API_KEY"))
    return {"status": "ok", "gemini_key_loaded": has_key}

@app.post("/analyze", response_model=StockAnalysis)
def analyze(stock_data: StockRequest):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set")

    try:
        market_data = fetch_stock_market_data(stock_data.ticker)
        result = analyze_asset(market_data)
        return result
    except MarketDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini analysis failed: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unexpected server error: {str(exc)}"},
    )

#cd /Volumes/SSD/stock-ai/Gemini
#uvicorn main_gemini:app --reload
