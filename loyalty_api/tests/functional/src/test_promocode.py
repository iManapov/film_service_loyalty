from http import HTTPStatus
import pytest

from tests.functional.testdata.promo_data import promo_id, promo_code, user_id, film_id, film_price

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                '/api/v1/promocodes/search',
                {"promo_code": promo_code},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/promocodes/{promo_id}',
                {},
                {'status': HTTPStatus.OK}
        ),
        (
                '/api/v1/promocodes/search',
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        )
    ]
)
async def test_promocode(make_get_request, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_get_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']


async def test_promocode_price(make_get_request):
    # 1. Запрашиваем данные из API
    body, status = await make_get_request('/api/v1/promocodes/search', {"promo_code": promo_code})
    assert status == HTTPStatus.OK
    promo_value = body['value']

    # 2. Проверяем данные
    body, status = await make_get_request(f'/api/v1/promocodes/film/price', {"promo_code": promo_code,
                                                                             "user_id": user_id,
                                                                             "film_id": film_id})
    assert status == HTTPStatus.OK
    assert body['price_after'] == film_price * (1 - promo_value / 100)


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                f'/api/v1/promocodes/{promo_id}',
                {"user_id": user_id},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/promocodes/{user_id}',
                {"user_id": user_id},
                {'status': HTTPStatus.NOT_FOUND}  # Не найдем промокод
        ),
        (
                f'/api/v1/promocodes/{promo_id}',
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        ),
    ]
)
async def test_promocode_put(make_put_request, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_put_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']
