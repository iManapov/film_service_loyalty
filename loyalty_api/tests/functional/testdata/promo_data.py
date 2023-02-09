import datetime
import uuid
import random

from src.core.test_data import test_data

promo_id = 'aadfcfb6-7e2e-46da-a151-f0e399b63d20'
promo_code = 'J892KZ37'
film_id = list(test_data.films.keys())[0]
film_price = test_data.films[film_id]['price']
user_id = list(test_data.user_subs.keys())[random.randint(0, 2)]

pg_promo_data = [
    {
        "id": str(uuid.uuid4()),
        "value": random.randint(0, 40),
        "code": promo_code,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "expiration_date": datetime.datetime.now() + datetime.timedelta(days=1),
        "measure": '%',
        "is_multiple": False
    }
    for _ in range(1)
]
pg_promo_data.append(
    {
        "id": promo_id,
        "value": random.randint(0, 40),
        "code": promo_code,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "expiration_date": datetime.datetime.now() + datetime.timedelta(days=1),
        "measure": '%',
        "is_multiple": False
    }
)
