from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel


class Actor(BaseModel):
    id: UUID
    name: str


class Writer(BaseModel):
    id: UUID
    name: str


class ESModel(BaseModel):
    id: UUID
    imdb_rating: Optional[float]
    genre: Optional[str]
    title: str
    description: Optional[str]
    director: Optional[List[str]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    actors: Optional[List[Actor]]
    writers: Optional[List[Writer]]

