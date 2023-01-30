import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union

from aioredis import Redis

from src.core.config import settings


class AbstractDiscountCache(ABC):
    """
    """

    @abstractmethod
    async def get(self, tag: str) -> Union[dict, None]:
        pass

    @abstractmethod
    async def set(self, tag: str, data: dict):
        pass


@dataclass
class RedisDiscountCache(AbstractDiscountCache):
    """
    """

    redis: Redis

    async def get(self, tag: str) -> Union[dict, None]:
        """
        """

        data = await self.redis.get(tag)
        if not data:
            return
        return json.loads(data)

    async def set(self, tag: str, data: dict):
        """
        """

        await self.redis.set(name=tag,
                             value=json.dumps(data),
                             ex=settings.discount_cache_expire_in_seconds)
