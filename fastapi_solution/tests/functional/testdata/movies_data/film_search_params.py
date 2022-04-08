from http import HTTPStatus

film_list_params = [
    # параметры без query
    ("films", {}, HTTPStatus.OK),
    # проверяем сортировку по возрастанию без параметра query
    ("films", {"sort": "imdb_rating"}, HTTPStatus.OK),
    # проверяем сортировку по убыванию без параметра query
    ("films", {"sort": "-imdb_rating"}, HTTPStatus.OK),
    # фильтрация по жанру
    ("films", {"genre": "Drama"}, HTTPStatus.OK),
    # параметры с query
    ("films", {"query": "Star"}, HTTPStatus.OK),
    # # проверяем сортировку по убыванию
    ("films", {"query": "Star", "sort": "imdb_rating"}, HTTPStatus.OK),
    # # проверяем сортировку по возрастанию
    ("films", {"query": "Star", "sort": "-imdb_rating"}, HTTPStatus.OK),
    # проверка наличия фильма
    ("films", {"query": "Sonic", "sort": "-imdb_rating",}, HTTPStatus.OK)
]
