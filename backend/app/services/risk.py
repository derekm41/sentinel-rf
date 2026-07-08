def calculate_risk_levels(price, atr, account_size=1000, risk_percent=1.0):
    """
    Calculates entry, stop loss, take profit, risk/reward,
    and position size for a long trade.

    account_size: total account balance
    risk_percent: percent of account to risk per trade
    """

    entry = price
    stop_loss = price - (1.5 * atr)
    take_profit = price + (3 * atr)

    risk_per_unit = entry - stop_loss
    reward_per_unit = take_profit - entry

    dollar_risk = account_size * (risk_percent / 100)

    if risk_per_unit <= 0:
        position_size = 0
    else:
        position_size = dollar_risk / risk_per_unit

    risk_reward = reward_per_unit / risk_per_unit if risk_per_unit > 0 else 0

    return {
        "entry": round(entry, 2),
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_reward": round(risk_reward, 2),
        "risk_percent": risk_percent,
        "dollar_risk": round(dollar_risk, 2),
        "position_size": round(position_size, 6),
    }