import uuid
import datetime

from databases import Database
from fastapi import Depends
from sqlalchemy import and_

from src.db.postgres import get_postgres
from src.models.discount import SubsDiscount, SubsDiscountUsage
from src.models.subscription import Subscription


class SubsDiscountService:
    """Subscription discount service"""

    def __init__(self, postgres: Database):
        self.postgres = postgres

    async def get_discount_by_id(self, discount_id: uuid.UUID) -> SubsDiscount:
        """
        Returns discount by id

        :param discount_id: discount id
        :return: discount
        """

        query = SubsDiscount.select().filter(SubsDiscount.c.id == discount_id)
        return await self.postgres.fetch_one(query=query)

    async def get_discount_for_sub(self, subs_id: uuid.UUID) -> SubsDiscount:
        """
        Returns discount by subscription id

        :param subs_id: subscription id
        :return: subscription
        """

        query = SubsDiscount.select().filter(
            and_(SubsDiscount.c.subscription_id == subs_id,
                 SubsDiscount.c.period_begin <= datetime.datetime.today(),
                 SubsDiscount.c.period_end >= datetime.datetime.today(),
                 SubsDiscount.c.enabled
                 )
        )
        return await self.postgres.fetch_one(query=query)

    @staticmethod
    async def calc_price(subscription: Subscription, discount: SubsDiscount) -> float:
        """
        Returns subscription price after applying discount

        :param subscription: subscription
        :param discount: discount
        :return: price after applying discount
        """

        return subscription.price - discount.value

    async def mark_discount_as_used(self, discount_id: uuid.UUID, user_id: uuid.UUID):
        """
        Marks discount as used by user with user_id

        :param discount_id: discount id
        :param user_id: user id
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
    SubsDiscountService provider
    using 'Depends', it says that it needs Database
    """
    return SubsDiscountService(postgres)
