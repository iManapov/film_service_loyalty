import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JsonMixin(BaseModel):
    class Config:
        """Faster class to work with json"""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
