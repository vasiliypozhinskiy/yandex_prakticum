from typing import Optional, List, Dict

from pydantic import validator

from models.mixin import CommonMixin


class Film(CommonMixin):
    """Для вывода полной инф-и по фильму и вывода на главной странице"""
    title: str
    description: Optional[str] = None
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = None
    director: Optional[Dict[str, str]] = None
    actors: Optional[List[Dict[str, str]]] = None
    writers: Optional[List[Dict[str, str]]] = None

    @validator('imdb_rating')
    def interval_rating(cls, rating: float) -> float:
        if rating > 10 or rating < 0:
            raise ValueError('Проверьте rating')
        return rating