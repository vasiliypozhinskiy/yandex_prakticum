from http import HTTPStatus

film_list_params = [
    # параметры без query
    ("films/search", {}, HTTPStatus.OK),
    # проверяем сортировку по возрастанию без параметра query
    ("films/search", {"sort": "imdb_rating"}, HTTPStatus.OK),
    # проверяем сортировку по убыванию без параметра query
    ("films/search", {"sort": "-imdb_rating"}, HTTPStatus.OK),
    # фильтрация по жанру
    ("films/search", {"genre": "Drama"}, HTTPStatus.OK),
    # параметры с query
    ("films/search", {"query": "Star", 'page_size': 10}, HTTPStatus.OK),
    # # проверяем сортировку по убыванию
    ("films/search", {"query": "Star", "sort": "imdb_rating"}, HTTPStatus.OK),
    # # проверяем сортировку по возрастанию
    ("films/search", {"query": "Star", "sort": "-imdb_rating", 'page_size': 10}, HTTPStatus.OK),
    # проверка наличия фильма
    ("films", {"query": "Sonic", "sort": "-imdb_rating", 'page_size': 10}, HTTPStatus.OK)
]
