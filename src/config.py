"""Configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    employee_db_name: str = "employees"
    users_table_name: str = "users"
    employee_table_name: str = "employee"
    host: str = "ems-db"
    port: int = 5432


def init_settings() -> None:
    global settings
    settings = Settings()


settings = None
if not settings:
    init_settings()
