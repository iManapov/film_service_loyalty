import uuid

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.core.config import settings


"""Модель скидки к подписке в бд"""
SubsDiscount = sqlalchemy.Table(
        "discount_subscription",
        sqlalchemy.MetaData(schema=settings.postgres_schema),
        sqlalchemy.Column("id", UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("subscription_id", UUID(), default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("value", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("period_begin", sqlalchemy.Date(), server_default=func.now()),
        sqlalchemy.Column("period_end", sqlalchemy.Date(), nullable=False),
        sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("enabled", sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now())
)


"""Модель скидки к фильму в бд"""
FilmsDiscount = sqlalchemy.Table(
        "discount_film",
        sqlalchemy.MetaData(schema=settings.postgres_schema),
        sqlalchemy.Column("id", UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
        sqlalchemy.Column("tag", sqlalchemy.String, unique=True, nullable=False),
        sqlalchemy.Column("value", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("period_begin", sqlalchemy.Date(), server_default=func.now()),
        sqlalchemy.Column("period_end", sqlalchemy.Date(), nullable=False),
        sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("enabled", sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now())
)


"""Модель использования скидок к подписке"""
SubsDiscountUsage = sqlalchemy.Table(
    "discount_subscription_usage",
    sqlalchemy.MetaData(schema=settings.postgres_schema),
    sqlalchemy.Column("id", UUID(), default=uuid.uuid4(), nullable=False, unique=True, primary_key=True),
    sqlalchemy.Column("discount_id", UUID(), nullable=False),
    sqlalchemy.Column("user_id", UUID(), nullable=False),
    sqlalchemy.Column("used_at", sqlalchemy.DateTime(timezone=True), nullable=False),
)


"""Модель использования скидок к фильму"""
FilmsDiscountUsage = sqlalchemy.Table(
    "discount_film_usage",
    sqlalchemy.MetaData(schema=settings.postgres_schema),
    sqlalchemy.Column("id", UUID(), default=uuid.uuid4(), nullable=False, unique=True, primary_key=True),
    sqlalchemy.Column("discount_id", UUID(), nullable=False),
    sqlalchemy.Column("user_id", UUID(), nullable=False),
    sqlalchemy.Column("used_at", sqlalchemy.DateTime(timezone=True), nullable=False),
)
<<<<<<< HEAD
=======


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


class FilmDiscountModel(JsonMixin):
    """Модель скидки к фильму"""

    id: uuid.UUID
    tag: str
    value: float
    title: Optional[str]
    period_begin: datetime
    period_end: datetime
    enabled: bool
    created_at: datetime
    updated_at: datetime
>>>>>>> 3d0a92849890ab98870707b4c8c2514ac727aab2
