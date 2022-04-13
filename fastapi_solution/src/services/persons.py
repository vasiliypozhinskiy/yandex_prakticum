from functools import lru_cache
from typing import Optional, List
from fastapi import Depends

from services.base import BaseService
from db.db import AbstractDB, get_db
from db.redis import get_redis, AbstractCache
from models.person import Person


class PersonService(BaseService):
    model = Person
    index = 'persons'

    async def get_by_id(self, id_: str, **kwargs) -> Optional[Person]:
        return await super().get_by_id(id_=id_)

    async def get_many(self, **kwargs) -> Optional[List[Person]]:
        return await super().get_many(search_type='persons', **kwargs)


@lru_cache()
def get_person_service(
        redis: AbstractCache = Depends(get_redis),
        elastic: AbstractDB = Depends(get_db),
) -> PersonService:
    return PersonService(redis, elastic)
