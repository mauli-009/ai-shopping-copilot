import json
import redis
from app.config import settings

redis_client = None
if settings.REDIS_URL and settings.REDIS_URL.startswith(("redis://", "rediss://")):
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def cache_get(key: str):
    if redis_client is None:
        return None
    raw = redis_client.get(key)
    return json.loads(raw) if raw else None


def cache_set(key: str, value, ttl_seconds: int = 43200):  # 12 hours
    if redis_client is None:
        return
    redis_client.set(key, json.dumps(value), ex=ttl_seconds)


def cache_ping() -> bool:
    if redis_client is None:
        return False
    try:
        return redis_client.ping()
    except Exception:
        return False