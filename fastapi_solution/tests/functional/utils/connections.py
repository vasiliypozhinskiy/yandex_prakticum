from elasticsearch import Elasticsearch, AsyncElasticsearch
import aioredis

from .settings import TestSettings


def get_elastic():
    es_settings = {
        'hosts': [TestSettings().dict()['es_host']]
    }

    if TestSettings().dict()['es_password']:
        es_settings.update({'auth': (TestSettings().dict()['es_user'], TestSettings().dict()['es_password'])})

    return AsyncElasticsearch(**es_settings)


async def get_redis():
    redis_settings = {
        'address': f'{TestSettings().dict()["redis_host"]}:{TestSettings().dict()["redis_port"]}'
    }

    if TestSettings().dict()['redis_password']:
        redis_settings.update({'password': TestSettings().dict()['redis_password']})

    return await aioredis.create_redis_pool(**redis_settings)
