def generate_trade_reason(result):
    """
    Generates a human-readable explanation for the
    trading recommendation.
    """

    recommendation = result["recommendation"]

    rules_passed = result["rules_passed"]
    rules_failed = result["rules_failed"]

    if recommendation == "BUY":
        return (
            "Bullish momentum and trend conditions are fully aligned. "
            "Price structure, RSI, and MACD confirmation support a potential long opportunity."
        )

    elif recommendation == "WATCHLIST":
        return (
            "Market conditions are improving, but not all bullish "
            "trend confirmations are fully aligned yet. "
            f"Strengths: {', '.join(rules_passed)}. "
            f"Weaknesses: {', '.join(rules_failed)}."
        )

    else:
        return (
            "Current market conditions do not show strong bullish alignment. "
            f"Failed conditions: {', '.join(rules_failed)}."
        )