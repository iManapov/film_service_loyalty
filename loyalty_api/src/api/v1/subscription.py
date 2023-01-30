import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.services.subscription import SubscriptionService, get_subscription_service
from src.core.params import params
from src.core.error_messages import error_msgs
from src.models.subscription import SubscriptionApi


router = APIRouter()


@router.get('/',
            response_model=list[SubscriptionApi],
            summary="Получение списка всех подписок",
            description="Получение списка всех подписок",
            )
async def get_subscriptions(
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> list[SubscriptionApi]:
    """

    """

    subs = await subs_service.get_subscriptions()
    if not subs:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.no_subs)
    return subs


@router.get('/{subs_id}',
            response_model=SubscriptionApi,
            summary="Получение информации по одной подписке",
            description="Получение информации по одной подписке",
            )
async def get_subscriptions_by_id(
        subs_id: uuid.UUID = params.subs_id,
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionApi:
    """

    """

    sub = await subs_service.get_subscription_by_id(subs_id=subs_id)
    if not sub:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.no_subs)
    return sub

