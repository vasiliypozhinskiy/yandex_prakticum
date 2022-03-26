from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from models.film import Film
from models.genre import Genre
from models.person import Person

Schemas: tuple = (Film, Genre, Person)


class ServiceMixin:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index):
        self.index = index
        self.total_count: int = 0
        # self.redis = redis
        self.elastic = elastic

    async def search_in_elastic(
        self, body: dict, _source=None, sort=None, _index=None
    ) -> Optional[dict]:

        if not _index:
            _index = self.index
        sort_field = sort[0] if not isinstance(sort, str) and sort else sort
        if sort_field:
            order = "desc" if sort_field.startswith("-") else "asc"
            sort_field = f"{sort_field.strip('-')}:{order}"

        return await self.elastic.search(
            index=_index, _source=_source, body=body, sort=sort_field
        )
