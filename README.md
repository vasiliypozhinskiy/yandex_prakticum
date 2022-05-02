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

Хочу заметить, что в настоящее время еще ведуться работы по доработке сервиса (незначительные) и возможно в момент проверки будет еще не конечный результат. Но в связи с поджиманием сроков было принято решение для отправки проекта на проверку. Хотелось бы услышать мнение ревьюера для одновременного исправления всех недостатков. 
