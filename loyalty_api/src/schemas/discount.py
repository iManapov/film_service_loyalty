import uuid

from datetime import datetime
from typing import Optional

from src.schemas.mixin import JsonMixin


class SubsDiscountModel(JsonMixin):
    """Модель скидки к подписке"""

    id: uuid.UUID
    subscription_id: uuid.UUID
    value: float
    title: Optional[str]
    period_begin: datetime
    period_end: datetime
    enabled: bool
    created_at: datetime
    updated_at: datetime


# Redis
class FilmDiscountModel(JsonMixin):
    """Модель скидки к фильму"""

    id: uuid.UUID
    tag: str  # key in redis
    value: float
    title: Optional[str]
    period_begin: datetime
    period_end: datetime
    enabled: bool
    created_at: datetime
    updated_at: datetime


class SubsDiscountResponseApi(JsonMixin):
    """Модель ответа после применения скидки к подписке"""

    discount_id: Optional[uuid.UUID]
    subscription_id: uuid.UUID
    price_before: float
    price_after: float


class FilmDiscountResponse(JsonMixin):
    """Модель после применения скидки к фильму"""

    discount_id: Optional[uuid.UUID]
    user_id: uuid.UUID
    subscriber_discount: int
    price_before: float
    price_after: float


class FilmDiscountResponseApi(FilmDiscountResponse):
    """Модель ответа после применения скидки к фильму"""

    film_id: uuid.UUID
    tag: Optional[str]