from http import HTTPStatus
import pytest

from tests.functional.testdata.subscription_data import sub_id

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                '/api/v1/subscriptions/',
                {},
                {'status': HTTPStatus.OK}
        ),
        (
                f'/api/v1/subscriptions/{sub_id}',
                {},
                {'status': HTTPStatus.OK}
        ),
    ]
)
async def test_subscription(make_get_request, query_data, expected_answer, url):
    # 1 Запрашиваем данные из Postgres по API
    body, status = await make_get_request(url, query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']

