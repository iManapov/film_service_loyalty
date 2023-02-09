import datetime
import uuid

sub_id = 'aadfcfb6-7e2e-46da-a151-f0e399b63d20'

pg_sub_data = [
    {
        "id": str(uuid.uuid4()),
        "name": 'Подписка на 3 месяца',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "price": 1000,
        "months": 3,
    }
    for _ in range(1)
]
pg_sub_data.append(
    {
        "id": sub_id,
        "name": 'Подписка на 12 месяцев',
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "price": 2500,
        "months": 12,
    }
)
