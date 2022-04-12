from typing import Optional, Union, List

import orjson
from aioredis import Redis
from elasticsearch import NotFoundError

from core.config import CACHE_EXPIRE_IN_SECONDS
from db.db import AbstractDB
from models.base import BaseServiceModel
from services.utils.utils import create_hash_key


class BaseService:
    model = None
    index = None

    def __init__(self, cache: Redis, db: AbstractDB):
        self.cache = cache
        self.db = db

    async def get_by_id(self, id_: str) -> Optional[BaseServiceModel]:
        cached_data = await self._get_from_cache(id_)
        if not cached_data:
            data = await self._get_from_db(id_)
            if not data:
                return None
            await self._put_to_cache(id_, data)
        else:
            data = self.model(**orjson.loads(cached_data))
        return data

    async def get_many(self, search_type, **kwargs) -> Optional[List[BaseServiceModel]]:
        # Получаем данные из кэша
        cached_data = await self._get_from_cache(
            key=create_hash_key(index=self.index, params=kwargs)
        )

        if not cached_data:
            search_params = {}
            if kwargs.get('genre'):
                search_params.update({'genre': kwargs['genre']})
            if kwargs.get('query'):
                search_params.update({'query': kwargs['query']})
            if kwargs.get('person_id'):
                search_params.update({'person_id': kwargs['person_id']})

            params = {
                'model': self.model,
                'search_type': search_type,
                'page_size': kwargs.get('page_size'),
                'sorting': kwargs.get('sorting'),
                'search_params': search_params
            }

            data: Optional[List[BaseServiceModel]] = await self.db.search(self.index, params)

            if not data:
                return None
            # Записываем данные в кеш
            await self._put_data_to_cache(
                key=create_hash_key(index=self.index, params=kwargs), data=data
            )
        else:
            data: List[BaseServiceModel] = [
                self.model(**row) for row in orjson.loads(cached_data)
            ]

        return data

    async def _get_from_db(self, id_: str) -> Optional[BaseServiceModel]:
        try:
            data = await self.db.get_by_id(index=self.index, id_=id_)
        except NotFoundError:
            return None
        return self.model(**data)

    async def _put_to_cache(self, id_: str, model: BaseServiceModel):
        await self.cache.set(id_, model.json(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def _get_from_cache(self, key: str) -> Optional[bytes]:
        return await self.cache.get(key=key) or None

    async def _put_data_to_cache(self, key: str, data: Union[BaseServiceModel, List[BaseServiceModel]]) -> None:
        value = orjson.dumps([item.dict() for item in data])
        await self.cache.set(key=key, value=value, expire=CACHE_EXPIRE_IN_SECONDS)