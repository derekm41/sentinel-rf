def detect_market_regime(df):
    """
    Detects the current market regime using trend, momentum, and volatility.

    Returns:
        str: "UPTREND", "DOWNTREND", "CHOPPY", or "HIGH_VOLATILITY"
    """

    latest = df.iloc[-1]

    price = latest["close"]
    ema_20 = latest["ema_20"]
    ema_50 = latest["ema_50"]
    ema_200 = latest["ema_200"]
    atr = latest["atr"]

    atr_percent = atr / price

    if atr_percent > 0.05:
        return "HIGH_VOLATILITY"

    if price > ema_200 and ema_20 > ema_50:
        return "UPTREND"

    if price < ema_200 and ema_20 < ema_50:
        return "DOWNTREND"

    return "CHOPPY"