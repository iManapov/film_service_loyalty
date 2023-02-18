import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.error_messages import error_msgs
from src.core.params import params
from src.schemas.subscription import SubscriptionApi
from src.schemas.shared import MessageResponseModel, UserIdBody
from src.services.subscription import SubscriptionService, get_subscription_service


router = APIRouter()


@router.get('/',
            response_model=list[SubscriptionApi],
            summary="Get all subscriptions",
            description="Get all subscriptions",
            )
async def get_subscriptions(
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> list[SubscriptionApi]:
    """
    Returns all subscriptions

    :param subs_service: subscriptions service
    :return: list of subscriptions
    """

    subs = await subs_service.get_subscriptions()
    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.no_subs)
    return subs


@router.put('/trial',
            response_model=MessageResponseModel,
            summary="Mark trial subscription as used",
            description="Mark trial subscription as used by user with user_id",
            )
async def mark_trial_subscription_as_used(
        body: UserIdBody,
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> MessageResponseModel:
    """
    Marks trial subscription as used

    :param body: request body
    :param subs_service: subscriptions service
    :return: OK
    """

    subs = await subs_service.get_trial_subscription()
    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.trial_subs_not_found)

    res = await subs_service.mark_trial_subscription_as_used(subs=subs, user_id=body.user_id)
    if res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)

    return MessageResponseModel(msg='OK')


@router.get('/trial',
            response_model=SubscriptionApi,
            summary="Get trial subscription",
            description="Get trial subscription",
            )
async def get_trial_subscription(
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionApi:
    """
    Returns trial subscription

    :param subs_service: subscription service
    :return: trial subscription
    """

    subs = await subs_service.get_trial_subscription()
    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.no_subs)
    return subs


@router.get('/paid',
            response_model=list[SubscriptionApi],
            summary="Get paid subscriptions",
            description="Get paid subscriptions",
            )
async def get_paid_subscriptions(
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> list[SubscriptionApi]:
    """
    Returns paid subscriptions

    :param subs_service: subscription service
    :return: list of paid subscriptions
    """

    subs = await subs_service.get_paid_subscriptions()
    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.no_subs)
    return subs


@router.get('/{subs_id}',
            response_model=SubscriptionApi,
            summary="Get information about subscription",
            description="Get information about subscription with subs_id",
            )
async def get_subscriptions_by_id(
        subs_id: uuid.UUID = params.subs_id,
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionApi:
    """
    Returns subscription by id

    :param subs_id: subscription id
    :param subs_service: subscription service
    :return: subscription
    """

    sub = await subs_service.get_subscription_by_id(subs_id=subs_id)
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.no_subs)
    return sub
