import uuid
import datetime

from aioredis import Redis
from databases import Database
from fastapi import Depends
from httpx import AsyncClient
import pytz
from sqlalchemy import and_

from src.core.config import settings
from src.db.postgres import get_postgres
from src.db.redis import get_redis_discounts, get_redis_users
from src.db.request import get_request
from src.schemas.film import Film
from src.schemas.discount import FilmDiscountModel
from src.models.discount import FilmsDiscount, FilmsDiscountUsage
from src.schemas.user import User
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

    async def calc_price(self, film: Film, user: User, discount: FilmsDiscount) -> float:
        """
        Вычисление цены фильма после применения скидок

        :param film: фильм
        :param user: пользователь
        :param discount: скидка на фильм
        :return: цена после применения скидка
        """

        discount_value = 0
        if discount:
            discount_value = discount.value

        price_after = film.price - discount_value

        if datetime.datetime.today() <= user.subscription_until:
            subs_discount = float(settings.subscriber_discount)
            price_after = (film.price - discount_value) * (1 - subs_discount / 100)

        return price_after

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
