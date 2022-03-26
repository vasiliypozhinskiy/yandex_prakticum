from typing import Optional, List
import hashlib
from pydantic import parse_obj_as

from services.mixin import Schemas


def get_params_films_to_elastic(
        page_size: int = 10, genre: str = None, query: str = None
) -> dict:

    films_search = None
    print(genre, query)
    if genre:
        films_search = {"fuzzy": {"genre": {"value": genre}}}

    if query and genre:
        print('query')
        body: dict = {
            "size": page_size,
            "query": {
                "bool": {
                    "must": {"match": {"title": {"query": query, "fuzziness": "auto"}}},
                }
            },
        }
    elif query and not genre:
        body: dict = {
            "size": page_size,
            "query": {
                "bool": {
                    "must": {"match": {"title": {"query": query, "fuzziness": "auto"}}},
                }
            },
        }
    elif not query and not genre:
        body: dict = {
            "size": page_size,
        }

    else:
        print('else')
        body: dict = {
            "size": page_size,
            "query": {
                "bool": {
                    "must": {
                        "match_all": {},
                    },
                    "filter": films_search,
                }
            },
        }
    return body


def get_hits(docs: Optional[dict], schema: Schemas):
    hits: dict = docs.get("hits").get("hits")
    data: list = [row.get("_source") for row in hits]
    parse_data = parse_obj_as(List[schema], data)
    return parse_data

def create_hash_key(index: str, params: str) -> str:
    """Хешируем ключ по индексу и параметрам запроса """
    hash_key = hashlib.md5(params.encode()).hexdigest()
    return f"{index}:{hash_key}"

