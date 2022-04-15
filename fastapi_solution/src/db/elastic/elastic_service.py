from typing import Optional, List

import backoff
from db.db import AbstractDB
from elasticsearch import AsyncElasticsearch
from models.base import BaseServiceModel
from pydantic import parse_obj_as


class ElasticService(AbstractDB):

    def __init__(self, es):
        self.es: AsyncElasticsearch = es
        self.search_params_mapping = {
            'films': self.get_params_films,
            'films_by_person_id': self.get_params_films_by_person_id,
            'genres': self.get_params_genres,
            'persons': self.get_params_persons
        }

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    async def get_by_id(self, index, id_: str) -> Optional[BaseServiceModel]:
        doc = await self.es.get(index=index, id=id_)

        return doc['_source']

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    async def search(self, index, params) -> Optional[BaseServiceModel]:

        sorting = params.get('sorting')
        if sorting:
            if sorting.startswith('-'):
                sorting = f'{sorting[1::]}:desc'
            else:
                sorting = f'{sorting}:asc'

        body = self.search_params_mapping[params['search_type']](params['page_size'], **params['search_params'])

        data = await self.es.search(
            index=index, _source=params.get('source'), body=body, sort=sorting
        )
        return self._parse_data(data, params['model'])

    async def close(self):
        await self.es.close()

    @staticmethod
    def _parse_data(docs: Optional[dict], model):
        hits: dict = docs.get("hits").get("hits")
        data: list = [row.get("_source") for row in hits]
        parse_data = parse_obj_as(List[model], data)
        return parse_data

    @staticmethod
    def get_params_films(
            page_size: int,
            genre: str = None,
            query: str = None
    ) -> dict:

        films_search = None
        body: dict = {
            "size": page_size,
        }
        if genre:
            films_search = {"fuzzy": {"genre": {"value": genre}}}
        if query:
            body.update(
                {
                    "query":
                        {
                            "bool": {
                                "must": {"match": {"title": {"query": query,
                                                             "fuzziness": "auto"}}},
                            }
                        }
                }
            )
        if films_search:
            if body.get("query"):
                body["query"]["bool"].update({"filter": films_search})
            else:
                body.update({"query": {"bool": {"filter": films_search}}})
        return body

    @staticmethod
    def get_params_films_by_person_id(
            page_size: int,
            person_id: str
    ) -> dict:
        body = {
            "size": page_size,
        }
        actors_query = {"term": {"actors.id": person_id}}
        writers_query = {"term": {"writers.id": person_id}}
        director_query = {"term": {"director.id": person_id}}
        nested_actors_query = {"nested": {"path": "actors", "query": actors_query}}
        nested_writers_query = {"nested": {"path": "writers", "query": writers_query}}

        body.update({
            "query":
                {
                    "bool": {
                        "should":
                            [
                                nested_actors_query,
                                nested_writers_query,
                                director_query
                            ],
                    }
                }
        })
        return body

    @staticmethod
    def get_params_genres(page_size: int) -> dict:
        body = {
            "size": page_size
        }

        return body

    @staticmethod
    def get_params_persons(
            page_size: int,
            query: str = None
    ) -> dict:
        if query:
            body = {
                "size": page_size,
                "query": {
                    "bool": {
                        "must": {"match": {"full_name": {"query": query,
                                                         "fuzziness": "auto"}}},
                    }
                },
            }

        else:
            body = {
                "size": page_size,
            }

        return body
