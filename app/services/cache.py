import redis
import json
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.redis_client = None

    async def set(self, key: str, value: dict, expire_seconds: int = 3600):
        """Set cache with TTL"""
        if not self.redis_client:
            return
        try:
            self.redis_client.setex(
                key, 
                expire_seconds, 
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Redis set error: {e}")

    async def get(self, key: str) -> dict | None:
        """Get cache value"""
        if not self.redis_client:
            return None
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None

    async def delete(self, key: str):
        """Delete cache key"""
        if not self.redis_client:
            return
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Redis delete error: {e}")

    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        if not self.redis_client:
            return
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Redis pattern delete error: {e}")

    async def is_connected(self) -> bool:
        """Check Redis connection status"""
        if not self.redis_client:
            return False
        try:
            self.redis_client.ping()
            return True
        except Exception:
            return False


cache = RedisCache()
