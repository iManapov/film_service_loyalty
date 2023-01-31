import uuid

from databases import Database
from fastapi import Depends

from src.db.postgres import get_postgres
from src.models.subscription import Subscription


class SubscriptionService:
    """Сервис взаимодействия с подписками"""

    def __init__(self, postgres: Database):
        self.postgres = postgres

    async def get_subscriptions(self) -> list[Subscription]:
        """
        Получить все подписки

        :return: список подписок
        """

        query = Subscription.select()
        return await self.postgres.fetch_all(query)

    async def get_subscription_by_id(self, subs_id: uuid.UUID) -> Subscription:
        """
        Получение подписки по ее id

        :param subs_id: id подписки
        :return: подписка
        """

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
