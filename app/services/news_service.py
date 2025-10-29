# app/services/news_service.py

from newsapi import NewsApiClient
from app.core.config import NEWS_API_KEY

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_news(symbol: str):
    query = f"{symbol} stock OR {symbol} company"
    articles = newsapi.get_everything(
        q=query, language='en', sort_by='relevancy', page_size=10
    )
    news_list = [
        (a['title'] or '') + ". " + (a['description'] or '')
        for a in articles.get('articles', [])
    ]
    return news_list
