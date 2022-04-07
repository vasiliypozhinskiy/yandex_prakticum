from elasticsearch import AsyncElasticsearch
import aioredis

from .settings import TestSettings


def get_elastic():
    es_settings = {
        'hosts': [TestSettings().es_host]
    }

    if TestSettings().es_password:
        es_settings.update({'auth': (TestSettings().es_user, TestSettings().es_password)})

    return AsyncElasticsearch(**es_settings)


async def get_redis():
    redis_settings = {
        'address': f'{TestSettings().redis_host}:{TestSettings().redis_port}'
    }

    if TestSettings().redis_password:
        redis_settings.update({'password': TestSettings().redis_password})

    return await aioredis.create_redis_pool(**redis_settings)
