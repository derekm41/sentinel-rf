def analyze_breakout(df, symbol: str):
    latest = df.iloc[-1]
    recent = df.tail(20)

    resistance = recent["high"].max()
    avg_volume = recent["volume"].mean()

    score = 0
    reasons = []

    if latest["close"] >= resistance * 0.995:
        score += 2
        reasons.append("Price is near recent resistance")

    if latest["volume"] > avg_volume:
        score += 2
        reasons.append("Volume is above recent average")

    if latest["atr"] > recent["atr"].mean():
        score += 1
        reasons.append("ATR is expanding")

    confidence = round((score / 5) * 100)

    return {
        "symbol": symbol,
        "strategy": "BREAKOUT",
        "direction": "LONG",
        "score": score,
        "max_score": 5,
        "confidence": confidence,
        "entry": float(latest["close"]),
        "reason": reasons,
    }