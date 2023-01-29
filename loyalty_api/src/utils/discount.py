from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Union

from aioredis import Redis


class AbstractDiscountDb(ABC):
    """
    """

    @abstractmethod
    def get(self, record_id: str):
        pass


@dataclass
class RedisDiscountDb(AbstractDiscountDb):
    """
    """

    redis: Redis

    async def get(self, record_id: str) -> Union[dict, None]:
        """
        """

        data = await self.redis.get(record_id)
        if not data:
            return None
        return json.loads(data)
