import ollama

def generate_ai_report(symbol, stock_data, sentiment, trend, news):
    """Generate detailed AI analysis using local LLM via Ollama"""
    
    # Construct the prompt with data
    prompt = f"""
    As a financial analyst, provide detailed analysis for {symbol}:
    
    Current Price: ${stock_data['current_price']}
    Price Change: {stock_data['price_change_percent']}%
    Sentiment Score: {sentiment}
    Trend: {trend}
    
    Recent News Headlines:
    {chr(10).join(news[:5])}
    
    Provide:
    1. Investment recommendation (Buy/Hold/Sell)
    2. Risk assessment (High/Medium/Low)
    3. Key factors driving the stock
    4. Short-term and long-term outlook
    """
    try:
        response = ollama.chat(
            model="deepseek-r1",  
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response['message']['content']
        
    except Exception as e:
        return f"Error generating report: {str(e)}"