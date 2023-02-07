import datetime
import uuid
import random

promo_id = 'aadfcfb6-7e2e-46da-a151-f0e399b63d20'

pg_promo_data = [
    {
        "id": str(uuid.uuid4()),
        "value": random.randint(0, 40),
        "code": 'J892KZ37',
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
        "code": 'J892KZ37',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "expiration_date": datetime.datetime.now() + datetime.timedelta(days=1),
        "measure": '%',
        "is_multiple": False
    }
)
