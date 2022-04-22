import os

import redis

settings = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': os.getenv('REDIS_PORT', 6739)
}

if os.getenv('REDIS_PASSWORD'):
    settings.update({'password': os.getenv('REDIS_PASSWORD')})

redis = redis.Redis(**settings)


def get_redis():
    return redis
