
from app.services.strategies.trend_strategy import analyze_trend
from app.services.strategies.breakout_strategy import analyze_breakout
from app.services.strategies.mean_reversion_strategy import analyze_mean_reversion


MIN_CONFIDENCE = 60

def select_best_strategies(df, symbol: str):
    candidates = [
        analyze_trend(df, symbol),
        analyze_breakout(df, symbol),
        analyze_mean_reversion(df, symbol),
    ]

    latest = df.iloc[-1]
    atr = float(latest["atr"])

    for trade in candidates:
        entry = float(trade["entry"])
        direction = trade["direction"]

        if direction == "LONG":
            stop_loss = entry - atr * 1.5
            take_profit = entry + atr * 3
        else:
            stop_loss = entry + atr * 1.5
            take_profit = entry - atr * 3

        trade["risk"] = {
            "entry": round(entry, 2),
            "stop_loss": round(entry - atr * 1.5, 2),
            "take_profit": round(entry + atr * 3, 2),
            "risk_reward": 2.0,
        }

        trade["risk_reward"] = 2.0

    # Only keep reasonably strong setups
    valid_trades = [
        trade for trade in candidates
        if trade["confidence"] >= MIN_CONFIDENCE
    ]

    ranked = sorted(
        valid_trades,
        key=lambda x: x["confidence"],
        reverse=True
    )

    return ranked[:3]