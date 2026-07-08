def analyze_trend(df, symbol: str):
    latest = df.iloc[-1]
    score = 0
    reasons = []

    if latest["close"] > latest["ema_200"]:
        score += 2
        reasons.append("Price is above EMA 200")

    if latest["ema_20"] > latest["ema_50"]:
        score += 2
        reasons.append("EMA 20 is above EMA 50")

    if 45 <= latest["rsi"] <= 68:
        score += 1
        reasons.append("RSI is healthy for trend continuation")

    if latest["macd"] > latest["macd_signal"]:
        score += 1
        reasons.append("MACD is bullish")

    confidence = round((score / 6) * 100)

    return {
        "symbol": symbol,
        "strategy": "TREND_CONTINUATION",
        "direction": "LONG",
        "score": score,
        "max_score": 6,
        "confidence": confidence,
        "entry": float(latest["close"]),
        "reason": reasons,
    }