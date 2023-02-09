# Код FAST API приложения

## Локальный запуск
Предварительно необходимо создать файл `src/core/.env` со следующими параметрами:
```dotenv
POSTGRES_USER - пользователь Postgres
POSTGRES_PSWD - пароль Postgres
```

Для запуска api под `uvicorn`:
```shell
uvicorn main:app --reload --host localhost --port 8009
```
Для запуска api под `gunicorn`:
```shell
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8009
```

Адрес документации: http://localhost:8009/api/openapi/


## Запуск в Docker
Предварительно необходимо в корне проекта создать файл `.env` со следующими параметрами:
```dotenv
REDIS_HOST - хост Redis
REDIS_PORT - порт Redis
POSTGRES_HOST - хост Postgres 
POSTGRES_PORT - порт Postgres
POSTGRES_DB - название бд в Postgres
POSTGRES_USER - пользователь Postgres
POSTGRES_PSWD - пароль Postgres
AUTH_API_URL - url от api авторизации (http://localhost:5001/api/v1)
FILM_API_URL - - url от api с фильмами (http://localhost:8001/api/v1)
IS_FUNCTIONAL_TESTING - флаг для функциональных тестов (тестовые данные)
```

Для запуска api в `Docker` необходимо выполнить команду
```shell
docker compose up --build
```

Адрес документации: http://localhost/api/openapi/
