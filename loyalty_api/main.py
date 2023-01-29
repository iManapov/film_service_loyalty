import logging

import aioredis
import uvicorn
import databases
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import httpx

from src.api.v1 import promo_code, orders
from src.core.config import settings
from src.core.logger import LOGGING
from src.db import redis, postgres, request

app = FastAPI(
    title=settings.project_name,
    description="Сервис системы лояльности",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    version='1.0.0'
)


@app.on_event('startup')
async def startup():
    # Подключаемся к базам при старте сервера
    redis.discounts = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", db=1)
    redis.user_cache = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", db=2)

    request.request = httpx.AsyncClient(verify=False)

    postgres_url = settings.get_postgres_url()
    postgres.postgres = databases.Database(postgres_url)
    await postgres.postgres.connect()

    # metadata = sqlalchemy.MetaData()
    # engine = sqlalchemy.create_engine(
    #     postgres_url, connect_args={"check_same_thread": False}
    # )
    # metadata.create_all(engine)


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await redis.discounts.close()
    await redis.user_cache.close()
    await postgres.postgres.disconnect()


# Подключаем роутер к серверу, указав префикс /v1/promo_codes
app.include_router(promo_code.router, prefix='/api/v1/promo_codes', tags=['promo_codes'])
app.include_router(orders.router, prefix='/api/v1/orders', tags=['orders'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
