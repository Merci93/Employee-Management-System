""" 
This module contains the API endpoint for adding new employee details to the employees table. 
It defines a POST endpoint that accepts employee details in the request body, validates the input,
and inserts the new employee record into the database. The endpoint includes error handling to manage
potential issues during the insertion process, such as database errors or validation failures,
and returns appropriate responses based on the outcome of the operation.
"""
from typing import Dict

from fastapi import APIRouter, HTTPException
from psycopg2.errors import (
    OperationalError,
    UniqueViolation,
    InFailedSqlTransaction,
)

from api.input_data_validations.pydantic_validations import EmployeeCreateRequest
from app.logger.log_handler import logger
from backend import db_connect


router = APIRouter(prefix="/v1", tags=["Add New Employee"])


@router.post("/add_new_employee/")
def add_new_employee(employee: EmployeeCreateRequest) -> Dict[str, str]:
    """
    Add new employee details to the employees table.

    :param employee: Employee details.
    :return: Success if added, failed is not.
    """
    logger.info("Adding new employee to the database ...")

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
        logger.error("Failed to add new employee to the database. Message: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Failed to add employee: {str(e)}")

    except Exception as e:
        db_connect.db_client.rollback()
        logger.error("Unexpected error occurred while adding employee. Message: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
