import uuid

from datetime import datetime
from typing import Optional

from src.schemas.mixin import JsonMixin


class SubscriptionApi(JsonMixin):
    """API-Модель для подробного описания подписок"""

    id: uuid.UUID
    name: str
    price: float
    description: Optional[str]
    months: int
    created_at: datetime
    updated_at: datetime
