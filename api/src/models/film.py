from typing import Optional, List, Dict

from pydantic import validator

from models.base import BaseServiceModel


class Film(BaseServiceModel):
    """Для вывода полной инф-и по фильму и вывода на главной странице"""
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]
    genre: Optional[List[str]]
    director: Optional[Dict[str, str]]
    actors: Optional[List[Dict[str, str]]]
    writers: Optional[List[Dict[str, str]]]

    @staticmethod
    @validator('imdb_rating')
    def interval_rating(rating: float) -> float:
        if rating > 10 or rating < 0:
            raise ValueError('Проверьте rating')
        return rating
