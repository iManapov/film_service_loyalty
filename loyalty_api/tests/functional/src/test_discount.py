from http import HTTPStatus
import pytest

from tests.functional.testdata.discount_data import discount_value, discount_sub_id, discount_id, film_id, invalid_id, \
    user_id, film_id_with_tag
from tests.functional.testdata.subscription_data import sub_id

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                '/api/v1/discounts/subscription/price',
                {"subs_id": sub_id},
                {'status': HTTPStatus.OK}
        ),
        (
                '/api/v1/discounts/subscription/price',
                {"subs_id": invalid_id},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                '/api/v1/discounts/subscription/price',
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        ),
        (
                f'/api/v1/discounts/subscription/{discount_sub_id}',
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
    if 'price_before' in body:
        assert body['price_before'] - body['price_after'] == discount_value
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                f'/api/v1/discounts/subscription/{discount_sub_id}',
                {"user_id": invalid_id},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/discounts/subscription/{invalid_id}',
                {"user_id": invalid_id},
                {'status': HTTPStatus.NOT_FOUND}  # Не найдем промокод
        ),
        (
                f'/api/v1/discounts/subscription/{discount_sub_id}',
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
                f'/api/v1/discounts/film/{discount_id}',
                {},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/discounts/film/{invalid_id}',
                {},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                '/api/v1/discounts/film/price',
                {"film_id": film_id, 'user_id': user_id},
                {'status': HTTPStatus.OK}
        ),
        (
                '/api/v1/discounts/film/price',
                {"film_id": film_id_with_tag, 'user_id': user_id},
                {'status': HTTPStatus.OK}
        ),
        (
                '/api/v1/discounts/film/price',
                {'user_id': user_id},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.missing'}
        ),
        (
                '/api/v1/discounts/film/price',
                {"film_id": film_id, 'user_id': invalid_id},
                {'status': HTTPStatus.NOT_FOUND}
        ),
    ]
)
async def test_discount_film(make_get_request, check_cache_discount, check_cache_user, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_get_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if 'price_before' in body and body['discount_id']:
        assert (body['price_before'] - discount_value) * (1 - body['subscriber_discount'] / 100) == body['price_after']
    elif 'price_before' in body:
        assert body['price_before'] * (1 - body['subscriber_discount'] / 100) == body['price_after']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']
    elif status == HTTPStatus.OK and url == '/api/v1/discounts/films':
        cache_response_discount = await check_cache_discount(film_id)
        assert cache_response_discount['id'] == body['discount_id']
        cache_response_user = await check_cache_user(query_data['user_id'])
        assert cache_response_user['user_id'] == body['user_id']


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                f'/api/v1/discounts/film/{discount_id}',
                {"user_id": invalid_id},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/discounts/film/{invalid_id}',
                {"user_id": invalid_id},
                {'status': HTTPStatus.NOT_FOUND}  # Не найдем промокод
        ),
        (
                f'/api/v1/discounts/film/{discount_id}',
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
