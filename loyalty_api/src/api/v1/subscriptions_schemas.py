from datetime import datetime
from typing import Optional
import uuid

from src.models.mixin import JsonMixin


class SubscriptionApi(JsonMixin):
    """API-Модель для подробного описания подписок"""

    id: uuid.UUID
    name: str
    price: float
    description: Optional[str]
    months: int
    created_at: datetime
    updated_at: datetime
