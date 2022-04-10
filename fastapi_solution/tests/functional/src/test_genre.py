import ast
import asyncio
import json
import pytest
from http import HTTPStatus
from testdata.movies_data.get_data_genre import genre_data
from utils.hash_creater_for_redis import create_hash_key
from utils.validation import GenreValidation

from fastapi_solution.tests.functional.utils.validation import FilmValidation


@pytest.mark.usefixtures("create_genres_schema")
class TestGenre:
    async def test_genre_by_id(self, make_get_request, redis_client):
        for test_genre in genre_data:
            genre_id: str = test_genre.get("id")
            response = await make_get_request(method=f"genres/{genre_id}")
            response_body = ast.literal_eval(response.data.decode('utf-8'))
            # Проверка результата Elastic
            assert response.status == HTTPStatus.OK
            assert test_genre.get("id") == response_body.get("id")
            assert test_genre.get("name") == response_body.get("name")
            # Проверка результата Redis
            assert await redis_client.get(key=genre_id) is not None
            await redis_client.flushall()
            assert await redis_client.get(key=genre_id) is None

    async def test_list_genre(self, make_get_request, redis_client):
        await asyncio.sleep(1)
        response = await make_get_request(method="genres/")
        response_body = json.loads(response.data.decode('utf-8'))
        response_genres = response_body.get("genres")
        # Проверка результата Elastic
        n = response_genres[0]
        assert response.status == HTTPStatus.OK
        assert GenreValidation(**response_genres[0])
        assert len(response_body['genres']) == len(genre_data)
        for genre in genre_data:
            for response_genre in response_genres:
                if genre.get("id") == response_genre.get("id"):
                    assert genre.get("id") == response_genre.get("id")
                    assert genre.get("name") == response_genre.get("name")
        # Проверка Redis
        key: str = create_hash_key(
            index='genres', params=str(response_body.get("page_size"))
        )
        assert await redis_client.get(key=key) is not None
        await redis_client.flushall()
        assert await redis_client.get(key=key) is None