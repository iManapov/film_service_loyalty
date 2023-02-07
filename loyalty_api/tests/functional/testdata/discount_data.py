import datetime
import uuid

from functional.testdata.subscription_data import sub_id

discount_sub_id = 'aadfcfb6-7e2e-46da-a151-f0e399b63d20'
discount_film_id = 'aadfcfb6-7e2e-46da-a151-f0e399b63d21'
discount_value = 300
discount_film_tag = 'fantastic'

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
        "tag": discount_film_tag,
    }
    for _ in range(1)
]
pg_discount_film_data.append(
    {
        "id": discount_film_id,
        "title": 'Скидка №2',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "value": discount_value,
        "enabled": True,
        "period_begin": datetime.datetime.today(),
        "period_end": datetime.datetime.today() + datetime.timedelta(days=10),
        "tag": discount_film_tag,
    }
)