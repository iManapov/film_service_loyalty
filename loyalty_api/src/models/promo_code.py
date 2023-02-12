import uuid

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.core.config import settings


"""Модель промокода в бд"""
PromoCode = sqlalchemy.Table(
    "promocode",
    sqlalchemy.MetaData(schema=settings.postgres_schema),
    sqlalchemy.Column("id", UUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    sqlalchemy.Column("user_id", UUID(), nullable=True),
    sqlalchemy.Column("value", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("code", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("expiration_date", sqlalchemy.Date(), nullable=False),
    sqlalchemy.Column("measure", sqlalchemy.String, default='%', nullable=False),
    sqlalchemy.Column("is_multiple", sqlalchemy.Boolean, default=False, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now()),
)


"""Модель использования промокода в бд"""
PromoUsage = sqlalchemy.Table(
    "promo_usage",
    sqlalchemy.MetaData(schema=settings.postgres_schema),
    sqlalchemy.Column("id", UUID(), default=uuid.uuid4(), nullable=False, unique=True, primary_key=True),
    sqlalchemy.Column("promo_id", UUID(), nullable=False),
    sqlalchemy.Column("user_id", UUID(), nullable=False),
    sqlalchemy.Column("used_at", sqlalchemy.DateTime(timezone=True), nullable=False),
)
