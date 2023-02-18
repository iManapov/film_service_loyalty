import uuid
from typing import Optional

from fastapi import Depends, status
from httpx import AsyncClient

from src.core.config import settings
from src.core.test_data import test_data
from src.db.request import get_request
from src.schemas.film import Film


class FilmService:
    """Film service"""

    def __init__(
            self,
            request: AsyncClient
    ):
        self.request = request

    async def get_by_id(self, film_id: uuid.UUID) -> Optional[Film]:
        """
        Returns film by id

        :param film_id: film id
        :return: Film object
        """

        film_id = str(film_id)
        if settings.is_functional_testing:
            film = test_data.films.get(film_id)
            if not film:
                return
            film['id'] = film_id
        else:
            film = await self.request.get(f'{settings.film_api_url}/films/{film_id}')
            if film.status_code != status.HTTP_200_OK:
                return
            film = film.json()
            film['id'] = film.pop('uuid')

        return Film(**film)


def get_film_service(
        request: AsyncClient = Depends(get_request)
) -> FilmService:
    """
    FilmService provider
    using 'Depends', it says that it needs AsyncClient
    """

    return FilmService(
        request=request
    )
