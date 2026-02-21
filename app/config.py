"""Configuration settings."""
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configs
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    database_name: str = "employees"
    users_table_name: str = "users"
    employee_table_name: str = "employee"
    gender_table_name: str = "gender"
    position_table_name: str = "position"
    dept_table_name: str = "department"
    fetch_employee_data_join_column: str = "id"
    gender_id: str = "gender_id"
    position_id: str = "position_id"
    department_id: str = "department_id"
    host: str = "ems-db"
    port: int = 5432

    # UI Configs
    EMPLOYEES_COLUMN: List[str] = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "phone",
        "address",
        "salary",
        "department",
        "position",
        "gender",
        "date_of_birth",
        "hired_date",
        "status",
        "date_resigned",
    ]

    DEPARTMENTS: List[str] = [
        "IT",
        "HR",
        "Sales",
        "Research",
        "Marketing",
        "Data & Analytics",
    ]

    POSITIONS: List[str] = [
        "HR",
        "Intern",
        "Data Engineer",
        "Solutions Architect",
        "Data Analyst",
        "Business Analyst",
        "Senior Engineering Manager",
        "Data Scientist",
        "Junior Data Engineer",
        "Web Developer",
        "Cloud Architect",
        "Software Engineer",
        "Network Engineer",
        "DevOps Engineer",
        "Product Owner",
    ]

    DATA_TO_UPDATE: List[str] = [
        "First Name",
        "Middle Name",
        "Last Name",
        "Address",
        "Phone",
        "Department",
        "Position",
        "Salary",
    ]

    GENDER: List[str] = ["Male", "Female"]


def init_settings() -> None:
    global settings
    settings = Settings()


settings = None
if not settings:
    init_settings()
