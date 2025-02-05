"""Database connection module."""
import psycopg2

from src.config import settings


users_client = None


def user_db_init() -> None:
    """Create a connection to the users database."""
    global users_client

    try:
        users_client = psycopg2.connect(
            dbname=settings.employee_db_name,
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.host,
            port=settings.port,
        )
    except Exception as e:
        raise psycopg2.OperationalError(e)
