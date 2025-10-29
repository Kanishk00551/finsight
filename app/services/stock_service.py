# app/services/stock_service.py
import yfinance as yf

def get_stock_prices(symbol: str, period="1mo"):
    data = yf.download(symbol, period=period, interval="1d")
    if data.empty:
        return None
    return data['Close']
