import json
import uuid

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union

from fastapi import Request
from aioredis import Redis

from src.core.config import settings


class AbstractCache(ABC):
    """
    Абстрактный класс для реализации кеширования
    """
    @abstractmethod
    def set(self, data: dict):
        pass

    @abstractmethod
    def get(self, record_id):
        pass


@dataclass
class RedisCache(AbstractCache):
    """
    Класс для кеширования в Redis
    В качестве ключа используется текущий запрошенный URL
    URL получаем из request
    """
    redis: Redis
    request: Request

    async def set(self, data: dict):
        """
        Сохранение в кеш по id

        @param data: данные для сохранения в кеш
        """
        data_id = str(uuid.uuid4())
        data.update(id=data_id)
        await self.redis.set(data_id,
                             json.dumps(data))
                             # ex=settings.FILM_CACHE_EXPIRE_IN_SECONDS)
        return data

    async def get(self, record_id) -> Union[dict, None]:
        """
        Извлечение из кеша

        @return: данные из кеша
        """
        data = await self.redis.get(record_id)
        if not data:
            return None
        return json.loads(data)
