from http import HTTPStatus

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.v1.utils import GenreQueryParams
from services.genres import GenreService, get_genre_service
from models.genre import GenrePage

router = APIRouter()


class Genre(BaseModel):
    """полная информация по жанру"""
    id: UUID
    name: str
    description: Optional[str]
    films_ids: List[UUID]


@router.get('/{genre_id}', response_model=Genre, summary="Детали жанра")
async def genre_details(genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre


@router.get('/', response_model=GenrePage, summary="Список всех жанром, сортировка по названию")
async def search_genre_list(
        params: GenreQueryParams = Depends(),
        genre_service: GenreService = Depends(get_genre_service),
        page_size: int = 10,
        ) -> GenrePage:
    genres: Optional[dict] = await genre_service.get_all_genres(
        sorting=params.sort,
        page_size=page_size,
    )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return GenrePage(**genres)
