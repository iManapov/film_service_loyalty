# Код панели администратора

## Локальный запуск
Для запуска панели администратора локально необходимо создать файл `config/.env` со следующими параметрами:

- DB_HOST - хост БД Postgres
- DB_PORT - порт БД Postgres
- POSTGRES_DB - имя БД Postgres
- DB_SCHEME - имя схемы БД Postgres
- POSTGRES_USER - пользователь БД Postgres
- POSTGRES_PASSWORD - пароль БД Postgres
- REDIS_HOST - хост БД Redis
- REDIS_PORT - порт БД Redis
- REDIS_DB - БД Redis
- SECRET_KEY - секретный ключ Django
- DEBUG - переключатель режима отладки


При первом запуске необходимо применить миграции:

`python manage.py migrate`


Запуск на порту :8000:

`python manage.py runserver 0.0.0.0:8000`
