import json
import uuid

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from redis import Redis

from config import settings


class AbstractCache(ABC):
    """Абстрактный класс кэша"""

    @abstractmethod
    def get(self, key: str) -> Union[dict, None]:
        """
        Получение записи из кэша по ключу
        :param key: ключ записи
        :return: содержимое кэша
        """
        pass

    @abstractmethod
    def delete(self, key: str):
        """
        Удаление записи из кэша
        :param key: ключ записи
        """
        pass


@dataclass
class RedisCache(AbstractCache):
    """Класс кэша Redis"""

    redis: Redis

    def get(self, key: str) -> Union[dict, None]:
        """
        Получение записи из Redis по ключу
        :param key: ключ записи
        :return: содержимое кэша
        """

        data = self.redis.get(key)
        if not data:
            return None
        return json.loads(data)

    def delete(self, key: str):
        """
        Удаление записи из Redis
        :param key: ключ записи
        """
        self.redis.delete(key)
