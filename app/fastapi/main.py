from fastapi import FastAPI, HTTPException
from app.services import stock_service, news_service
from app.ml import sentimentanalysis, trend_analysis, llm_analysis  # Added llm_analysis
# from app.utils import insight_generator # (Optional) Keep if you want a fallback
from mlops import FinSightTracker

app = FastAPI(
    title="FinSight",
    description="AI-powered financial insight engine with MLOps tracking",
    version="1.2.0"
)

# Initialize tracker
tracker = FinSightTracker()

@app.get("/")
def root():
    return {"message": "🚀 FinSight backend is running successfully"}

@app.get("/analyze/{symbol}")
def analyze_stock(symbol: str):
    """
    Master endpoint: fetches stock data, related news, sentiment, and insights.
    Uses GenAI models for final report generation.
    """
    # Start MLflow tracking
    with tracker.start_analysis_run(symbol):
        try:
            # Log analysis parameters
            tracker.log_stock_params(symbol)
            
            # 1️⃣ Fetch stock data
            stock_prices = stock_service.get_stock_prices(symbol)
            
            if stock_prices is None or stock_prices.empty:
                tracker.log_failure(f"No data found for {symbol}")
                raise HTTPException(
                    status_code=404, 
                    detail=f"No stock data found for symbol: {symbol}"
                )
            
            # Extract metrics
            current_price = float(stock_prices.iloc[-1])
            previous_price = float(stock_prices.iloc[-2]) if len(stock_prices) > 1 else current_price
            price_change = current_price - previous_price
            price_change_pct = (price_change / previous_price * 100) if previous_price != 0 else 0
            
            stock_data = {
                "current_price": current_price,
                "previous_price": previous_price,
                "price_change": price_change,
                "price_change_percent": price_change_pct
            }
            
            # Log stock metrics
            tracker.log_stock_metrics(stock_data)

            # 2️⃣ Fetch related news
            news_articles = news_service.get_news(symbol)
            if not news_articles:
                news_articles = []
            
            # Log news metrics
            tracker.log_news_metrics(len(news_articles))

            # 3️⃣ Sentiment Analysis
            sentiment_score = sentimentanalysis.analyze_sentiment(news_articles)
            
            # Log sentiment
            tracker.log_sentiment(sentiment_score)

            # 4️⃣ Trend Analysis
            trend_summary = trend_analysis.analyze_trend(stock_prices)
            
            # Log trend
            tracker.log_trend(trend_summary)

            # 5️⃣ Generate AI Insights (Replaces old insight_generator)
            # Now passing the full data to the LLM
            insights = llm_analysis.generate_ai_report(
                symbol=symbol,
                stock_data=stock_data,
                sentiment=sentiment_score,
                trend=trend_summary,
                news=news_articles
            )
            
            # Log insight
            tracker.log_insight(insights)
            
            # Mark as successful
            tracker.log_success()
            
            # Get run ID for response
            run_id = tracker.get_current_run_id()

            return {
                "symbol": symbol,
                "stock_data": stock_data,
                "news_count": len(news_articles),
                "news_samples": news_articles[:3],
                "sentiment": {
                    "score": sentiment_score,
                    "interpretation": "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
                },
                "trend": trend_summary,
                "insights": insights,  # This will now contain the DeepSeek analysis
                "mlflow_run_id": run_id
            }
            
        except HTTPException as he:
            tracker.log_failure(str(he.detail))
            raise he
        except Exception as e:
            tracker.log_failure(str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing {symbol}: {str(e)}"
            )   