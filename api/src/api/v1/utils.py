from typing import Optional
from fastapi import Query


class FilmQueryParams:
    """
    Класс задает параметры для поиска по фильму
    """

    def __init__(
        self,
        sort_imdb_rating: Optional[str] = Query(
            None,
            title="Сортировка по рейтингу",
            description="Сортирует по возрастанию и убыванию,"
            " -field если нужна сортировка по убыванию или field,"
            " если нужна сортировка по возрастанию",
            alias="sort",
        ),
        genre_filter: Optional[str] = Query(
            None,
            title="Фильтр жанров",
            description="Фильтрует фильмы по жанрам",
            alias="filter[genre]",
        ),
        query: Optional[str] = Query(
            None,
            title="Запрос",
            description="Осуществляет поиск по названию фильма",
        ),
    ) -> None:
        self.sort = sort_imdb_rating
        self.genre_filter = genre_filter
        self.query = query


class GenreQueryParams:
    """
    Класс задает параметры для поиска по жанру
    """

    def __init__(
        self,
        sort_by_name: Optional[str] = Query(
            None,
            title="Сортировка по названию жанра",
            description="Сортирует по возрастанию и убыванию,"
            " -field если нужна сортировка по убыванию или field,"
            " если нужна сортировка по возрастанию",
            alias="sort",
        )
    ) -> None:
        self.sort = sort_by_name


class PersonQueryParams:
    """
    Класс задает параметры для поиска по персоне
    """

    def __init__(
        self,
        sort_by_name: Optional[str] = Query(
            None,
            title="Сортировка по имени",
            description="Сортирует по возрастанию и убыванию,"
            " -field если нужна сортировка по убыванию или field,"
            " если нужна сортировка по возрастанию",
            alias="sort",
        ),
        query: Optional[str] = Query(
            None,
            title="Запрос",
            description="Осуществляет поиск по имени",
        )
    ) -> None:
        self.sort = sort_by_name
        self.query = query


class FilmByPersonQueryParams:
    """
    Класс задает параметры для поиска по персоне
    """

    def __init__(
        self,
        sort_by_name: Optional[str] = Query(
            None,
            title="Сортировка по имени",
            description="Сортирует по возрастанию и убыванию,"
            " -field если нужна сортировка по убыванию или field,"
            " если нужна сортировка по возрастанию",
            alias="sort",
        )
    ) -> None:
        self.sort = sort_by_name
