import os
from logging import config as logging_config

from src.core.logger import LOGGING
from pydantic import BaseSettings, Field


logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Конфиг сервиса"""

    project_name: str = Field('Loyalty API', env="PROJECT_NAME")
    subscriber_discount: int = 20
    user_cache_expire_in_seconds = 1 * 60  # 1 minute
    discount_cache_expire_in_seconds = 5 * 60  # 1 minute

    redis_host: str = Field('localhost', env="REDIS_HOST")
    redis_port: int = Field('6379', env="REDIS_PORT")

    postgres_host: str = Field('localhost', env='POSTGRES_HOST')
    postgres_port: int = Field(5432, env='POSTGRES_PORT')
    postgres_db: str = Field('loyalty_db', env='POSTGRES_DB')
    postgres_user: str = Field(..., env='POSTGRES_USER')
    postgres_pswd: str = Field(..., env='POSTGRES_PSWD')

    auth_api_url: str = Field('http://localhost:5001/api/v1', env='AUTH_API_URL')

    def get_postgres_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_pswd}@{self.postgres_host}:" \
               f"{self.postgres_port}/{self.postgres_db}?currentSchema=loyalty"

    class Config:
        env_file = "src/core/.env"
        env_file_encoding = "utf-8"


settings = Settings()
