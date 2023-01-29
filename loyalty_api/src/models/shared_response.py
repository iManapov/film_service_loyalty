from pydantic import BaseModel


class MessageResponseModel(BaseModel):
    msg: str
