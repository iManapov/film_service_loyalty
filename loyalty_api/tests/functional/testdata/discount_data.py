import datetime
import random
import uuid

from src.core.test_data import test_data
from tests.functional.testdata.subscription_data import sub_id

discount_sub_id = 'aadfcfb6-7e2e-46da-a151-f0e399b63d20'
discount_id = 'aadfcfb6-7e2e-46da-a151-f0e399b63d21'
discount_value = 300
film_id = list(test_data.films.keys())[0]
film_id_with_tag = list(test_data.films.keys())[1]
film_tag = 'fantastic'
invalid_id = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
user_id = list(test_data.user_subs.keys())[random.randint(0, 2)]

pg_discount_sub_data = [
    {
        "id": str(uuid.uuid4()),
        "title": 'Скидка №1',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "value": discount_value,
        "enabled": True,
        "period_begin": datetime.datetime.today(),
        "period_end": datetime.datetime.today() + datetime.timedelta(days=10),
        "subscription_id": sub_id,
    }
    for _ in range(1)
]
pg_discount_sub_data.append(
    {
        "id": discount_sub_id,
        "title": 'Скидка №2',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "value": discount_value,
        "enabled": True,
        "period_begin": datetime.datetime.today(),
        "period_end": datetime.datetime.today() + datetime.timedelta(days=10),
        "subscription_id": sub_id,
    }
)

pg_discount_film_data = [
    {
        "id": str(uuid.uuid4()),
        "title": 'Скидка №1',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "value": discount_value,
        "enabled": True,
        "period_begin": datetime.datetime.today(),
        "period_end": datetime.datetime.today() + datetime.timedelta(days=10),
        "tag": film_tag,
    }
    for _ in range(1)
]
pg_discount_film_data.append(
    {
        "id": discount_id,
        "title": 'Скидка №2',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "value": discount_value,
        "enabled": True,
        "period_begin": datetime.datetime.today(),
        "period_end": datetime.datetime.today() + datetime.timedelta(days=10),
        "tag": film_tag,
    }
)