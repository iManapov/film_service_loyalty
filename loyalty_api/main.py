import logging

import aioredis
import databases
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import httpx
import uvicorn

from src.api.v1 import promo_code, subscription, discount
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
    redis.discounts = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", db=3)
    redis.user_cache = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", db=4)
    redis.film_cache = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", db=5)

    request.request = httpx.AsyncClient(verify=False)

    postgres_url = settings.get_postgres_url()
    postgres.postgres = databases.Database(postgres_url)
    await postgres.postgres.connect()


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await redis.discounts.close()
    await redis.user_cache.close()
    await redis.film_cache.close()
    await postgres.postgres.disconnect()


app.include_router(promo_code.router, prefix='/api/v1/promocodes', tags=['Promo codes'])
app.include_router(subscription.router, prefix='/api/v1/subscriptions', tags=['Subscriptions'])
app.include_router(discount.router, prefix='/api/v1/discounts', tags=['Discounts'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8009,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
