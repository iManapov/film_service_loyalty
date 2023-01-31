import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.services.promo_code import PromoCodeService, get_promo_service
from src.core.params import params
from src.core.error_messages import error_msgs
from src.models.promo_code import PromoCode, BasePromoApi, PromoPriceApi
from src.models.shared import MessageResponseModel, UserIdBody


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
    Возвращает информацию промокода по коду
    """
    promo = await promo_service.get_by_name(promo_code)
    if not promo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.promo_not_found)
    return promo


@router.get('/price',
            response_model=PromoPriceApi,
            summary="Цена фильма/подписки после применения промокода",
            description="Возвращает цену фильма/подписки после применения промокода",
            )
async def get_price_by_promocode(
        promo_code: str = params.promo_code,
        user_id: uuid.UUID = params.user_id,
        price: float = params.price,
        promo_service: PromoCodeService = Depends(get_promo_service)
) -> PromoPriceApi:
    """
    Возвращает информацию промокода по id
    """
    price_after_promo = await promo_service.calc_price(user_id=user_id, promo_code=promo_code, price=price)
    if not price_after_promo[0]:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=price_after_promo[1])

    return PromoPriceApi(
        price_before=price,
        price_after=price_after_promo[1],
        promo_code=promo_code,
        user_id=user_id
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
    Возвращает информацию промокода по id
    """
    promo = await promo_service.get_by_id(promo_id)
    if not promo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
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
    """
    promo = await promo_service.get_by_id(promo_id)
    if not promo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.promo_not_found)
    return promo
