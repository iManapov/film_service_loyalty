import random
from http import HTTPStatus
import pytest

from core.test_data import test_data
from functional.testdata.discount_data import discount_value, discount_sub_id, discount_film_id, discount_film_tag
from tests.functional.testdata.subscription_data import sub_id

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                '/api/v1/discounts/subs',
                {"subs_id": sub_id},
                {'status': HTTPStatus.OK}
        ),
        (
                '/api/v1/discounts/subs',
                {"subs_id": '3fa85f64-5717-4562-b3fc-2c963f66afa6'},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                '/api/v1/discounts/subs',
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        ),
        (
                f'/api/v1/discounts/subs/{discount_sub_id}',
                {},
                {'status': HTTPStatus.OK}
        )
    ]
)
async def test_discount_sub(make_get_request, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_get_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if hasattr(body, 'price_before'):
        assert body['price_before'] - body['price_after'] == discount_value
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                f'/api/v1/discounts/subs/{discount_sub_id}',
                {"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/discounts/subs/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                {"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                {'status': HTTPStatus.NOT_FOUND}  # Не найдем промокод
        ),
        (
                f'/api/v1/discounts/subs/{discount_sub_id}',
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        ),
    ]
)
async def test_discount_sub_put(make_put_request, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_put_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                f'/api/v1/discounts/films/{discount_film_id}',
                {},
                {'status': HTTPStatus.OK}
        ),
        (
                '/api/v1/discounts/films/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                {},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                '/api/v1/discounts/films',
                {"tag": discount_film_tag, 'user_id': list(test_data.user_subs.keys())[random.randint(0, 2)],
                 'price': 1000},
                {'status': HTTPStatus.OK}
        ),
        (
                '/api/v1/discounts/films',
                {"tag": discount_film_tag, 'user_id': list(test_data.user_subs.keys())[random.randint(0, 2)]},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        ),
        (
                '/api/v1/discounts/films/',
                {"tag": discount_film_tag, 'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                 'price': 1000},
                {'status': HTTPStatus.NOT_FOUND}
        ),
    ]
)
async def test_discount_film(make_get_request, check_cache_discount, check_cache_user, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_get_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if hasattr(body, 'price_before'):
        assert (body['price_before'] - discount_value) * (1 - body['subscriber_discount'] / 100) == body['price_after']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']
    elif status == HTTPStatus.OK and url == '/api/v1/discounts/films':
        cache_response_discount = await check_cache_discount(discount_film_tag)
        assert cache_response_discount['id'] == body['discount_id']
        cache_response_user = await check_cache_user(query_data['user_id'])
        assert cache_response_user['user_id'] == body['user_id']


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                f'/api/v1/discounts/films/{discount_film_id}',
                {"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/discounts/films/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                {"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                {'status': HTTPStatus.NOT_FOUND}  # Не найдем промокод
        ),
        (
                f'/api/v1/discounts/films/{discount_film_id}',
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        ),
    ]
)
async def test_discount_film_put(make_put_request, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_put_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']
