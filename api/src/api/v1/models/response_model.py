from typing import Optional, List, Dict
from uuid import UUID

from pydantic import BaseModel


class FilmDetailResponse(BaseModel):
    """полная информация по фильму"""
    id: UUID
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]
    genre: Optional[List[str]]
    director: Optional[Dict[str, str]]
    actors: Optional[List[Dict[str, str]]]
    writers: Optional[List[Dict[str, str]]]


class GenreDetailResponse(BaseModel):
    """полная информация по жанру"""
    id: UUID
    name: str
    description: Optional[str]
    films_ids: List[UUID]


class PersonDetailResponse(BaseModel):
    """полная информация по персоне"""
    id: UUID
    full_name: str
    films_ids: List[UUID]


class ListResponseFilm(BaseModel):
    """Схема для всех фильмов"""
    id: UUID
    title: str
    imdb_rating: Optional[float] = None


class FilmPageResponse(BaseModel):
    films: List[ListResponseFilm] = []
    page_size: int


class GenrePageResponse(BaseModel):
    genres: List[GenreDetailResponse] = []
    page_size: int


class PersonPageResponse(BaseModel):
    persons: List[PersonDetailResponse] = []
    page_size: int
