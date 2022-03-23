from http import HTTPStatus
from typing import Optional, List, Dict
from uuid import UUID
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from fastapi_solution.src.models.person import Person
from fastapi_solution.src.services.films import FilmService, get_film_service

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
@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    logger.info(film)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
                # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    # Перекладываем данные из models.Film в Film
    # Обратите внимание, что у модели бизнес-логики есть поле description
        # Которое отсутствует в модели ответа API.
        # Если бы использовалась общая модель для бизнес-логики и формирования ответов API
        # вы бы предоставляли клиентам данные, которые им не нужны
        # и, возможно, данные, которые опасно возвращать
    actors_list: List[Person] = [
        Person(id=actor.get("id"), full_name=actor.get("name"))
        for actor in film.actors
    ]
    return Film(id=film.id, title=film.title, description=film.description, genre=film.genre,
                imdb_rating=film.imdb_rating, actors=film.actors, writers=film.writers,
                directors=film.directors)