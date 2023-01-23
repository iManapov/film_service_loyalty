import logging

import aioredis
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import promo_code

from src.core.config import settings
from src.core.logger import LOGGING
from src.db import redis

app = FastAPI(
    title=settings.project_name,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    version='1.0.0'
)


@app.on_event('startup')
async def startup():
    # Подключаемся к базам при старте сервера
    redis.redis = await aioredis.from_url("redis://{host}:{port}".format(host=settings.redis_host,
                                                                         port=settings.redis_port)
                                          )
    print(1)


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await redis.redis.close()


# Подключаем роутер к серверу, указав префикс /v1/promo_codes
app.include_router(promo_code.router, prefix='/api/v1/promo_codes', tags=['promo_codes'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
