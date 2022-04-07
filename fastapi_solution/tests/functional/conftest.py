import asyncio
import inspect
from typing import Optional

import aiohttp
import pytest
from urllib3 import HTTPResponse

from utils.connections import get_elastic, get_redis
from utils.settings import TestSettings
from testdata.es_schema.movies import Movies
from testdata.es_schema.persons import Persons
from testdata.es_schema.settings import settings as es_schema_settings


def pytest_collection_modifyitems(config, items):
    """
    Магия, чтобы не надо было добавлять декоратор pytest.mark.asyncio перед каждым тестом
    """
    for item in items:
        if inspect.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)


@pytest.fixture(scope='session')
def event_loop():
    """
    Закрываем event loop только в конце сессии
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = get_elastic()
    await client.indices.delete('*')
    async with client:
        yield client


@pytest.fixture(scope='session')
async def redis_client():
    client = await get_redis()
    await client.flushdb()

    yield client

    await client.flushdb()
    client.close()
    await client.wait_closed()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    async with session:
        yield session


@pytest.fixture(scope='class')
async def create_movies_schema(es_client):
    await es_client.indices.create(
        index='movies',
        body={"settings": es_schema_settings, "mappings": Movies.mappings}
    )

    yield

    await es_client.indices.delete('movies')


@pytest.fixture(scope='class')
async def create_persons_schema(es_client):
    await es_client.indices.create(
        index='persons',
        body={"settings": es_schema_settings, "mappings": Persons.mappings}
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
