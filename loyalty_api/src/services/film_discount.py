import uuid
import datetime
from http import HTTPStatus

from aioredis import Redis
from databases import Database
from fastapi import Depends
from httpx import AsyncClient
import pytz
from sqlalchemy import and_

from src.core.config import settings
from src.core.error_messages import error_msgs
from src.core.test_data import test_data
from src.db.postgres import get_postgres
from src.db.redis import get_redis_discounts, get_redis_users
from src.db.request import get_request
from src.models.discount import FilmDiscountResponse, FilmsDiscount, FilmDiscountModel, FilmsDiscountUsage
from src.utils.cache import AbstractCache, RedisCache
from src.utils.row_to_dict import row_to_dict


class FilmDiscountService:
    """Сервис взаимодействия со скидками к фильмам"""

    def __init__(
            self,
            postgres: Database,
            discount_cache: AbstractCache,
            user_cache: AbstractCache,
            request: AsyncClient
    ):
        self.postgres = postgres
        self.discount_cache = discount_cache
        self.user_cache = user_cache
        self.request = request
        self.utc = pytz.UTC

    async def get_by_id(self, discount_id: uuid.UUID) -> FilmsDiscount:
        """
        Получение скидки к фильму по id скидки

        :param discount_id: id скидки
        :return: скидка
        """

        query = FilmsDiscount.select().filter(FilmsDiscount.c.id == discount_id)
        return await self.postgres.fetch_one(query=query)

    async def get_discount(self, tag: str) -> FilmsDiscount:
        """
        Получение скидки к фильму по тэгу

        :param tag: тэг фильма
        :return: скидка
        """

        discount = await self.discount_cache.get(tag)
        if discount:
            discount = FilmDiscountModel(**discount)
        else:
            query = FilmsDiscount.select().filter(
                and_(
                    FilmsDiscount.c.tag == tag,
                    FilmsDiscount.c.period_begin <= datetime.datetime.today(),
                    FilmsDiscount.c.period_end >= datetime.datetime.today(),
                    FilmsDiscount.c.enabled
                )
            )
            discount = await self.postgres.fetch_one(query)
            if discount:
                await self.discount_cache.set(key=tag, data=row_to_dict(discount))
            else:
                await self.discount_cache.set(key=tag, data={})

        return discount

    async def calc_price(self, tag: str, price: float, user_id: uuid.UUID) -> tuple[bool, FilmDiscountResponse]:
        """
        Вычисление цены фильма после применения скидок

        :param tag: тэг фильма
        :param price: цена фильма
        :param user_id: id пользователя
        :return: цена после применения скидка
        """

        discount = await self.get_discount(tag=tag)

        discount_id, discount_value = None, 0
        if discount:
            discount_id, discount_value = discount.id, discount.value

        user = await self.user_cache.get(str(user_id))
        if not user:
            if settings.is_functional_testing:
                user = test_data.user_subs.get(str(user_id))
                if not user:
                    return False, error_msgs.user_not_found
                user['user_id'] = str(user_id)
            else:
                user = await self.request.get(f'{settings.auth_api_url}/user/{user_id}/subscriptions')
                if user.status_code != HTTPStatus.OK:
                    return False, error_msgs.user_not_found
                user = user.json()['result']
            await self.user_cache.set(str(user_id), user)

        price_after = price - discount_value
        subs_discount = 0
        if datetime.datetime.today() <= datetime.datetime.strptime(user['subscription_until'], '%Y-%m-%d'):
            subs_discount = float(settings.subscriber_discount)
            price_after = (price - discount_value) * (1 - subs_discount / 100)

        return True, FilmDiscountResponse(
            discount_id=discount_id,
            user_id=user_id,
            subscriber_discount=subs_discount,
            price_before=price,
            price_after=price_after
        )

    async def mark_discount_as_used(self, discount_id: uuid.UUID, user_id: uuid.UUID):
        """
        Отметить скидку discount_id как использованную пользователем user_id

        :param discount_id: id скидки
        :param user_id: id пользователя
        """

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
    Провайдер FilmDiscountService,
    с помощью Depends он сообщает, что ему необходимы Database, Redis и AsyncClient
    """

    return FilmDiscountService(
        postgres,
        RedisCache(redis=discount_cache, expiration_time=settings.discount_cache_expire_in_seconds),
        RedisCache(redis=user_cache, expiration_time=settings.user_cache_expire_in_seconds),
        request
    )
