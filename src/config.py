"""Configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    database_name: str = "employees"
    users_table_name: str = "users"
    employee_table_name: str = "employee"
    gender_table_name: str = "gender"
    position_table_name: str = "position"
    dept_table_name: str = "department"
    join_column: str = "id"
    gender_id: str = "gender_id"
    position_id: str = "position_id"
    department_id: str = "department_id"
    host: str = "ems-db"
    port: int = 5432


def init_settings() -> None:
    global settings
    settings = Settings()


settings = None
if not settings:
    init_settings()
