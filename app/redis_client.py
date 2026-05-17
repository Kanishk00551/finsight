# app/redis_client.py
import redis, json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_cached(symbol):
    data = r.get(f"stock:{symbol}")
    return json.loads(data) if data else None

def set_cached(symbol, data, ttl=1800):
    r.setex(f"stock:{symbol}", ttl, json.dumps(data))
