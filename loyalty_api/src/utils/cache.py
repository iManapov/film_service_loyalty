from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union

from aioredis import Redis


class AbstractCache(ABC):
    """Abstract cache class"""

    @abstractmethod
    async def get(self, key: str) -> Union[dict, None]:
        """
        Returns record by key

        :param key: record key
        :return: record data
        """
        pass

    @abstractmethod
    async def set(self, key: str, data: dict):
        """
        Adds record to cache

        :param key: record key
        :param data: record data
        """
        pass


@dataclass
class RedisCache(AbstractCache):
    """Redis cache class"""

    redis: Redis
    expiration_time: int

    async def get(self, key: str) -> Union[dict, None]:
        """
        Returns record by key

        :param key: record key
        :return: record data
        """

        data = await self.redis.get(key)
        if not data:
            return
        return json.loads(data)

    async def set(self, key: str, data: dict):
        """
        Adds record to cache

        :param key: record key
        :param data: record data
        """

        await self.redis.set(name=key,
                             value=json.dumps(data),
                             ex=self.expiration_time)
