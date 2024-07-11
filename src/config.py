"""Configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_username: str = "postgres"
    postgres_password: str = "postgres"
    postgres_database: str = "employees"


def init_settings() -> None:
    global settings
    settings = Settings()


settings = None
if not settings:
    settings()
