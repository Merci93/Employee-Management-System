"""Data and users verification module"""
from enum import Enum
from typing import Dict

from fastapi import APIRouter, HTTPException
from psycopg2 import sql

from src.backend import db_connect
from src.config import settings
from src.log_handler import logger


router = APIRouter(prefix="v1", tags=["Employee Data Verification"])


class WhoToVerify(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


@router.get("/verify_email/{email}")
async def verify_email_exists(email: str, who: WhoToVerify) -> Dict[str, bool]:
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
                logger.info(f"Email {email} exists in {who} database.")
                return {"exist": True}
            else:
                logger.info(f"Email {email} does not exists in {who} database.")
                return {"exist": False}

    except Exception as e:
        logger.error(f"Unexpected error occurred while verifying email {email}: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/verify_phone_number/{phone_number}")
async def verify_phone_number(phone_number: str) -> Dict[str, bool]:
    """Verify if phone number already exists in database."""

    logger.info(f"Verifying phone number {phone_number}")

    try:
        with db_connect.db_client.cursor() as cursor:
            query = sql.SQL("SELECT phone FROM {} WHERE phone = %s").format(
                sql.Identifier(settings.employee_table_name)
            )
            cursor.execute(query, (phone_number,))
            employee_phone = cursor.fetchone()

            if employee_phone:
                logger.info(f"Phone number {phone_number} exists.")
                return {"exist": True}
            else:
                logger.info(f"Phone number {phone_number} does not exist.")
                return {"exist": False}
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while verifying phone number {phone_number}: {e}"
        )
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
