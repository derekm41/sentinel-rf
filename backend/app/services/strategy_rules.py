def evaluate_strategy(df):
    latest = df.iloc[-1]

    rules_passed = []
    rules_failed = []

    if latest["close"] > latest["ema_20"]:
        rules_passed.append("Price is above EMA 20")
    else: 
        rules_failed.append("Price is below EMA 20")

    if latest["close"] > latest["ema_200"]:
        rules_passed.append("Price is above EMA 200")
    else:
        rules_failed.append("Price is below EMA 200")

    if 45 <= latest["rsi"] <= 65:
        rules_passed.append("RSI is in a healthy range")
    else:
        rules_failed.append("RSI is outside healthy range")

    if latest["macd"] > latest["macd_signal"]:
        rules_passed.append("MACD is bullish")
    else:
        rules_failed.append("MACD is bearish")

    score = len(rules_passed)
    confidence = int((score / 4) * 100)

    if score == 4:
        recommendation = "BUY"
    elif score >= 2:
        recommendation = "WATCHLIST"
    else:
        recommendation = "HOLD"

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "price": float(latest["close"]),
        "rules_passed": rules_passed,
        "rules_failed": rules_failed,
    }