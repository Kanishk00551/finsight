# app/ml/sentiment_model.py
from transformers import pipeline

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def analyze_sentiment(news_list):
    if not news_list:
        return 0
    results = sentiment_analyzer(news_list)
    score = sum(
        1 if r['label'] == 'positive' else -1 if r['label'] == 'negative' else 0
        for r in results
    ) / len(results)
    return score
