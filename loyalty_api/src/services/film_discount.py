import uuid
import datetime

from aioredis import Redis
from fastapi import Depends
from httpx import AsyncClient

from src.db.redis import get_redis_discounts, get_redis_users
from src.db.request import get_request
from src.utils.discount import AbstractDiscountDb, RedisDiscountDb
from src.utils.user import AbstractUserCache, RedisUserCache
from src.models.discount import FilmDiscount
from src.core.config import settings


class FilmDiscountService:
    def __init__(self, discount_db: AbstractDiscountDb, user_cache: AbstractUserCache, request: AsyncClient):
        self.discount = discount_db
        self.user_cache = user_cache
        self.request = request

    async def get_discount(self, tag: str) -> FilmDiscount:
        raw_discount = await self.discount.get(tag)
        discount = FilmDiscount(**raw_discount)
        if discount.enabled and discount.period_begin <= datetime.date.today() <= discount.period_end:
            return discount

    async def calc_price(self, tag: str, price: float, user_id: uuid.UUID) -> float:
        discount = await self.get_discount(tag=tag)

        user = await self.user_cache.get(user_id)
        if not user:
            user = await self.request.get(f'{settings.auth_api_url}/user/{user_id}/')
            user = user.json()
            await self.user_cache.set(user_id, user)
        if datetime.date.today() <= user['subs_valid_until']:
            return (price - discount.value) * settings.subscriber_discount
        return price - discount.value


def get_film_discount_service(
        redis_discount: Redis = Depends(get_redis_discounts),
        user_cache: Redis = Depends(get_redis_users),
        request: AsyncClient = Depends(get_request)
) -> FilmDiscountService:
    """
    """
    return FilmDiscountService(
        RedisDiscountDb(redis_discount),
        RedisUserCache(user_cache),
        request
    )
