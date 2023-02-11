import uuid

from src.models.mixin import JsonMixin


class MessageResponseModel(JsonMixin):
    """Модель ответа сообщением"""
    msg: str


class UserIdBody(JsonMixin):
    """Модель тела с user_id"""
    user_id: uuid.UUID
