import uuid
import datetime
from typing import Union

from fastapi import Depends
from databases import Database
from sqlalchemy import and_

from src.db.postgres import get_postgres
from src.models.promo_code import Promocode, PromoUsage
from src.core.error_messages import error_msgs


class PromoCodeService:
    """
    Сервис взаимодействия с Postgres
    """
    def __init__(self, postgres: Database):
        self.postgres = postgres

    async def get_by_id(self, promo_id: uuid.UUID) -> Promocode:
        query = Promocode.select().filter(Promocode.c.id == promo_id)
        return await self.postgres.fetch_one(query=query)

    async def get_by_name(self, promo_code: str) -> Promocode:
        query = Promocode.select().filter(Promocode.c.code == promo_code)
        return await self.postgres.fetch_one(query=query)

    async def calc_price(self, user_id: uuid.UUID, promo_code: str, price: float) -> tuple[bool, Union[str, float]]:
        promo = await self.get_by_name(promo_code)
        if len(promo) == 0:
            return False, error_msgs.promo_not_found
        if promo.user_id and promo.user_id != user_id:
            return False, error_msgs.promo_wrong_user
        if promo.expiration_date < datetime.date.today():
            return False, error_msgs.promo_expired
        if not promo.is_multiple:
            usage_query = PromoUsage.select().filter(and_(PromoUsage.c.promo_id == promo.id,
                                                          PromoUsage.c.user_id == user_id))
            usage = await self.postgres.fetch_one(usage_query)
            if len(usage) > 0:
                return False, error_msgs.promo_used

        if promo.measure == '%':
            return True, price * (1 - promo.value / 100)
        return True, price - promo.value

    async def mark_promo_as_used(self, promo_code: str, user_id: uuid.UUID):
        promo = await self.get_by_name(promo_code)
        query = PromoUsage.insert().values(user_id=user_id, promo_id=promo.id, used_at=datetime.datetime.now())
        await self.postgres.execute(query)


def get_promo_service(
        postgres: Database = Depends(get_postgres)
) -> PromoCodeService:
    """
    Провайдер PromoCodeService,
    с помощью Depends он сообщает, что ему необходимы Database
    """
    return PromoCodeService(postgres)
