import uuid
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

from src.utils.cache import AbstractCache


class AbstractViewEngine(ABC):
    """
    Абстрактный класс для реализации отдачи данных сервисом
    """

    @abstractmethod
    def get_record_by_id(self, record_id):
        pass

    @abstractmethod
    def set_record_to_redis(self, data):
        pass


@dataclass
class Views(AbstractViewEngine):
    cache: AbstractCache

    async def get_record_by_id(self, record_id: uuid.UUID) -> Optional[dict]:
        """
        Получаем запись по uuid

        @param record_id: uuid записи
        @return: запись в виде словаря
        """
        record = await self.cache.get(record_id)

        if not record:
            return None
        return record

    async def set_record_to_redis(self, data: dict) -> Optional[dict]:
        """
        Создаем запись по uuid

        @param data: объект записи
        @return: запись в виде словаря
        """
        record = await self.cache.set(data)

        if not record:
            return None
        return record
