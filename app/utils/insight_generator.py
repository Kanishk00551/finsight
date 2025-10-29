# app/utils/insight_generator.py
def generate_insight(symbol, sentiment_score, trend):
    if sentiment_score > 0:
        sentiment_text = "positive"
    elif sentiment_score < 0:
        sentiment_text = "negative"
    else:
        sentiment_text = "neutral"
    
    trend_text = "upward" if trend == "uptrend" else "downward"
    return (
        f"{symbol} shows a {trend_text} market trend with overall "
        f"{sentiment_text} sentiment from recent financial news."
    )
