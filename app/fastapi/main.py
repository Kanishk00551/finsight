from fastapi import FastAPI
from app.services import stock_service, news_service
from app.ml import sentimentanalysis, trend_analysis
from app.utils import insight_generator

app = FastAPI(
    title="FinSight",
    description="AI-powered financial insight engine combining stock data, news, and sentiment",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "🚀 FinSight backend is running successfully"}

@app.get("/analyze/{symbol}")
def analyze_stock(symbol: str):
    """
    Master endpoint: fetches stock data, related news, sentiment, and insights.
    """
    # 1 Fetch stock data
    stock_data = stock_service.get_stock_info(symbol)

    # 2️ Fetch related news
    news_articles = news_service.get_latest_news(symbol)

    # 3️ Sentiment Analysis on news
    sentiment_score = sentimentanalysis.analyze_news_sentiment(news_articles)

    # 4️ Trend Analysis on stock
    trend_summary = trend_analysis.get_trend(stock_data)

    # 5️ Generate Insights
    insights = insight_generator.generate_insights(symbol, stock_data, sentiment_score, trend_summary)

    return {
        "symbol": symbol,
        "stock_data": stock_data,
        "news": news_articles,
        "sentiment": sentiment_score,
        "trend": trend_summary,
        "insights": insights
    }
