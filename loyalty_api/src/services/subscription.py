import uuid
from typing import Optional

from databases import Database
from fastapi import Depends, status
from httpx import AsyncClient

from src.core.config import settings
from src.db.postgres import get_postgres
from src.db.request import get_request
from src.models.subscription import Subscription


class SubscriptionService:
    """Subscription service"""

    def __init__(self, postgres: Database, request: AsyncClient):
        self.postgres = postgres
        self.request = request

    async def get_subscriptions(self) -> list[Subscription]:
        """
        Returns all subscriptions

        :return: all subscriptions list
        """

        query = Subscription.select()
        return await self.postgres.fetch_all(query)

    async def get_paid_subscriptions(self) -> list[Subscription]:
        """
        Returns all paid subscriptions

        :return: all paid subscriptions list
        """

        query = Subscription.select().filter(Subscription.c.price > 0)
        return await self.postgres.fetch_all(query)

    async def get_trial_subscription(self) -> Subscription:
        """
        Returns trial subscription

        :return: trial subscription
        """

        query = Subscription.select().filter(Subscription.c.price == 0)
        return await self.postgres.fetch_one(query)

    async def get_subscription_by_id(self, subs_id: uuid.UUID) -> Subscription:
        """
        Returns subscription by id

        :param subs_id: subscription id
        :return: subscription
        """

        query = Subscription.select().filter(Subscription.c.id == subs_id)
        return await self.postgres.fetch_one(query)

    async def mark_trial_subscription_as_used(self, subs: Subscription, user_id: uuid.UUID) -> Optional[str]:
        """
        Marks trial subscription as used by user with user_id

        :param subs: trial subscription
        :param user_id: user id
        :return: error if exists
        """

        response = await self.request.put(
            url=f'{settings.auth_api_url}/user/{user_id}/subscriptions',
            data={
                'trial_used': True,
                'months': subs.months
            }
        )
        if response.status_code != status.HTTP_200_OK:
            return response.text


def get_subscription_service(
        postgres: Database = Depends(get_postgres),
        request: AsyncClient = Depends(get_request)
) -> SubscriptionService:
    """
    SubscriptionService provider
    using 'Depends', it says that it needs Database and AsyncClient
    """
    return SubscriptionService(postgres, request)
