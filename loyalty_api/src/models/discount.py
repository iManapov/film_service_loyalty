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
        sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("subscription_id", UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("value", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("period_begin", sqlalchemy.Date(), server_default=func.now()),
        sqlalchemy.Column("period_end", sqlalchemy.Date(), default='2050-01-01', nullable=False),
        sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("enabled", sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now())
)


# Redis
class FilmDiscount(JsonMixin):
    id: uuid.UUID
    tag: str  # key in redis
    value: float
    title: Optional[str]
    period_begin: datetime
    period_end: datetime
    enabled: bool
    created_at: datetime
    modified_at: datetime


# API request
# class UserTrialUsage(JsonMixin):
#     trial_sub_id: uuid.UUID
#     user_id: uuid.UUID
#     started_at: datetime
