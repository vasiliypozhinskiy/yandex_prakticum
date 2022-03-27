from functools import lru_cache
from typing import Optional, List
from uuid import UUID

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import CACHE_EXPIRE_IN_SECONDS
from services.films import FilmService
from services.mixin import ServiceMixin
from services.utils import get_params_persons_to_elastic, get_params_films_by_person_id_to_elastic, get_hits, \
    create_hash_key
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from models.film import ListResponseFilm


class PersonService(FilmService):
    async def get_all_persons(
            self,
            page_size: int,
            sorting: str = None,
            query: str = None
    ) -> Optional[dict]:
        _source: tuple = ("id", "full_name", "films_ids")
        body: dict = get_params_persons_to_elastic(
            page_size=page_size,
            query=query
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
            persons: List[Person] = get_hits(docs=docs, schema=Person)
            """Записываем данные в кеш """
            data = orjson.dumps([i.dict() for i in persons])
            await self._put_data_to_cache(
                key=create_hash_key(index=self.index, params=params.lower()), value=data
            )
            return {
                "persons": persons,
                "page_size": page_size,
            }
        persons_from_instance: List[Person] = [
            Person(**row) for row in orjson.loads(instance)
        ]
        return {
            "films": persons_from_instance,
            "page_size": page_size,
        }

    async def get_by_id(self, person_id: UUID) -> Optional[Person]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def get_films_by_person(
            self,
            person_id: UUID,
            page_size: int,
            sorting: str
    ) -> Optional[dict]:
        _source: tuple = ("id", "title", "imdb_rating")
        body: dict = get_params_films_by_person_id_to_elastic(
            page_size=page_size, person_id=person_id
        )

        docs: Optional[dict] = await self.search_in_elastic(
            body=body, _source=_source, sort=sorting, _index="movies"
        )
        if not docs:
            return None
        films = get_hits(docs=docs, schema=ListResponseFilm)
        return {
            "films": films,
            "page_size": page_size,
        }

    async def _get_person_from_elastic(self, person_id: UUID) -> Optional[Person]:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _person_from_cache(self, person_id: UUID) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(person.id, person.json(), expire=CACHE_EXPIRE_IN_SECONDS)
        pass


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic, index="persons")
