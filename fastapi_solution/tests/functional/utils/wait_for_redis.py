import logging
import time
import aioredis
import asyncio

from settings import TestSettings


async def get_redis():
    redis_settings = {
        'address': f'{TestSettings().dict()["redis_host"]}:{TestSettings().dict()["redis_port"]}',
    }

    if TestSettings().dict()['redis_password']:
        redis_settings.update({'password': TestSettings().dict()['redis_password']})

    return await aioredis.create_redis_pool(**redis_settings)


async def check_redis():
    while True:
        try:
            redis = await get_redis()
            response = await redis.ping(encoding='utf-8')
            if response == 'PONG':
                redis.close()
                break
        except ConnectionError:
            pass

        logging.warning('Wait for redis. Sleep 1 second.')
        time.sleep(1)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(check_redis())
