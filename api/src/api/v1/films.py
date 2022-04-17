from fastapi import APIRouter, Depends

from api.v1.exceptions import NotFoundException
from api.v1.models.response_model import FilmDetailResponse, FilmPageResponse, ListResponseFilm
from api.v1.utils import FilmQueryParams
from services.films import FilmService, get_film_service

router = APIRouter()


@router.get('/{film_id}', response_model=FilmDetailResponse, summary="Детали фильма")
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FilmDetailResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise NotFoundException
    return FilmDetailResponse(**dict(film))


@router.get('/search/', response_model=FilmPageResponse, summary="Поиск по жанру и названию")
async def search_film_list(
        params: FilmQueryParams = Depends(),
        film_service: FilmService = Depends(get_film_service),
        page_size: int = 10,
        ) -> FilmPageResponse:
    films = await film_service.get_many(
        sorting=params.sort,
        page_size=page_size,
        query=params.query,
        genre=params.genre_filter,
    )
    if not films:
        raise NotFoundException

    list_response_films = [ListResponseFilm(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating
        ) for film in films
    ]

    return FilmPageResponse(
        films=list_response_films,
        page_size=page_size
    )
