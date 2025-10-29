# app/core/config.py
import os
import dotenv

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
DEFAULT_STOCKS = ["AAPL", "TSLA", "MSFT", "AMZN"]
