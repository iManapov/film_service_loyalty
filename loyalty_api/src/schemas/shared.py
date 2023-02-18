import uuid

from src.schemas.mixin import JsonMixin


class MessageResponseModel(JsonMixin):
    """Message response schema"""

    msg: str


class UserIdBody(JsonMixin):
    """User id body schema"""
    user_id: uuid.UUID
