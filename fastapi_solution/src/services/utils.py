from typing import Optional, List

from pydantic import parse_obj_as

from fastapi_solution.src.services.mixin import Schemas


def get_params_films_to_elastic(
        page_size: int = 10, genre: str = None, query: str = None
) -> dict:
    films_search = None
    if genre:
        films_search = {"fuzzy": {"genre": {"value": genre}}}
    if query:
        body: dict = {
            "size": page_size,
            "query": {
                "bool": {
                    "must": {"match": {"title": {"query": query,
                                                 "fuzziness": "auto"}}},
                    "filter": films_search,
                }
            },
        }
    else:
        body: dict = {
            "size": page_size,
        }
    return body


def get_hits(docs: Optional[dict], schema: Schemas):
    hits: dict = docs.get("hits").get("hits")
    data: list = [row.get("_source") for row in hits]
    parse_data = parse_obj_as(List[schema], data)
    return parse_data
