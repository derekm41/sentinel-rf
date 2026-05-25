import requests
import yfinance as yf

def get_crypto_candles(symbol: str, interval: str = "1h", period: str = "7d"):
    """
    Retrieves historical cryptocurrency candlestick data from Yahoo Finance.

    This function downloads OHLCV (Open, High, Low, Close, Volume)
    market data for a specified cryptocurrency trading pair and returns
    the data as a cleaned pandas DataFrame for indicator calculations
    and trading analysis.

    Parameters:
        symbol (str):
            Cryptocurrency ticker symbol without the USD suffix.
            Example: "ETH", "BTC", "SOL"

        interval (str):
            Candle timeframe interval.
            Examples: "5m", "15m", "1h", "1d"

        period (str):
            Historical lookback window to retrieve.
            Examples: "1d", "7d", "30d", "90d"

    Returns:
        pandas.DataFrame:
            Cleaned DataFrame containing historical OHLCV data.

    Raises:
        ValueError:
            Raised when no market data is returned for the symbol.

    Notes:
        - Uses Yahoo Finance as the market data provider.
        - Automatically formats symbols into the Yahoo Finance
          crypto ticker format (e.g., ETH -> ETH-USD).
        - Column names are normalized to lowercase for consistency
          across downstream indicator and strategy functions.
    """
    ticker = f"{symbol}-USD"

    df = yf.download(
        ticker,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=True,
    )

    if df.empty:
        raise ValueError(f"No market data found for {symbol}")
    
    if isinstance(df.columns, tuple) or hasattr(df.columns, "levels"):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    df = df.reset_index()

    df.columns = [
        str(col).lower().replace(" ", "_")
        for col in df.columns
    ]

    return df






def get_crypto_price(symbol: str):
    symbol = symbol.upper()
    product_id = f"{symbol}-USD"

    url = f"https://api.exchange.coinbase.com/products/{product_id}/ticker"

    response = requests.get(url, timeout=10)
    response.raise_for_status()


    data = response.json()

    return {
        "symbol": symbol,
        "price": float(data["price"]),
        "bid": float(data["bid"]),
        "ask": float(data["ask"]),
        "volume": float(data["volume"]),
    }