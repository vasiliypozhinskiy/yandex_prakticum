from typing import Optional, List
from uuid import UUID

from pydantic import parse_obj_as

from services.mixin import Schemas


def get_params_films_to_elastic(
        page_size: int = 10,
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


def get_params_films_by_person_id_to_elastic(page_size: int, person_id: UUID = None):
    body: dict = {
        "size": page_size,
    }
    actors_query = {"term": {"actors.id": person_id}}
    writers_query = {"term": {"writers.id": person_id}}
    director_query = {"term": {"director.id": person_id}}
    nested_actors_query = {"nested": {"path": "actors", "query": actors_query}}
    nested_writers_query = {"nested": {"path": "writers", "query": writers_query}}

    body.update(
        {"query":
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
        }
    )
    return body


def get_params_genres_to_elastic(page_size: int = 10) -> dict:
    body: dict = {
        "size": page_size
    }

    return body


def get_params_persons_to_elastic(query: str, page_size: int = 10) -> dict:
    if query:
        body: dict = {
            "size": page_size,
            "query": {
                "bool": {
                    "must": {"match": {"full_name": {"query": query,
                                                     "fuzziness": "auto"}}},
                }
            },
        }
    else:
        body: dict = {
            "size": page_size
        }

    return body


def get_hits(docs: Optional[dict], schema: Schemas):
    hits: dict = docs.get("hits").get("hits")
    data: list = [row.get("_source") for row in hits]
    parse_data = parse_obj_as(List[schema], data)
    return parse_data
