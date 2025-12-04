import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

# Configure the API
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    print("WARNING: GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)

def generate_ai_report(symbol, stock_data, sentiment, trend, news):
    """
    Generate detailed AI analysis using Google Gemini API.
    Replaces local Ollama execution to prevent system crashes.
    """
    

    news_text = ""
    if news and isinstance(news, list):
        news_text = "\n".join(news[:5])
    
   
    prompt = f"""
    You are a professional financial analyst. Provide a detailed analysis for the stock {symbol}.
    
    Data:
    - Current Price: ${stock_data.get('current_price', 'N/A')}
    - Price Change: {stock_data.get('price_change_percent', 'N/A')}%
    - Sentiment Score: {sentiment}
    - Trend: {trend}
    
    Recent News Headlines:
    {news_text}
    
    Please provide a structured report with:
    1. Investment Recommendation (Buy/Hold/Sell)
    2. Risk Assessment (High/Medium/Low)
    3. Key Driving Factors
    4. Short-term vs Long-term Outlook
    """

    try:
       
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
      
        return response.text
        
    except Exception as e:
      
        error_msg = f"Error generating report via Gemini: {str(e)}"
        print(error_msg)
        return error_msg