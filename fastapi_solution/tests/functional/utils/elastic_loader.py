from typing import Optional, List
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from elasticsearch._async.helpers import async_bulk

from pydantic import BaseModel


class Actor(BaseModel):
    id: UUID
    name: str


class Writer(BaseModel):
    id: UUID
    name: str


class Director(BaseModel):
    id: UUID
    name: str


class ESFilm(BaseModel):
    id: UUID
    imdb_rating: Optional[float]
    genre: Optional[List[str]]
    title: str
    description: Optional[str]
    director: Optional[Director]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    actors: Optional[List[Actor]]
    writers: Optional[List[Writer]]


class ElasticLoader:
    def __init__(self, client: AsyncElasticsearch, index: str):
        self.client = client
        self.index = index

    async def load(self, data: list) -> None:
        await async_bulk(self.client, self.generate_docs(self.index, data))

    @staticmethod
    def generate_docs(index: str, data: list):
        return [{
            '_index': index,
            '_id': item['id'],
            '_source': item
        } for item in data]
