import ta   

def add_indicators(df):
    """
    Adds common technical indicators to the candle DataFrame.

    These indicators will be used by the strategy rules to determine
    whether a crypto asset has bullish, bearish, or neutral conditions.
    """

    df["rsi"] = ta.momentum.RSIIndicator(
        close=df["close"],
        window=14
    ).rsi()

    df["ema_20"] = ta.trend.EMAIndicator(
        close=df["close"],
        window=20
    ).ema_indicator()

    df["ema_200"] = ta.trend.EMAIndicator(
        close=df["close"],
        window=200
    ).ema_indicator()

    macd = ta.trend.MACD(close=df["close"])

    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    return df