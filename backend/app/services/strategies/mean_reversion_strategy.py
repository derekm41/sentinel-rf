def analyze_mean_reversion(df, symbol: str):
    latest = df.iloc[-1]
    recent = df.tail(20)

    mean_price = recent["close"].mean()
    std_price = recent["close"].std()
    z_score = (latest["close"] - mean_price) / std_price if std_price != 0 else 0

    score = 0
    reasons = []

    if z_score < -1.5:
        score += 2
        reasons.append("Price is stretched below recent mean")

    if latest["rsi"] < 35:
        score += 2
        reasons.append("RSI suggests oversold conditions")

    if latest["close"] > latest["ema_200"]:
        score += 1
        reasons.append("Long-term trend is still supportive")

    confidence = round((score / 5) * 100)

    return {
        "symbol": symbol,
        "strategy": "MEAN_REVERSION",
        "direction": "LONG",
        "score": score,
        "max_score": 5,
        "confidence": confidence,
        "entry": float(latest["close"]),
        "reason": reasons,
    }