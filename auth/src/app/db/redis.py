import redis

redis = redis.Redis(
    host='redis',
    port='6379',
    password='123qwe'
)


def get_redis():
    return redis
