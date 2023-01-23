import uuid

from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException

from src.services.promo_code import PromoService, get_promo_service
from src.core.params import params
from src.core.error_messages import error_msgs

from src.models.promo_code import PromoCode, BasePromoApi

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/{promo_id}',
            response_model=PromoCode,
            summary="Информация по одному промокоду",
            description="Детальная информация по отдельному промокоду",
            )
async def promo_details(promo_id: uuid.UUID = params.promo_id,
                        promo_service: PromoService =
                        Depends(get_promo_service)) -> PromoCode:
    """
    Возвращает информацию по одному промокоду
    """
    promo = await promo_service.get_promo_by_id(promo_id)
    if not promo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.code_not_found)
    return PromoCode(uuid=promo.id,
                     user_id=promo.user_id,
                     expired=promo.expired,
                     value=promo.value,
                     measure=promo.measure,
                     multiple=promo.multiple
                     )


@router.post('/promo/',
             response_model=BasePromoApi,
             summary="Добавление одного промокода",
             description="Детальная информация по отдельному промокоду",
             )
async def create_promo(promo: PromoCode,
                       promo_service: PromoService =
                       Depends(get_promo_service)) -> BasePromoApi:
    """
    Добавляет запись в redis по одному промокоду
    """
    promo = await promo_service.create_promo(promo.dict())

    return BasePromoApi(
        id=promo.id,
        code=promo.code,
        measure=promo.measure,
        value=promo.value
    )
