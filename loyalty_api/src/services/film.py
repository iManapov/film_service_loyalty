import uuid
from http import HTTPStatus

from fastapi import Depends
from httpx import AsyncClient

from src.core.config import settings
from src.core.error_messages import error_msgs
from src.core.test_data import test_data
from src.db.request import get_request
from src.schemas.film import Film


class FilmService:
    """Сервис взаимодействия с фильмами"""

    def __init__(
            self,
            request: AsyncClient
    ):
        self.request = request

    async def get_by_id(self, film_id: uuid.UUID) -> tuple[bool, Film]:
        """
        Получение фильма по id

        :param film_id: id фильма
        :return: фильм
        """

        film_id = str(film_id)
        if settings.is_functional_testing:
            film = test_data.films.get(film_id)
            if not film:
                return False, error_msgs.film_not_found
            film['id'] = film_id
        else:
            film = await self.request.get(f'{settings.film_api_url}/films/{film_id}')
            if film.status_code != HTTPStatus.OK:
                return False, film.json()
            film = film.json()
            film['id'] = film.pop('uuid')

        return True, Film(**film)


def get_film_service(
        request: AsyncClient = Depends(get_request)
) -> FilmService:
    """
    Провайдер FilmService,
    с помощью Depends он сообщает, что ему необходимы AsyncClient
    """

    return FilmService(
        request=request
    )
