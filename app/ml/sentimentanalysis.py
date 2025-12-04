# app/ml/sentimentanalysis.py
from transformers import pipeline

# 1. Initialize as None (Empty) so it uses 0 RAM at startup
_sentiment_analyzer = None

def get_analyzer():
    """
    Singleton pattern: Only load the heavy model if it hasn't been loaded yet.
    """
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        print("⏳ Loading Sentiment Model... (This takes a few seconds on first run)")
        _sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        print("✅ Sentiment Model Loaded Successfully!")
    return _sentiment_analyzer

def analyze_sentiment(news_list):
    """
    Analyzes sentiment of a list of news headlines.
    This function signature matches your existing code exactly.
    """
    if not news_list:
        return 0
    
    # 2. Load the model NOW (Lazy Loading) instead of at top of file
    analyzer = get_analyzer()
    
    try:
        results = analyzer(news_list)
        score = sum(
            1 if r['label'] == 'positive' else -1 if r['label'] == 'negative' else 0
            for r in results
        ) / len(results)
        return score
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 0
