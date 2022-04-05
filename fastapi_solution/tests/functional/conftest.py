from typing import Optional

import aiohttp
import pytest
from urllib3 import HTTPResponse

from utils.connections import get_elastic, get_redis
from utils.settings import TestSettings
from testdata.es_schema.movies import Movies
from testdata.es_schema.persons import Persons
from testdata.es_schema.settings import settings as es_schema_settings


@pytest.fixture(scope='session')
async def es_client():
    client = get_elastic()
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = await get_redis()
    await client.flushall()
    yield client
    await client.flushall()
    await client.wait_closed()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='class')
async def create_movies_schema(es_client):
    await es_client.indices.delete('movies', ignore=404)
    await es_client.indices.create(
        index='movies',
        body={"settings": es_schema_settings, "mappings": Movies.mappings},
        ignore=400
    )

    yield
    await es_client.indices.delete('movies')


@pytest.fixture(scope='class')
async def create_persons_schema(es_client):
    await es_client.indices.delete('persons', ignore=400)
    await es_client.indices.create(
        index='persons',
        body={"settings": es_schema_settings, "mappings": Persons.mappings},
        ignore=400
    )

    yield
    await es_client.indices.delete('persons')


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> (dict, HTTPResponse):
        params = params or {}
        url = f'{TestSettings().dict()["service_url"]}{TestSettings().dict()["api_url"]}{method}'
        async with session.get(url, params=params) as response:
            # TODO разобраться, что не так к body в HTTPResponse
            body = await response.json()
            return body, HTTPResponse(
                body=body,
                headers=response.headers,
                status=response.status,
            )
    return inner
