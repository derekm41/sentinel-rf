def analyze_short_trend(df, symbol: str):
    latest = df.iloc[-1]
    score = 0
    reasons = []

    if latest["close"] < latest["ema_200"]:
        score += 2
        reasons.append("Price is below EMA 200")

    if latest["ema_20"] < latest["ema_50"]:
        score += 2
        reasons.append("EMA 20 is below EMA 50")

    if 32 <= latest["rsi"] <= 55:
        score += 1
        reasons.append("RSI is weak but not extremely oversold")

    if latest["macd"] < latest["macd_signal"]:
        score += 1
        reasons.append("MACD is bearish")

    confidence = round((score / 6) * 100)

    return {
        "symbol": symbol,
        "strategy": "SHORT_TREND_CONTINUATION",
        "direction": "SHORT",
        "score": score,
        "max_score": 6,
        "confidence": confidence,
        "entry": float(latest["close"]),
        "reason": reasons,
    }