from typing import Optional

from databases import Database


postgres: Optional[Database] = None


async def get_postgres() -> Database:
    return postgres
