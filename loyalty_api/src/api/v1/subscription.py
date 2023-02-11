import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.core.error_messages import error_msgs
from src.core.params import params
from src.models.subscription import SubscriptionApi
from src.models.shared import MessageResponseModel, UserIdBody
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


@router.put('/trial',
            response_model=MessageResponseModel,
            summary="Отметить пробную подписку использованной пользователем user_id",
            description="Отметить пробную подписку использованной пользователем user_id",
            )
async def mark_trial_subscription_as_used(
        body: UserIdBody,
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> MessageResponseModel:
    """
    Отмечает пробную подписку использованной пользователем user_id

    :param body: тело запроса
    :param subs_service: сервис взаимодействия с подписками
    :return: OK
    """

    subs = await subs_service.get_trial_subscription()
    if not subs:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.trial_subs_not_found)

    res = await subs_service.mark_trial_subscription_as_used(subs=subs, user_id=body.user_id)
    if res:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=res)

    return MessageResponseModel(msg='OK')


@router.get('/trial',
            response_model=SubscriptionApi,
            summary="Получение пробной подписки",
            description="Получение пробной подписки",
            )
async def get_trial_subscription(
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionApi:
    """
    Возвращает пробную подписку

    :param subs_service: сервис взаимодействия с подписками
    :return: Пробная подписка
    """

    subs = await subs_service.get_trial_subscription()
    if not subs:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.no_subs)
    return subs


@router.get('/paid',
            response_model=list[SubscriptionApi],
            summary="Получение платных подписок",
            description="Получение платных подписок",
            )
async def get_paid_subscriptions(
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> list[SubscriptionApi]:
    """
    Возвращает платные подписки

    :param subs_service: сервис взаимодействия с подписками
    :return: Платные подписки
    """

    subs = await subs_service.get_paid_subscriptions()
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
