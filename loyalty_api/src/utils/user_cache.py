import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union

from aioredis import Redis

from src.core.config import settings


class AbstractUserCache(ABC):
    """
    """

    @abstractmethod
    async def get(self, user_id: uuid.UUID) -> Union[dict, None]:
        pass

    @abstractmethod
    async def set(self, user_id: uuid.UUID, data: dict):
        pass


@dataclass
class RedisUserCache(AbstractUserCache):
    """
    """

    redis: Redis

    async def get(self, user_id: uuid.UUID) -> Union[dict, None]:
        """
        """

        data = await self.redis.get(str(user_id))
        if not data:
            return
        return json.loads(data)

    async def set(self, user_id: uuid.UUID, data: dict):
        """
        """

        await self.redis.set(name=str(user_id),
                             value=json.dumps(data),
                             ex=settings.user_cache_expire_in_seconds)
