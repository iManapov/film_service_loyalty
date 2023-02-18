# Loyalty admin panel

## Local run
Firstly create env file `config/.env` with following parameters:
```dotenv
DB_HOST - Postgres host
DB_PORT - Postgres port
POSTGRES_DB - Postgres database name
DB_SCHEME - Postgres schema name
POSTGRES_USER - Postgres user
POSTGRES_PASSWORD - Postgres password
REDIS_HOST - Redis host
REDIS_PORT - Redis port
REDIS_DB - Redis database
SECRET_KEY - Django secret key
DEBUG - flag for debug mode
```

At first run apply database migration executing following command:

```shell
python manage.py migrate
```

To run on `8010` port execute command:

```shell
python manage.py runserver 0.0.0.0:8010
```

Admin panel URL: http://localhost:8010/admin
