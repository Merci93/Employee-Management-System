"""
This module defines the API endpoints for updating employee data.
It includes a PATCH endpoint that allows clients to update specific fields of an employee's record by providing the employee ID
and the fields to be updated. The endpoint validates the input, constructs a dynamic SQL query based on the provided fields,
and executes the update operation in the database. It also includes error handling to manage potential issues during the update process.
"""
from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config.config import settings
from app.logger.log_handler import logger
from backend import db_connect


router = APIRouter(prefix="/v1", tags=["Employee Data Update"])


class EmployeeUpdateRequest(BaseModel):
    employee_id: int
    address: str | None = None
    salary: int | float | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    position_id: int | None = None
    department_id: int | None = None
    phone: str | None = None


def update_data(employee_id: int, updates: dict) -> Dict[str, bool]:
    """A helper function to update employee data."""
    logger.info("Updating employee data ...")

    set_clauses = []
    values = []

    for column, value in updates.items():
        set_clauses.append(f"{column} = %s")
        values.append(value)

    query = f"""
        UPDATE {settings.employee_table_name}
        SET {', '.join(set_clauses)}
        WHERE id = %s;
    """

    try:
        with db_connect.db_client.cursor() as cursor:
            cursor.execute(query, (*values, employee_id))
        db_connect.db_client.commit()

        logger.info("Employee data update completed successfully.")
        return {"success": True}

    except Exception as e:
        db_connect.db_client.rollback()
        logger.error("Error updating employee data. Message: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.patch("/v1/update_employee_data", tags=["Employee Data Update"], description="""
    - Provide only the fields you want to update.

    - **employee_id** is required

    - Other fields (address, phone, position, department, first name, middle name, last name) are optional

    - ⚠️ Delete keys you don't want to update, instead of sending them as `null`
    """)
async def employee_data_update(request: EmployeeUpdateRequest) -> Dict[str, bool]:
    """Update employee data."""

    # Exclude fields without any value
    updates = request.model_dump(exclude_none=True)

    employee_id = updates.pop("employee_id", None)
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID is required.")

    if not updates:
        raise HTTPException(status_code=400, detail="No update fields provided.")

    return update_data(
        employee_id=employee_id,
        updates=updates,
    )
