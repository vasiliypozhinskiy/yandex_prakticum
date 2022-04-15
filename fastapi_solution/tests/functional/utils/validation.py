from typing import Optional, List, Dict
from uuid import UUID

from pydantic import BaseModel


class UUIDValidation(BaseModel):
    id: UUID


class FilmValidation(UUIDValidation):
    title: str
    description: Optional[str]
    imdb_rating: Optional[float]
    genre: Optional[List[str]]
    director: Optional[Dict[str, str]]
    actors: Optional[List[Dict[str, str]]]
    writers: Optional[List[Dict[str, str]]]


class PersonValidation(UUIDValidation):
    full_name: str
    roles: Optional[List[str]] = []
    films_ids: List[UUID] = []


class GenreValidation(UUIDValidation):
    name: str
    description: Optional[str] = None
    films_ids: Optional[List[UUID]]
