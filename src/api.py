"""API endpoint module."""
from contextlib import asynccontextmanager
from enum import Enum
from pydantic import BaseModel
from typing import Any, AsyncContextManager, Dict

import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg2 import sql
from psycopg2.errors import OperationalError, UniqueViolation, InFailedSqlTransaction

from src.backend import db_connect
from src.config import init_settings, settings
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
    yield
    # Shutdown
    db_connect.users_client.close()


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


class Role(str, Enum):
    admin = "Admin"
    user = "User"


class UserCreateRequest(BaseModel):
    role: Role
    username: str
    firstname: str
    lastname: str
    dob: str
    email: str
    password: str


class EmployeeCreateRequest(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    address: str
    date_of_birth: str
    gender: str
    phone: str
    role: str
    email: str
    department: str
    salary: int


@app.get("/v1/root/")
def get_root() -> dict[str, str]:
    """API root endpoint."""
    return {"message": "Hello!!! Root API running."}


@app.get("/v1/verify_employee_id/")
def verify_employee_id(email: str) -> Dict[str, Any]:
    """Verify if user to be created has an email associated with an employee ID"""

    logger.info("Verifying employee id ...")

    try:
        with db_connect.users_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE email = %s").format(sql.Identifier(settings.employee_table_name))
            cursor.execute(query, (email,))
            employee_id = cursor.fetchone()
            if employee_id:
                logger.info(f"Employee with email {email} has id {employee_id}")
                return {"exist": True}
            else:
                logger.info(f"Employee with email {email} does not exist.")
                return {"exist": False}
    except Exception as e:
        logger.error(f"Unexpected error occurred while fetching employee id with email {email}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/v1/verify_email/")
def verify_email(email: str, who: str) -> Dict[str, bool]:
    """Verify if email already exists."""

    logger.info(f"Verifying email {email} ...")

    try:
        with db_connect.users_client.cursor() as cursor:
            query = sql.SQL("SELECT email from {} WHERE email = %s")
            if who == "user":
                query = query.format(sql.Identifier(settings.users_table_name))
            elif who == "employee":
                query = query.format(sql.Identifier(settings.employee_table_name))

            cursor.execute(query, (email,))
            user_email = cursor.fetchone()
            if user_email:
                logger.info(f"Email {email} exists.")
                return {"exist": True}
            else:
                logger.info(f"Email {email} does not exist.")
                return {"exist": False}

    except Exception as e:
        logger.error(f"Unexpected error occurred while verifying email {email}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/v1/verify_phone_number/")
def verify_phone_number(phone: str) -> Dict[str, bool]:
    """Verify if phone number already exists in database."""

    logger.info(f"Verifying phone number {phone}")

    try:
        with db_connect.users_client.cursor() as cursor:
            query = sql.SQL("SELECT phone FROM {} WHERE phone = %s").format(sql.Identifier(settings.employee_table_name))
            cursor.execute(query, (phone,))
            employee_phone = cursor.fetchone()
            if employee_phone:
                logger.info(f"Phone number {phone} exists.")
                return {"exist": True}
            else:
                logger.info(f"Phone number {phone} does not exist.")
                return {"exist": False}
    except Exception as e:
        logger.error(f"Unexpected error occurred while verifying phone number {phone}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/v1/add_user/")
def add_new_user(user: UserCreateRequest) -> Dict[str, str]:
    """
    Add new user to the user's database with assigned role as admin or user.

    User role: can only view employee data.
    Admin role: can perform all operations including addin, deleting and updating data.
    """
    logger.info(f"Adding user {user.username} and details to the database ...")
    query = """
        INSERT INTO users (username, first_name, last_name, email, date_of_birth, role, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING username;
    """
    try:
        encrypted_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
        with db_connect.users_client.cursor() as cursor:
            cursor.execute(query, (user.username, user.firstname, user.lastname, user.email, user.dob, user.role, encrypted_password))
            inserted_username = cursor.fetchone()[0]

        db_connect.users_client.commit()

        logger.info(f"User {inserted_username} added successfully.")

        return {
            "status": "Success",
            "message": f"User {user.username} added to database successfully",
        }

    except (InFailedSqlTransaction, OperationalError, UniqueViolation) as e:
        db_connect.users_client.rollback()
        logger.error(f"Failed to add user {user.username}: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to add user: {str(e)}")

    except Exception as e:
        db_connect.users_client.rollback()
        logger.error(f"Unexpected error occurred while adding user {user.username}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/v1/add_new_employee")
def add_new_employee(employee: EmployeeCreateRequest) -> Dict[str, str]:
    """
    Add new employee details to the employees table.

    :param employee: Employee details.
    :return: Success if added, failed is not.
    """
    logger.info(f"Adding new employee {employee.first_name} {employee.last_name} to the database ...")
    pass


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)
