from typing import Optional, List, Dict

import orjson
from pydantic import BaseModel, validator

from src.models.mixin import CommonMixin


class Film(CommonMixin):
    """Для вывода полной инф-и по фильму и вывода на главной странице"""
    title: str
    description: Optional[str] = None
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = None
    directors: Optional[List[Dict[str, str]]] = None
    actors: Optional[List[Dict[str, str]]] = None
    writers: Optional[List[Dict[str, str]]] = None

    @validator('imdb_rating')
    def interval_rating(self, rating: float) -> float:
        if rating > 10 or rating < 0:
            raise ValueError('Проверьте rating')
        return rating