import uuid
from datetime import datetime

from typing import Optional

from pydantic import BaseModel

from src.models.mixin import JsonMixin


# Модели ответа API
class PromoCode(JsonMixin):
    """
    API-Модель для подробного описания промокода
    """
    id: Optional[uuid.UUID]  # Сделал Optional, потому что создавать id буду перед записью в redis
    user_id: Optional[uuid.UUID]
    code: str
    expired: Optional[datetime]
    value: Optional[float]
    measure: str = '%'
    multiple: bool = False
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class BasePromoApi(BaseModel):
    """
    API-Модель для краткого описания фильма
    """
    id: uuid.UUID
    code: str
    measure: str = '%'
    value: Optional[float]
