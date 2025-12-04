# 🚀 FinSight - AI-Powered Stock Insight Generator

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green.svg)](https://fastapi.tiangolo.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange.svg)](https://mlflow.org/)
[![Airflow](https://img.shields.io/badge/Airflow-3.1.1-red.svg)](https://airflow.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

An intelligent backend system that generates AI-powered insights for stock market analysis by combining real-time market data, news sentiment analysis, and trend detection with complete MLOps tracking.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [MLOps Integration](#-mlops-integration)
- [Automation](#-automation)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- 🔍 **Real-time Stock Analysis** - Fetch live market data using Yahoo Finance API
- 📰 **News Sentiment Analysis** - Analyze financial news using RoBERTa transformer model
- 📈 **Trend Detection** - Calculate stock trends using linear regression
- 🤖 **AI Insight Generation** - Generate human-readable summaries combining all analyses

### MLOps & Automation
- 📊 **MLflow Tracking** - Track every analysis with metrics, parameters, and artifacts
- ⏰ **Airflow Automation** - Schedule daily automated stock analysis
- 🐳 **Docker Deployment** - Containerized Airflow setup for production
- 📦 **Experiment Management** - Compare analyses across stocks and time periods

### Production Ready
- ✅ **RESTful API** - Built with FastAPI for high performance
- 🔄 **Async Processing** - Handle multiple requests efficiently
- 📝 **Comprehensive Logging** - Track all operations and errors
- 🔒 **Environment-based Config** - Secure API key management

---

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  ┌─────────────────────────────────┐   │
│  │  /analyze/{symbol} endpoint     │   │
│  └─────────────────────────────────┘   │
└───────┬──────────────┬──────────────────┘
        │              │
        ▼              ▼
┌──────────────┐  ┌──────────────┐
│   Services   │  │  ML Models   │
│              │  │              │
│ Stock Data   │  │ Sentiment    │
│ News API     │  │ Trend        │
│ Yahoo Finance│  │ Insight Gen  │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
        ┌──────────────┐
        │   MLflow     │
        │  Tracking    │
        └──────────────┘
                │
                ▼
        ┌──────────────┐
        │  Airflow     │
        │ Automation   │
        └──────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.11** - Core programming language
- **Uvicorn** - ASGI server for production

### Data & APIs
- **yfinance** - Yahoo Finance API for stock data
- **NewsAPI** - Financial news aggregation
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Machine Learning
- **Transformers (Hugging Face)** - Pre-trained RoBERTa sentiment model
- **PyTorch** - Deep learning framework
- **CardiffNLP/twitter-roberta-base-sentiment-latest** - Fine-tuned sentiment model

### MLOps
- **MLflow** - Experiment tracking, model registry
- **Apache Airflow** - Workflow orchestration
- **Docker & Docker Compose** - Containerization
- **PostgreSQL** - Airflow metadata database
- **Redis** - Airflow task queue

---

## 📁 Project Structure

```
finsight/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuration & environment variables
│   ├── fastapi/
│   │   ├── __init__.py
│   │   └── main.py                # FastAPI application entry point
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── sentimentanalysis.py  # Sentiment analysis model
│   │   └── trend_analysis.py     # Trend detection model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── news_service.py       # NewsAPI integration
│   │   └── stock_service.py      # Yahoo Finance integration
│   └── utils/
│       ├── __init__.py
│       └── insight_generator.py  # AI insight generation
│
├── mlops/
│   ├── __init__.py
│   ├── config.py                  # MLflow configuration
│   └── mlflow_tracker.py         # MLflow tracking wrapper
│
├── dags/
│   └── finsight_daily.py         # Airflow DAG for automation
│
├── mlruns/                        # MLflow experiment data
├── logs/                          # Airflow logs
├── plugins/                       # Airflow plugins
├── config/                        # Airflow config
│
├── docker-compose.yaml           # Airflow Docker setup
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (not in git)
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Docker Desktop (for Airflow)
- NewsAPI Key ([Get free key](https://newsapi.org/register))

### Step 1: Clone Repository
```bash
git clone https://github.com/Kanishk00551/finsight.git
cd finsight
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create `.env` file:
```bash
NEWS_API_KEY=your_newsapi_key_here
AIRFLOW_UID=50000
```

### Step 5: Create Required Folders
```bash
mkdir -p dags logs plugins config mlruns
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# NewsAPI Configuration
NEWS_API_KEY=your_newsapi_key_here

# Airflow Configuration
AIRFLOW_UID=50000

# MLflow Configuration (optional)
MLFLOW_TRACKING_URI=./mlruns
MLFLOW_EXPERIMENT_NAME=finsight-stock-analysis
```

### Default Stocks

Edit `app/core/config.py` to change default stocks:

```python
DEFAULT_STOCKS = ["AAPL", "TSLA", "MSFT", "AMZN"]
```

---

## 🎯 Usage

### Quick Start (All Services)

**Terminal 1 - MLflow UI:**
```bash
cd finsight
source venv/bin/activate  # Windows: venv\Scripts\activate
mlflow ui --host 127.0.0.1 --port 5000
```

**Terminal 2 - FastAPI:**
```bash
cd finsight
source venv/bin/activate
uvicorn app.fastapi.main:app --reload --port 8001
```

**Terminal 3 - Airflow (Docker):**
```bash
cd finsight
docker-compose up
```

### Access Points
- **FastAPI Docs:** http://localhost:8001/docs
- **MLflow Dashboard:** http://localhost:5000
- **Airflow UI:** http://localhost:8080
  - Username: `airflow`
  - Password: `airflow`

---

## 📡 API Endpoints

### Analyze Stock

**Endpoint:** `GET /analyze/{symbol}`

**Example Request:**
```bash
curl http://localhost:8001/analyze/TSLA
```

**Example Response:**
```json
{
  "symbol": "TSLA",
  "stock_data": {
    "current_price": 461.01,
    "previous_price": 460.55,
    "price_change": 0.46,
    "price_change_percent": 0.099
  },
  "news_count": 10,
  "news_samples": [
    "Tesla reveals cheaper Model Y...",
    "Jim Cramer on Tesla CEO...",
    "Tesla's Optimus robot..."
  ],
  "sentiment": {
    "score": 0.2,
    "interpretation": "positive"
  },
  "trend": "uptrend",
  "insights": "TSLA shows an upward market trend with overall positive sentiment from recent financial news.",
  "mlflow_run_id": "abc123xyz456"
}
```

### Root Endpoint

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "🚀 FinSight backend is running successfully"
}
```

---

## 📊 MLOps Integration

### MLflow Tracking

Every analysis is automatically logged with:

**Parameters:**
- `stock_symbol` - Stock ticker
- `timestamp` - Analysis time
- `trend_direction` - Market trend
- `status` - Success/failure

**Metrics:**
- `current_price` - Latest stock price
- `price_change` - Price movement
- `price_change_percent` - Percentage change
- `sentiment_score` - News sentiment (-1 to 1)
- `news_count` - Number of articles analyzed

**Artifacts:**
- `insight.txt` - Generated insight text

**Tags:**
- `model_version` - System version
- `sentiment_model` - ML model used
- `sentiment_category` - Positive/negative/neutral

### Viewing Results

1. Open MLflow UI: http://localhost:5000
2. Click on "finsight-stock-analysis" experiment
3. View all runs in table format
4. Compare metrics across different stocks
5. Filter by parameters or metrics

### Example Queries

**Compare sentiment across stocks:**
```
Sort by: metrics.sentiment_score DESC
```

**Find analyses with positive sentiment:**
```
metrics.sentiment_score > 0
```

**Filter by specific stock:**
```
params.stock_symbol = "TSLA"
```

---

## ⏰ Automation

### Airflow DAG

The `finsight_daily_analysis` DAG:
- **Schedule:** Daily at 9:00 AM
- **Tasks:** Analyze AAPL, TSLA, MSFT, AMZN
- **Execution:** Tasks run in parallel
- **Retry Logic:** 2 retries with 3-minute delay

### Manual Trigger

1. Open Airflow UI: http://localhost:8080
2. Find "finsight_daily_analysis" DAG
3. Toggle it **ON**
4. Click "Trigger DAG" button

### Customize Schedule

Edit `dags/finsight_daily.py`:

```python
# Daily at 9 AM
schedule_interval='0 9 * * *'

# Every 6 hours
schedule_interval='0 */6 * * *'

# Every Monday at 9 AM
schedule_interval='0 9 * * 1'

# Hourly
schedule_interval='@hourly'
```

---

## 🔧 Development

### Running Tests

```bash
pytest app/tests/
```

### Code Formatting

```bash
black app/
flake8 app/
```

### Adding New Stocks

Edit `app/core/config.py`:

```python
DEFAULT_STOCKS = ["AAPL", "TSLA", "MSFT", "AMZN", "GOOGL", "META"]
```

### Adding New Features

1. Create feature branch
2. Implement in appropriate module
3. Add tests
4. Update documentation
5. Submit pull request

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ImportError: cannot import name 'NewsApiClient'`
```bash
pip uninstall newsapi
pip install newsapi-python
```

**Issue:** `protobuf version conflict`
```bash
pip uninstall protobuf
pip install protobuf==3.20.3
```

**Issue:** Port already in use
```bash
# Change port in startup command
uvicorn app.fastapi.main:app --port 8002
mlflow ui --port 5001
```

**Issue:** Docker not starting
- Ensure Docker Desktop is running
- Check Docker has enough resources (4GB+ RAM)
- Restart Docker Desktop

**Issue:** Airflow DAG not appearing
- Check `dags/` folder location
- Verify DAG file has no syntax errors
- Check Airflow logs in `logs/dag_processor/`

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Kanishk** - [@Kanishk00551](https://github.com/Kanishk00551)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [MLflow](https://mlflow.org/) - MLOps platform
- [Apache Airflow](https://airflow.apache.org/) - Workflow orchestration
- [CardiffNLP](https://huggingface.co/cardiffnlp) - Pre-trained sentiment models
- [NewsAPI](https://newsapi.org/) - News data provider
- [Yahoo Finance](https://finance.yahoo.com/) - Stock data

---



---



---

**⭐ If you find this project helpful, please give it a star!**


Impact: Reduced manual analysis time by 90%, enabled data-driven investment decisions through automated sentiment tracking and trend detection across 4+ major stocks.
