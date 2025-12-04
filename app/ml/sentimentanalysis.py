from transformers import pipeline


sentiment_analyzer = None

def get_analyzer():
    """
    Checks if 'sentiment_analyzer' is loaded. If not, loads it.
    """
    global sentiment_analyzer
    if sentiment_analyzer is None:
        print("⏳ Loading Sentiment Model... (First request only)")
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        print("✅ Sentiment Model Loaded!")
    return sentiment_analyzer

def analyze_sentiment(news_list):
    """
    This function signature matches your original code EXACTLY.
    """
    if not news_list:
        return 0
    
  
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
