from functools import lru_cache
from typing import Optional, List
from uuid import UUID

from aioredis import Redis
from fastapi import Depends

from services.base import BaseService
from db.db import AbstractDB, get_db
from db.redis import get_redis
from models.genre import Genre


class GenreService(BaseService):
    model = Genre
    index = 'genres'

    async def get_by_id(self, id_: str, **kwargs) -> Optional[Genre]:
        return await super().get_by_id(id_=id_)

    async def get_many(self, **kwargs) -> Optional[List[Genre]]:
        return await super().get_many(search_type='genres', **kwargs)


@lru_cache()
def get_genre_service(
        cache: Redis = Depends(get_redis),
        db: AbstractDB = Depends(get_db)
) -> GenreService:
    return GenreService(cache, db)
