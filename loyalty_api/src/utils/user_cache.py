from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union
import uuid

from aioredis import Redis

from src.core.config import settings


class AbstractUserCache(ABC):
    """Абстрактный класс кэша для пользователей"""

    @abstractmethod
    async def get(self, user_id: uuid.UUID) -> Union[dict, None]:
        """
        Получение пользователя из кэша по id

        :param user_id: id пользователя
        :return: данные пользователя
        """
        pass

    @abstractmethod
    async def set(self, user_id: uuid.UUID, data: dict):
        """
        Добавление пользователя в кэш

        :param user_id: id пользователя
        :param data: данные пользователя
        """
        pass


@dataclass
class RedisUserCache(AbstractUserCache):
    """Класс кэша для пользователей в Redis"""

    redis: Redis

    async def get(self, user_id: uuid.UUID) -> Union[dict, None]:
        """
        Получение пользователя из кэша по id

        :param user_id: id пользователя
        :return: данные пользователя
        """

        data = await self.redis.get(str(user_id))
        if not data:
            return
        return json.loads(data)

    async def set(self, user_id: uuid.UUID, data: dict):
        """
        Добавление пользователя в кэш

        :param user_id: id пользователя
        :param data: данные пользователя
        """

        await self.redis.set(name=str(user_id),
                             value=json.dumps(data),
                             ex=settings.user_cache_expire_in_seconds)
