import uuid
from datetime import datetime

from typing import Optional

from src.models.mixin import JsonMixin


class Subscription(JsonMixin):
    """
    API-Модель для подробного описания подписок
    """
    id: uuid.UUID
    name: str
    price: float
    description: str
    months: int
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


