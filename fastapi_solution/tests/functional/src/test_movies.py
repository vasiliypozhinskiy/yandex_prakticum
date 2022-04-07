import pytest

from testdata.movies_data.get_by_id import films_data, expected_film_data, expect_not_found_film_data
from http import HTTPStatus

from utils.elastic_loader import ElasticLoader


@pytest.mark.usefixtures("create_movies_schema")
class TestMovies:

    async def test_get_film_by_id(self, es_client, make_get_request, redis_client):
        loader = ElasticLoader(es_client, 'movies')
        await loader.load(films_data)
        body, response = await make_get_request(f"/films/{expected_film_data['id']}")

        data_list = ['id', 'title', 'imdb_rating', 'description', 'genre', 'actors', 'writers', 'director']
        assert HTTPStatus.OK == response.status

        for i in data_list:
            assert expected_film_data.get(i) == body.get(i)

        assert redis_client.get(key=expected_film_data['id']) is not None
        await redis_client.flushall()
        assert await redis_client.get(key=expected_film_data['id']) is None

        # проверка несуществуеего фильма
        _, response = await make_get_request(f"/films/{expect_not_found_film_data['id']}")
        assert HTTPStatus.NOT_FOUND == response.status
