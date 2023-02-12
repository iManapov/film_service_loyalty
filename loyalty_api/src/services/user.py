import datetime
import uuid
from typing import Optional

from aioredis import Redis
from fastapi import Depends, status
from httpx import AsyncClient

from src.core.config import settings
from src.core.test_data import test_data
from src.db.request import get_request
from src.db.redis import get_redis_users
from src.models.user import User
from src.utils.cache import AbstractCache, RedisCache


class UserService:
    """Сервис взаимодействия с пользователями"""

    def __init__(
            self,
            request: AsyncClient,
            user_cache: AbstractCache,
    ):
        self.request = request
        self.user_cache = user_cache

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Получение пользователя по id

        :param user_id: id пользователя
        :return: пользователь
        """

        user = await self.user_cache.get(str(user_id))
        if not user:
            if settings.is_functional_testing:
                user = test_data.user_subs.get(str(user_id))
                if not user:
                    return
                user['user_id'] = str(user_id)
            else:
                user = await self.request.get(f'{settings.auth_api_url}/user/{user_id}/subscriptions')
                if user.status_code != status.HTTP_200_OK:
                    return
                user = user.json()['result']
            user['id'] = user.pop('user_id')
            await self.user_cache.set(str(user_id), user)
        user['subscription_until'] = datetime.datetime.strptime(user['subscription_until'], '%Y-%m-%d')
        return User(**user)


def get_user_service(
        request: AsyncClient = Depends(get_request),
        user_cache: Redis = Depends(get_redis_users),
) -> UserService:
    """
    Провайдер UserService,
    с помощью Depends он сообщает, что ему необходимы AsyncClient и Redis
    """

    return UserService(
        request=request,
        user_cache=RedisCache(redis=user_cache, expiration_time=settings.user_cache_expire_in_seconds),
    )
