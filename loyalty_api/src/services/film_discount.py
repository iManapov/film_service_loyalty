import uuid
import datetime
from http import HTTPStatus
import pytz

from aioredis import Redis
from fastapi import Depends
from httpx import AsyncClient
from databases import Database

from src.db.postgres import get_postgres
from src.db.redis import get_redis_discounts, get_redis_users
from src.db.request import get_request
from src.utils.discount_cache import AbstractDiscountCache, RedisDiscountCache
from src.utils.user_cache import AbstractUserCache, RedisUserCache
from src.models.discount import FilmDiscountResponseApi, FilmsDiscount, FilmDiscountModel, FilmsDiscountUsage
from src.core.config import settings
from src.core.error_messages import error_msgs


class FilmDiscountService:
    def __init__(
            self,
            postgres: Database,
            discount_cache: AbstractDiscountCache,
            user_cache: AbstractUserCache,
            request: AsyncClient
    ):
        self.postgres = postgres
        self.discount_cache = discount_cache
        self.user_cache = user_cache
        self.request = request
        self.utc = pytz.UTC

    async def get_by_id(self, discount_id: uuid.UUID) -> FilmsDiscount:
        query = FilmsDiscount.select().filter(FilmsDiscount.c.id == discount_id)
        return await self.postgres.fetch_one(query=query)

    async def get_discount(self, tag: str) -> FilmsDiscount:
        discount = await self.discount_cache.get(tag)
        if discount:
            discount = FilmDiscountModel(**discount)
        else:
            query = FilmsDiscount.select().filter(FilmsDiscount.c.tag == tag)
            discount = await self.postgres.fetch_one(query)
            if discount:
                print(discount.__dict__)
                await self.discount_cache.set(tag=tag, data=discount.__dict__)
            else:
                await self.discount_cache.set(tag=tag, data={})

        if discount and discount.enabled and discount.period_begin <= datetime.datetime.now(tz=self.utc) <= discount.period_end:
            return discount

    async def calc_price(self, tag: str, price: float, user_id: uuid.UUID) -> tuple[bool, FilmDiscountResponseApi]:
        discount = await self.get_discount(tag=tag)

        discount_id, discount_value = None, 0
        if discount:
            discount_id, discount_value = discount.id, discount.value

        user = await self.user_cache.get(user_id)
        if not user:
            user = await self.request.get(f'{settings.auth_api_url}/user/{user_id}/subscriptions')
            if not user.status_code == HTTPStatus.OK:
                return False, error_msgs.user_not_found
            user = user.json()
            await self.user_cache.set(user_id, user)

        price_after = price - discount_value
        subs_discount = 0
        if datetime.datetime.today() <= datetime.datetime.strptime(user['result']['subscription_until'], '%Y-%m-%d'):
            subs_discount = float(settings.subscriber_discount)
            price_after = (price - discount_value) * (1 - subs_discount / 100)

        return True, FilmDiscountResponseApi(
            discount_id=discount_id,
            tag=tag,
            user_id=user_id,
            subscriber_discount=subs_discount,
            price_before=price,
            price_after=price_after
        )

    async def mark_discount_as_used(self, discount_id: uuid.UUID, user_id: uuid.UUID):
        query = FilmsDiscountUsage.insert().values(
            id=uuid.uuid4(),
            user_id=user_id,
            discount_id=discount_id,
            used_at=datetime.datetime.now(),
        )
        await self.postgres.execute(query)


def get_film_discount_service(
        postgres: Database = Depends(get_postgres),
        discount_cache: Redis = Depends(get_redis_discounts),
        user_cache: Redis = Depends(get_redis_users),
        request: AsyncClient = Depends(get_request)
) -> FilmDiscountService:
    """
    """
    return FilmDiscountService(
        postgres,
        RedisDiscountCache(discount_cache),
        RedisUserCache(user_cache),
        request
    )
