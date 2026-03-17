import redis
import json
from config import Config

redis_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True
)

def get_cached_recommendations(user_id): #lexon nga cache
    key = f"recommendations:{user_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cached_recommendations(user_id, recommendations, expire_seconds=300): #ruan ne cache per 300 sekonda
    key = f"recommendations:{user_id}"
    redis_client.setex(key, expire_seconds, json.dumps(recommendations))