# Код функциональных тестов

## Локальный запуск
Для запуска тестов локально необходимо создать файл `tests/functional/.env` со следующими параметрами:

- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- FAST_API_URL - url тестируемого api
- POSTGRES_USER - пользователь Postgres
- POSTGRES_PSWD - пароль Postgres
- POSTGRES_DB - база данных Postgres
- AUTH_API_URL - адрес сервиса авторизации

Для запуска тестов используется команда `pytest ./tests/functional/src` из папки `loyalty_api`

