# File: streamlit_app.py
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="FinSight", layout="wide")

st.title("🚀 FinSight - AI Stock Analysis")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    symbol = st.text_input("Stock Symbol", "TSLA")
    analyze_btn = st.button("Analyze", type="primary")

if analyze_btn:
    with st.spinner(f"Analyzing {symbol}..."):
        # Call FastAPI
        response = requests.get(f"http://localhost:8001/analyze/{symbol}")
        data = response.json()
    
    # Display Results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${data['stock_data']['current_price']:.2f}",
            f"{data['stock_data']['price_change_percent']:.2f}%"
        )
    
    with col2:
        sentiment = data['sentiment']['score']
        st.metric("Sentiment", f"{sentiment:.2f}", 
                 data['sentiment']['interpretation'].upper())
    
    with col3:
        st.metric("Trend", data['trend'].upper())
    
    # AI Insights
    st.subheader("🤖 AI Analysis")
    st.info(data['insights'])
    
    # News
    st.subheader("📰 Latest News")
    for news in data['news_samples']:
        st.write(f"• {news}")
    
    # Historical Comparison (from MLflow)
    st.subheader("📊 Historical Performance")
    # Fetch from MLflow API
    # Plot with Plotly