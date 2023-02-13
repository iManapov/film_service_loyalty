import json
from typing import Union

import aioredis
import pytest_asyncio

from aioredis import Redis

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope="session")
async def redis_discount():
    """
    Фикстура для установления соединения с Redis
    на время тестов
    """
    redis_discount_cache = await aioredis.from_url(f"redis://{test_settings.redis_host}:{test_settings.redis_port}",
                                                   db=1)
    yield redis_discount_cache
    redis_discount_cache.close()


@pytest_asyncio.fixture(scope="session")
async def redis_user():
    """
    Фикстура для установления соединения с Redis
    на время тестов
    """
    user_cache = await aioredis.from_url(f"redis://{test_settings.redis_host}:{test_settings.redis_port}", db=2)
    yield user_cache
    user_cache.close()


@pytest_asyncio.fixture
def check_cache_discount(redis_discount: Redis):
    """
    Фикстура для проверки результата запроса в кеше
    """

    async def inner(key: str) -> Union[dict, None]:
        cache_data = await redis_discount.get(key)
        if cache_data:
            return json.loads(cache_data)
        return None

    return inner


@pytest_asyncio.fixture
def check_cache_user(redis_user: Redis):
    """
    Фикстура для проверки результата запроса в кеше
    """

    async def inner(key: str) -> Union[dict, None]:
        cache_data = await redis_user.get(key)
        if cache_data:
            return json.loads(cache_data)
        return None

    return inner
