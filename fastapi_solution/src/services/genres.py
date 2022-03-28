from functools import lru_cache
from typing import Optional, List
from uuid import UUID

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import CACHE_EXPIRE_IN_SECONDS
from services.films import FilmService
from services.utils import get_params_genres_to_elastic, get_hits, create_hash_key
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre


class GenreService(FilmService):
    async def get_all_genres(
            self,
            page_size: int,
            sorting: str = None,
            query: str = None,
    ) -> Optional[dict]:
        _source: tuple = ("id", "name", "films_ids")
        body: dict = get_params_genres_to_elastic(
            page_size=page_size
        )
        params = f"{page_size}{query}"
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

            genres: List[Genre] = get_hits(docs=docs, schema=Genre)
            """Записываем данные в кеш """
            data = orjson.dumps([i.dict() for i in genres])
            await self._put_data_to_cache(
                key=create_hash_key(index=self.index, params=params.lower()), value=data
            )
            return {
                "genres": genres,
                "page_size": page_size,
            }
        genres: List[Genre] = [
            Genre(**row) for row in orjson.loads(instance)
        ]

        return {
            "films": genres,
            "page_size": page_size,
        }

    async def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def _get_genre_from_elastic(self, genre_id: UUID) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _genre_from_cache(self, genre_id: UUID) -> Optional[Genre]:
        data = await self.redis.get(str(genre_id))
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(str(genre.id), genre.json(), expire=CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic, index="genres")
