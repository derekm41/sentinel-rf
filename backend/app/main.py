from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.advisor import get_trade_advice
from app.services.market_data import get_crypto_price
from app.services.market_data import get_crypto_candles
from app.services.indicators import add_indicators
from app.services.strategy_rules import evaluate_strategy
from app.services.analyst import generate_trade_reason
app = FastAPI(title="Sentinel Crypto Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.app\.github\.dev",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Sentinel Crypto Advisor API is running"}

@app.get("/advisor/{symbol}")
def advisor(symbol: str):
    df = get_crypto_candles(
        symbol.upper(),
        interval="1h",
        period="30d"
    )

    df = add_indicators(df)

    result = evaluate_strategy(df)
    
    reason = generate_trade_reason(result)

    return {
        "symbol": symbol.upper(),
        **result,
        "reason": reason
    }

@app.get("/price/{symbol}")
def price(symbol: str):
    return get_crypto_price(symbol.upper())

@app.get("/candles/{symbol}")
def candles(symbol: str):
    df = get_crypto_candles(symbol.upper())
    return df.tail(5).to_dict(orient="records")

@app.get("/indicators/{symbol}")
def indicators(symbol: str):
    df = get_crypto_candles(symbol.upper(), interval="1h", period="30d")
    df = add_indicators(df)

    return df.tail(5).to_dict(orient="records")