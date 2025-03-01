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
    db_connect.db_init()
    yield
    # Shutdown
    db_connect.db_client.close()


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
    openapi_tags=[
        {
            "name": "Employee Data Verification",
            "description": "Endpoints for verifying employee data - email, phone number and ID."
        },
        {
            "name": "Retrieve ID",
            "description": "Endpoints for retrieving id for specified gender, department and position from their respective tables.",
        },
        {
            "name": "Admin and User Management",
            "description": "Endpoints to add employees as user and admins in order to access or modify data."
        },
        {
            "name": "Employee Management",
            "description": "Endpoints to manage employee data - add, update and delete."
        }
    ]
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


class WhoToVerify(str, Enum):
    user = "user"
    employee = "employee"


class UserCreateRequest(BaseModel):
    role: Role
    firstname: str
    lastname: str
    dob: str
    email: str
    password: str
    employee_id: int


class GenderIdRequest(str, Enum):
    male = "Male"
    female = "Female"


class DepartmentIdRequest(str, Enum):
    it = "IT"
    hr = "HR"
    sales = "Sales"
    research = "Research"
    marketing = "Marketing"
    data_analytics = "Data & Analytics"


class PositionIdRequest(str, Enum):
    hr = "HR"
    de = "Data Engineer"
    sa = "Solutions Architect"
    da = "Data Analyst"
    inte = "Intern"
    ba = "Business Analyst"
    sem = "Senior Manager Engineering"
    ds = "Data Scientist"
    jde = "Junior Data Engineer"
    wd = "Web Developer"
    ca = "Cloud Architect"
    se = "Software Engineer"
    ne = "Network Engineer"
    dev = "DevOps Engineer"
    po = "Product Owner"


