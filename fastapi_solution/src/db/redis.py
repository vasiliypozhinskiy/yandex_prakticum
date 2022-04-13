from typing import Optional
from aioredis import Redis
import backoff

redis: Optional[Redis] = None


@backoff.on_exception(backoff.expo, exception=Exception)
async def get_redis() -> Redis:
    return redis
