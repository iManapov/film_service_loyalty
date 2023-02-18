import uuid

from datetime import datetime
from typing import Optional

from src.schemas.mixin import JsonMixin


class SubsDiscountModel(JsonMixin):
    """Subscription discount schema"""

    id: uuid.UUID
    subscription_id: uuid.UUID
    value: float
    title: Optional[str]
    period_begin: datetime
    period_end: datetime
    enabled: bool
    created_at: datetime
    updated_at: datetime


class FilmDiscountModel(JsonMixin):
    """Film discount schema"""

    id: uuid.UUID
    tag: str
    value: float
    title: Optional[str]
    period_begin: datetime
    period_end: datetime
    enabled: bool
    created_at: datetime
    updated_at: datetime


class SubsDiscountResponseApi(JsonMixin):
    """Subscription discount response schema"""

    discount_id: Optional[uuid.UUID]
    subscription_id: uuid.UUID
    price_before: float
    price_after: float


class FilmDiscountResponse(JsonMixin):
    """Film discount response schema"""

    discount_id: Optional[uuid.UUID]
    user_id: uuid.UUID
    subscriber_discount: int
    price_before: float
    price_after: float


class FilmDiscountResponseApi(FilmDiscountResponse):
    """Film discount response schema"""

    film_id: uuid.UUID
    tag: Optional[str]