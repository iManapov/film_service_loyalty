import uuid
import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.config import settings
from src.core.error_messages import error_msgs
from src.core.params import params
from src.schemas.discount import SubsDiscountResponseApi, FilmDiscountResponseApi, \
    FilmDiscountModel, SubsDiscountModel
from src.schemas.shared import MessageResponseModel, UserIdBody
from src.services.film import FilmService, get_film_service
from src.services.film_discount import FilmDiscountService, get_film_discount_service
from src.services.subs_discount import SubsDiscountService, get_sub_discount_service
from src.services.subscription import SubscriptionService, get_subscription_service
from src.services.user import UserService, get_user_service


router = APIRouter()


@router.get('/subscription/price',
            response_model=SubsDiscountResponseApi,
            summary="Get subscription price after applying discount",
            description="Get subscription price after applying discount",
            )
async def get_subscriptions_discount_by_subscription_id(
        subs_id: uuid.UUID = params.subs_id,
        subs_service: SubscriptionService = Depends(get_subscription_service),
        subs_discount_service: SubsDiscountService = Depends(get_sub_discount_service)
) -> SubsDiscountResponseApi:
    """
    Returns subscription discount by id

    :param subs_id: subscription id
    :param subs_service: subscription service
    :param subs_discount_service: subscription discount service
    :return: price after discount
    """

    subs = await subs_service.get_subscription_by_id(subs_id)
    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.no_subs)

    discount = await subs_discount_service.get_discount_for_sub(subs_id=subs.id)

    if not discount:
        return SubsDiscountResponseApi(
            price_before=subs.price,
            price_after=subs.price,
            discount_id=None,
            subscription_id=subs.id
        )

    new_price = await subs_discount_service.calc_price(subscription=subs, discount=discount)

    return SubsDiscountResponseApi(
        price_before=subs.price,
        price_after=new_price,
        discount_id=discount.id,
        subscription_id=subs.id
    )


@router.get('/subscription/{discount_id}',
            response_model=SubsDiscountModel,
            summary="Get information about subscription discount by id",
            description="Get information about subscription discount by id",
            )
async def get_subscription_discount_by_discount_id(
        discount_id: uuid.UUID = params.discount_id,
        subs_discount_service: SubsDiscountService = Depends(get_sub_discount_service)
) -> SubsDiscountModel:
    """
    Returns information about subscription discount by id

    :param discount_id: discount id
    :param subs_discount_service: subscription discount service
    :return: discount
    """

    discount = await subs_discount_service.get_discount_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.discount_not_found)

    return discount


@router.put('/subscription/{discount_id}',
            response_model=MessageResponseModel,
            summary="Mark subscription discount as used",
            description="Mark subscription discount as used",
            )
async def mark_subs_discount_as_used(
        body: UserIdBody,
        discount_id: uuid.UUID = params.discount_id,
        subs_discount_service: SubsDiscountService = Depends(get_sub_discount_service)
) -> MessageResponseModel:
    """
    Marks subscription discount as used

    :param body: request body
    :param discount_id: discount id
    :param subs_discount_service: subscription discount service
    :return: OK
    """

    discount = await subs_discount_service.get_discount_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.discount_not_found)
    await subs_discount_service.mark_discount_as_used(discount_id=discount_id, user_id=body.user_id)

    return MessageResponseModel(msg='OK')


@router.get('/film/price',
            response_model=FilmDiscountResponseApi,
            summary="Get film price after applying discount",
            description="Get film price after applying discount",
            )
async def get_film_discount_by_film_id(
        film_id: uuid.UUID = params.film_id,
        user_id: uuid.UUID = params.user_id,
        film_discount_service: FilmDiscountService = Depends(get_film_discount_service),
        film_service: FilmService = Depends(get_film_service),
        user_service: UserService = Depends(get_user_service),
) -> FilmDiscountResponseApi:
    """
    Returns film discount by film id

    :param film_id: film id
    :param user_id: user id
    :param film_discount_service: film discount service
    :param film_service: film service
    :param user_service: user service
    :return: price after discount
    """

    discount = None
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.film_not_found)

    if film.tag:
        discount = await film_discount_service.get_discount(tag=film.tag)

    user = await user_service.get_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.user_not_found)

    price_after = await film_discount_service.calc_price(film=film, user=user, discount=discount)

    return FilmDiscountResponseApi(
        discount_id=discount.id if discount else None,
        user_id=user.id,
        subscriber_discount=settings.subscriber_discount if datetime.datetime.today() <= user.subscription_until else 0,
        price_before=film.price,
        price_after=price_after,
        film_id=film.id,
        tag=film.tag
    )


@router.get('/film/{discount_id}',
            response_model=FilmDiscountModel,
            summary="Get information about film discount by id",
            description="Get information about film discount by id",
            )
async def get_film_discount_by_discount_id(
        discount_id: uuid.UUID = params.discount_id,
        film_discount_service: FilmDiscountService = Depends(get_film_discount_service)
) -> FilmDiscountModel:
    """
    Returns information about film discount by id

    :param discount_id: discount id
    :param film_discount_service: film discount service
    :return: discount
    """

    discount = await film_discount_service.get_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.discount_not_found)

    return discount


@router.put('/film/{discount_id}',
            response_model=MessageResponseModel,
            summary="Mark film discount as used",
            description="Mark film discount as used",
            )
async def mark_film_discount_as_used(
        body: UserIdBody,
        discount_id: uuid.UUID = params.discount_id,
        film_discount_service: FilmDiscountService = Depends(get_film_discount_service)
) -> MessageResponseModel:
    """
    Marks film discount as used

    :param body: request body
    :param discount_id: discount id
    :param film_discount_service: film discount service
    :return: OK
    """

    discount = await film_discount_service.get_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.discount_not_found)
    await film_discount_service.mark_discount_as_used(discount_id=discount_id, user_id=body.user_id)

    return MessageResponseModel(msg='OK')
