from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union

from aioredis import Redis


class AbstractCache(ABC):
    """Абстрактный класс кэша"""

    @abstractmethod
    async def get(self, key: str) -> Union[dict, None]:
        """
        Получение записи из кэша по ключу

        :param key: ключ записи
        :return: содержимое кэша
        """
        pass

    @abstractmethod
    async def set(self, key: str, data: dict):
        """
        Добавление записи в кэш

        :param key: ключ записи
        :param data: содержимое кэша
        """
        pass


@dataclass
class RedisCache(AbstractCache):
    """Класс кэша Redis"""

    redis: Redis
    expiration_time: int

    async def get(self, key: str) -> Union[dict, None]:
        """
        Получение записи из кэша по ключу

        :param key: ключ записи
        :return: содержимое кэша
        """

        data = await self.redis.get(key)
        if not data:
            return
        return json.loads(data)

    async def set(self, key: str, data: dict):
        """
        Добавление записи в кэш

        :param key: ключ записи
        :param data: содержимое кэша
        """

        await self.redis.set(name=key,
                             value=json.dumps(data),
                             ex=self.expiration_time)
