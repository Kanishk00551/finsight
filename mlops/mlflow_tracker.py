import mlflow
from datetime import datetime
from typing import Dict, Any
from mlops.config import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME

class FinSightTracker:
    """
    MLflow tracking wrapper for FinSight stock analysis
    """
    
    def __init__(self):
        """Initialize MLflow configuration"""
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    def start_analysis_run(self, symbol: str):
        """
        Start a new MLflow run for stock analysis
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            MLflow run context manager
        """
        run_name = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return mlflow.start_run(run_name=run_name)
    
    def log_stock_params(self, symbol: str):
        """Log stock analysis parameters"""
        mlflow.log_param("stock_symbol", symbol.upper())
        mlflow.log_param("timestamp", datetime.now().isoformat())
        mlflow.set_tag("analysis_type", "stock_insight")
    
    def log_stock_metrics(self, stock_data: Dict[str, float]):
        """
        Log stock price metrics
        
        Args:
            stock_data: Dict with current_price, price_change, price_change_percent
        """
        mlflow.log_metric("current_price", stock_data.get("current_price", 0))
        mlflow.log_metric("price_change", stock_data.get("price_change", 0))
        mlflow.log_metric("price_change_percent", stock_data.get("price_change_percent", 0))
    
    def log_news_metrics(self, news_count: int):
        """Log news analysis metrics"""
        mlflow.log_metric("news_count", news_count)
    
    def log_sentiment(self, sentiment_score: float):
        """
        Log sentiment analysis results
        
        Args:
            sentiment_score: Sentiment score between -1 and 1
        """
        mlflow.log_metric("sentiment_score", sentiment_score)
        
        # Add sentiment category as tag
        if sentiment_score > 0.2:
            sentiment_category = "positive"
        elif sentiment_score < -0.2:
            sentiment_category = "negative"
        else:
            sentiment_category = "neutral"
        
        mlflow.set_tag("sentiment_category", sentiment_category)
    
    def log_trend(self, trend_direction: str):
        """Log trend analysis results"""
        mlflow.log_param("trend_direction", trend_direction)
        mlflow.set_tag("trend", trend_direction)
    
    def log_insight(self, insight_text: str):
        """Save generated insight as artifact"""
        mlflow.log_text(insight_text, "insight.txt")
    
    def log_success(self):
        """Mark run as successful"""
        mlflow.log_param("status", "success")
        mlflow.set_tag("success", "true")
    
    def log_failure(self, error_message: str):
        """Log failure information"""
        mlflow.log_param("status", "failed")
        mlflow.log_param("error_message", error_message)
        mlflow.set_tag("success", "false")
    
    def get_current_run_id(self) -> str:
        """Get current MLflow run ID"""
        active_run = mlflow.active_run()
        return active_run.info.run_id if active_run else None