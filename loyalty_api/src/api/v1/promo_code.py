import uuid
import datetime

from fastapi import APIRouter, Depends, HTTPException, status
import pytz

from src.core.error_messages import error_msgs
from src.core.params import params
from src.models.promo_code import PromoCode, BasePromoApi, FilmPromoPriceApi, SubsPromoPriceApi
from src.models.shared import MessageResponseModel, UserIdBody
from src.services.film import FilmService, get_film_service
from src.services.promo_code import PromoCodeService, get_promo_service
from src.services.subscription import SubscriptionService, get_subscription_service


router = APIRouter()


@router.get('/search',
            response_model=BasePromoApi,
            summary="Информация по одному промокоду по его коду",
            description="Детальная информация по отдельному промокоду по его коду",
            )
async def get_promo_by_code(
        promo_code: str = params.promo_code,
        promo_service: PromoCodeService = Depends(get_promo_service)
) -> PromoCode:
    """
    Возвращает информацию промокода по коду.

    :param promo_code: промокод
    :param promo_service: сервис взаимодействия с промокодами
    :return: промокод
    """

    promo = await promo_service.get_by_name(promo_code)
    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.promo_not_found)
    return promo


@router.get('/film/price',
            response_model=FilmPromoPriceApi,
            summary="Цена фильма после применения промокода",
            description="Возвращает цену фильма после применения промокода",
            )
async def get_film_price_after_promocode(
        promo_code: str = params.promo_code,
        user_id: uuid.UUID = params.user_id,
        film_id: uuid.UUID = params.film_id,
        promo_service: PromoCodeService = Depends(get_promo_service),
        film_service: FilmService = Depends(get_film_service)
) -> FilmPromoPriceApi:
    """
    Возвращает цену фильма после применения промокода

    :param promo_code: Промокод
    :param user_id: id пользователя
    :param film_id: id фильма
    :param promo_service: сервис взаимодействия с промокодами
    :param film_service: сервис взаимодействия с фильмами
    :return: цена после применения промокода
    """

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.film_not_found)

    promo = await promo_service.get_by_name(promo_code=promo_code)
    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.promo_not_found)
    if promo.user_id and promo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_msgs.promo_wrong_user)
    if promo.expiration_date.replace(tzinfo=pytz.UTC) < datetime.datetime.now(tz=pytz.UTC):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_msgs.promo_expired)
    if not promo.is_multiple:
        if await promo_service.is_promo_used(promo_id=promo.id, user_id=user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=error_msgs.promo_used)

    price_after_promo = await promo_service.calc_price(promo=promo, price=film.price)

    return FilmPromoPriceApi(
        film_id=film.id,
        user_id=user_id,
        price_before=film.price,
        price_after=price_after_promo,
        promo_code=promo_code,
    )


@router.get('/subscription/price',
            response_model=SubsPromoPriceApi,
            summary="Цена подписки после применения промокода",
            description="Возвращает цену подписки после применения промокода",
            )
async def get_subs_price_after_promocode(
        promo_code: str = params.promo_code,
        user_id: uuid.UUID = params.user_id,
        subs_id: uuid.UUID = params.subs_id,
        promo_service: PromoCodeService = Depends(get_promo_service),
        subs_service: SubscriptionService = Depends(get_subscription_service)
) -> SubsPromoPriceApi:
    """
    Возвращает цену подписки после применения промокода

    :param promo_code: Промокод
    :param user_id: id пользователя
    :param subs_id: id подписки
    :param promo_service: сервис взаимодействия с промокодами
    :param subs_service: сервис взаимодействия с подписками
    :return: цена после применения промокода
    """

    subs = await subs_service.get_subscription_by_id(subs_id)
    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.no_subs)

    promo = await promo_service.get_by_name(promo_code=promo_code)
    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.promo_not_found)
    if promo.user_id and promo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_msgs.promo_wrong_user)
    if promo.expiration_date.replace(tzinfo=pytz.UTC) < datetime.datetime.now(tz=pytz.UTC):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_msgs.promo_expired)
    if not promo.is_multiple:
        if await promo_service.is_promo_used(promo_id=promo.id, user_id=user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=error_msgs.promo_used)

    price_after_promo = await promo_service.calc_price(promo=promo, price=subs.price)

    return SubsPromoPriceApi(
        subscription_id=subs.id,
        user_id=user_id,
        price_before=subs.price,
        price_after=price_after_promo,
        promo_code=promo_code,
    )


@router.put('/{promo_id}',
            response_model=MessageResponseModel,
            summary="Отметить промокод как использованный",
            description="Отметить промокод с promo_id как использованный для пользователя с user_id",
            )
async def mark_promo_used_by_user(
        body: UserIdBody,
        promo_id: uuid.UUID = params.promo_id,
        promo_service: PromoCodeService = Depends(get_promo_service)
):
    """
    Отмечает промокод как использованный

    :param body: тело запроса
    :param promo_id: id промокода
    :param promo_service: сервис взаимодействия с промокодами
    :return: OK
    """

    promo = await promo_service.get_by_id(promo_id)
    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.promo_not_found)
    await promo_service.mark_promo_as_used(promo=promo, user_id=body.user_id)
    return MessageResponseModel(msg='OK')


@router.get('/{promo_id}',
            response_model=BasePromoApi,
            summary="Информация по одному промокоду по его id",
            description="Детальная информация по отдельному промокоду по его id",
            )
async def get_promo_by_id(
        promo_id: uuid.UUID = params.promo_id,
        promo_service: PromoCodeService = Depends(get_promo_service)
) -> PromoCode:
    """
    Возвращает информацию промокода по id

    :param promo_id: id промокода
    :param promo_service: сервис взаимодействия с промокодами
    :return: промокод
    """

    promo = await promo_service.get_by_id(promo_id)
    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_msgs.promo_not_found)
    return promo
