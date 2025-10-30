from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add your project to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services import stock_service, news_service
from app.ml import sentimentanalysis, trend_analysis
from app.utils import insight_generator
from mlops import FinSightTracker
from app.core.config import DEFAULT_STOCKS

# Initialize MLflow tracker
tracker = FinSightTracker()

def analyze_single_stock(symbol: str):
    """
    Analyze a single stock and log to MLflow
    """
    print(f"🔍 Analyzing {symbol}...")
    
    with tracker.start_analysis_run(symbol):
        try:
            # Log parameters
            tracker.log_stock_params(symbol)
            
            # 1. Fetch stock data
            stock_prices = stock_service.get_stock_prices(symbol)
            if stock_prices is None or stock_prices.empty:
                print(f"❌ No data for {symbol}")
                tracker.log_failure(f"No data found for {symbol}")
                return
            
            # Calculate metrics
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
            
            # 2. Fetch news
            news_articles = news_service.get_news(symbol)
            if not news_articles:
                news_articles = []
            tracker.log_news_metrics(len(news_articles))
            
            # 3. Sentiment analysis
            sentiment_score = sentimentanalysis.analyze_sentiment(news_articles)
            tracker.log_sentiment(sentiment_score)
            
            # 4. Trend analysis
            trend_summary = trend_analysis.analyze_trend(stock_prices)
            tracker.log_trend(trend_summary)
            
            # 5. Generate insight
            insights = insight_generator.generate_insight(symbol, sentiment_score, trend_summary)
            tracker.log_insight(insights)
            
            # Mark success
            tracker.log_success()
            
            print(f"✅ {symbol}: Price=${current_price:.2f}, Sentiment={sentiment_score:.2f}, Trend={trend_summary}")
            
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {str(e)}")
            tracker.log_failure(str(e))

def run_daily_analysis():
    """
    Analyze all default stocks
    """
    print(f"\n{'='*50}")
    print(f"🚀 Starting Daily Stock Analysis")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Stocks: {', '.join(DEFAULT_STOCKS)}")
    print(f"{'='*50}\n")
    
    for symbol in DEFAULT_STOCKS:
        analyze_single_stock(symbol)
    
    print(f"\n{'='*50}")
    print(f"✅ Daily Analysis Complete!")
    print(f"{'='*50}\n")

# Define DAG
default_args = {
    'owner': 'finsight',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'finsight_daily_stock_analysis',
    default_args=default_args,
    description='Daily automated stock analysis for FinSight',
    schedule_interval='0 9 * * *',  # Run daily at 9 AM
    catchup=False,
    tags=['stocks', 'mlops', 'daily'],
)

# Create task
daily_analysis_task = PythonOperator(
    task_id='analyze_default_stocks',
    python_callable=run_daily_analysis,
    dag=dag,
)
