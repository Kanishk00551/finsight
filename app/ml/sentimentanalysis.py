from transformers import pipeline


sentiment_analyzer = None

def get_analyzer():
    """
    Singleton pattern: Loads the model only when needed.
    """
    global sentiment_analyzer
    if sentiment_analyzer is None:
        print("⏳ Loading Light Sentiment Model...")
        # Use a smaller model (DistilBERT) to stay under the 512MB RAM limit
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        print("✅ Light Sentiment Model Loaded!")
    return sentiment_analyzer

def analyze_sentiment(news_list):
    """
    Analyzes sentiment of a list of news headlines.
    """
    if not news_list:
        return 0
    
    # Load the model if it's not ready yet
    analyzer = get_analyzer()
    
    try:
   
        shortened_news = [text[:512] for text in news_list]
        
        results = analyzer(shortened_news)
        
        # Calculate score (Model labels are slightly different: POSITIVE/NEGATIVE)
        score = sum(
            1 if r['label'] == 'POSITIVE' else -1 if r['label'] == 'NEGATIVE' else 0
            for r in results
        ) / len(results)
        
        return score
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 0
