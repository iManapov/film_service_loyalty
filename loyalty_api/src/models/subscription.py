import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.core.config import settings
from src.models.mixin import JsonMixin


"""Модель подписки в бд"""
Subscription = sqlalchemy.Table(
    "subscription",
    sqlalchemy.MetaData(schema=settings.postgres_schema),
    sqlalchemy.Column("id", UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("months", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now())
)


class SubscriptionApi(JsonMixin):
    """API-Модель для подробного описания подписок"""

    id: uuid.UUID
    name: str
    price: float
    description: Optional[str]
    months: int
    created_at: datetime
    updated_at: datetime
