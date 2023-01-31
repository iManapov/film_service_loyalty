import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.core.error_messages import error_msgs
from src.core.params import params
from src.models.subscription import SubscriptionApi
from src.services.subscription import SubscriptionService, get_subscription_service


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
    Возвращает все имеющиеся подписки

    :param subs_service: сервис взаимодействия с подписками
    :return: Список подписок
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
    Получение подписки по id

    :param subs_id: id подписки
    :param subs_service: сервис взаимодействия с подписками
    :return: подписка
    """

    sub = await subs_service.get_subscription_by_id(subs_id=subs_id)
    if not sub:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.no_subs)
    return sub
