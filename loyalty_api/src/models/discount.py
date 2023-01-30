import uuid
from datetime import datetime
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from typing import Optional

from src.models.mixin import JsonMixin


SubsDiscount = sqlalchemy.Table(
        "discount_subscription",
        sqlalchemy.MetaData(),
        sqlalchemy.Column("id", UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("subscription_id", UUID(), default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("value", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("period_begin", sqlalchemy.Date(), server_default=func.now()),
        sqlalchemy.Column("period_end", sqlalchemy.Date(), default='2050-01-01', nullable=False),
        sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("enabled", sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now())
)


FilmsDiscount = sqlalchemy.Table(
        "discount_film",
        sqlalchemy.MetaData(),
        sqlalchemy.Column("id", UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("tag", sqlalchemy.String, unique=True, nullable=False),
        sqlalchemy.Column("value", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("period_begin", sqlalchemy.Date(), server_default=func.now()),
        sqlalchemy.Column("period_end", sqlalchemy.Date(), default='2050-01-01', nullable=False),
        sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("enabled", sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now())
)


# Redis
class FilmDiscountModel(JsonMixin):
    id: uuid.UUID
    tag: str  # key in redis
    value: float
    title: Optional[str]
    period_begin: datetime
    period_end: datetime
    enabled: bool
    created_at: datetime
    modified_at: datetime


class SubsDiscountResponseApi(JsonMixin):
    discount_id: Optional[uuid.UUID]
    subscription_id: uuid.UUID
    price_before: float
    price_after: float


class FilmDiscountResponseApi(JsonMixin):
    discount_id: Optional[uuid.UUID]
    tag: str
    user_id: uuid.UUID
    subscriber_discount: int
    price_before: float
    price_after: float

