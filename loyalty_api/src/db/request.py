from typing import Optional

from httpx import AsyncClient


request: Optional[AsyncClient] = None


async def get_request() -> AsyncClient:
    return request
