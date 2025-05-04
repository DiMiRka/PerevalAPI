import multiprocessing
import os
from pathlib import Path

from pydantic import PostgresDsn, Field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


env_path = Path('.env.docker' if os.getenv('DOCKER_MODE') else '.env')
load_dotenv(env_path)


class AppSettings(BaseSettings):
    postgres_user: str = Field(default='postgres', env='POSTGRES_USER')
    postgres_password: str = Field(default='postgres', env='POSTGRES_PASSWORD')
    postgres_host: str = Field(default='localhost', env='POSTGRES_HOST')
    postgres_port: str = Field(default='5432', env='POSTGRES_PORT')
    postgres_db: str = Field(default='pereval', env='POSTGRES_DB')

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=int(self.postgres_port),
            path=self.postgres_db
        )

    host: str = Field(default='localhost', env='HOST')  # Изменил app_host → host
    port: int = Field(default=8000, env='PORT')  # Изменил app_port → port
    reload: bool = Field(default=True, env='RELOAD')

    class Config:
        _env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'


app_settings = AppSettings()


uvicorn_options = {
    "host": app_settings.host,
    "port": app_settings.port,
    "reload": app_settings.reload
}
