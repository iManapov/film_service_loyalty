import uuid
from typing import Optional

from src.models.mixin import JsonMixin


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
