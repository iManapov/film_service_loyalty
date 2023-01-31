from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union

from aioredis import Redis

from src.core.config import settings


class AbstractDiscountCache(ABC):
    """Абстрактный класс кэша для скидок"""

    @abstractmethod
    async def get(self, tag: str) -> Union[dict, None]:
        """
        Получение скидки из кэша

        :param tag: тэг фильма
        :return: скидка
        """
        pass

    @abstractmethod
    async def set(self, tag: str, data: dict):
        """
        Добавление скидки в кэш

        :param tag: тэг фильма
        :param data: данные скидки
        """
        pass


@dataclass
class RedisDiscountCache(AbstractDiscountCache):
    """Класс кэша скидок в Redis"""

    redis: Redis

    async def get(self, tag: str) -> Union[dict, None]:
        """
        Получение скидки из кэша

        :param tag: тэг фильма
        :return: скидка
        """

        data = await self.redis.get(tag)
        if not data:
            return
        return json.loads(data)

    async def set(self, tag: str, data: dict):
        """
        Добавление скидки в кэш

        :param tag: тэг фильма
        :param data: данные скидки
        """

        await self.redis.set(name=tag,
                             value=json.dumps(data),
                             ex=settings.discount_cache_expire_in_seconds)
