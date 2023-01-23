import uuid
from datetime import datetime

from typing import Optional

from src.models.mixin import JsonMixin
from src.models.subscription import Subscription


class Discounts(JsonMixin):
    """
    API-Модель для подробного описания скидок
    """
    id: uuid.UUID
    subscription_id: Optional[Subscription]
    value: Optional[int]
    period_begin: Optional[datetime]
    period_end: Optional[datetime]
    enabled: bool
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


