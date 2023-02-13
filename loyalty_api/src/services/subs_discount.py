import uuid
import datetime

from databases import Database
from fastapi import Depends
from sqlalchemy import and_

from src.db.postgres import get_postgres
from src.models.discount import SubsDiscount, SubsDiscountUsage
from src.models.subscription import Subscription


class SubsDiscountService:
    """Сервис взаимодействия со скидкой к подписке"""

    def __init__(self, postgres: Database):
        self.postgres = postgres

    async def get_discount_by_id(self, discount_id: uuid.UUID) -> SubsDiscount:
        """
        Получение скидки по его id

        :param discount_id: id скидки
        :return: скидка
        """

        query = SubsDiscount.select().filter(SubsDiscount.c.id == discount_id)
        return await self.postgres.fetch_one(query=query)

    async def get_discount_for_sub(self, subs_id: uuid.UUID) -> SubsDiscount:
        """
        Получение скидки к подписке по id подписки

        :param subs_id: id подписки
        :return: скидка
        """

        query = SubsDiscount.select().filter(
            and_(SubsDiscount.c.subscription_id == subs_id,
                 SubsDiscount.c.period_begin <= datetime.datetime.today(),
                 SubsDiscount.c.period_end >= datetime.datetime.today(),
                 SubsDiscount.c.enabled
                 )
        )
        return await self.postgres.fetch_one(query=query)

    async def calc_price(self, subscription: Subscription, discount: SubsDiscount) -> float:
        """
        Вычисление цены подписки после скидки

        :param subscription: подписка
        :param discount: скидка
        :return: цена после скидки
        """

        return subscription.price-discount.value

    async def mark_discount_as_used(self, discount_id: uuid.UUID, user_id: uuid.UUID):
        """
        Отметить скидку discount_id как использованную пользователем user_id

        :param discount_id: id скидки
        :param user_id: id пользователя
        """

        query = SubsDiscountUsage.insert().values(
            id=uuid.uuid4(),
            user_id=user_id,
            discount_id=discount_id,
            used_at=datetime.datetime.now(),
        )
        await self.postgres.execute(query)


def get_sub_discount_service(
        postgres: Database = Depends(get_postgres)
) -> SubsDiscountService:
    """
    Провайдер SubsDiscountService,
    с помощью Depends он сообщает, что ему необходимы Database
    """
    return SubsDiscountService(postgres)
