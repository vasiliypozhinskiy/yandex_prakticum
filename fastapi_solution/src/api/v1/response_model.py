from typing import Optional, List, Dict
from uuid import UUID

from pydantic import BaseModel

from models.mixin import CommonMixin, PageSizeMixin


class Film(BaseModel):
    """полная информация по фильму"""
    id: UUID
    title: str
    description: Optional[str] = None
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = None
    director: Optional[List[str]] = None
    actors: Optional[List[Dict[str, str]]] = None
    writers: Optional[List[Dict[str, str]]] = None


class Genre(BaseModel):
    """полная информация по жанру"""
    id: UUID
    name: str
    description: Optional[str]
    films_ids: List[UUID]

class Person(BaseModel):
    """полная информация по персоне"""
    id: UUID
    full_name: str
    films_ids: List[UUID]

class ListResponseFilm(CommonMixin):
    """Схема для всех фильмов"""
    title: str
    imdb_rating: Optional[float] = None


class FilmPage(PageSizeMixin):
    films: List[ListResponseFilm] = []


class GenrePage(PageSizeMixin):
    genres: List[Genre] = []


class PersonPage(PageSizeMixin):
    persons: List[Person] = []
