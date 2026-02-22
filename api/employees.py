"""
This module defines the API endpoints for employee data management, including retrieval and addition of employee records.
The endpoints allow clients to fetch employee data based on various criteria such as ID, first name, last name, department,
and position. Additionally, it provides an endpoint to add new employee records to the database.
"""
from datetime import date
from enum import Enum
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from psycopg2 import sql
from psycopg2.errors import (
    OperationalError,
    UniqueViolation,
    InFailedSqlTransaction,
)
from pydantic import BaseModel

from app.config.config import settings
from app.logger.log_handler import logger
from backend import db_connect


router = APIRouter(prefix="/v1", tags=["Employee Data"])


class DepartmentIdRequest(str, Enum):
    it = "IT"
    hr = "HR"
    sales = "Sales"
    research = "Research"
    marketing = "Marketing"
    data_analytics = "Data & Analytics"


class EmployeeCreateRequest(BaseModel):
    phone: str
    email: str
    status: str
    address: str
    salary: float
    gender_id: int
    last_name: str
    first_name: str
    hired_date: str
    position_id: int
    middle_name: str
    date_of_birth: str
    department_id: int


class EmployeeResponseModel(BaseModel):
    id: int
    email: str
    phone: str
    gender: str
    status: str
    address: str
    position: str
    salary: float
    last_name: str
    department: str
    first_name: str
    hired_date: date
    date_of_birth: date
    middle_name: str | None = None
    date_resigned: date | None = None


class PositionIdRequest(str, Enum):
    hr = "HR"
    intern = "Intern"
    data_analyst = "Data Analyst"
    data_engineer = "Data Engineer"
    product_owner = "Product Owner"
    web_developer = "Web Developer"
    data_scientist = "Data Scientist"
    devops_engineer = "DevOps Engineer"
    cloud_architect = "Cloud Architect"
    network_engineer = "Network Engineer"
    business_analyst = "Business Analyst"
    software_engineer = "Software Engineer"
    jnr_data_eengieer = "Junior Data Engineer"
    solutions_architect = "Solutions Architect"
    senior_engr_mgr = "Senior Engineering Manager"


ALLOWED_EMPLOYEE_FILTERS = {
    "id": "e.id",
    "first_name": "e.first_name",
    "last_name": "e.last_name",
    "department": "d.department",
    "status": "e.status"
}


def fetch_employee_data(filter_field: str, value: Any) -> List[Dict[str, Any]]:
    """
    A helper function for fetching employee data via API calss to the Database

    :param filter_field: The field to filter on (e.g., "id", "first_name")
    :param value: value for filter
    :return: List of dictionary values for retrieved data.
    """

    if filter_field not in ALLOWED_EMPLOYEE_FILTERS:
        raise ValueError("Invalid filter field")

    column = ALLOWED_EMPLOYEE_FILTERS[filter_field]

    with db_connect.db_client.cursor() as cursor:
        query = sql.SQL("""
                SELECT
                    e.id,
                    e.first_name,
                    e.middle_name,
                    e.last_name,
                    e.email,
                    e.phone,
                    e.address,
                    e.salary,
                    d.department,
                    p.position,
                    g.gender,
                    e.date_of_birth,
                    e.hired_date,
                    e.status,
                    e.date_resigned
                FROM {employee} AS e
                JOIN {department} AS d ON e.{department_id} = d.{data_join_column}
                JOIN {gender} AS g ON e.{gender_id} = g.{data_join_column}
                JOIN {position} AS p ON e.{position_id} = p.{data_join_column}
                WHERE {filter_column} = %s;
            """
            ).format(
                employee=sql.Identifier(settings.employee_table_name),
                department=sql.Identifier(settings.dept_table_name),
                department_id=sql.Identifier(settings.department_id),
                gender=sql.Identifier(settings.gender_table_name),
                gender_id=sql.Identifier(settings.gender_id),
                position=sql.Identifier(settings.position_table_name),
                position_id=sql.Identifier(settings.position_id),
                data_join_column=sql.Identifier(settings.fetch_employee_data_join_column),
                filter_column=sql.SQL(column)
            )
        cursor.execute(query, (value,))
        rows = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]  # type: ignore

        return [dict(zip(col_names, row)) for row in rows]


@router.get("/get_employee_data/by_id/{employee_id}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_id(employee_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using employee ID.

    :param employee_id: Employee ID
    :return: Employee data from all tables, if available.
    """
    logger.info(f"Retrieving employee data. ID: {employee_id}")
    result = fetch_employee_data(
        filter_field="id",
        value=employee_id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@router.get("/get_employee_data/by_first_name/{first_name}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_first_name(first_name: str) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using employee first name.

    :param first_name: Employee first name
    :return: Employee data from all tables, if available.
    """
    logger.info(f"Retrieving employee data. first name: {first_name.capitalize()}")
    result = fetch_employee_data(
        filter_field="first_name",
        value=first_name.capitalize()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@router.get("/get_employee_data/by_last_name/{last_name}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_last_name(last_name: str) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using employee last name.

    :param last_name: Employee last name
    :return: Employee data from all tables, if available.
    """
    logger.info(f"Retrieving employee data. last name: {last_name.capitalize()}")
    result = fetch_employee_data(
        filter_field="last_name",
        value=last_name.capitalize()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@router.get("/get_employee_data/by_department/{department}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_department(department: DepartmentIdRequest) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using department. This returns at least one result if available.

    :param department: Department name
    :return: Employee data from all tables, if available.
    """
    logger.info(f"Retrieving employee data. department: {department}")
    result = fetch_employee_data(
        filter_field="department",
        value=department
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@router.get("/get_employee_data/by_position/{position}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_position(position: PositionIdRequest) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using department. This returns at least one result if available.

    :param position: Employee position
    :return: Employee data from all tables, if available.
    """
    logger.info(f"Retrieving employee data. position: {position}")
    result = fetch_employee_data(
        filter_field="position",
        value=position
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@router.post("/add_new_employee/")
def add_new_employee(employee: EmployeeCreateRequest) -> Dict[str, str]:
    """
    Add new employee details to the employees table.

    :param employee: Employee details.
    :return: Success if added, failed is not.
    """
    logger.info(
        f"Adding new employee {employee.first_name} {employee.last_name} to the database ..."
    )

    query = """
        INSERT INTO employee (
        first_name, middle_name, last_name, email, phone, address, salary, department_id, position_id, gender_id, date_of_birth, hired_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING first_name last_name;
    """

    try:
        with db_connect.db_client.cursor() as cursor:
            cursor.execute(
                query,
                (
                    employee.first_name,
                    employee.middle_name,
                    employee.last_name,
                    employee.email,
                    employee.phone,
                    employee.address,
                    employee.salary,
                    employee.department_id,
                    employee.position_id,
                    employee.gender_id,
                    employee.date_of_birth,
                    employee.hired_date,
                    employee.status
                ),
            )
            inserted_name = cursor.fetchone()[0]  # type: ignore

        db_connect.db_client.commit()

        logger.info(f"{inserted_name} added successfully as an employee.")

        return {
            "status": "Success",
            "message": f"{inserted_name} added successfully as an employee.",
        }

    except (InFailedSqlTransaction, OperationalError, UniqueViolation) as e:
        db_connect.db_client.rollback()
        logger.error(
            f"Failed to add employee {employee.first_name} {employee.last_name}: {e}"
        )
        raise HTTPException(status_code=400, detail=f"Failed to add employee: {str(e)}")

    except Exception as e:
        db_connect.db_client.rollback()
        logger.error(
            f"Unexpected error occurred while adding employee {employee.first_name} {employee.last_name}: {e}"
        )
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
