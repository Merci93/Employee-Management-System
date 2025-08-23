""""Backend module"""
from datetime import date
from typing import Dict

import httpx
import pandas as pd
from fastapi import HTTPException

from src.log_handler import logger


BASE_URL = "http://localhost:8000/v1"
HEADERS = {"accept": "application/json"}


async def verify_employee_id(email: str) -> bool:
    """
    Verify if the user to be added is an employee.

    :param Email: Employee email to check.
    return: A boolean True if it exists, False otherwise.
    """
    logger.info("Starting Employee ID verification...")

    url = f"{BASE_URL}/verify_employee_id/"
    params = {
        "email": email,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        logger.info("Employee ID verification completed.")
        response = response.json()

        if response.get("exist"):
            return response.get("value")

        logger.error(f"User with email {email} is not an employee.")
        return response.get("value", False)


async def verify_email(email: str, who: str) -> bool:
    """
    Verify if user email already exists in the database.

    :param Email: Input email to check.
    :param who: Input parameter to either verify employee email or user/admin email.
    return: A boolean True if it exists, False otherwise.
    """
    logger.info("Starting email verification...")

    url = f"{BASE_URL}/verify_email/"
    params = {
        "email": email,
        "who": who,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        response = response.json()

        if response.get("exist"):
            logger.info(f"{who.capitalize()} with email {email} already exists.")
        else:
            logger.info(f"Email {email} does not exist in {who.lower()}s table.")

        return response.get("exist", False)


async def get_gender_id(gender: str) -> int | bool:
    """
    Get the gender ID for the employee.

    :param gender: Gender
    :return: Gender ID from the gender table.
    """
    logger.info("Starting gender id retrieval ...")

    url = f"{BASE_URL}/get_gender_id/"
    params = {
        "gender": gender
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        response = response.json()

        if response.get("value") is not False:
            logger.info("Gender ID retrieved successfully.")
            return response.get("value")

        logger.info("Gender ID not retrieved.")
        return response.get("value", False)


async def get_department_id(department: str) -> int | bool:
    """
    Get the department ID for the employee.

    :param department: Department
    :return: Department ID from the department table.
    """
    logger.info("Starting department id retrieval ...")

    url = f"{BASE_URL}/get_department_id/"
    params = {
        "department": department
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        response = response.json()

        if response.get("value") is not False:
            logger.info("Department ID retrieved successfully.")
            return response.get("value")

        logger.info("Department ID not retrieved.")
        return response.get("value", False)


async def get_position_id(position: str) -> int:
    """
    Get the position ID for the employee.

    :param position: Position
    :return: Position ID from the position table.
    """
    logger.info("Starting position id retrieval ...")

    url = f"{BASE_URL}/get_position_id/"
    params = {
        "position": position
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        response = response.json()

        if response.get("value") is not False:
            logger.info("Position ID retrieved successfully")
            return response.get("value")

        logger.info("position ID not retrieved.")
        return response.get("value", False)


async def verify_phone_number(phone: str) -> bool:
    """
    Verify if phone number already exists in database.

    :param phone: Phone number to verify.
    :return: Boolean True if esist, False otherwise.
    """
    logger.info("Starting phone number verification...")

    url = f"{BASE_URL}/verify_phone_number/"
    params = {
        "phone": phone
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        logger.info("Phone number verification completed.")
        response = response.json()

        if response.get("exist"):
            logger.info(f"Phone number {phone} exists.")
            return response.get("exist")

        logger.info(f"Phone number {phone} does not exist.")
        return response.get("exist", False)


async def add_new_user(
    role: str,
    firstname: str,
    lastname: str,
    dob: date,
    email: str,
    password: str,
    employee_id: int
) -> Dict[str, str]:
    """
    Add a new user to the user database for specified roles.

    User role: can only view employee data.
    Admin role: can perform all operations including addin, deleting and updating data.
    """
    logger.info("Initiating new user creating process ...")

    url = f"{BASE_URL}/add_user/"
    payload = {
        "role": role,
        "firstname": firstname,
        "lastname": lastname,
        "dob": dob.strftime("%Y-%m-%d"),
        "email": email,
        "password": password,
        "employee_id": employee_id,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        response = response.json()
        logger.info(f"{response.get('message')} with assigned role {role}")
        return response


async def add_new_employee_data(
    first_name: str,
    middle_name: str,
    last_name: str,
    address: str,
    date_of_birth: date,
    gender_id: int,
    phone: str,
    position_id: int,
    email: str,
    department_id: int,
    salary: int,
    hired_date: date,
) -> Dict[str, str]: # type: ignore
    """
    Add a new employee details to the database.
    """
    logger.info("Initiating new employee creating process ...")

    url = f"{BASE_URL}/add_new_employee/"
    payload = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "address": address,
        "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
        "gender_id": gender_id,
        "phone": phone,
        "position_id": position_id,
        "department_id": department_id,
        "email": email,
        "salary": salary,
        "hired_date": hired_date.strftime("%Y-%m-%d"),
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=HEADERS)
            response.raise_for_status()
            response = response.json()

            if response.get("status") == "Success":
                logger.info(f"{response.get('message')}")
                return response
        except Exception as e:
            logger.error(f"Unexpected error occurred while adding employee data for {first_name} {last_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def get_employee_data(employee_id: int) -> pd.DataFrame | None:
    """Fetch employee data using employee id"""
    logger.info("Initiating employee data retrieval process ...")
    url = f"{BASE_URL}/get_employee_data/"
    payload = {"employee_id": employee_id}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=payload, headers=HEADERS)
            response.raise_for_status()
            response = response.json()

            data = response.get("value")

            if data:
                logger.info("Pandas DataFrame with employee data created.")
                return pd.DataFrame(data)
            return data
        except Exception as e:
            logger.error(f"Unexpected error occurred while retrieving data for employee ID {employee_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# TODO - Add new enpoint call for deleting employee data
# TODO - Add new enpoint call for updating employee data
