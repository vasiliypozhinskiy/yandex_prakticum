from http import HTTPStatus
from typing import Optional, List, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from fastapi_solution.src.api.v1.utils import FilmQueryParams
from fastapi_solution.src.services.films import FilmService, get_film_service
from fastapi_solution.src.models.film import  FilmPage

router = APIRouter()


class Film(BaseModel):
    """полная информация по фильму"""
    id: UUID
    title: str
    description: Optional[str] = None
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = None
    directors: Optional[List[Dict[str, str]]] = None
    actors: Optional[List[Dict[str, str]]] = None
    writers: Optional[List[Dict[str, str]]] = None



# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/{film_id}', response_model=Film, summary="Детали фильма")
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film


@router.get('/', response_model=FilmPage, summary="Поиск по жанру и названию")
async def search_film_list(
        params: FilmQueryParams = Depends(),
        film_service: FilmService = Depends(get_film_service),
        page_size: int = 10,
        ) -> FilmPage:
    films: Optional[dict] = await film_service.get_all_films(
        sorting=params.sort,
        page_size=page_size,
        query=params.query,
        genre=params.genre_filter,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmPage(**films)
