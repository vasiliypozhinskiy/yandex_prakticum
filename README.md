Для проверки работы сервиса auth:
1. Скачать репозиторий
2. создать файл .env заполнить по примеру .env.example
3. перейти в дирректорию с проектом (Async-Api_practicum_comand) и запустить docker-compose build, docker-compose up
4. послезапуска проекта выполнить docker exec -it async-api_parcticum_comand_auth_1 flask db init
5. зайти в контейнер async-api_parcticum_comand_auth_1 заййти в папку migrations добавить в файл env.py импорт моделей (from app.models.db_models import *)
6. выполнить docker exec -it async-api_parcticum_comand_auth_1 flask db migrate, docker exec -it async-api_parcticum_comand_auth_1 flask db upgrade
7. создать суперюзера docker exec -it async-api_parcticum_comand_auth_1 python create_superuser.py,
8. http://localhost:80/auth/openapi - расположена документация swagger сервира.


Для тестирования сервиса auth:
1. перейти в дирректорию c с тестами(auth/tests/functional).
2. Создать файл .env по примеру файла .env.sample
3. Выполнить docker-compose build, docker-compose up
4. Выполнить docker exec -it <название контейнера c окончанием test> pytest src

Некоторые пункты в которых мы уловили посыл "альтернативного способа" мы не выполняли т.к приняли больше за расширение нашего кругозора.


Так чтобы проверить авторизацию без живого ETL нужно запустить тестовый контейнер в тестах
- я открыл порты
- закоментил удоление данных в фикстурах
- добавил фильма категории Adults (как просил Руслан)

Можно брать по id все фильмы кроме него, там нужна автоиризация:
- логинимся как админ
- смотрим adults
- вот id для Adults `57beb3fd-b1c9-4f8a-9c06-2da13f95251d`
- вот чтото еще `57beb3fd-b1c9-4f8a-9c06-2da13f95251c`
