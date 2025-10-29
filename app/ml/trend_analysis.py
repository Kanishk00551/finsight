# app/ml/trend_analysis.py
import numpy as np

def analyze_trend(prices):
    if prices is None or len(prices) < 2:
        return "no data"
    x = np.arange(len(prices))
    slope = np.polyfit(x, prices.values, 1)[0]
    return "uptrend" if slope > 0 else "downtrend"
