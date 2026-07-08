import ta   

def add_indicators(df):
    """
    Adds common technical indicators to the candle DataFrame.

    These indicators will be used by the strategy rules to determine
    whether a crypto asset has bullish, bearish, or neutral conditions.
    """
    """
    RSI Indicator
    """
    df["rsi"] = ta.momentum.RSIIndicator(
        close=df["close"],
        window=14
    ).rsi()

    """
    EMA Indicators
    """
    df["ema_20"] = ta.trend.EMAIndicator(
        close=df["close"],
        window=20
    ).ema_indicator()

    df["ema_50"] = ta.trend.EMAIndicator(
        close=df["close"],
        window=50
    ).ema_indicator()

    df["ema_200"] = ta.trend.EMAIndicator(
        close=df["close"],
        window=200
    ).ema_indicator()

    """
    MACD Indicator
    """
    macd = ta.trend.MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_histogram"] = df["macd"] - df["macd_signal"]

    """
    ATR Indicator
    """
    df["atr"] = ta.volatility.AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=14
    ).average_true_range()

    """
    Volume
    """

    df["volume_avg_20"] = df["volume"].rolling(window=20).mean()

    return df