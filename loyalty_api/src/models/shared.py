import uuid

from src.models.mixin import JsonMixin


class MessageResponseModel(JsonMixin):
    msg: str


class UserIdBody(JsonMixin):
    user_id: uuid.UUID

