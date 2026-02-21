"""Database connection module."""
import psycopg2

from src.config import settings


db_client = None


def db_init() -> None:
    """Create a connection to the database."""
    global db_client

    try:
        db_client = psycopg2.connect(
            dbname=settings.database_name,
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.host,
            port=settings.port,
        )
    except Exception as e:
        raise psycopg2.OperationalError(e)
