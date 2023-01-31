import uuid
import datetime
from typing import Union

from databases import Database
from fastapi import Depends
from sqlalchemy import and_
import pytz

from src.core.error_messages import error_msgs
from src.db.postgres import get_postgres
from src.models.promo_code import PromoCode, PromoUsage


class PromoCodeService:
    """Сервис взаимодействия с промокодами"""

    def __init__(self, postgres: Database):
        self.postgres = postgres
        self.utc = pytz.UTC

    async def get_by_id(self, promo_id: uuid.UUID) -> PromoCode:
        """
        Получение промокода по его id

        :param promo_id: id промокода
        :return: промокод
        """

        query = PromoCode.select().filter(PromoCode.c.id == promo_id)
        return await self.postgres.fetch_one(query=query)

    async def get_by_name(self, promo_code: str) -> PromoCode:
        """
        Получение промокода по его коду (названию)

        :param promo_code: код промокода
        :return: промокод
        """

        query = PromoCode.select().filter(PromoCode.c.code == promo_code)
        return await self.postgres.fetch_one(query=query)

    async def calc_price(self, user_id: uuid.UUID, promo_code: str, price: float) -> tuple[bool, Union[str, float]]:
        """
        Вычисление цены после применения промокода

        :param user_id: id пользователя
        :param promo_code: код промокода
        :param price: цена фильма/подписки
        :return: цены после применения промокода
        """

        promo = await self.get_by_name(promo_code)
        if not promo:
            return False, error_msgs.promo_not_found
        if promo.user_id and promo.user_id != user_id:
            return False, error_msgs.promo_wrong_user
        if promo.expiration_date.replace(tzinfo=self.utc) < datetime.datetime.now(tz=self.utc):
            return False, error_msgs.promo_expired
        if not promo.is_multiple:
            usage_query = PromoUsage.select().filter(and_(PromoUsage.c.promo_id == promo.id,
                                                          PromoUsage.c.user_id == user_id))
            usage = await self.postgres.fetch_one(usage_query)
            if usage and len(usage) > 0:
                return False, error_msgs.promo_used

        if promo.measure == '%':
            return True, price * (1 - promo.value / 100)
        return True, price - promo.value

    async def mark_promo_as_used(self, promo: PromoCode, user_id: uuid.UUID):
        """
        Отметить промокод promo как использованную пользователем user_id

        :param promo: промокод
        :param user_id: id пользователя
        """
        query = PromoUsage.insert().values(
            id=uuid.uuid4(),
            user_id=user_id,
            promo_id=promo.id,
            used_at=datetime.datetime.now(),
        )
        await self.postgres.execute(query)


def get_promo_service(
        postgres: Database = Depends(get_postgres)
) -> PromoCodeService:
    """
    Провайдер PromoCodeService,
    с помощью Depends он сообщает, что ему необходимы Database
    """

    return PromoCodeService(postgres)
