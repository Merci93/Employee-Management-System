"""
This module defines API endpoints for retrieving IDs for employee gender, department, and position.
It includes GET endpoints that accept specific parameters (gender, department, or position) and
return the corresponding ID from the database. The endpoints handle database interactions,
including executing SQL queries to fetch the required IDs, and include error handling to manage
potential issues during the retrieval process.   
"""
from enum import Enum
from typing import Dict

from fastapi import (
    APIRouter,
    HTTPException,
)
from psycopg2 import sql

from backend import db_connect
from app.config.config import settings
from app.logger.log_handler import logger


router = APIRouter(prefix="/v1", tags=["Retrieve ID"])


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
    intern = "Intern"
    data_analyst = "Data Analyst"
    web_developer = "Web Developer"
    product_owner = "Product Owner"
    data_engineer = "Data Engineer"
    data_scientist = "Data Scientist"
    devops_engineer = "DevOps Engineer"
    cloud_architect = "Cloud Architect"
    network_engineer = "Network Engineer"
    business_analyst = "Business Analyst"
    software_engineer = "Software Engineer"
    jnr_data_eengieer = "Junior Data Engineer"
    solutions_architect = "Solutions Architect"
    senior_engr_mgr = "Senior Engineering Manager"


@router.get("/get_gender_id/{gender}")
async def get_gender_id(gender: GenderIdRequest) -> Dict[str, int]:
    """Get employee gender id."""
    logger.info("Retrieving Employee gender id  ...")
    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE gender = %s").format(
                sql.Identifier(settings.gender_table_name)
            )
            cursor.execute(query, (gender,))
            employee_gender_id = cursor.fetchone()

            if employee_gender_id:
                logger.info(
                    f"Gender ID retrieved successfully. Value: {employee_gender_id[0]}"
                )
                return {"value": employee_gender_id[0]}
            else:
                logger.info("Gender ID not retrieved.")
                return {"value": False}

    except Exception as e:
        logger.error("Unexpected error occurred while retrieving id for employee gender. Message: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/get_department_id/{department}")
async def get_department_id(department: DepartmentIdRequest) -> Dict[str, int]:
    """Get employee department id."""
    logger.info("Retrieving Employee department id ...")
    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE department = %s").format(
                sql.Identifier(settings.dept_table_name)
            )
            cursor.execute(query, (department,))
            employee_dept_id = cursor.fetchone()

            if employee_dept_id:
                logger.info("Department ID retrieved successfully.")
                return {"value": employee_dept_id[0]}
            else:
                logger.info("Department ID not retrieved.")
                return {"value": False}

    except Exception as e:
        logger.error("Unexpected error occurred while retrieving id for department. Message: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/get_position_id/{position}")
async def get_position_id(position: PositionIdRequest) -> Dict[str, int]:
    """Get employee position id."""
    logger.info("Retrieving Employee position id ...")
    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT id FROM {} WHERE position = %s").format(
                sql.Identifier(settings.position_table_name)
            )
            cursor.execute(query, (position,))
            employee_position_id = cursor.fetchone()

            if employee_position_id:
                logger.info("Position ID retrieved successfully.")
                return {"value": employee_position_id[0]}
            else:
                logger.info("Position ID not retrieved.")
                return {"value": False}

    except Exception as e:
        logger.error("Unexpected error occurred while retrieving id for employee position. Message: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
