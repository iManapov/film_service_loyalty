from typing import Optional
import uuid

from src.models.mixin import JsonMixin


class Film(JsonMixin):
    id: uuid.UUID
    title: str
    imdb_rating: Optional[float]
    price: float
    tag: Optional[str]
    description: Optional[str]
    genre: Optional[list]
    actors: Optional[list]
    writers: Optional[list]
    director: Optional[list]
