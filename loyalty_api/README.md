# Loyalty Api

## Local run
Firstly create env file `src/core/.env` with following parameters:
```dotenv
POSTGRES_USER - Postgres user
POSTGRES_PSWD - Postgres password
```

To run under `uvicorn` execute following commands:
```shell
uvicorn main:app --reload --host localhost --port 8009
```
To run under `gunicorn` execute following commands:
```shell
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8009
```

OpenApi documentation url: http://localhost:8009/api/openapi/


## Run in Docker
Env parameters:
```dotenv
REDIS_HOST - Redis host
REDIS_PORT - Redis port
POSTGRES_HOST - Postgres host 
POSTGRES_PORT - Postgres port
POSTGRES_DB - Postgres database name
POSTGRES_USER - Postgres user
POSTGRES_PSWD - Postgres password
AUTH_API_URL - authorization api url (http://localhost:5001/api/v1)
FILM_API_URL - film api url (http://localhost:8001/api/v1)
IS_FUNCTIONAL_TESTING - flag for functional testing
IS_PRODUCTION - flag for dev/production
```
