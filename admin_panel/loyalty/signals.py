import logging

import redis

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from loyalty.models import DiscountFilm
from loyalty.utils.redis import AbstractCache, RedisCache
from config import settings


logger = logging.getLogger(__name__)


@receiver([post_delete, post_save], sender=DiscountFilm)
def signal_clear_cache(sender, instance, using, **kwargs):
    """Signal triggered when saving or deleting a record"""

    del_cache(instance)


def del_cache(row):
    """
    Deletes record from Redis cache when deleting record from Postgres

    :param row: deleting row
    """

    try:
        redis_cache = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", db=int(settings.REDIS_DB)
        )
        cache = RedisCache(redis=redis_cache)
        cache.delete(row.tag)
    except Exception as e:
        logger.error(e)
