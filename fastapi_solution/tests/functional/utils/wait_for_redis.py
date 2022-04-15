import asyncio

import aioredis
import backoff

from settings import TestSettings


class RedisNotReadyError(Exception):
    pass


async def get_redis():
    redis_settings = {
        'address': f'{TestSettings().redis_host}:{TestSettings().redis_port}',
    }

    if TestSettings().redis_password:
        redis_settings.update({'password': TestSettings().redis_password})

    return await aioredis.create_redis_pool(**redis_settings)


async def check_redis():
    redis = await get_redis()
    response = await redis.ping(encoding='utf-8')

    if response == 'PONG':
        redis.close()
    else:
        raise RedisNotReadyError


@backoff.on_exception(backoff.expo, exception=(OSError, RedisNotReadyError), max_time=30)
def main():
    asyncio.get_event_loop().run_until_complete(check_redis())


if __name__ == '__main__':
    main()