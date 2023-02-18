import uuid

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.core.config import settings


"""Subscription discount model"""
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


"""Film discount model"""
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


"""Subscription discount usage model"""
SubsDiscountUsage = sqlalchemy.Table(
    "discount_subscription_usage",
    sqlalchemy.MetaData(schema=settings.postgres_schema),
    sqlalchemy.Column("id", UUID(), default=uuid.uuid4(), nullable=False, unique=True, primary_key=True),
    sqlalchemy.Column("discount_id", UUID(), nullable=False),
    sqlalchemy.Column("user_id", UUID(), nullable=False),
    sqlalchemy.Column("used_at", sqlalchemy.DateTime(timezone=True), nullable=False),
)


"""Film discount usage model"""
FilmsDiscountUsage = sqlalchemy.Table(
    "discount_film_usage",
    sqlalchemy.MetaData(schema=settings.postgres_schema),
    sqlalchemy.Column("id", UUID(), default=uuid.uuid4(), nullable=False, unique=True, primary_key=True),
    sqlalchemy.Column("discount_id", UUID(), nullable=False),
    sqlalchemy.Column("user_id", UUID(), nullable=False),
    sqlalchemy.Column("used_at", sqlalchemy.DateTime(timezone=True), nullable=False),
)
