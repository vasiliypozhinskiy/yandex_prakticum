from functools import lru_cache
from typing import Optional, List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from .mixin import ServiceMixin
from .utils import get_params_films_to_elastic, get_hits
from ..db.elastic import get_elastic
from ..db.redis import get_redis
from ..models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService(ServiceMixin):
    async def get_all_films(
            self,
            page_size: int,
            sorting: str = None,
            query: str = None,
            genre: str = None,
    ) -> Optional[dict]:
        _source: tuple = ("id", "title", "imdb_rating", "genre")
        body: dict = get_params_films_to_elastic(
            page_size=page_size, genre=genre, query=query
        )
        docs: Optional[dict] = await self.search_in_elastic(
            body=body, _source=_source, sort=sorting
        )
        if not docs:
            return None
        hits = get_hits(docs=docs, schema=Film)
        films: List[Film] = [
            Film(
                id = row.id, title=row.title, imdb_rating=row.imdb_rating
            )
            for row in hits
        ]
        return {
            "films": films,
            "page_size": page_size,
        }

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        # TODO: добавить кэширование с помощью redis
        # data = await self.redis.get(film_id)
        # if not data:
        #     return None
        #
        # film = Film.parse_raw(data)
        # return film
        pass

    async def _put_film_to_cache(self, film: Film):
        # TODO: добавить кэширование с помощью redis
        # await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)
        pass


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, index="movies")
