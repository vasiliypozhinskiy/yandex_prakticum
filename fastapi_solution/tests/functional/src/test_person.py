import ast
import asyncio
import pytest
from http import HTTPStatus

from testdata.movies_data.get_by_person_id import person_data
from utils.hash_creater_for_redis import create_hash_key
from utils.validation import PersonValidation

check_list = ['id', 'full_name', 'film_ids']

@pytest.mark.usefixtures("create_persons_schema")
class TestPerson:
    async def test_person_by_id(self, make_get_request, redis_client):
        for person in person_data:
            person_id: str = person.get("id")
            # Выполнение запроса
            response = await make_get_request(f"persons/{person_id}")
            response_body = ast.literal_eval(response.data.decode('utf-8'))
            # Проверка результата Elastic
            assert response.status == HTTPStatus.OK
            for i in check_list:
                assert response_body.get(i) == person.get(i)
            # Проверка результата Redis
            assert await redis_client.get(key=person.get("id")) is not None
            await redis_client.flushall()
            assert await redis_client.get(key=person_id) is None

    async def test_search_person(self, make_get_request, redis_client):
        test_person: dict = person_data[1]
        query: str = "Jake"
        await asyncio.sleep(2)
        # Выполнение запроса
        response = await make_get_request(method="persons/search/", params={"query": query})
        response_body = ast.literal_eval(response.data.decode('utf-8'))
        response_person: dict = response_body.get("persons")[0]
        # Проверка результата Elastic
        assert response.status == HTTPStatus.OK
        assert PersonValidation(**response_person)
        for i in check_list:
            assert response_person.get(i) == test_person.get(i)
        assert query in test_person.get("full_name")
        # Проверка результата Redis
        page_size: int = response_body.get("page_size")
        params = f"{page_size}{query}"
        key: str = create_hash_key(
            index='persons', params=params.lower()
        )
        assert await redis_client.get(key=key) is not None
        await redis_client.flushall()
        assert await redis_client.get(key=key) is None

