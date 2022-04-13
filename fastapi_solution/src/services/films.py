from functools import lru_cache
from typing import Optional, List
from fastapi import Depends

from db.db import get_db, AbstractDB
from models.film import Film
from services.base import BaseService
from db.redis import get_redis, AbstractCache


class FilmService(BaseService):
    model = Film
    index = 'movies'

    async def get_by_id(self, id_: str) -> Optional[Film]:
        return await super().get_by_id(id_=id_)

    async def get_many(self, **kwargs) -> Optional[List[Film]]:
        return await super().get_many(search_type='films', **kwargs)

    async def get_films_by_person_id(self, **kwargs) -> Optional[List[Film]]:
        return await super().get_many(search_type='films_by_person_id', **kwargs)


@lru_cache()
def get_film_service(
        cache: AbstractCache = Depends(get_redis),
        db: AbstractDB = Depends(get_db)
) -> FilmService:
    return FilmService(cache, db)
