import asyncio
from typing import Optional

import pytest
import ast

from http import HTTPStatus

from testdata.movies_data.film_search_params import film_list_params
from testdata.movies_data.get_by_film_id import films_data, expected_film_data, expect_not_found_film_data
from utils.hash_creater_for_redis import create_hash_key
from utils.elastic_loader import ElasticLoader

check_list = ['id', 'title', 'imdb_rating', 'description', 'genre', 'actors', 'writers', 'director']

@pytest.mark.usefixtures("create_movies_schema")
class TestMovies:
    async def test_get_film_by_id(self, es_client, make_get_request, redis_client):
        response = await make_get_request(f"films/{expected_film_data['id']}")
        body = ast.literal_eval(response.data.decode('utf-8'))
        assert HTTPStatus.OK == response.status
        for i in check_list:
            assert expected_film_data.get(i) == body.get(i)
        assert redis_client.get(key=expected_film_data['id']) is not None
        await redis_client.flushall()
        assert await redis_client.get(key=expected_film_data['id']) is None
        # проверка несуществуеего фильма
        response = await make_get_request(f"films/{expect_not_found_film_data['id']}")
        assert HTTPStatus.NOT_FOUND == response.status

    @pytest.mark.parametrize(
        "method, query, expected_status",
        [
            *film_list_params
        ]
    )
    async def test_get_search_film(self, make_get_request, redis_client, method, query, expected_status):
        await asyncio.sleep(0.3)
        response = await make_get_request(method=f"{method}", params=query)
        body = ast.literal_eval(response.data.decode('utf-8'))
        if query.get("query") == "Sonic":
            assert body["films"] == []
        if query.get("query") == 'Star' and expected_status != HTTPStatus.NOT_FOUND:
            result_response = [res.get("title") for res in body["films"]]
            for row in result_response:
                assert query.get("query") in row

        if query.get("query"):
            page_size: int = body["page_size"]
            title: str = query.get("query")
            sort: Optional[str] = query.get("sort")
            genre: Optional[str] = query.get("genre")

            key: str = create_hash_key(
                index='movies',
                params=f"{title}{sort}{page_size}{genre}"
            )
            assert redis_client.get(key=key) is not None
            await redis_client.flushall()
            assert await redis_client.get(key=key) is None
