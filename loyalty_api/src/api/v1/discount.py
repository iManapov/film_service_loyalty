import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.services.subs_discount import SubsDiscountService, get_sub_discount_service
from src.services.film_discount import FilmDiscountService, get_film_discount_service
from src.core.params import params
from src.models.discount import SubsDiscountResponseApi, FilmDiscountResponseApi


router = APIRouter()


@router.get('/subs/{subs_id}',
            response_model=SubsDiscountResponseApi,
            summary="Получение цены подписки после применения скидки",
            description="Получение цены подписки после применения скидки",
            )
async def get_subscriptions_discount_by_id(
        subs_id: uuid.UUID = params.subs_id,
        subs_discount_service: SubsDiscountService = Depends(get_sub_discount_service)
) -> SubsDiscountResponseApi:
    """

    """

    new_price = await subs_discount_service.calc_price(subs_id=subs_id)
    if not new_price[0]:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=new_price[1])
    return new_price[1]


@router.get('/films',
            response_model=FilmDiscountResponseApi,
            summary="Получение цены фильма после применения скидок",
            description="Получение цены фильма после применения скидок",
            )
async def get_film_discount_by_tag(
        tag: str = params.film_tag,
        user_id: uuid.UUID = params.user_id,
        price: float = params.price,
        film_discount_service: FilmDiscountService = Depends(get_film_discount_service)
) -> FilmDiscountResponseApi:
    """

    """

    result = await film_discount_service.calc_price(tag=tag, price=price, user_id=user_id)
    print(result)
    if not result[0]:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=result[1])
    return result[1]
