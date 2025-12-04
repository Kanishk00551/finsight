# app/ml/sentimentanalysis.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER (Uses <1MB RAM)
_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(news_list):
    """
    Analyzes sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner).
    Perfect for financial texts and headlines on low-resource servers.
    """
    if not news_list:
        return 0
    
    try:
        total_score = 0
        count = 0
        
        for text in news_list:
            # VADER is robust and doesn't need truncation
            scores = _analyzer.polarity_scores(text)
            # 'compound' is a normalized score between -1 (Negative) and +1 (Positive)
            total_score += scores['compound']
            count += 1
            
        if count == 0:
            return 0
            
        return total_score / count

    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 0
        
        
