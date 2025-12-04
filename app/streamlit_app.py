import streamlit as st
import requests
import time
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="FinSight AI Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Custom CSS for Styling ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .ai-report-box {
        background-color: #1e1e1e;
        color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Sidebar: System Status & Config ---
with st.sidebar:
    st.title("⚙️ System Status")
    
    # Check FastAPI Connection
    api_status = st.empty()
    try:
        response = requests.get("http://localhost:8001/", timeout=2)
        if response.status_code == 200:
            api_status.success("✅ Backend (FastAPI): Online")
        else:
            api_status.warning(f"⚠️ Backend: Status {response.status_code}")
    except requests.exceptions.ConnectionError:
        api_status.error("❌ Backend: Offline")
        st.info("💡 Tip: Run `uvicorn app.fastapi.main:app --reload --port 8001`")

    st.markdown("---")
    st.markdown("### 🤖 Model Info")
    st.text("Engine: Ollama (Local)")
    st.text("Model: Llama 3.2 / DeepSeek")
    
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# --- 4. Main Content Area ---
st.title("📈 FinSight AI")
st.markdown("### Intelligent Stock Market Analysis")

# Search Input
col1, col2 = st.columns([3, 1])
with col1:
    symbol = st.text_input("Enter Stock Ticker", value="AAPL", placeholder="e.g., NVDA, TSLA").upper()
with col2:
    st.write("##") # Spacing
    analyze_btn = st.button("🚀 Analyze Stock", type="primary")

# --- 5. Analysis Logic ---
if analyze_btn:
    if not symbol:
        st.toast("Please enter a stock symbol!", icon="⚠️")
    else:
        start_time = time.time()
        
        # UI Container for results
        result_container = st.container()
        
        with result_container:
            try:
                with st.spinner(f"Connecting to AI Agent... Reading news for {symbol}..."):
                    # Call FastAPI
                    response = requests.get(f"http://localhost:8001/analyze/{symbol}", timeout=120)
                    
                    if response.status_code == 200:
                        data = response.json()
                        stock = data.get("stock_data", {})
                        sentiment = data.get("sentiment", {})
                        
                        # --- Metrics Row ---
                        st.markdown("---")
                        m1, m2, m3, m4 = st.columns(4)
                        
                        # Price Metric
                        price = stock.get('current_price', 0)
                        change = stock.get('price_change', 0)
                        pct = stock.get('price_change_percent', 0)
                        
                        m1.metric("Current Price", f"${price:,.2f}", f"{change:+.2f} ({pct:+.2f}%)")
                        
                        # Sentiment Metric
                        sent_score = sentiment.get('score', 0)
                        sent_color = "normal"
                        if sent_score > 0.1: sent_color = "off" # Streamlit doesn't strictly support green metric delta without arrow
                        m2.metric("News Sentiment", f"{sent_score:.2f}", sentiment.get('interpretation', 'neutral').upper())
                        
                        # Trend Metric
                        trend = data.get('trend', 'Unknown')
                        trend_icon = "↗️" if "up" in trend.lower() else "↘️"
                        m3.metric("Market Trend", trend.upper(), trend_icon)
                        
                        # News Count
                        m4.metric("Articles Analyzed", data.get("news_count", 0))
                        
                        # --- AI Report Section ---
                        st.markdown("### 🧠 AI Analyst Report")
                        insight_text = data.get("insights", "No insights generated.")
                        
                        # Styled AI Box
                        st.markdown(f"""
                        <div class="ai-report-box">
                            {insight_text.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # --- Raw Data Expander ---
                        st.write("##")
                        with st.expander("📰 View Source News Headlines"):
                            for news in data.get("news_samples", []):
                                st.info(news)
                                
                        # Footer
                        elapsed = time.time() - start_time
                        st.caption(f"Analysis completed in {elapsed:.2f}s | MLflow Run ID: {data.get('mlflow_run_id', 'N/A')}")
                        st.toast("Analysis Complete!", icon="✅")
                        
                    elif response.status_code == 404:
                        st.error(f"❌ Stock '{symbol}' not found. Please check the ticker symbol.")
                    else:
                        st.error(f"❌ API Error: {response.status_code} - {response.text}")
                        
            except requests.exceptions.ConnectionError:
                st.error("🛑 Connection Refused. Please ensure FastAPI backend is running.")
                st.code("uvicorn app.fastapi.main:app --reload --port 8001")
            except Exception as e:
                st.error(f"⚠️ An unexpected error occurred: {str(e)}")