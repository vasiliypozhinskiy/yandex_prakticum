from functools import lru_cache
from typing import Optional, List, Union

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from api.v1.response_model import ListResponseFilm, Film
from core.config import CACHE_EXPIRE_IN_SECONDS
from services.mixin import ServiceMixin, CacheMixin
from services.utils import get_params_films_to_elastic, get_hits, create_hash_key
from db.elastic import get_elastic
from db.redis import get_redis


class FilmService(ServiceMixin, CacheMixin):
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
        params = f"{page_size}{query}{genre}"
        """Получаем данные из кэша"""
        instance = await self._get_result_from_cache(
            key=create_hash_key(index=self.index, params=params.lower())
        )
        if not instance:
            docs: Optional[dict] = await self.search_in_elastic(
                body=body, _source=_source, sort=sorting
            )
            if not docs:
                return None
            hits = get_hits(docs=docs, schema=Film)
            films: List[Film] = [
                Film(
                    id=row.id, title=row.title, imdb_rating=row.imdb_rating
                )
                for row in hits
            ]
            """Записываем данные в кеш """
            data = orjson.dumps([i.dict() for i in films])
            await self._put_data_to_cache(
                key=create_hash_key(index=self.index, params=params.lower()), value=data
            )
            return {
                "films": films,
                "page_size": page_size,
            }
        films_from_instance: List[ListResponseFilm] = [
            ListResponseFilm(**row) for row in orjson.loads(instance)
        ]
        return {
            "films": films_from_instance,
            "page_size": page_size,
        }

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self.get_film_from_cache(film_id)
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

    async def get_film_from_cache(self, key: str) -> Optional[Film]:
        data = await self.redis.get(key)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(str(film.id), film.json(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def _get_result_from_cache(self, key: str) -> Optional[bytes]:
        return await self.redis.get(key=key) or None

    async def _put_data_to_cache(self, key: str, value: Union[bytes, str]) -> None:
        await self.redis.set(key=key, value=value, expire=CACHE_EXPIRE_IN_SECONDS)

@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, index="movies")