class EmployeeCreateRequest(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    address: str
    date_of_birth: str
    gender_id: int
    phone: str
    position_id: int
    email: str
    department_id: int
    salary: float
    hired_date: str


@app.get("/v1/root/", tags=["Root"])
def get_root() -> dict[str, str]:
    """API root endpoint."""
    return {"message": "Hello!!! Root API running."}


@app.get("/v1/verify_employee_id/", tags=["Employee Data Verification"])
def verify_employee_id(email: str) -> Dict[str, Any]:
    """Verify if user to be created has an email associated with an employee ID"""

    logger.info("Verifying employee id ...")

    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE email = %s").format(sql.Identifier(settings.employee_table_name))
            cursor.execute(query, (email,))
            employee_id = cursor.fetchone()
            if employee_id:
                logger.info(f"Employee with email {email} has id {employee_id}")
                return {
                    "exist": True,
                    "value": employee_id[0]
                }
            else:
                logger.info(f"Employee with email {email} does not exist.")
                return {
                    "exist": False,
                    "value": False
                }
    except Exception as e:
        logger.error(f"Unexpected error occurred while fetching employee id with email {email}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/v1/verify_email/", tags=["Employee Data Verification"])
def verify_email(email: str, who: WhoToVerify) -> Dict[str, bool]:
    """Verify if email already exists."""

    logger.info(f"Verifying email {email} ...")

    try:
        with db_connect.db_client.cursor() as cursor:
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


@app.get("/v1/verify_phone_number/", tags=["Employee Data Verification"])
def verify_phone_number(phone: str) -> Dict[str, bool]:
    """Verify if phone number already exists in database."""

    logger.info(f"Verifying phone number {phone}")

    try:
        with db_connect.db_client.cursor() as cursor:
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


@app.get("/v1/get_gender_id/", tags=["Retrieve ID"])
def get_gender_id(gender: GenderIdRequest) -> Dict[str, Any]:
    """Get employee gender id."""
    logger.info(f"Retrieving gender id for gender {gender} ...")
    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE gender = %s").format(sql.Identifier(settings.gender_table_name))
            cursor.execute(query, (gender,))
            employee_gender_id = cursor.fetchone()
            if employee_gender_id:
                logger.info(f"Gender ID retrieved successfully. Value: {employee_gender_id[0]}")
                return {"value": employee_gender_id[0]}
            else:
                logger.info("Gender ID not retrieved.")
                return {"value": False}

    except Exception as e:
        logger.error(f"Unexpected error occurred while retrieving id for gender {gender}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/v1/get_department_id/", tags=["Retrieve ID"])
def get_department_id(department: DepartmentIdRequest) -> Dict[str, Any]:
    """Get employee department id."""
    logger.info(f"Retrieving department id for {department} ...")
    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE department = %s").format(sql.Identifier(settings.dept_table_name))
            cursor.execute(query, (department,))
            employee_dept_id = cursor.fetchone()
            if employee_dept_id:
                logger.info(f"Department ID retrieved successfully. Value: {employee_dept_id[0]}")
                return {"value": employee_dept_id[0]}
            else:
                logger.info("Department ID not retrieved.")
                return {"value": False}

    except Exception as e:
        logger.error(f"Unexpected error occurred while retrieving id for {department}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/v1/get_position_id/", tags=["Retrieve ID"])
def get_position_id(position: PositionIdRequest) -> Dict[str, Any]:
    """Get employee position id."""
    logger.info(f"Retrieving position id for {position} ...")
    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE position = %s").format(sql.Identifier(settings.position_table_name))
            cursor.execute(query, (position,))
            employee_position_id = cursor.fetchone()
            if employee_position_id:
                logger.info(f"Position ID retrieved successfully. Value: {employee_position_id[0]}")
                return {"value": employee_position_id[0]}
            else:
                logger.info("position ID not retrieved.")
                return {"value": False}

    except Exception as e:
        logger.error(f"Unexpected error occurred while retrieving id for {position}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/v1/add_user/", tags=["Admin and User Management"])
def add_new_user(user: UserCreateRequest) -> Dict[str, str]:
    """
    Add new user to the user's database with assigned role as admin or user.

    User role: can only view employee data.
    Admin role: can perform all operations including addin, deleting and updating data.
    """
    logger.info(f"Adding user {user.firstname} {user.lastname} and details to the database ...")
    query = """
        INSERT INTO users (first_name, last_name, email, date_of_birth, role, password, employee_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING first_name last_name;
    """
    try:
        encrypted_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
        with db_connect.db_client.cursor() as cursor:
            cursor.execute(query, (user.firstname, user.lastname, user.email, user.dob, user.role, encrypted_password, user.employee_id))
            inserted_name = cursor.fetchone()[0]

        db_connect.db_client.commit()

        logger.info(f"User {inserted_name} added successfully.")

        return {
            "status": "Success",
            "message": f"User {inserted_name} added to database successfully",
        }

    except (InFailedSqlTransaction, OperationalError, UniqueViolation) as e:
        db_connect.db_client.rollback()
        logger.error(f"Failed to add user {user.firstname} {user.lastname}: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to add user: {str(e)}")

    except Exception as e:
        db_connect.db_client.rollback()
        logger.error(f"Unexpected error occurred while adding user {user.firstname} {user.lastname}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/v1/add_new_employee/", tags=["Employee Management"])
def add_new_employee(employee: EmployeeCreateRequest) -> Dict[str, str]:
    """
    Add new employee details to the employees table.

    :param employee: Employee details.
    :return: Success if added, failed is not.
    """
    logger.info(f"Adding new employee {employee.first_name} {employee.last_name} to the database ...")

    query = """
        INSERT INTO employee (
            first_name, middle_name, last_name, email, phone, address, salary, department_id, position_id, gender_id, date_of_birth, hired_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING first_name last_name;
    """

    try:
        with db_connect.db_client.cursor() as cursor:
            cursor.execute(
                query, (employee.first_name, employee.middle_name, employee.last_name, employee.email, employee.phone,
                        employee.address, employee.salary, employee.department_id, employee.position_id, employee.gender_id,
                        employee.date_of_birth, employee.hired_date)
                )
            inserted_name = cursor.fetchone()[0]

        db_connect.db_client.commit()

        logger.info(f"{inserted_name} added successfully as an employee.")

        return {
            "status": "Success",
            "message": f"{inserted_name} added successfully as an employee.",
        }

    except (InFailedSqlTransaction, OperationalError, UniqueViolation) as e:
        db_connect.db_client.rollback()
        logger.error(f"Failed to add employee {employee.first_name} {employee.last_name}: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to add employee: {str(e)}")

    except Exception as e:
        db_connect.db_client.rollback()
        logger.error(f"Unexpected error occurred while adding employee {employee.first_name} {employee.last_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# TODO - Add endpoint to delete employee data
# TODO - Add endpoint for updating employee data


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)
