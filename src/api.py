"""API endpoint module."""
import datetime
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.errors import OperationalError, UniqueViolation, InFailedSqlTransaction

from src.backend import db_connect, httpx_client
from src.config import init_settings
from src.log_handler import logger


description = """
An API developed for the data retrieval and updates for the Employee Management System.

Developed and and managed by David Asogwa.

PS: This API is for this project purpose only.

📝[Source Code](https://github.com/Merci93/Employee-Management-System)
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[Any]:  # type: ignore
    # Startup
    init_settings()
    db_connect.user_db_init()
    httpx_client.init_httpx_client()
    yield
    # Shutdown
    db_connect.users_client.close()
    httpx_client.httpx_client.close()


app = FastAPI(
    title="Employee Data Retriever",
    docs_url="/",
    description=description,
    version="0.1",
    contact={
        "name": "David Asogwa",
        "contact": "https://github.com/Merci93/Employee-Management-System",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/v1/root/")
def get_root() -> dict[str, str]:
    """API root endpoint."""
    return {"message": "Hello!!! Root API running."}


@app.get("/v1/verify_user/")
def verify_user(username: str) -> Dict[str, Any]:
    """Verify user credentials in the database"""
    logger.info(f"Verifying user {username} ...")
    cursor = db_connect.users_client.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
    user_details = cursor.fetchall()
    if user_details:
        user_data = {"exist": True, "password": user_details[0][1]}
        logger.info(f"User {username} exists.")
    else:
        user_data = {"exist": False, "password": None}
        logger.info(f"User {username} does not exist.")
    db_connect.users_client.commit()
    return user_data


@app.get("/v1/verify_email/")
def verify_email(email: str) -> Dict[str, bool]:
    """Verify if email already exists."""
    logger.info(f"Verifying email {email} ...")
    cursor = db_connect.users_client.cursor()
    cursor.execute("SELECT email from users WHERE email = %s", (email,))
    user_email = cursor.fetchall()
    if user_email:
        user_data = {"exist": True}
        logger.info(f"Email {email} exists.")
    else:
        user_data = {"exist": False}
        logger.info(f"Email {email} does not exist.")
    db_connect.users_client.commit()
    return user_data


@app.post("/v1/add_user/")
def add_new_user(
    role: str,
    username: str,
    firstname: str,
    lastname: str,
    dob: datetime.date,
    email: str,
    password: str,
) -> Dict[str, str]:
    """
    Add new user to the user's database with assigned role as admin or user.

    User role: can only view employee data.
    Admin role: can perform all operations including addin, deleting and updating data.
    """
    logger.info(f"Adding user {username} and details to the database ...")
    query = """
        INSERT INTO users (username, first_name, last_name, email, date_of_birth, role, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        with db_connect.users_client.cursor() as cursor:
            cursor.execute(query, (username, firstname, lastname, email, dob, role, password))
        db_connect.users_client.commit()
        logger.info(f"User {username} added successfully.")
        return {
            "status": "Success",
            "message": f"User {username} added to database successfully.",
        }
    except (InFailedSqlTransaction, OperationalError, UniqueViolation) as e:
        db_connect.users_client.rollback()
        logger.error(f"Failed to add user: {e}")
        return {
            "status": "Failed",
            "message": str(e),
        }


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)
