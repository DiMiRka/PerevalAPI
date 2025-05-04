import multiprocessing
import os

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class AppSettings(BaseSettings):
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_port: str = os.getenv("POSTGRES_PORT")
    postgres_db: str = os.getenv("POSTGRES_DB")
    postgres_dsn: PostgresDsn = MultiHostUrl(
        f'postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}')
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None
    algorithm: str = 'HS256'

    class Config:
        _env_file = ".env"
        _extra = 'allow'


app_settings = AppSettings()


uvicorn_options = {
    "host": app_settings.app_host,
    "port": app_settings.app_port,
    "workers": app_settings.cpu_count or multiprocessing.cpu_count(),
    "reload": app_settings.reload
}
