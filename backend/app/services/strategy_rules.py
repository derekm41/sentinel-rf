from app.services.regime import detect_market_regime
from app.services.risk import calculate_risk_levels


def evaluate_strategy(df):

    latest = df.iloc[-1]

    regime = detect_market_regime(df)

    score = 0
    max_score = 8

    rules_passed = []
    rules_failed = []
    rules_neutral = []

    # -------------------------
    # TREND RULES
    # -------------------------

    if latest["close"] > latest["ema_200"]:
        score += 2
        rules_passed.append("Price is above EMA 200")
    else:
        rules_failed.append("Price is below EMA 200")

    if latest["ema_20"] > latest["ema_50"]:
        score += 2
        rules_passed.append("EMA 20 is above EMA 50")
    else:
        rules_failed.append("EMA 20 is below EMA 50")

    # -------------------------
    # MOMENTUM RULES
    # -------------------------

    if 45 <= latest["rsi"] <= 68:
        score += 1
        rules_passed.append("RSI is in healthy range")
    else:
        rules_failed.append("RSI is outside healthy range")

    if latest["macd"] > latest["macd_signal"]:
        score += 1
        rules_passed.append("MACD is bullish")
    else:
        rules_failed.append("MACD is bearish")

    # -------------------------
    # VOLUME RULES
    # -------------------------

    volume = latest.get("volume", 0)
    volume_avg = latest.get("volume_avg_20", 0)
    
    if volume_avg and volume_avg > 0:
        volume_ratio = volume / volume_avg
    
        if volume_ratio > 1.2:
            rules_neutral.append("Volume confirms above-average participation")
        else:
            rules_neutral.append("Volume is below average")
    else:
        rules_neutral.append("Volume data unavailable")

    # -------------------------
    # REGIME RULES
    # -------------------------

    if regime == "UPTREND":
        score += 1
        rules_passed.append("Market regime is UPTREND")

    elif regime == "CHOPPY":
        score -= 2
        rules_failed.append("Market regime is CHOPPY")

    elif regime == "DOWNTREND":
        score -= 2
        rules_failed.append("Market regime is DOWNTREND")

    elif regime == "HIGH_VOLATILITY":
        score -= 1
        rules_failed.append("Market regime is HIGH_VOLATILITY")

    # -------------------------
    # FINAL SCORING
    # -------------------------

    confidence = int((score / max_score) * 100)

    if score >= 7:
        recommendation = "BUY"
    elif score >= 5:
        recommendation = "WATCHLIST"
    else:
        recommendation = "HOLD"

    risk = None

    if recommendation in ["BUY", "WATCHLIST"]:
        risk = calculate_risk_levels(
            price=float(latest["close"]),
            atr=float(latest["atr"]),
            account_size=1000,
            risk_percent=1.0
        )

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "score": score,
        "max_score": max_score,
        "regime": regime,
        "price": float(latest["close"]),
        "risk": risk,
        "rules_passed": rules_passed,
        "rules_failed": rules_failed,
        "rules_neutral": rules_neutral,
        "indicators": {
            "rsi": float(latest["rsi"]),
            "ema_20": float(latest["ema_20"]),
            "ema_50": float(latest["ema_50"]),
            "ema_200": float(latest["ema_200"]),
            "macd": float(latest["macd"]),
            "macd_signal": float(latest["macd_signal"]),
            "macd_histogram": latest["macd_histogram"],
            "atr": float(latest["atr"]),
            "volume": float(latest["volume"]),
            "volume_avg_20": float(latest["volume_avg_20"]),
        }
    }