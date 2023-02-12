import uuid
import datetime

from typing import Optional

from src.schemas.mixin import JsonMixin


class BasePromoApi(JsonMixin):
    """Модель промокода"""

    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    code: str
    measure: str
    value: float
    is_multiple: bool
    expiration_date: datetime.date
    created_at: datetime.date
    updated_at: datetime.date


class PromoPrice(JsonMixin):
    """Модель ответа после применения промокода"""

    price_before: float
    price_after: float
    promo_code: str
    user_id: uuid.UUID


class FilmPromoPriceApi(PromoPrice):
    film_id: uuid.UUID


class SubsPromoPriceApi(PromoPrice):
    subscription_id: uuid.UUID
