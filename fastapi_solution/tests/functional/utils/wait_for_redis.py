import logging
import time

from redis import Redis
from redis.exceptions import ConnectionError

from settings import TestSettings


def get_redis():
    # TODO поменять на aioredis
    redis_settings = {
        'host': 'redis',
        'port': TestSettings().dict()["redis_port"]
    }

    if TestSettings().dict()['redis_password']:
        redis_settings.update({'password': TestSettings().dict()['redis_password']})

    return Redis(**redis_settings)


if __name__ == '__main__':
    while True:
        try:
            redis = get_redis()
            ping = redis.ping()
            if ping:
                break
        except ConnectionError:
            pass

        logging.warning('Wait for redis. Sleep 1 second.')
        time.sleep(1)
