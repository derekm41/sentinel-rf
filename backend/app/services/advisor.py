def get_trade_advice(symbol: str):
    return {
        "symbol": symbol,
        "recommendation": "HOLD",
        "confidence": 62,
        "reason": "MVP placeholder: market data and indicators will be added next.",
        "entry": None,
        "stop_loss": None,
        "take_profit": None,
    }