import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.core.error_messages import error_msgs
from src.core.params import params
from src.models.discount import SubsDiscountResponseApi, FilmDiscountResponseApi, \
    FilmDiscountModel, SubsDiscountModel
from src.models.shared import MessageResponseModel, UserIdBody
from src.services.film import FilmService, get_film_service
from src.services.film_discount import FilmDiscountService, get_film_discount_service
from src.services.subs_discount import SubsDiscountService, get_sub_discount_service


router = APIRouter()


@router.get('/subscription/price',
            response_model=SubsDiscountResponseApi,
            summary="Получение цены подписки после применения скидки",
            description="Получение цены подписки после применения скидки",
            )
async def get_subscriptions_discount_by_subscription_id(
        subs_id: uuid.UUID = params.subs_id,
        subs_discount_service: SubsDiscountService = Depends(get_sub_discount_service)
) -> SubsDiscountResponseApi:
    """
    Возвращает скидку на подписку по ее id.

    :param subs_id: id подписки
    :param subs_discount_service: сервис взаимодействия со скидками к подпискам
    :return: Цена со скидкой
    """

    new_price = await subs_discount_service.calc_price(subs_id=subs_id)
    if not new_price[0]:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=new_price[1])
    return new_price[1]


@router.get('/subscription/{discount_id}',
            response_model=SubsDiscountModel,
            summary="Получение информации о скидки для подписки по id",
            description="Получение информации о скидки для подписки по id",
            )
async def get_subscription_discount_by_discount_id(
        discount_id: uuid.UUID = params.discount_id,
        subs_discount_service: SubsDiscountService = Depends(get_sub_discount_service)
) -> SubsDiscountModel:
    """
    Возвращает информацию о скидке для подписки по id

    :param discount_id: id скидки
    :param subs_discount_service: сервис взаимодействия со скидками к подпискам
    :return: Скидка
    """

    discount = await subs_discount_service.get_discount_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.discount_not_found)

    return discount


@router.put('/subscription/{discount_id}',
            response_model=MessageResponseModel,
            summary="Отметить скидку для подписки как примененную",
            description="Отметить скидки для подписки как примененную",
            )
async def mark_subs_discount_as_used(
        body: UserIdBody,
        discount_id: uuid.UUID = params.discount_id,
        subs_discount_service: SubsDiscountService = Depends(get_sub_discount_service)
) -> MessageResponseModel:
    """
    Отмечает скидку для подписки как использованную.

    :param body: тело запроса
    :param discount_id: id скидки
    :param subs_discount_service: сервис взаимодействия со скидками к подпискам
    :return: OK
    """

    discount = await subs_discount_service.get_discount_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.discount_not_found)
    await subs_discount_service.mark_discount_as_used(discount_id=discount_id, user_id=body.user_id)

    return MessageResponseModel(msg='OK')


@router.get('/film/price',
            response_model=FilmDiscountResponseApi,
            summary="Получение цены фильма после применения скидок",
            description="Получение цены фильма после применения скидок",
            )
async def get_film_discount_by_film_id(
        film_id: uuid.UUID = params.film_id,
        user_id: uuid.UUID = params.user_id,
        film_discount_service: FilmDiscountService = Depends(get_film_discount_service),
        film_service: FilmService = Depends(get_film_service),
) -> FilmDiscountResponseApi:
    """
    Получение скидки к фильму по id фильма.

    :param film_id: id фильма
    :param user_id: id пользователя
    :param film_discount_service: сервис взаимодействия со скидками к фильмам
    :param film_service: сервис взаимодействия с фильмами
    :return: Цена со скидкой
    """

    film = await film_service.get_by_id(film_id)
    if not film[0]:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=film[1])
    film = film[1]
    result = await film_discount_service.calc_price(film=film, user_id=user_id)
    if not result[0]:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=result[1])

    return FilmDiscountResponseApi(**{**result[1].dict(), 'tag': film.tag, 'film_id': film_id})


@router.get('/film/{discount_id}',
            response_model=FilmDiscountModel,
            summary="Получение информации о скидки для фильма по id",
            description="Получение информации о скидки для фильма по id",
            )
async def get_film_discount_by_discount_id(
        discount_id: uuid.UUID = params.discount_id,
        film_discount_service: FilmDiscountService = Depends(get_film_discount_service)
) -> FilmDiscountModel:
    """
    Возвращает информацию о скидке к фильму по id

    :param discount_id: id скидки
    :param film_discount_service: сервис взаимодействия со скидками к фильмам
    :return: скидка
    """

    discount = await film_discount_service.get_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.discount_not_found)

    return discount


@router.put('/film/{discount_id}',
            response_model=MessageResponseModel,
            summary="Отметить скидку для фильма как примененную",
            description="Отметить скидку для фильма как примененную",
            )
async def mark_film_discount_as_used(
        body: UserIdBody,
        discount_id: uuid.UUID = params.discount_id,
        film_discount_service: FilmDiscountService = Depends(get_film_discount_service)
) -> MessageResponseModel:
    """
    Отмечает скидку к фильму как использованную.

    :param body: тело запроса
    :param discount_id: id скидки
    :param film_discount_service: сервис взаимодействия со скидками к фильмам
    :return: OK
    """

    discount = await film_discount_service.get_by_id(discount_id=discount_id)
    if not discount:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.discount_not_found)
    await film_discount_service.mark_discount_as_used(discount_id=discount_id, user_id=body.user_id)

    return MessageResponseModel(msg='OK')
