import uuid
from typing import Optional

from pydantic import BaseModel
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


Promocode = sqlalchemy.Table(
    "promocodes",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    sqlalchemy.Column("user_id", UUID(as_uuid=True), nullable=True),
    sqlalchemy.Column("value", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("code", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("expiration_date", sqlalchemy.Date(), default='2050-01-01', nullable=False),
    sqlalchemy.Column("measure", sqlalchemy.String, default='%', nullable=False),
    sqlalchemy.Column("is_multiple", sqlalchemy.Boolean, default=False, nullable=False),
    sqlalchemy.Column("is_used", sqlalchemy.Boolean, default=False, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now()),
)


PromoUsage = sqlalchemy.Table(
    "promo_usage",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("promo_id", UUID(as_uuid=True), nullable=False),
    sqlalchemy.Column("user_id", UUID(as_uuid=True), nullable=False),
    sqlalchemy.Column("used_at", sqlalchemy.DateTime(timezone=True), nullable=False),
)


class BasePromoApi(BaseModel):
    """
    API-Модель для краткого описания фильма
    """
    id: uuid.UUID
    code: str
    measure: str = '%'
    value: Optional[float]


# # Модели ответа API
# class PromoCode(JsonMixin):
#     """
#     API-Модель для подробного описания промокода
#     """
#     id: Optional[uuid.UUID]  # Сделал Optional, потому что создавать id буду перед записью в redis
#     user_id: Optional[uuid.UUID]
#     value: Optional[float]
#     code: str
#     expired: Optional[datetime]
#     measure: str = '%'
#     multiple: bool = False
#     created_at: Optional[datetime]
#     modified_at: Optional[datetime]
