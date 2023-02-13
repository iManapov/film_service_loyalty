from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    """Конфиг тестов"""

    redis_host: str = Field('127.0.0.1', env="REDIS_HOST")
    redis_port: int = Field('6379', env="REDIS_PORT")
    service_url: str = Field("http://localhost:8009", env="FAST_API_URL")
    postgres_host: str = Field('localhost', env='POSTGRES_HOST')
    postgres_port: int = Field(5432, env='POSTGRES_PORT')
    postgres_db: str = Field('loyalty_api', env='POSTGRES_DB')
    postgres_user: str = Field('app', env='POSTGRES_USER')
    postgres_pswd: str = Field('123qwe', env='POSTGRES_PSWD')

    auth_api_url: str = Field('http://localhost:5001/api/v1', env='AUTH_API_URL')

    backoff_start_sleep_time: float = 1
    backoff_factor: int = 2
    backoff_border_sleep_time: int = 10

    def get_postgres_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_pswd}@{self.postgres_host}:" \
               f"{self.postgres_port}/{self.postgres_db}?currentSchema=loyalty"

    class Config:
        env_file = "tests/functional/.env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()
