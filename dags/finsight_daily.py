
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import time

def analyze_stock(symbol: str):
    """
    Call FastAPI endpoint to analyze a stock
    """
    try:
        print(f"🔍 Analyzing {symbol}...")
        
        # Call FastAPI running on host machine
        # Use host.docker.internal to reach Windows host from Docker
        response = requests.get(
            f"http://host.docker.internal:8001/analyze/{symbol}",
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            sentiment = result.get('sentiment', {}).get('score', 0)
            trend = result.get('trend', 'unknown')
            price = result.get('stock_data', {}).get('current_price', 0)
            
            print(f"✅ {symbol}: Price=${price:.2f}, Sentiment={sentiment:.2f}, Trend={trend}")
            return result
        else:
            print(f"❌ {symbol}: API returned status {response.status_code}")
            raise Exception(f"API error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"⏱️ {symbol}: Request timeout")
        raise
    except requests.exceptions.ConnectionError:
        print(f"🔌 {symbol}: Cannot connect to FastAPI. Is it running on port 8001?")
        raise
    except Exception as e:
        print(f"❌ {symbol}: Error - {str(e)}")
        raise

def analyze_aapl():
    return analyze_stock("AAPL")

def analyze_tsla():
    return analyze_stock("TSLA")

def analyze_msft():
    return analyze_stock("MSFT")

def analyze_amzn():
    return analyze_stock("AMZN")

# DAG configuration
default_args = {
    'owner': 'finsight',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

# Create DAG
dag = DAG(
    'finsight_daily_analysis',
    default_args=default_args,
    description='Daily stock analysis via FastAPI',
    schedule_interval='0 9 * * *',  # 9 AM daily
    catchup=False,
    tags=['stocks', 'finsight', 'mlops'],
)

# Create tasks (run in parallel)
task_aapl = PythonOperator(
    task_id='analyze_aapl',
    python_callable=analyze_aapl,
    dag=dag,
)

task_tsla = PythonOperator(
    task_id='analyze_tsla',
    python_callable=analyze_tsla,
    dag=dag,
)

task_msft = PythonOperator(
    task_id='analyze_msft',
    python_callable=analyze_msft,
    dag=dag,
)

task_amzn = PythonOperator(
    task_id='analyze_amzn',
    python_callable=analyze_amzn,
    dag=dag,
)