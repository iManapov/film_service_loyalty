import uuid
import datetime

from databases import Database
from fastapi import Depends
from sqlalchemy import and_
import pytz

from src.db.postgres import get_postgres
from src.models.promo_code import PromoCode, PromoUsage


class PromoCodeService:
    """Promocodes service"""

    def __init__(self, postgres: Database):
        self.postgres = postgres
        self.utc = pytz.UTC

    async def get_by_id(self, promo_id: uuid.UUID) -> PromoCode:
        """
        Returns promocode by id

        :param promo_id: promocode id
        :return: promocode
        """

        query = PromoCode.select().filter(PromoCode.c.id == promo_id)
        return await self.postgres.fetch_one(query=query)

    async def get_by_name(self, promo_code: str) -> PromoCode:
        """
        Returns promocode by promo code (string)

        :param promo_code: promo code
        :return: promocode
        """

        query = PromoCode.select().filter(PromoCode.c.code == promo_code)
        return await self.postgres.fetch_one(query=query)

    @staticmethod
    async def calc_price(promo: PromoCode, price: float) -> float:
        """
        Returns price after applying promocode

        :param promo: promocode
        :param price: film or subscription price
        :return: price after applying promocode
        """

        if promo.measure == '%':
            return price * (1 - promo.value / 100)
        return price - promo.value

    async def is_promo_used(self, promo_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """
        Checks if promocode is used by user with user_id

        :param promo_id: promocode id
        :param user_id: user id
        :return: flag 'is promocode used'
        """

        usage_query = PromoUsage.select().filter(and_(PromoUsage.c.promo_id == promo_id,
                                                      PromoUsage.c.user_id == user_id))
        usage = await self.postgres.fetch_one(usage_query)
        if usage and len(usage) > 0:
            return True
        return False

    async def mark_promo_as_used(self, promo: PromoCode, user_id: uuid.UUID):
        """
        Marks promocode used by user with user_id

        :param promo: promocode
        :param user_id: user id
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
    PromoCodeService provider
    using 'Depends', it says that it needs Database
    """

    return PromoCodeService(postgres)
