import uuid
from datetime import datetime

from typing import Optional

from src.models.mixin import JsonMixin
from src.models.subscription import Subscription


class Order(JsonMixin):
    """
    API-Модель для подробного описания заказов
    """
    id: uuid.UUID
    subscription_id: Optional[Subscription]
    user_id: Optional[uuid.UUID]
    status: int
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


