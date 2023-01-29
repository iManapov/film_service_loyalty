import uuid
import datetime

from fastapi import Depends
from databases import Database
from sqlalchemy import and_

from src.db.postgres import get_postgres
from src.models.subscription import Subscription


class SubscriptionService:
    def __init__(self, postgres: Database):
        self.postgres = postgres

    async def get_subscriptions(self):
        query = Subscription.select()
        return await self.postgres.fetch_all(query)

    async def get_subscription_by_id(self, subs_id: uuid.UUID):
        query = Subscription.select().filter(Subscription.c.id == subs_id)
        return await self.postgres.fetch_one(query)


def get_subscription_service(
        postgres: Database = Depends(get_postgres)
) -> SubscriptionService:
    """
    Провайдер SubscriptionService,
    с помощью Depends он сообщает, что ему необходимы Database
    """
    return SubscriptionService(postgres)
