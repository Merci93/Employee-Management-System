"""
This module defines the API endpoints for employee data management, including retrieval and addition of employee records.
The endpoints allow clients to fetch employee data based on various criteria such as ID, first name, last name, department,
and position. Additionally, it provides an endpoint to add new employee records to the database.
"""
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from psycopg2 import sql

from api.input_data_validations.pydantic_validations import (
    EmployeeResponseModel,
    DepartmentIdRequest,
    PositionIdRequest,
)
from app.config.config import settings
from app.logger.log_handler import logger
from backend import db_connect


employees_data_router = APIRouter(prefix="/v1", tags=["Employee Data"])

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


@employees_data_router.get("/get_employee_data/by_id/{employee_id}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_id(employee_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using employee ID.

    :param employee_id: Employee ID
    :return: Employee data from all tables, if available.
    """
    logger.info("Retrieving employee data using ID ...")
    result = fetch_employee_data(
        filter_field="id",
        value=employee_id
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@employees_data_router.get("/get_employee_data/by_first_name/{first_name}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_first_name(first_name: str) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using employee first name.

    :param first_name: Employee first name
    :return: Employee data from all tables, if available.
    """
    logger.info("Retrieving employee data by first name ...")
    result = fetch_employee_data(
        filter_field="first_name",
        value=first_name.capitalize()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@employees_data_router.get("/get_employee_data/by_last_name/{last_name}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_last_name(last_name: str) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using employee last name.

    :param last_name: Employee last name
    :return: Employee data from all tables, if available.
    """
    logger.info("Retrieving employee data by last name ...")
    result = fetch_employee_data(
        filter_field="last_name",
        value=last_name.capitalize()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@employees_data_router.get("/get_employee_data/by_department/{department}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_department(department: DepartmentIdRequest) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using department. This returns at least one result if available.

    :param department: Department name
    :return: Employee data from all tables, if available.
    """
    logger.info("Retrieving employee data by department ...")
    result = fetch_employee_data(
        filter_field="department",
        value=department
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result


@employees_data_router.get("/get_employee_data/by_position/{position}", response_model=List[EmployeeResponseModel])
async def get_employee_data_by_position(position: PositionIdRequest) -> List[Dict[str, Any]]:
    """
    Retrieve employee data using department. This returns at least one result if available.

    :param position: Employee position
    :return: Employee data from all tables, if available.
    """
    logger.info("Retrieving employee data by position ...")
    result = fetch_employee_data(
        filter_field="position",
        value=position
    )

    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee data retrieved successfully.")
    return result
