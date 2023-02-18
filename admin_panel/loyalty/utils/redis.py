import json

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from redis import Redis


class AbstractCache(ABC):
    """Abstract cache class"""

    @abstractmethod
    def get(self, key: str) -> Union[dict, None]:
        """
        Returns cache record by key

        :param key: record key
        :return: record
        """
        pass

    @abstractmethod
    def delete(self, key: str):
        """
        Deletes record from cache by key

        :param key: record key
        """
        pass


@dataclass
class RedisCache(AbstractCache):
    """Class for Redis cache"""

    redis: Redis

    def get(self, key: str) -> Union[dict, None]:
        """
        Returns Redis cache record by key

        :param key: record key
        :return: record
        """

        data = self.redis.get(key)
        if not data:
            return None
        return json.loads(data)

    def delete(self, key: str):
        """
        Deletes record from Redis cache by key

        :param key: record key
        """

        self.redis.delete(key)
