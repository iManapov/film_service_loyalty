import uuid
# from datetime import datetime
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

# from typing import Optional
#
# from src.models.mixin import JsonMixin


Subscription = sqlalchemy.Table(
    "subscription",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("months", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
    sqlalchemy.Column("modified_at", sqlalchemy.DateTime(timezone=True), onupdate=func.now())
)


# class Subscription(JsonMixin):
#     """
#     API-Модель для подробного описания подписок
#     """
#     id: uuid.UUID
#     name: str
#     price: float
#     description: str
#     months: int
#     created_at: Optional[datetime]
#     modified_at: Optional[datetime]


