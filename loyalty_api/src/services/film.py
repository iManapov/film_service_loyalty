import uuid
from http import HTTPStatus

from aioredis import Redis
from fastapi import Depends
from httpx import AsyncClient

from src.core.config import settings
from src.core.error_messages import error_msgs
from src.core.test_data import test_data
from src.db.redis import get_redis_films
from src.db.request import get_request
from src.models.film import Film
from src.utils.cache import AbstractCache, RedisCache


class FilmService:
    """Сервис взаимодействия с фильмами"""

    def __init__(
            self,
            film_cache: AbstractCache,
            request: AsyncClient
    ):
        self.film_cache = film_cache
        self.request = request

    async def get_by_id(self, film_id: uuid.UUID) -> tuple[bool, Film]:
        """
        Получение фильма по id

        :param film_id: id фильма
        :return: фильм
        """

        film_id = str(film_id)
        film = await self.film_cache.get(film_id)
        if not film:
            if settings.is_functional_testing:
                film = test_data.films.get(film_id)
                if not film:
                    return False, error_msgs.film_not_found
                film['uuid'] = film_id
            else:
                film = await self.request.get(f'{settings.film_api_url}/films/{film_id}')
                if film.status_code != HTTPStatus.OK:
                    return False, film.json()
                film = film.json()
            await self.film_cache.set(film_id, film)

        return True, Film(**film)


def get_film_service(
        film_cache: Redis = Depends(get_redis_films),
        request: AsyncClient = Depends(get_request)
) -> FilmService:
    """
    Провайдер FilmService,
    с помощью Depends он сообщает, что ему необходимы Redis и AsyncClient
    """

    return FilmService(
        RedisCache(redis=film_cache, expiration_time=settings.film_cache_expire_in_seconds),
        request
    )
